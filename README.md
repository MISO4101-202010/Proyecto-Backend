# Proyecto-Backend

[![Codeship Status for MISO4101-202010/Proyecto-Backend](https://app.codeship.com/projects/8990d090-6974-0138-28d7-22c0d1c6829f/status?branch=master)](https://app.codeship.com/projects/394223)

Backend del proyecto MISO4101-202010

## Uso de pipenv

## Contenido

- [Instalación del entorno de desarrollo](#instalación-del-entorno-de-desarrollo)
  - [MacOS](#mac-os)
- [Crear entorno de desarrollo](#crear-entorno-de-desarrollo)
- [Instalar librerias](#instalar-librerias)
- [Iniciar servidor](#iniciar-servidor)

***


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
***
## Instalar librerias

```sh
pipenv install
```

***

## Iniciar servidor

```sh
python3 manage.py runserver
```
