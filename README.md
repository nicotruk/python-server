# App Server

[![Build Status](https://travis-ci.org/taller2-2018-1-grupo2/python-server.svg?branch=master)](https://travis-ci.org/taller2-2018-1-grupo2/python-server)
[![Coverage Status](https://coveralls.io/repos/github/taller2-2018-1-grupo2/python-server/badge.svg?branch=master)](https://coveralls.io/github/taller2-2018-1-grupo2/python-server?branch=master)

## Setup

1. Generar entorno mediante virtualenv `virtualenv -p python3 env` o pyenv `pyenv env`.
1. Activar virtualenv/pyenv con `source ./env/bin/activate`.
1. Instalar las dependencias (debe hacerse corriendo en el env) con `(sudo) pip install -r requirements.txt`.
1. Ejecutar aplicación utilizando un webserver:
    * Utilizando flask `export FLASK_APP=app.py && flask run --host=0.0.0.0 --port=8000`.
    * Ejecutar aplicacion con gunicorn como webserver `gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-level=debug`

### Instalación de MongoDB

Correr en una terminal la siguiente línuea de comandos

```
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```

## Instalacion con Docker

> **Nota:** se necesita [Docker](https://www.docker.com/) instalado en la máquina para ejecutar estos pasos. Para ello, sigue estas instrucciones [en Mac](https://docs.docker.com/docker-for-mac/install/) o [en Windows](https://docs.docker.com/docker-for-windows/install/). Al finalizar la instalación, valida que todo funciona correctamente corriendo `docker --version`.

1. Abrir una terminal en el directorio base del proyecto.
1. Construye la imagen de docker con los siguientes comandos:

    ```
    (sudo) docker-compose build
    (sudo) docker-compose up
    ```
