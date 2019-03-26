FROM python:3.7.2-alpine3.9

RUN pip install dropbox

WORKDIR /btcpay-dropbox

COPY . /btcpay-dropbox

ENV DROPBOX_TOKEN=$DROPBOX_TOKEN

ENTRYPOINT ["python3", "dropbox-script.py"]
