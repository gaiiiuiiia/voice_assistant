FROM python:3.10-slim

# добавление пользователя в контейнере
#ARG USER_ID
#ARG GROUP_ID
#
#RUN addgroup --gid $GROUP_ID userma
#RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID userma

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y libespeak-dev portaudio19-dev python3-pyaudio \
    && apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 \
    && apt-get install -y build-essential \
    && apt-get install -y python3-tk python3-dev \
    && apt-get install -y alsa-utils \
    && apt-get install -y ffmpeg \
    && apt-get install -y libmagic-dev

RUN pip install --upgrade pip setuptools

ADD . /app
ADD ./asound.conf /etc/

RUN pip install --no-cache-dir -r requirements.txt

# активация пользователя в контейнере
#USER userma

ENTRYPOINT ["/bin/bash"]
