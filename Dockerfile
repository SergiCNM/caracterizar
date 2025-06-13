FROM python:3.11.5
COPY . usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
# for solve error => ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y

CMD [ "python", "./main.py" ]