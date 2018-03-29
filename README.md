Para correr:

1. Generar entorno mediante virtualenv

```
$ virtualenv -p python3 env
```
2. Activar virtualenv
´´´
source ./env/bin/activate
´´´

3. Instalar las dependencias (debe hacerse corriendo en el env)
```
$ (sudo) pip install -r requirements.txt
```

5. Ejecutar aplicación utilizando flask como webserver

5.1 Utilizando flask
```
$ export FLASK_APP=app.py
$ flask run
```

5.2 Ejecutar aplicacion con gunicorn como webserver
```
gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-file=-
```
