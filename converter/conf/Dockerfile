FROM python:3.7-slim-buster


################################################################################
## install app
## copy files one by one and split commands to use docker cache
################################################################################

WORKDIR /code

COPY ./conf/pip /code/conf/pip
RUN pip install -q --upgrade pip && \
    pip install -q -r /code/conf/pip/requirements.txt

COPY ./ /code

RUN useradd -ms /bin/false trivago
RUN chown -R trivago: /code
RUN chmod +x /code/convert-cli.py

ENTRYPOINT ["/code/conf/entrypoint.sh"]
