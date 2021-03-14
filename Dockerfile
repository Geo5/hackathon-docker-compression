FROM python:3.9

WORKDIR /docker_compression

RUN apt update && apt-get install zstd -y
COPY . .
ENTRYPOINT ["python", "compress.py"]
