FROM ubuntu:latest
RUN apt update -y && apt upgrade -y
RUN apt install build-essential -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update -y
RUN apt install python3.7 -y
RUN apt install python3.7-venv python3.7-dev unzip -y
COPY . /app
WORKDIR /app
RUN apt install python3-pip -y
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --upgrade -r requirements.txt
ENTRYPOINT ["src/main.py"]
CMD ["python3.7", "src/main.py"]