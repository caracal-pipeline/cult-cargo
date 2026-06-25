"""Importable cab objects for use with the Stimela3 Python API.

This module exposes cult-cargo's YAML cab definitions as callable
CabProxy objects, enabling the Stimela3 import syntax::

    from cultcargo.cabs import wsclean, quartical

    result = wsclean(ms="obs.ms", size=4096)
    print(result.restored)

Cab names use underscores in Python (matching Python identifier rules).
YAML cab names with hyphens are converted automatically::

    pfb_imaging = CabProxy("pfb-imaging")

Any cab defined in cult-cargo's YAML files is accessible — this module
uses ``__getattr__`` for lazy resolution, so no manual registration is
needed when new cabs are added.
"""

from __future__ import annotations

from stimela.api.cab_proxy import CabProxy

# Explicitly list common cabs for IDE autocomplete and documentation.
# These are the most frequently used cabs in radio astronomy pipelines.
aimfast = CabProxy("aimfast")
bdsf_catalog = CabProxy("bdsf.catalog")
breizorro = CabProxy("breizorro")
chgcentre = CabProxy("chgcentre")
crystalball = CabProxy("crystalball")
cubical = CabProxy("cubical")
fitstool = CabProxy("fitstool")
quartical = CabProxy("quartical")
shadems = CabProxy("shadems")
tricolour = CabProxy("tricolour")
wsclean = CabProxy("wsclean")

# CASA cabs
casa_bandpass = CabProxy("casa.bandpass")
casa_calibration = CabProxy("casa.calibration")
casa_clearcal = CabProxy("casa.clearcal")
casa_concat = CabProxy("casa.concat")
casa_flag = CabProxy("casa.flag")
casa_listobs = CabProxy("casa.listobs")
casa_mstransform = CabProxy("casa.mstransform")
casa_plotants = CabProxy("casa.plotants")
casa_plotms = CabProxy("casa.plotms")
casa_polcal = CabProxy("casa.polcal")
casa_setjy = CabProxy("casa.setjy")
casa_split = CabProxy("casa.split")


def __getattr__(name: str) -> CabProxy:
    """Lazy cab resolution for any cab not explicitly listed above.

    Converts Python identifiers to YAML cab names:
    - Underscores → hyphens: ``pfb_imaging`` → ``pfb-imaging``
    - Double underscores → dots: ``casa__bandpass`` → ``casa.bandpass``

    This means every cab in cult-cargo is importable without explicit
    registration — adding a new YAML file is sufficient.
    """
    if name.startswith("_"):
        raise AttributeError(name)
    cab_name = name.replace("__", ".").replace("_", "-")
    return CabProxy(cab_name)
