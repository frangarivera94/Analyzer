# Guía de Despliegue para Aplicación Flask

## Descripción del Proyecto

Este proyecto es una aplicación web basada en Flask que incluye varias características de visualización de datos. Utiliza plantillas HTML, CSS para el diseño, y scripts en Python para generar gráficos interactivos con Plotly. La aplicación se puede desplegar en un servidor Windows o Linux.

Requisitos Previos

* Python 3.8 o superior

* Entorno Virtual: Para gestionar las dependencias y aislar el entorno.

* pip: Para instalar las dependencias necesarias.

 Archivos Incluidos

* carpeta_proyecto/: Esta carpeta contiene todos los scripts (.py), plantillas HTML (.html), hojas de estilo (.css) y otros recursos.

* requirements.txt: Una lista de todas las dependencias necesarias para el proyecto.

* README.md: Esta guía.

# Configuración del Entorno

## Instrucciones para Servidor Linux

Instalar Python (si no está instalado):

`sudo apt-get update`
`sudo apt-get install python3.8 python3-pip`

Crear un Entorno Virtual:

`python3 -m venv venv`
`source venv/bin/activate`

Instalar Dependencias:

`pip install -r requirements.txt`

Ejecutar la Aplicación Flask (Modo Desarrollo):

`flask run`

Instrucciones para Servidor Windows

Instalar Python:

Descargar desde sitio oficial de Python.

Agregar Python al PATH del sistema.

Crear un Entorno Virtual:

`python -m venv venv
venv\Scripts\activate`

Instalar Dependencias:

`pip install -r requirements.txt`

Ejecutar la Aplicación Flask (Modo Desarrollo):

`flask run`


Variables de Entorno:

FLASK_APP: Configurar a app.py para apuntar al script principal.

FLASK_ENV: Configurar a production para el modo de producción.

Configuración del Puerto: Asegúrate de que el puerto deseado esté abierto para conexiones externas.

Mantener la Aplicación Activa

Linux: Utilizar supervisor para mantener la aplicación corriendo:

`sudo apt-get install supervisor`



Para cualquier pregunta o problema relacionado con el despliegue, contacta a **coacopaco@gmail.com**.

