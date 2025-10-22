FROM {REGISTRY}/{default_pip_base_image}:{default_python_version}-{BUNDLE_VERSION}

{pre_install}

RUN uv python pin python{default_python_version}
RUN uv pip -n install --system {package} {extra_deps}

## leaving old command for reference
# RUN python{default_python_version} -m pip install --no-cache-dir {package} {extra_deps}

{post_install}

CMD {CMD}
