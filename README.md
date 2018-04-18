[![Build Status](https://travis-ci.org/taller2-2018-1-grupo2/python-server.svg?branch=master)](https://travis-ci.org/taller2-2018-1-grupo2/python-server)
[![Coverage Status](https://coveralls.io/repos/github/taller2-2018-1-grupo2/python-server/badge.svg?branch=master)](https://coveralls.io/github/taller2-2018-1-grupo2/python-server?branch=master)

# Python App Server

1. Generar entorno mediante virtualenv
```
$ virtualenv -p python3 env
```
2. Activar virtualenv
```
source ./env/bin/activate
```
3. Instalar las dependencias (debe hacerse corriendo en el env)
```
$ (sudo) pip install -r requirements.txt
```
4. Ejecutar aplicación utilizando flask como webserver

    4.1 Utilizando flask
    ```
    $ export FLASK_APP=app.py
    $ flask run --host=0.0.0.0 --port=8000
    ```
    4.2 Ejecutar aplicacion con gunicorn como webserver
    ```
    gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-file=-
    ```

### Intalación de MongoDB (por línea de comandos)

```
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```

### Instalacion con Docker

Proceder a la carpeta root del proyecto (en la que se encuentran los archivos Dockerfile y docker-compose.yml) y correr los siguientes comando:

```
(sudo) docker-compose build
```

```
(sudo) docker-compose up
```
