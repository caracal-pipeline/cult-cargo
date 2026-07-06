#!/usr/bin/env python3
"""
Batch convert stimela-classic parameters.json files to scabha YAML format.

This script:
1. Identifies cabs in stimela-classic that are missing from cult-cargo
2. Converts them to scabha YAML format
3. Writes them to an output directory ready for PR
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import yaml


def convert_dtype(dtype: Any) -> str:
    """Convert stimela-classic dtype to scabha dtype."""
    if isinstance(dtype, list):
        # Union types - take the first non-null type
        for t in dtype:
            if t != "null":
                return convert_dtype(t)
        return "str"
    
    # Type mappings
    type_map = {
        "file": "File",
        "list:file": "list:File",
        "list:str": "list:str",
        "list:int": "list:int",
        "list:float": "list:float",
        "list:bool": "list:bool",
    }
    
    return type_map.get(dtype, dtype)


def convert_parameter(param: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single parameter from classic to scabha format."""
    result = {}
    
    # Basic fields
    if "info" in param:
        result["info"] = param["info"]
    
    # Convert dtype
    if "dtype" in param:
        result["dtype"] = convert_dtype(param["dtype"])
    
    # Default value
    if "default" in param and param["default"] is not None:
        result["default"] = param["default"]
    
    # Required flag
    if param.get("required", False):
        result["required"] = True
    
    # Choices (enum values)
    if "choices" in param:
        result["choices"] = param["choices"]
    
    # Mapping becomes nom_de_guerre
    if "mapping" in param:
        result["nom_de_guerre"] = param["mapping"]
    
    # IO-specific handling
    io_type = param.get("io")
    if io_type == "msfile":
        result["dtype"] = "MS"
    
    return result


def convert_cab(classic: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a complete cab definition from classic to scabha format."""
    cab_name = classic["task"]
    
    # Build the scabha structure
    scabha = {
        "_include": ["genesis/cult-cargo-base.yml"],
        "cabs": {
            cab_name: {}
        }
    }
    
    cab = scabha["cabs"][cab_name]
    
    # Basic metadata
    cab["name"] = cab_name
    if "description" in classic:
        cab["info"] = classic["description"]
    
    # Command (binary name)
    if "binary" in classic:
        cab["command"] = classic["binary"]
    
    # Image reference
    if "base" in classic:
        # Map common base images
        base = classic["base"]
        image_name = base.split("/")[-1] if "/" in base else base
        cab["image"] = {
            "_use": "vars.cult-cargo.images",
            "name": image_name
        }
    
    # Policies
    policies = {}
    if "prefix" in classic:
        policies["prefix"] = classic["prefix"]
    
    # Add standard policies for CASA tasks
    if cab_name.startswith("casa_"):
        policies["replace"] = {"_": "-"}
    
    if policies:
        cab["policies"] = policies
    
    # Split parameters into inputs and outputs
    inputs = {}
    outputs = {}
    
    for param in classic.get("parameters", []):
        name = param["name"]
        io_type = param.get("io")
        
        converted = convert_parameter(param)
        
        if io_type == "output":
            outputs[name] = converted
        else:
            inputs[name] = converted
    
    if inputs:
        cab["inputs"] = inputs
    if outputs:
        cab["outputs"] = outputs
    
    return scabha


def get_cult_cargo_cabs(cult_cargo_dir: Path) -> Set[str]:
    """Get list of cab names already in cult-cargo."""
    cabs = set()
    for yml_file in cult_cargo_dir.glob("*.yml"):
        if yml_file.name.startswith("_"):
            continue
        try:
            with open(yml_file) as f:
                data = yaml.safe_load(f)
                if data and "cabs" in data:
                    cabs.update(data["cabs"].keys())
        except Exception as e:
            print(f"Warning: Could not parse {yml_file}: {e}", file=sys.stderr)
    return cabs


def get_classic_cabs(classic_dir: Path) -> Dict[str, Path]:
    """Get all cabs from stimela-classic."""
    cabs = {}
    for params_file in classic_dir.glob("*/parameters.json"):
        cab_name = params_file.parent.name
        cabs[cab_name] = params_file
    return cabs


def main():
    if len(sys.argv) != 4:
        print("Usage: python batch_convert.py <classic_dir> <cult_cargo_dir> <output_dir>")
        print("\nExample:")
        print("  python batch_convert.py /tmp/Stimela-classic/stimela/cargo/cab /tmp/cult-cargo/cultcargo /tmp/converted_cabs")
        sys.exit(1)
    
    classic_dir = Path(sys.argv[1])
    cult_cargo_dir = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])
    
    if not classic_dir.exists():
        print(f"Error: {classic_dir} not found")
        sys.exit(1)
    
    if not cult_cargo_dir.exists():
        print(f"Error: {cult_cargo_dir} not found")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get existing cabs
    existing_cabs = get_cult_cargo_cabs(cult_cargo_dir)
    print(f"Found {len(existing_cabs)} cabs in cult-cargo")
    
    # Get all classic cabs
    classic_cabs = get_classic_cabs(classic_dir)
    print(f"Found {len(classic_cabs)} cabs in stimela-classic")
    
    # Find missing cabs
    missing_cabs = set(classic_cabs.keys()) - existing_cabs
    print(f"Found {len(missing_cabs)} cabs to convert")
    
    # Convert missing cabs
    converted = 0
    errors = []
    
    for cab_name in sorted(missing_cabs):
        params_file = classic_cabs[cab_name]
        try:
            with open(params_file) as f:
                classic = json.load(f)
            
            scabha = convert_cab(classic)
            
            # Write to output
            output_file = output_dir / f"{cab_name}.yml"
            with open(output_file, "w") as f:
                yaml.dump(scabha, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            converted += 1
            print(f"✓ Converted {cab_name}")
            
        except Exception as e:
            errors.append((cab_name, str(e)))
            print(f"✗ Error converting {cab_name}: {e}")
    
    print(f"\nConversion complete:")
    print(f"  Converted: {converted}")
    print(f"  Errors: {len(errors)}")
    
    if errors:
        print("\nErrors:")
        for cab_name, error in errors:
            print(f"  {cab_name}: {error}")


if __name__ == "__main__":
    main()
