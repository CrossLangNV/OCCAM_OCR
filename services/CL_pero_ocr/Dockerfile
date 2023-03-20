FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

RUN apt-get update && apt-get install -y python3-opencv

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# PERO-OCR - release 0.6.1
RUN pip3 install pero-ocr==0.6.1


COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#https://stackoverflow.com/questions/73171473/how-to-resolve-error-could-not-build-wheels-for-hdbscan-which-is-required-to-i
RUN conda install -c conda-forge hdbscan

# Issue with Protobuf
# https://stackoverflow.com/questions/72441758/typeerror-descriptors-cannot-not-be-created-directly
RUN pip3 install protobuf==3.20.*

WORKDIR "/app"

# TODO remove reload in deployment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
