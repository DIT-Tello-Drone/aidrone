FROM tensorflow/tensorflow:2.4.0-gpu-jupyter
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

RUN /opt/conda/bin/conda install av -c conda-forge
ENV TZ=Europe/Warsaw DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install python3-opencv libswscale-dev libavcodec-dev libavutil-dev -yq
RUN pip install opencv-python opencv-contrib-python aiohttp aiortc minio jinja2 cachetools pyyaml pyzmq aiohttp_cors ujson qdi tensorflow-hub
RUN pip install https://github.com/damiafuentes/DJITelloPy/archive/master.zip
RUN git clone --depth 1 https://github.com/tensorflow/models
RUN apt install -y protobuf-compiler
RUN cd models/research/ && \
        protoc object_detection/protos/*.proto --python_out=. && \
        cp object_detection/packages/tf2/setup.py . && \
        python -m pip install -v .

WORKDIR /app
COPY ./app /app
RUN cp /tf/models/research/object_detection/data/mscoco_label_map.pbtxt / && rm -rf /tf/models/

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

