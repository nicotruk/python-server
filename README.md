[![Coverage Status](https://coveralls.io/repos/github/nicotruk/python-server/badge.svg?branch=Coverage)](https://coveralls.io/github/nicotruk/python-server?branch=Coverage)

# Python App Server:

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
    $ flask run
    ```
    4.2 Ejecutar aplicacion con gunicorn como webserver
    ```
    gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-file=-
    ```
5. Intalación de MongoDB (por línea de comandos)
```
$ sudo apt-get install -y mongodb-org
$ sudo service mongod start
```