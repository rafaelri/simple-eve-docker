FROM python:3.7.7-stretch
WORKDIR /src
VOLUME /var/eve
ENV DB_URL sqlite:////var/eve/teste.db
ADD . /src/
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "app.py"]
