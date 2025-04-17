#FROM {REGISTRY}/base-cult:{BUNDLE_VERSION}
FROM python:{VERSION}-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install apt-utils && \
    apt-get install -y python3-pip git \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives 

## left as reminder in case of future problems
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python{VERSION} 1

## left as reminder in case of future problems
## needed to upgrade pip properly -- sometimes it gets stuck and is unable to upgrade itself
#RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python{VERSION}

RUN python{VERSION} -m pip install --no-cache-dir -U pip setuptools wheel packaging uv

## install stimela -- needed to form output arguments
RUN python{VERSION} -m pip install --no-cache-dir stimela

CMD python{VERSION}

