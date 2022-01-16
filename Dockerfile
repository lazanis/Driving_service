FROM python:3.8

WORKDIR /Driving_service_image
ADD . /Driving_service_image

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip3 install pip --upgrade
RUN /opt/venv/bin/pip3 install -r requirements.txt

CMD . /opt/venv/bin/activate && exec python3 app.py
