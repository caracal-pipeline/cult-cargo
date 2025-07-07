# FROM {REGISTRY}/ddfacet:{VERSION}-cc0.2.0

#{REGISTRY}/python-base:{default_python_version}-{BUNDLE_VERSION}

# better than the lite python images -- otherwise numpy 2 causes kak
FROM ubuntu:22.04


ENV DEBIAN_FRONTEND noninteractive
ENV DEBIAN_PRIORITY critical

RUN apt-get update && \
   apt-get -y install \
       dpkg-dev \
       libc-dev \
       cmake \
       git \
       wget \
       subversion \
       rsync \
       python3-virtualenv \
       python3-pip \
       libfftw3-dev \
       python3-numpy \
       libfreetype6 \
       libfreetype6-dev \
       libpng-dev \
       pkg-config \
       python3-dev \
       libboost-all-dev \
       libcfitsio-dev \
       libhdf5-dev \
       wcslib-dev \
       libatlas-base-dev \
       liblapack-dev \
       python3-tk \
       libreadline6-dev \
       subversion \
       liblog4cplus-dev \
       libhdf5-dev \
       libncurses5-dev \
       flex \
       bison \
       libbison-dev \
       libqdbm-dev \
       libgsl-dev \
       make \
   && rm -rf /var/lib/apt/lists/* \
   && rm -rf /var/cache/apt/archives 

{pre_install}

RUN python{default_python_version} -mpip install --use-pep517 --no-cache-dir -U matplotlib mpl-tools dask-ms python-casacore casadata ninja
RUN python{default_python_version} -mpip install --use-pep517 --no-cache-dir {package} {extra_deps}

{post_install}

CMD DDF.py --help

