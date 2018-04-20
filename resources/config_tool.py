#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import unique,ceil
import os
import enum
from datetime import datetime
import re
import argparse

from config_lib import *

import configparser


#%%


do_verilog = False
do_main    = False
do_html    = False
do_py      = False

if '__file__' in globals():
    scriptFolder = os.path.dirname(os.path.realpath(__file__))
else:
    scriptFolder = 'rp_dummy/resources'


folder = os.path.sep.join(scriptFolder.split(os.path.sep)[:-1]) # + os.path.sep + AppName

# Save original working directory for later
cwd = os.getcwd()

# Change to configuration folder
os.chdir(folder)
print('Working folder: '+folder)


#%%


AppName = 'dummy'

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(
                description='Configure the Dummy app files to ease the Web Browser <--> C controller <--> FPGA registers comunication'
            )

    parser.add_argument("AppName", type=str,
                        help="Name of the application folder")
    parser.add_argument("-v", "--do-verilog", dest='do_verilog', action="store_true",
                        help="configure verilog files")
    parser.add_argument("-m", "--do-main"   , dest='do_main'   , action="store_true",
                        help="configure C files")
    parser.add_argument("-w", "--do-html"   , dest='do_html'   , action="store_true",
                        help="configure web HTML index file")
    parser.add_argument("-p", "--do-python" ,  dest='do_py'    , action="store_true",
                        help="configure HTML index file")
    parser.add_argument("-a", "--all"       ,  dest='do_all'   , action="store_true",
                        help="configure all the files")

    parser.add_argument("-n", "--create-new" ,  dest='new'     , action="store_true",
                        help="Create new AppName folder if does not exist")

    parser.add_argument("-c", "--config-file" ,  dest='config', default=os.path.join(folder,'config.ini') ,type=str,
                        help="Read configuration from this file")

    args = parser.parse_args()

    AppName = args.AppName

    if not os.path.isdir(  os.path.join(folder,AppName) ):
        if args.new:
            print('Creating folder: '+ AppName)
            os.system('cp -a dummy '+args.AppName)
        else:
            print('"{:s}" is not a folder or does not exists'.format(args.AppName))
            exit(1)


    if args.do_all:
        args.do_verilog = True
        args.do_main     = True
        args.do_html    = True
        args.do_py      = True


    if args.new:
        #print(args.config.read())
        config = configparser.ConfigParser()
        if folder in args.config:
            config_file = args.config
        else:
            config_file = os.path.join(cwd,args.config)

        config.read(config_file)
        print('Reading configuration from: '+ config_file )
        #print(config.sections())


        txt_control=[]
        txt_monitor=[]

        print('paste this in config_tool.py file:\ngrp="dummy"')
        for section in config.sections():
            if section == 'general':
                print('PENDING: configure genfun and pids')
                continue
            c_type  = config.get(section,'type')
            c_label = config.get(section,'label')
            if c_type=='combo' or c_type=='number' or c_type=='monitor':
                c_nbits = config.getint(section,'bits_number')
            else:
                c_nbits = 1

            if c_type=='number' or c_type=='monitor':
                c_signed = config.getboolean(section,'signed')
            else:
                c_signed = False

            if c_type=='combo':
                txt_control.append( print_html_combo(    section,c_label,c_nbits) )
            if c_type=='number':
                txt_control.append( print_html_number(   section,c_label,c_nbits,c_signed) )
            if c_type=='checkbox':
                txt_control.append( print_html_checkbox( section,c_label) )
            if c_type=='button':
                txt_control.append( print_html_button( section,c_label) )
            print('f.add( name="'+section+'"               , group=grp , val=    0, rw='+ ('False' if c_type=='monitor' else 'True')+
                         ',  nbits='+str(c_nbits)+
                         ', min_val=      '+( str(-2**(c_nbits-1)) if c_signed else '0' )+
                         ', max_val=      '+( str(2**(c_nbits-1)-1) if c_signed else str(2**c_nbits-1))+
                         ', fpga_update='+('False' if c_type=='monitor' else 'True')+
                         ' , signed='+str(c_signed)+
                         ' , desc="Added automatically by script" )')

            #print(c_type,c_label)
            #print(c_nbits,c_signed)

        update_html_controls(os.path.join(folder,AppName,'index.html'),
                             'Dummy panel controls',
                             txt='\n'.join(txt_control)
                             )
        print('After updating config_tool.py, run it with -a option for '+ AppName)
        exit(0)



#%%

f = fpga_registers()

