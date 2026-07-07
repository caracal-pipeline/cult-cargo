FROM {REGISTRY}/casa6:6.7-{BUNDLE_VERSION}

{pre_install}

RUN uv pip -n install --system setuptools\<82 
RUN uv pip -n install --system {pip_install_flags} {package} {extra_deps}

{post_install}

CMD {CMD}
