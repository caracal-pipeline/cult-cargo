FROM {REGISTRY}/python-base:{VERSION}-{BUNDLE_VERSION}

# add casacore-tools
RUN apt-get update && apt-get install apt-utils && \
    apt-get install -y casacore-tools \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives 


# add useful astro stuff
# RUN python{VERSION} -m 
RUN uv python pin python{VERSION}
RUN uv pip -n install --system \
    python-casacore astropy astroplan regions astro-tigger-lsm \
    owlcat dask-ms scipy omegaconf msutils \
    stimela katbeam

# set XDG cache (normally ~/.cache)
ENV XDG_CACHE_HOME /var/cache
ENV XDG_CONFIG_HOME /var/config
RUN mkdir -p /var/cache/astropy /var/config/astropy

# keep matplotlib happy in this environment, wants a writable config dir
RUN ln -s /tmp /var/config/matplotlib
RUN ln -s /tmp /var/cache/matplotlib

RUN python{VERSION} -c "from astropy.config.paths import get_cache_dir, get_config_dir; print(get_cache_dir()); print(get_config_dir())"

# force download of basic astropy data
RUN python{VERSION} -c "from astropy.time import Time; Time.now().ut1"
RUN python{VERSION} -c "from astropy.coordinates import EarthLocation; EarthLocation.of_site('VLA')"

# this now disables astropy downloads so should be done last 
COPY astropy.cfg  /var/config/astropy

# change permissions inside image
RUN chmod -R a+rX /var/config/astropy /var/cache/astropy

CMD python{VERSION}

