#!/usr/bin/env python3
"""
Convert stimela-classic parameters.json to scabha YAML format for cult-cargo.

Usage:
    python convert_classic_to_scabha.py <cab_directory>

Example:
    python convert_classic_to_scabha.py /tmp/Stimela-classic/stimela/cargo/cab/casa_gaincal
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


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


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_classic_to_scabha.py <cab_directory>")
        sys.exit(1)
    
    cab_dir = Path(sys.argv[1])
    params_file = cab_dir / "parameters.json"
    
    if not params_file.exists():
        print(f"Error: {params_file} not found")
        sys.exit(1)
    
    # Load classic format
    with open(params_file) as f:
        classic = json.load(f)
    
    # Convert to scabha
    scabha = convert_cab(classic)
    
    # Output as YAML (using simple format for now)
    import yaml
    print(yaml.dump(scabha, default_flow_style=False, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    main()
