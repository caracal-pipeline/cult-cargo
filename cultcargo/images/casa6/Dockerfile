FROM {REGISTRY}/python-base:{default_python_version}-{BUNDLE_VERSION}

RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install xvfb python3-casacore libblas-dev liblapack-dev libfuse-dev fuse \
    libgoogle-perftools-dev libglib2.0-0 libqt5gui5 \
   && rm -rf /var/lib/apt/lists/* \
   && rm -rf /var/cache/apt/archives 

RUN uv python pin python{default_python_version}
 
## leaving old command for reference
#RUN pip install --no-cache-dir --upgrade numpy casatools=={wheel_version} casatasks=={wheel_version} casaplotms casaconfig casadata

# NB: protobuf==3.20 required by casa
RUN uv pip -n install --system --upgrade numpy \
    casatools=={wheel_version} casatasks=={wheel_version} casaplotms casaconfig casadata protobuf==3.20

RUN mkdir -p /opt/casa/data

COPY casasiteconfig.py /opt/casa

ENV CASASITECONFIG /opt/casa/casasiteconfig.py

RUN python{default_python_version} -m casaconfig --measurespath /opt/casa/data --update-all

RUN python{default_python_version} -m casaconfig --measurespath /opt/casa/data --current-data

# extract casaplotms AppImage 
RUN cd opt; /usr/local/lib/python{default_python_version}/site-packages/casaplotms/__bin__/casaplotms-x86_64.AppImage --appimage-extract
RUN mv /opt/squashfs-root /opt/casaplotms
RUN chmod -R go+rx /opt/casaplotms
RUN sed -i -e "s|app_path = __os.path.join( __os.path.abspath( __os.path.join(__os.path.dirname(__file__),\"..\") ), '__bin__/casaplotms-x86_64.AppImage')|app_path = '/opt/casaplotms/usr/bin/casaplotms'|g" /usr/local/lib/python{default_python_version}/site-packages/casaplotms/private/plotmstool.py
ENV LD_LIBRARY_PATH /opt/casaplotms/usr/lib/
ENV QT_QPA_PLATFORM_PLUGIN_PATH /opt/casaplotms/usr/lib/plugins/platforms

# point to CASA data
RUN mkdir -p /usr/local/share/data/
RUN ln -s /opt/casa/data /usr/local/share/data/casacore

CMD python{default_python_version}
