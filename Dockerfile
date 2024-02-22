FROM ubuntu:latest 

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y 


ENTRYPOINT ["python3", "ktp.py"]
