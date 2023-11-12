# base image
FROM python:3.11.6
#apt-get의version을갱신하고, SoLite3의설치
RUN apt-get update && apt-get install -y sqlite3

# 디렉터리와 파일의 복사
WORKDIR /app

# upgrade pip
RUN pip install --upgrade pip
COPY ./requirements.txt .
# install pip library
RUN pip install -r requirements.txt

COPY . .

# 필요한 각 환경 변수를 설정
ENV FLASK_APP=app.py

# CMD ["flask", "run", "-h", "0.0.0.0"]