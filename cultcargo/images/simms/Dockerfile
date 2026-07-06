FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y python3.12 python3.12-venv python3-pip git \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives

RUN python3.12 -m pip install --no-cache-dir --break-system-packages -U pip setuptools wheel uv

{pre_install}

RUN uv pip -n install --system --python python3.12 {pip_install_flags} {package} {extra_deps}

{post_install}

CMD {CMD}
