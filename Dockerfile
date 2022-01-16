FROM python:3.8

WORKDIR /Driving_service_image
ADD . /Driving_service_image
RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
