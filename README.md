# Proyecto-Backend

SP3-Integracion
[![Codeship Status for MISO4101-202010/Proyecto-Backend](https://app.codeship.com/projects/5db252f0-697c-0138-1110-6a1b1fd1aa4f/status?branch=SP3-Integracion)](https://app.codeship.com/projects/394230)

SP3-Release
[![Codeship Status for MISO4101-202010/Proyecto-Backend](https://app.codeship.com/projects/5db252f0-697c-0138-1110-6a1b1fd1aa4f/status?branch=SP3-Release)](https://app.codeship.com/projects/394230)

Codacy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4be13517ea7d45b4ac36718541bb1c77)](https://www.codacy.com/gh/MISO4101-202010/Proyecto-Backend?utm_source=github.com&utm_medium=referral&utm_content=MISO4101-202010/Proyecto-Backend&utm_campaign=Badge_Grade)

Backend del proyecto MISO4101-202010

## Uso de pipenv

## Contenido

-   [Instalación del entorno de desarrollo](#instalación-del-entorno-de-desarrollo)
    -   [MacOS](#mac-os)
-   [Crear entorno de desarrollo](#crear-entorno-de-desarrollo)
-   [Instalar librerias](#instalar-librerias)
-   [Iniciar servidor](#iniciar-servidor)

* * *

## Instalación del entorno de desarrollo

### MacOS

#### Python 3

```sh
brew upgrade python3
pip install pipenv
```

## Crear entorno de desarrollo

```sh
cd Proyecto-Backend
pipenv --python /usr/local/opt/python@3.8/bin/python3
```

**Siempre debe ingresar al entorno de desarrollo para depurar**

Sobre la carpeta **Proyecto-Backend** del proyecto

```sh
pipenv shell
```

* * *

## Instalar librerias

```sh
pipenv install
```

* * *

## Iniciar servidor

```sh
python3 manage.py runserver
```
