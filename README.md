# rp_dummy
Empty Red Pitaya Oscilloscope application for test and development purposes

Based in [Scope App v0.95](https://github.com/RedPitaya/RedPitaya/tree/release-v0.95/apps-free/scope)
of community applications for Red Pitaya Project.


# Begin a new project

To start a new project you just need to run the new_project.py script. This script reads
a config fila and creates a new dummy folder with added HTML controllers, already mapped
to FPGA Verilog registers.

`./new_project.py [-c CONFIG] [-u] AppName`

Default config file: config.ini

Edit the config file before running the new_project.py script.

## Make your circuit design

First, you need to load the Vivado (FPGA synthesys tool) and Linaro (cross
compiling C languge) envoroment variables, executing:

```
source settings.sh

```

If your Linaro version is not the same as in the settings.sh file, adit it and correct it.

Inside the created folder you will find severla files and folders:

css, js, index.html : files/folders related to Web GUI. You may need to edit index.html
                      to change controllers names or style.

fpga                : Inside this folder are all the FPGA Verilog modules
info                : Just version information and app icon
py                  : Python scripts for remote control
src                 : C source code

You may want to start editing the file:

fpga/rtl/dummy.v

You have there wires for all the inputs/outputs and the memory registers.

If you want to instantiate new modules, just paste them or create them in folder:

fpga/rtl/dummy/

And after that, run:

```
./config_tool.py -a
```

After that you can use the added module inside the dummy.v file for your project.

## Compile all

To compile the C components, run:

```
make app
```

To compile the FPGA circuit, run:

```
make fpga
```

If you have to re-compila one of this parts, first clean it:

```
make clean_fpga
make clean_app
```
or
```
make clean
```

## Example of compilation / synthesys:

```
./new_project.py  NAME
source settings.sh
cd dummy_NAME
make
```

## Upload testing application to a Red Pitaya device

The file rp_dummy/_settings.env  has the parameters for ssh testing upload

It looks like:

```
RPIP=rp-XXXXXX.local
RPOPTS=-l root -p 22
RPSCP=-P 22
```

You have to edit it and set RPIP to your RP address.

Then, you can run the upload command inside the project folder

```
make upload
```


# Other Resources:

  - [Write MicroSD card for Red Pitaya](http://redpitaya.readthedocs.io/en/latest/quickStart/SDcard/SDcard.html)
