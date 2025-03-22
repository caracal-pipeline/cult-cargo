FROM {REGISTRY}/python-base:{VERSION}-{BUNDLE_VERSION}

# add useful astro stuff
RUN python{VERSION} -m pip install --no-cache-dir \
    python-casacore astropy astroplan regions astro-tigger-lsm \
    owlcat dask-ms scipy omegaconf bdsf msutils \
    stimela katbeam

# set XDG cache (normally ~/.cache)
ENV XDG_CACHE_HOME /var/cache
ENV XDG_CONFIG_HOME /var/config
RUN mkdir -p /var/cache/astropy /var/config/astropy

RUN python{VERSION} -c "from astropy.config.paths import get_cache_dir, get_config_dir; print(get_cache_dir()); print(get_config_dir())"

# force download of basic astropy data
RUN python{VERSION} -c "from astropy.time import Time; Time.now().ut1"
RUN python{VERSION} -c "from astropy.coordinates import EarthLocation; EarthLocation.of_site('VLA')"

# this now disables astropy downloads so should be done last 
COPY astropy.cfg  /var/config/astropy

CMD python{VERSION}

