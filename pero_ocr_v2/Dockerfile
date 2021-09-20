#FROM tiangolo/uvicorn-gunicorn:python3.8
FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    libgtk2.0-dev
#    libglib2.0-0 \
#    libsm6 \
#    libxrender1 \
#    libxext6

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

#COPY ./requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

# PERO-OCR 15/09/2021
RUN pip install git+git://github.com/DCGM/pero-ocr.git@8b20f2927b73b9398ed86c7a5843720b86da06b6

RUN conda install -y -c conda-forge hdbscan==0.8.26
RUN pip install opencv-python==4.2.0.32
RUN pip install torchvision

WORKDIR "/app"

## TODO remove reload in deployment
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
#


