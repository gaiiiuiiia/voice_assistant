FROM python:3.10-slim

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y libespeak-dev portaudio19-dev python3-pyaudio \
    && apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 \
    && apt-get install -y build-essential \
    && apt-get install -y python3-tk python3-dev

RUN pip install --upgrade pip setuptools

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash"]
