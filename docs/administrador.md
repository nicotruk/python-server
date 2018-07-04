# Manual de Administrador - Stories App Server
---

## Índice
---
* Generalidades
  * ¿Qué es Stories App Server?
  * Características y ventajas de Stories App Server
  * Requisitos
    * Para instalación local
      * Instalación local (sin Docker)
      * Instalación local (con Docker)
    * Para instalación remota (Deploy en Heroku)
* Instalación y Configuración
  * Instalación local
    * Instalación de MongoDB
    * Instalación local (sin Docker)
    * Instalación local (con Docker)
  * Deploy en PaaS (Heroku) - Utilizando Docker
  * Configuración de variables de entorno
* Uso de la Aplicación


## 1. Generalidades
---
### 1.1. ¿Qué es Stories App Server?
---

* Stories App Server, como su nombre lo indica, es una aplicación por consola que funciona como backend, sirviendo datos y proveyendo logica de negocio mediante una interfaz [REST](https://github.com/taller2-2018-1-grupo2/python-server/blob/master/stories_app_server.json) para "Stories", una red social desarrollada en la plataforma Android para uso masivo por parte de los usuarios, con el objeto de compartir imagenes y videos, conectarse con otros amigos y enviar mensajes, entre otras cosas. 
El App Server funciona como una capa de negocio entre la aplicación "Stories" y la base de datos de la misma, realizada utilizando MongoDB, en la cual se guardan todos los datos necesarios para el uso de la aplicación por los usuarios.
A su vez, el App Server también tiene la responsabilidad comunicarse con el Shared Server de la aplicación "Stories" mediante la interfaz REST provista por este con el fin de servir de fachada en caso de que la aplicación de Android necesitara de algun servicio provisto por el Shared Server.

### 1.2. Características y ventajas de Stories App Server
---
* Fácil instalación
* Soporte de instalación en múltiples servicios de PaaS (Heroku, AWS, etc.) que soporten MongoDB. A efectos de este manual, se ejemplificará su instalación y uso en Heroku.
* Instalación local completa en cualquier sistema gracias al uso de Docker Compose.

### 1.3. Requisitos
---
#### 1.3.1. Para instalación local
---
##### 1.3.1.1. Instalación local (sin Docker)
---
* Python (versión 2.7 o 3.x)
* VirtualEnv
* PIP
* MongoDB

##### 1.3.1.2. Instalación local (con Docker)
---
* Docker (para Mac, Windows o Linux). 
    > **Nota:** En el caso de Linux, se debe tener instalado tambien Docker Compose.
* MongoDB

#### 1.3.2. Para instalación remota (Deploy en Heroku)
---
* Registrarse previamente como usuario en la pltaforma Heroku (PaaS)
* Registrarse en algun servicio de DBaaS como mLab, por ejemplo. (Heroku ofrece algunas opciones, entre ellas mLab)
* Docker (para Mac, Windows o Linux)

## 2. Instalación y Configuración
---
Como primera medida para la instalación de esta aplicación, habrá que clonar el repositorio en nuestra máquina utilizando el siguiente comando:

```
$ git clone https://github.com/taller2-2018-1-grupo2/python-server.git
``` 
> **Nota:** Vale aclarar que para la clonación de este repositorio habrá que tener instalado Git. Podemos encontrar instrucciones sobre como hacer esto para los distintos sistemas operativos en [este](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) link. 

### 2.1. Instalación local
---
>**Nota:** Una instalación de este tipo puede ser útil para realizar pruebas o efectuar cambios en el App Server sin afectar al ambiente de producción que usan nuestros usuarios.

#### 2.1.0. Instalación de MongoDB
---
* [Linux](https://docs.mongodb.com/manual/administration/install-on-linux/)
* [macOS](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
* [Windows](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)

#### 2.1.1. Instalación local (sin Docker)
---
>**Nota:** Las siguientes instrucciones son validas para sistemas UNIX (Linux/macOS). Para sistemas Windows, utilizar Docker (instrucciones en 2.1.2. Instalación local (con Docker))

Para la instalación local sin utilizar Docker, se deberán seguir los siguientes pasos: 
1. Abrir una terminal en el directorio base del proyecto.
2. Generar entorno mediante VirtualEnv (NOTA: En caso de tener instalado Python 2.7 en lugar de Python 3.x, cambiar *python3* por *python* en el comando.)
    ```
    $ virtualenv -p python3 env
    ``` 
    o PyEnv:
    ```
    $ pyenv env
    ``` 
3. Activar virtualenv/pyenv con el comando:
    ```
    $ source ./env/bin/activate
    ``` 
4. Instalar las dependencias (debe hacerse corriendo en el env) con
    ```
    $ (sudo) pip install -r requirements.txt
    ``` 
5. Ejecutar la aplicación utilizando un webserver con:
    ```
    $ export FLASK_APP=app.py
    $ flask run --host=0.0.0.0 --port=8000
    ``` 
    o
    ```
    $ gunicorn -w 4 -b 0.0.0.0:8000 app:app --log-level=debug
    ``` 
    > **Nota:** La segunda opción, utilizando Green Unicorn (*gunicorn*) nos permite utilizar el sistema de logueo de la aplicación, que puede ser muy útil a la hora de descubrir errores en la misma.
    
6. Para enviar un request a la aplicación, utiliza la direccion: `http://0.0.0.0:8000/api/v1` como se indica en la sección ***Uso de la Aplicación*** a continuación.
    
#### 2.1.2. Instalación local (con Docker)
---
> **Nota:** como se aclara en los requisitos, se necesita [Docker](https://www.docker.com/) instalado en la máquina para ejecutar estos pasos. Para ello, sigue estas instrucciones [en Mac](https://docs.docker.com/docker-for-mac/install/) o [en Windows](https://docs.docker.com/docker-for-windows/install/). Al finalizar la instalación, valida que todo funciona correctamente corriendo `docker --version`.

Para la instalación local utilizando Docker, se deberán seguir los siguientes pasos:

1. Abrir una terminal en el directorio base del proyecto
2. Construye la imagen de Docker con el siguiente comando:
    ```
    $ (sudo) docker-compose build
    ```
3. Corre la imagen de Docker construido con el siguiente comando:
    ```
    $ (sudo) docker-compose up
    ```
4. Para enviar un request a la aplicación, utiliza la direccion: `http://0.0.0.0:5000/api/v1` como se indica en la sección ***Uso de la Aplicación*** a continuación.

### 2.2. Deploy en PaaS (Heroku) - Utilizando Docker
---
> **Nota:** Como se menciono antes, para el deploy de la aplicación en Heroku será necesario tener un usuario registrado en este servicio.

Para el deploy de nuestra aplicación en Heroku, será necesario seguir los siguientes pasos (los mismos se encuentran explicados con más detalle en [este](https://devcenter.heroku.com/articles/container-registry-and-runtime) link):

1. Abrir una terminal en el directorio base de nuestro proyecto.
2. Loguearse a Heroku Container Registry con las credenciales del usuario creado anteriormente, usando el siguiente comando:
```
$ heroku container:login
```
3. Una vez logueado, ingresar el siguiente comando para crear una aplicación en Heroku:
```
$ heroku create
```
4. Por último, construimos nuestra imagen (según el Dockerfile de nuestro proyecto) y la subimos a Heroku:
```
$ heroku container:push web
```
5. Ahora, podemos abrir nuestra aplicación en su dirección asignada mediante:
```
$ heroku open
```

### 2.3. Configuración de variables de entorno
---
En cuanto a las variables de entorno necesarias para correr el App Server con éxito, las mismas se encuentran ya definidas y seteadas en los respectivos Dockerfile y docker-compose.yml utilizados tanto para la instalación local como para la remota. 

Por último, para el caso de la *Instalación local (sin Docker)*, la aplicación utilizará los valores por defecto seteados en la misma para esas variables de entorno y de esta forma la aplicación funcionara correctamente.

## 3. Uso de la Aplicación
---

Para el uso del App Server, cabe recordar que su **API** (Application Programming Interface, o Interfaz de Programación de Interfaces, en castellano) será consumido principalmente por la aplicación de Android "Stories", como se menciono previamente en este documento.

Aun así, el mismo puede consumirse fuera de la aplicación de Android mediante el uso de algún entorno de desarrollo de APIs como Postman. Esto debe hacerse utilizando las direcciones encontradas en los puntos 6 del inciso 2.1.1. *Instalación local (sin Docker)* y 4 del inciso 2.1.2. *Instalación local (con Docker)* y agregandole a estas la extensión de cada URI de cada recurso según la [especificación](https://github.com/taller2-2018-1-grupo2/python-server/blob/master/stories_app_server.json) del API REST encontrada en este mismo repositorio.

