---
title: Dummy System para Red Pitaya
subtitle: Tutorial de uso
layout: page
mathjax: true
---


## ¿Que es Dummy System?

Es una aplicación vacía de Red Pitaya, como las que se pueden ver en el repositorio
de aplicaciones "libres" (en el sentido de [software libre](https://es.wikipedia.org/wiki/Software_libre))
del proyecto Red Pitaya:
[https://github.com/RedPitaya/RedPitaya/tree/release-v0.95/apps-free](https://github.com/RedPitaya/RedPitaya/tree/release-v0.95/apps-free)
.

Este entorno permite configurar fácilmente un conjunto de controles Web (en HTML) que
serán mapeados a cables y registros en la capa FPGA, lo que permite resolver rápida y fácilmente
la interfaz gráfica de una aplicación y concentrarse únicamente en la programación FPGA en Verilog.

El Dummy System incluye:
  - El osciloscopio de las Apps libres de Red pitaya
  - El generador de funciones de las Apps libres de Red pitaya
  - Los filtros PID de las Apps libres de Red pitaya
  - Un panel extra de controles configurables
  - Multiplexores para seleccionar las señales que se quieren ver en el osciloscopio
    o enviar a las salidas
  - Opciones para guardar los datos del Osciloscopio.
  - Opciones para guardar el estado de la aplicación.
  - Scripts que facilitan la programación automática en C y HTML
  - Módulos pre-programados en verilog para funciones más habituales.
    - Filtro pasabajos
    - Filtro pasaaltos
    - Control de saturación
    - etc ...

## Instrucciones de uso

Estos son los pasos a seguir, a modo de tutorial, para crear un poryecto nuevo.

### Editar el archivo `config.ini`

Este archivo tiene una sección `[general]` donde se pueden elegir algunas opciones
para la aplicación a armar, como si debe incluir o no el generador de funciones
o los filtros PID.

Luego, cada sección será un control HTML que aparecerá en el panel de la izquierda
de la aplicación web, y será mapeado a un cable o registro de la FPGA.

Una vez configurados los controles / registros que se quieren disponer, se pasa
a crear el nuevo proyecto

### Crear la carpeta del nuevo proyecto

Dentro de la carpeta `rp_dummy` ejecutar:

```bash
./new_project.py NOMBRE
```

Eso creará el proyecto `dummy_NOMBRE`. Dentro de esa carpeta estará todo
el código fuente de la aplicación.

Antes de poder compilar la nueva aplicación es necesario cargar algunas variables
de entorno con el comando:

```bash
source settings.sh
```

Luego, sí, se puede ingresar a la carpeta del nuevo proyecto y realizar ediciones:

```bash
cd dummy_NOMBRE
```

### Estructura del nuevo proyecto

Dentro de la carpeta creada se encuentra la siguiente estructura de archivos y directorios

  - `index.html` : Página web con la interfaz gráfica
  - `src`: Carpeta con el código del controlador en `C` que permite
    "traducir" coma comandos de la página web en valores de memoria para
    modificar los registros de la FPGA. También acondiciona los datos leidos
    de la FPGA para enviarlos a la Web.
    - `main.c`: archivo principal
    - `worker.c`
    - `dummy.c`: Registros para el sistema Dummy
    - ...
  - `fpga`: Aquí está todo el código FPGA
    - `red_pitaya_vivado.tcl`: Instrucciones de síntesis e implementación.
    - `red_pitaya_vivado_project.tcl`: Instrucciones de síntesis e implementación en modo gráfico.
    - `rtl`: Carpeta con el código en Verilog.
      - `dummy.v`: **En este archivo hay que editar el código que se quiera implementar**.
      - `red_pitaya_top.v`: Archivo raíz de la implementación FPGA para Red Pitaya. Acá se instancian el osciloscopio y el generador de funciones.
      - `dummy`: Carpeta con módulos para instanciar dentro del archivo `dummy.v`.
  - `config_tool.py`: Comando de configuracion semi-automatizado.
  - `upload_app.sh`: Comando para subir la aplicación a una Red Pitaya.

### Editar el archivo `dummy.v`

Dentro del archivo Dummy hay secciones predefinidas para declarar cables y registros y otra
para instanciar módulos y cablearlos.

Hay cables importantes que ya están definidos, como `in1` e `in2`, que son las señales
provenientes de las entradas 1 y 2, o `out1` y `out2` que son las correspondientes
salidas.

También se hayan definidos los cables y registros asociados a el sistema Dummy, que habían
sido declarados en el archivo `config.ini`.

### Salidas y uso de osciloscopio

Las salidas `out1` y `out2` y las entradas de los canales del osciloscopio
`oscA` y `oscB` se encuentran conectados a las salidas de multiplexores, controlables
desde la aplicación web. De esta forma, se pueden configurar en esos multipexores varios
cables distintos para visualizar o para enviar señales de salida y elegir luego,
con la aplicación andando, cual de ellos usar.

### Compilación y síntesis

Una vez diseñado el cableado deseado, se pasa a compilar todo el proyecto
ejecutado los siguiente desde la carpeta `dummy_NOMBRE`:

```bash
./config_tool.py -a
make
```

Si todo sale bien, generará un archivo `red_pitaya.bit` .

### Probar aplicación

Para subir la aplicación a una Red Pitaya hay que saber el nombre de red de la
misma. Para ello, como se indica en la
[documentación oficial](http://redpitaya.readthedocs.io/en/latest/quickStart/troubleshooting/troubleshooting.html#how-to-find-red-pitaya-url-if-it-is-not-written-on-sticker),
se debe buscar en el dispositivo los últimos 6 valores de la MAC Address:

![mac]({{ site.baseurl }}/img/MAC.png "mac")

Luego usar esos valores para armar la dirección:
`rp-XXXXXX.local`.

Una vez que se tiene la dirección, ejecutar:


```bash
./upload_app.sh rp-XXXXXX.local
```

Se solicitará la contraseña de el usuario root de la Red Pitaya
(por defecto: `root`), si es que no se dispone de login automático con
clave SSH.

Si finaliza sin errores, ya se puede acceder a la aplicación ingresando desde
el navegador a:

`http://rp-XXXXXX.local`

### Abrir la aplicación gráfica

Si se quiere ver cómo fue implementado el sistema desde la interfaz gráfica
de Xilinx Vivado, se debe ingresar a la carpeta `fpga` y desde allí ejecutar:

```bash
cd fpga/
LANG=C make project
```

### Limpiar la carpeta para re-compilar

Si se va a volver a compilar / sintetizar código luego de un cambio es
necesario limpiar los binarios. Esto se puede hacer desde la carpeta
`dummy_NOMBRE` con el comando:

```bash
make clean
```