# Oscilloscope
grp='scope'
f.add( name="oscA_sw"            , group=grp , val=    1, rw=True ,  nbits= 5, min_val=          0, max_val=         31, fpga_update=True , signed=False, desc="switch for muxer oscA" )
f.add( name="oscB_sw"            , group=grp , val=    2, rw=True ,  nbits= 5, min_val=          0, max_val=         31, fpga_update=True , signed=False, desc="switch for muxer oscB" )
f.add( name="osc_ctrl"           , group=grp , val=    3, rw=True ,  nbits= 2, min_val=          0, max_val= 4294967295, fpga_update=True , signed=False, desc="oscilloscope control\n[osc2_filt_off,osc1_filt_off]" )
f.add( name="trig_sw"            , group=grp , val=    0, rw=True ,  nbits= 8, min_val=          0, max_val=        255, fpga_update=True , signed=False, desc="Select the external trigger signal" )

# Outputs
grp='outputs'
f.add( name="out1_sw"            , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer out1" )
f.add( name="out2_sw"            , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer out2" )
f.add( name="slow_out1_sw"       , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer slow_out1" )
f.add( name="slow_out2_sw"       , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer slow_out2" )
f.add( name="slow_out3_sw"       , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer slow_out3" )
f.add( name="slow_out4_sw"       , group=grp , val=    0, rw=True ,  nbits= 4, min_val=          0, max_val=         15, fpga_update=True , signed=False, desc="switch for muxer slow_out4" )

# Other signals
grp='inout'
f.add( name="in1"                , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="Input signal IN1" )
f.add( name="in2"                , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="Input signal IN2" )
f.add( name="out1"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="signal for RP RF DAC Out1" )
f.add( name="out2"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="signal for RP RF DAC Out2" )
f.add( name="slow_out1"          , group=grp , val=    0, rw=False,  nbits=12, min_val=      -2048, max_val=       2047, fpga_update=True , signed=False, desc="signal for RP slow DAC 1" )
f.add( name="slow_out2"          , group=grp , val=    0, rw=False,  nbits=12, min_val=      -2048, max_val=       2047, fpga_update=True , signed=False, desc="signal for RP slow DAC 2" )
f.add( name="slow_out3"          , group=grp , val=    0, rw=False,  nbits=12, min_val=      -2048, max_val=       2047, fpga_update=True , signed=False, desc="signal for RP slow DAC 3" )
f.add( name="slow_out4"          , group=grp , val=    0, rw=False,  nbits=12, min_val=      -2048, max_val=       2047, fpga_update=True , signed=False, desc="signal for RP slow DAC 4" )
f.add( name="oscA"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="signal for Oscilloscope Channel A" )
f.add( name="oscB"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="signal for Oscilloscope Channel B" )


# Automated add
f.add( name="comboA"               , group=grp , val=    0, rw=True,  nbits=4, min_val=      0, max_val=      15, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="comboB"               , group=grp , val=    0, rw=True,  nbits=4, min_val=      0, max_val=      15, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="numberA"               , group=grp , val=    0, rw=True,  nbits=14, min_val=      -8192, max_val=      8191, fpga_update=True , signed=True , desc="Added automatically by script" )
f.add( name="numberB"               , group=grp , val=    0, rw=True,  nbits=14, min_val=      -8192, max_val=      8191, fpga_update=True , signed=True , desc="Added automatically by script" )
f.add( name="checkboxA"               , group=grp , val=    0, rw=True,  nbits=1, min_val=      0, max_val=      1, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="checkboxB"               , group=grp , val=    0, rw=True,  nbits=1, min_val=      0, max_val=      1, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="buttonA"               , group=grp , val=    0, rw=True,  nbits=1, min_val=      0, max_val=      1, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="buttonB"               , group=grp , val=    0, rw=True,  nbits=1, min_val=      0, max_val=      1, fpga_update=True , signed=False , desc="Added automatically by script" )
f.add( name="monitorA"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=      8191, fpga_update=False , signed=True , desc="Added automatically by script" )
f.add( name="monitorB"               , group=grp , val=    0, rw=False,  nbits=14, min_val=      -8192, max_val=      8191, fpga_update=False , signed=True , desc="Added automatically by script" )

#grp='aux_signals'
#f.add( name="cnt_clk"            , group=grp , val=    0, rw=False,  nbits=32, min_val=          0, max_val= 4294967295, fpga_update=False, signed=False, desc="Clock count" )
#f.add( name="cnt_clk2"           , group=grp , val=    0, rw=False,  nbits=32, min_val=          0, max_val= 4294967295, fpga_update=False, signed=False, desc="Clock count" )
f.add( name="read_ctrl"          , group=grp , val=    0, rw=True ,  nbits= 3, min_val=          0, max_val=          7, fpga_update=True , signed=False, desc="[unused,start_clk,Freeze]" )
#
## aux
#grp='mix'
#f.add( name="aux_A"              , group=grp , val=    0, rw=True ,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="auxiliar value of 14 bits" )
#f.add( name="aux_B"              , group=grp , val=    0, rw=True ,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="auxiliar value of 14 bits" )


for r in f:
    if r.ro:
        r.fpga_update=False

for i in ['osc_ctrl','in1','in2','out1','out2']:
    f[i].write_def=False



if __name__ == '__main__' and args.do_verilog:
    print('do_verilog')
    f.update_verilog_files(folder,AppName)


#%%


m = main_registers(num_base=81)

for r in f:
    m.add(r)

m.insert_reg("dummy_osc_ctrl",
             main_register(name="dummy_osc1_filt_off", val=1, rw=True,
                           nbits=1, group="scope",
                           min_val=0, max_val=1, signed=False,
                           desc="oscilloscope control osc1_filt_off",
                           fpga_update=True,
                           c_update='(float) ((g_dummy_reg->osc_ctrl      )& 0x01)'
                           )
             )
m.insert_reg("dummy_osc_ctrl",
             main_register(name="dummy_osc2_filt_off", val=1, rw=True,
                           nbits=1, group="scope",
                           min_val=0, max_val=1, signed=False,
                           desc="oscilloscope control osc2_filt_off",
                           fpga_update=True,
                           c_update='(float) ((g_dummy_reg->osc_ctrl >> 1 )& 0x01)'
                           )
             )

m.insert_reg("dummy_osc_ctrl",
             main_register(name="dummy_osc_raw_mode", val=0, rw=True,
                           nbits=1, group="scope",
                           min_val=0, max_val=1, signed=False,
                           desc="Set oscilloscope mode in Raw (int unit instead of Volts)",
                           fpga_update=False
                           )
             )

m.insert_reg("dummy_osc_ctrl",
             main_register(name="dummy_osc_lockin_mode", val=0, rw=True,
                           nbits=1, group="scope",
                           min_val=0, max_val=1, signed=False,
                           desc="Set oscilloscope mode in lock-in (ch1 as R [V|int], ch2 as Phase [rad])",
                           fpga_update=False
                           )
             )

m.del_reg("dummy_osc_ctrl")

m["dummy_osc1_filt_off"].fpga_reg="osc_ctrl"
m["dummy_osc2_filt_off"].fpga_reg="osc_ctrl"

r=f["osc_ctrl"]; r.c_update='(((int)params[{:s}].value)<<1) + ((int)params[{:s}].value)'.format( m["dummy_osc2_filt_off"].cdef , m["dummy_osc1_filt_off"].cdef )


m.fix_c_update(f)



#%%

if __name__ == '__main__' and args.do_main:
    print('do_main')
    m.update_c_files(folder,AppName,f)

#%%

h = html_registers(num_base=81)

for i in m:
    h.add(i)



h.guess_control_type(AppName+'/fpga/rtl/dummy.v')

# Print control type
# h.print_control_type()

h['dummy_osc_raw_mode'   ].type = 'button'
h['dummy_osc_lockin_mode'].type = 'button'

h['dummy_oscA_sw'].type         = 'select'
h['dummy_oscB_sw'].type         = 'select'
h['dummy_trig_sw'].type         = 'select'
h['dummy_out1_sw'].type         = 'select'
h['dummy_out2_sw'].type         = 'select'
h['dummy_slow_out3_sw'].type    = 'select'
h['dummy_slow_out4_sw'].type    = 'select'

h['dummy_comboA'].type          = 'select'
h['dummy_comboB'].type          = 'select'





h.auto_set_controls(AppName+'/fpga/rtl/dummy.v','dummy')



h['dummy_osc1_filt_off'].control.text='Ch1'
h['dummy_osc2_filt_off'].control.text='Ch2'
h['dummy_osc_raw_mode'    ].control.text = 'Raw&nbsp;Mode'
h['dummy_osc_lockin_mode' ].control.text = 'R|Phase&nbsp;Mode'



h['dummy_oscA_sw'].control.enable = [True]*30 + [False]*2
h['dummy_oscB_sw'].control.enable = [True]*30 + [False]*2

h.set_global_configs()

if __name__ == '__main__' and args.do_html:
    print('do_html')
    h.update_html_files(folder,AppName)


#%%



f.set_py_global_config()


if __name__ == '__main__' and args.do_py:
    print('do_py')
    f.update_python_files(folder)


if __name__ == '__main__':
    print('end')
