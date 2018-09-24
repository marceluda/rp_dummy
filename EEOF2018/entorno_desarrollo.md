---
title: Instalación del entorno de desarrollo
subtitle: Ubuntu linux + Xilinx Vivado 2005.2 + linaro
layout: page
mathjax: true
---

## Instalación del sistema operativo

Para la demostración del taller en EEOF 2018 se prepararon máquinas con
[Ubuntu MATE](https://ubuntu-mate.org/)] 16.04 LTS.

No se describirá cómo hacer esa instalación. Pero hay muchos tutoriales web que
explican paso a paso, ya sea para Ubuntu o para Ubuntu MATE (cualquiera es indistinto).

  - [Tutorial de instalación](https://www.profesionalreview.com/2016/06/08/como-instalar-ubuntu-16-04-lts-en-tu-pc-paso-a-paso/)

Se necesita instalar algun sistema Linux porque el framework para compilación de
aplicaciones para Red Pitaya corre en Linux. En algunos casos
se puede instalar el sistema operativo GNU/Linux junto al windows o en una
[máquina virtual](http://pavel-demin.github.io/red-pitaya-notes/development-machine/).


## Preparación del entorno de desarrollo

Una vez instalado, hay que instalar algunos paquetes extra. Desde una consola se
puede correr:

```bash
sudo apt install -y build-essential chromium-browser geany xtightvncviewer git libvte9

TOOLCHAIN="http://releases.linaro.org/15.02/components/toolchain/binaries/arm-linux-gnueabihf/gcc-linaro-4.9-2015.02-3-x86_64_arm-linux-gnueabihf.tar.xz"
curl -O $TOOLCHAIN
sudo mkdir -p /opt/linaro
sudo chown $USER:$USER /opt/linaro
tar -xpf *linaro*.tar.xz -C /opt/linaro

```

Luego hay que descargar el [Vivado Designs Suite 2015.2 para linux](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive.html).
Tiene que ser esa versión, porque el código aún no fue portado para las posteriores.

```bash
tar -xzf Xilinx/Xilinx_Vivado_SDK_Lin_2015.2_0626_1.tar.gz
sudo Xilinx_Vivado_SDK_Lin_2015.2_0626_1/xsetup
```

Instalar el WebPack, que se puede usar gratuitamente.

En el mismo sitio de Xilinx se puede acceder a una licencia gratuita de por vida
para el uso de WebPack

Para cargar la licencia, una vez obtenida, hay que correr como usuario el manejador
de licencias:

```bash
/opt/Xilinx/Vivado/2015.2/bin/vlm
```
