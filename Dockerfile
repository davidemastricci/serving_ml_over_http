FROM python:3.8

ARG VERSION

LABEL org.label-schema.version=$VERSION

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install -r requirements.txt

COPY src/* /webapp

ENTRYPOINT [ "python" ]

CMD [ "flask_app.py" ]