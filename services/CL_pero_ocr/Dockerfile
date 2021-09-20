#FROM tiangolo/uvicorn-gunicorn:python3.8
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get update && \
    apt-get install -y \
    git \
    curl
#    python3.8 \
#    python3-pip

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Install miniconda to /miniconda

RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
RUN bash Miniconda3-py37_4.8.2-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda3-py37_4.8.2-Linux-x86_64.sh
#RUN curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh
#RUN bash Miniconda3-py38_4.10.3-Linux-x86_64.sh -p /miniconda -b
#RUN rm Miniconda3-py38_4.10.3-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

RUN conda install -y python=3.7 && conda install -y pip

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install pero-ocr==0.4 --ignore-installed tensorflow-gpu
# PERO-OCR
RUN pip install git+git://github.com/DCGM/pero-ocr.git@ade605d751c1bae076aa1327861d3f2ea44a5c05

## Copy dependencies
#COPY ./API/translation/ /app/API/translation
## Copy all the subdirs.
#COPY ./CEF-eTranslation_connector/ /app
#COPY ./multilingual_pageXML/ /app/multilingual_pageXML

RUN conda install -y -c conda-forge opencv==4.2.0 && \
  conda install -c conda-forge hdbscan==0.8.26
# RUN apt-get install -y libx11-6

WORKDIR "/app"

# TODO remove reload in deployment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]

RUN pip install opencv-python==4.2.0.32

