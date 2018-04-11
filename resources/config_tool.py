#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import unique,ceil
import os
import enum
from datetime import datetime
import re




do_verilog = True
do_main    = True
do_html    = True
do_py      = False

if '__file__' in globals():
    scriptFolder = os.path.dirname(os.path.realpath(__file__))
else:
    scriptFolder = 'rp_dummy/resources'

AppName = 'dummy'

folder = os.path.sep.join(scriptFolder.split(os.path.sep)[:-1]) # + os.path.sep + AppName

print('Working o folder: '+folder)


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

grp='aux_signals'
f.add( name="cnt_clk"            , group=grp , val=    0, rw=False,  nbits=32, min_val=          0, max_val= 4294967295, fpga_update=False, signed=False, desc="Clock count" )
f.add( name="cnt_clk2"           , group=grp , val=    0, rw=False,  nbits=32, min_val=          0, max_val= 4294967295, fpga_update=False, signed=False, desc="Clock count" )
f.add( name="read_ctrl"          , group=grp , val=    0, rw=True ,  nbits= 3, min_val=          0, max_val=          7, fpga_update=True , signed=False, desc="[unused,start_clk,Freeze]" )

# aux
grp='mix'
f.add( name="aux_A"              , group=grp , val=    0, rw=True ,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="auxiliar value of 14 bits" )
f.add( name="aux_B"              , group=grp , val=    0, rw=True ,  nbits=14, min_val=      -8192, max_val=       8191, fpga_update=True , signed=True , desc="auxiliar value of 14 bits" )


for r in f:
    if r.ro:
        r.fpga_update=False

for i in ['osc_ctrl','in1','in2','out1','out2']:
    f[i].write_def=False


fpga_mod_fn = AppName+'/fpga/rtl/dummy.v'

if __name__ == '__main__' and do_verilog:
    print('do_verilog')
    if not os.path.isdir(folder):
        raise ValueError('"folder" variable should be the source code folder path.')
    os.chdir(folder)
    update_verilog(fpga_mod_fn,dock=['WIREREG','FPGA MEMORY'],
                   txt=[fpga_defs(),fpga_reg_write()+fpga_reg_read()])





m = main_registers(num_base=81)

# group: scope
m.add( name="dummy_oscA_sw"       , fpga_reg="oscA_sw"       , val=1    , rw=True , nbits=5 , min_val=0         , max_val=31        , fpga_update=True , signed=False, group="scope"          , desc="switch for muxer oscA")
m.add( name="dummy_oscB_sw"       , fpga_reg="oscB_sw"       , val=2    , rw=True , nbits=5 , min_val=0         , max_val=31        , fpga_update=True , signed=False, group="scope"          , desc="switch for muxer oscB")
if True:
    m.add( name="dummy_osc1_filt_off"      , fpga_reg="osc_ctrl" , val=1    , rw=True , nbits=1 , min_val=0         , max_val=1         , fpga_update=True , signed=False, group="scope"          , desc="oscilloscope control osc1_filt_off")
    m.add( name="dummy_osc2_filt_off"      , fpga_reg="osc_ctrl" , val=1    , rw=True , nbits=1 , min_val=0         , max_val=1         , fpga_update=True , signed=False, group="scope"          , desc="oscilloscope control osc2_filt_off")
    r=m["dummy_osc1_filt_off"]; r.c_update='(float) ((g_dummy_reg->{:s}      )& 0x01)'.format(r.fpga_reg)
    r=m["dummy_osc2_filt_off"]; r.c_update='(float) ((g_dummy_reg->{:s} >> 1 )& 0x01)'.format(r.fpga_reg)
    r=f["osc_ctrl"]; r.c_update='(((int)params[{:s}].value)<<1) + ((int)params[{:s}].value)'.format( m["dummy_osc2_filt_off"].cdef , m["dummy_osc1_filt_off"].cdef )
else:
    m.add( name="dummy_osc_ctrl"      , fpga_reg="osc_ctrl"      , val=3    , rw=True , nbits=2 , min_val=0         , max_val=4294967295, fpga_update=True , signed=False, group="scope"          , desc="oscilloscope control[osc2_filt_off,osc1_filt_off]")
m.add( name="dummy_osc_raw_mode"      ,                            val=0    , rw=True , nbits=1 , min_val=0         , max_val=1         , fpga_update=False, signed=False, group="scope"          , desc="Set oscilloscope mode in Raw (int unit instead of Volts)")
m.add( name="dummy_osc_lockin_mode"   ,                            val=0    , rw=True , nbits=1 , min_val=0         , max_val=1         , fpga_update=False, signed=False, group="scope"          , desc="Set oscilloscope mode in lock-in (ch1 as R [V|int], ch2 as Phase [rad])")
m.add( name="dummy_trig_sw"           , fpga_reg="trig_sw"       , val=0    , rw=True , nbits=8 , min_val=0         , max_val=255       , fpga_update=True , signed=False, group="scope"          , desc="Select the external trigger signal")

# group: outputs
m.add( name="dummy_out1_sw"       , fpga_reg="out1_sw"       , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer out1")
m.add( name="dummy_out2_sw"       , fpga_reg="out2_sw"       , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer out2")
m.add( name="dummy_slow_out1_sw"  , fpga_reg="slow_out1_sw"  , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer slow_out1")
m.add( name="dummy_slow_out2_sw"  , fpga_reg="slow_out2_sw"  , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer slow_out2")
m.add( name="dummy_slow_out3_sw"  , fpga_reg="slow_out3_sw"  , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer slow_out3")
m.add( name="dummy_slow_out4_sw"  , fpga_reg="slow_out4_sw"  , val=0    , rw=True , nbits=4 , min_val=0         , max_val=15        , fpga_update=True , signed=False, group="outputs"        , desc="switch for muxer slow_out4")

# group: inout
m.add( name="dummy_in1"           , fpga_reg="in1"           , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="Input signal IN1")
m.add( name="dummy_in2"           , fpga_reg="in2"           , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="Input signal IN2")
m.add( name="dummy_out1"          , fpga_reg="out1"          , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="signal for RP RF DAC Out1")
m.add( name="dummy_out2"          , fpga_reg="out2"          , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="signal for RP RF DAC Out2")
m.add( name="dummy_slow_out1"     , fpga_reg="slow_out1"     , val=0    , rw=False, nbits=12, min_val=-2048     , max_val=2047      , fpga_update=False, signed=False, group="inout"          , desc="signal for RP slow DAC 1")
m.add( name="dummy_slow_out2"     , fpga_reg="slow_out2"     , val=0    , rw=False, nbits=12, min_val=-2048     , max_val=2047      , fpga_update=False, signed=False, group="inout"          , desc="signal for RP slow DAC 2")
m.add( name="dummy_slow_out3"     , fpga_reg="slow_out3"     , val=0    , rw=False, nbits=12, min_val=-2048     , max_val=2047      , fpga_update=False, signed=False, group="inout"          , desc="signal for RP slow DAC 3")
m.add( name="dummy_slow_out4"     , fpga_reg="slow_out4"     , val=0    , rw=False, nbits=12, min_val=-2048     , max_val=2047      , fpga_update=False, signed=False, group="inout"          , desc="signal for RP slow DAC 4")
m.add( name="dummy_oscA"          , fpga_reg="oscA"          , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="signal for Oscilloscope Channel A")
m.add( name="dummy_oscB"          , fpga_reg="oscB"          , val=0    , rw=False, nbits=14, min_val=-8192     , max_val=8191      , fpga_update=False, signed=True , group="inout"          , desc="signal for Oscilloscope Channel B")

# group: product_signals
m.add( name="dummy_cnt_clk"       , fpga_reg="cnt_clk"       , val=0    , rw=False, nbits=32, min_val=0          , max_val=4294967295, fpga_update=False, signed=False, group="product_signals", desc="Clock count")
m.add( name="dummy_cnt_clk2"      , fpga_reg="cnt_clk2"      , val=0    , rw=False, nbits=32, min_val=0          , max_val=4294967295, fpga_update=False, signed=False, group="product_signals", desc="Clock count")
m.add( name="dummy_read_ctrl"     , fpga_reg="read_ctrl"     , val=0    , rw=True , nbits=3 , min_val=0          , max_val=7         , fpga_update=True , signed=False, group="product_signals", desc="[unused,start_clk,Freeze]")

# group: mix
m.add( name="dummy_aux_A"         , fpga_reg="aux_A"         , val=0    , rw=True , nbits=14, min_val=-8192     , max_val=8191      , fpga_update=True , signed=True , group="mix"            , desc="auxiliar value of 14 bits")
m.add( name="dummy_aux_B"         , fpga_reg="aux_B"         , val=0    , rw=True , nbits=14, min_val=-8192     , max_val=8191      , fpga_update=True , signed=True , group="mix"            , desc="auxiliar value of 14 bits")






for r in [ y for y in filter(lambda x: ( x.c_update==None and x.fpga_reg!=None) , m) ]:
    r.c_update='(float)g_dummy_reg->{:20s}'.format(r.fpga_reg)


for i in [ y  for y in filter(lambda x:  x.name[-3:]=='_28' , m) ]:
    i.name=i.name[:-3]

for r in f:
    if r.c_update==None:
        r.main_reg='dummy_'+r.name
        r.c_update='(int)params[{:30s}].value'.format( m[r.main_reg].cdef )




if __name__ == '__main__' and do_main:
    print('do_main')
    if not os.path.isdir(folder):
        raise ValueError('"folder" variable should be the source code folder path.')
    os.chdir(folder)

    filename='dummy/src/lock.c'
    update_main(filename , dock = ['PARAMSUPDATE'      , 'FPGAUPDATE'],
                           txt  = [main_update_params(), main_update_fpga()])

    filename='dummy/src/fpga_lock.c'
    update_main(filename , dock = ['FPGARESET'],
                           txt  = [main_fpga_regs_reset()])


    filename='dummy/src/fpga_lock.h'

    update_main(filename , dock = ['FPGAREG'],
                           txt  = [main_fpga_regs_def()])

    filename='dummy/src/main.c'
    update_main(filename , dock = ['MAINDEF'],
                           txt  = [main_def()])

    filename='dummy/src/main.h'
    update_main(filename , dock = ['MAINDEFH'],
                           txt  = [main_defh()])

    replace_pattern(filename , pattern = ['^#define[ ]+PARAMS_NUM[ ]+[0-9]+'],
                               txt     = [ '#define PARAMS_NUM        {:>3d}'.format(m[-1].index+1) ])








h = html_registers(num_base=81)

for i in m:
    h.add(i)


for r in h:
    if r.ro:
        r.type='none'
    else:
        if r.name[-3:]=='_sw' or r.max==15 or r.max==7 or r.max==3:
            r.type='select'
        elif r.max==1:
            r.type='checkbox'
        else:
            r.type='number'

if False:
    for r in h:
        print("h[{:32s}].type = '{:s}'".format("'"+r.name+"'",r.type))


h['dummy_oscA_sw'                  ].type = 'select'
h['dummy_oscB_sw'                  ].type = 'select'
h['dummy_trig_sw'                  ].type = 'select'

if True:
    h['dummy_osc1_filt_off'            ].type = 'checkbox'
    h['dummy_osc2_filt_off'            ].type = 'checkbox'

h['dummy_osc_raw_mode'             ].type = 'button'
h['dummy_osc_lockin_mode'          ].type = 'button'

h['dummy_out1_sw'                  ].type = 'select'
h['dummy_out2_sw'                  ].type = 'select'
h['dummy_slow_out1_sw'             ].type = 'select'
h['dummy_slow_out2_sw'             ].type = 'select'
h['dummy_slow_out3_sw'             ].type = 'select'
h['dummy_slow_out4_sw'             ].type = 'select'

h['dummy_aux_A'                    ].type = 'number'
h['dummy_aux_B'                    ].type = 'number'

for r in h:
    r.control=None



# load controls for number inputs
for i in [ y.name for y in filter( lambda x: x.type=='number' , h) ]:
    h[i].control = input_number(idd=h[i])

# load controls for checkbox inputs
for i in [ y.name for y in filter( lambda x: x.type=='checkbox' , h) ]:
    h[i].control = input_checkbox(idd=h[i])

h['dummy_osc1_filt_off'].control.text='Ch1'
h['dummy_osc2_filt_off'].control.text='Ch2'



# load controls for button inputs
for i in [ y.name for y in filter( lambda x: x.type=='button' , h) ]:
    h[i].control = input_button(idd=h[i])


h['dummy_osc_raw_mode'             ].control.text = 'Raw&nbsp;Mode'
h['dummy_osc_lockin_mode'          ].control.text = 'R|Phase&nbsp;Mode'




filename='dummy/fpga/rtl/dummy.v'
if not os.path.isdir(folder):
    raise ValueError('"folder" variable should be the source code folder path.')
os.chdir(folder)

for i in [ y.name for y in filter( lambda x: x.type=='select' , h) ]:
    if len(get_muxer(filename,i[(len(AppName)+1):] ))>0:
        h[i].control = select(idd=i , items=get_muxer(filename,i[5:] ) );
    else:
        print(i)




h['dummy_oscA_sw'].control.enable = [True]*30 + [False]*2
h['dummy_oscB_sw'].control.enable = [True]*30 + [False]*2


html_global_configs=[]

if True:  # config_params_txts  ***********************************************
    txt=[]
    txt.append("config_params_txts = 'xmin,xmax,trig_mode,trig_source,trig_edge,trig_delay,trig_level,time_range,time_units,en_avg_at_dec,min_y,'+")
    txt.append(' '*21+"'max_y,prb_att_ch1,gain_ch1,prb_att_ch2,gain_ch2,gui_xmin,gui_xmax,'+")
    tmp=' '*21+"'"
    for i in [ y.name for y in filter( lambda x: x.rw , h) ]:
        tmp += i+","
        if len(tmp)>130:
            tmp+="'+"
            txt.append(tmp)
            tmp=' '*21+"'"
    if len(tmp)>25:
        tmp=tmp[0:-1]
        tmp+="';"
        txt.append(tmp)
    else:
        txt[-1]=txt[-1][0:-3]+"';"
    txt=('\n'.join(txt))

html_global_configs.append(
        html_global_config( regex_start = ' *config_params_txts *=',
                            regex_end   = '.*;.*',
                            text        = txt )
        )

if True:  # input_checkboxes  *************************************************
    txt=[]
    tmp="var input_checkboxes = '"
    for i in [ '#'+y.name for y in filter( lambda x: x.type=='checkbox' , h) ]:
        tmp += i+","
        if len(tmp)>130:
            tmp+="'+"
            txt.append(tmp)
            tmp=' '*23+"'"
    if len(tmp)>25:
        tmp=tmp[0:-1]
        tmp+="';"
        txt.append(tmp)
    else:
        txt[-1]=txt[-1][0:-3]+"';"
    txt=('\n'.join(txt))

html_global_configs.append(
        html_global_config( regex_start = ' *var *input_checkboxes *=',
                            regex_end   = '.*;.*',
                            text        =  txt)
        )

if True:  # input_select  *************************************************
    txt=[]
    tmp="var switches=["
    for i in [ "'#"+y.name+"'" for y in filter( lambda x: x.type=='select' , h) ]:
        tmp += i+","
        if len(tmp)>130:
            txt.append(tmp)
            tmp=' '*14
    if len(tmp)>16:
        tmp=tmp[0:-1]
        tmp+="];"
        txt.append(tmp)
    else:
        txt[-1]=txt[-1][0:-1]+"];"
    txt=('\n'.join(txt))

html_global_configs.append(
        html_global_config( regex_start = ' *var *switches *= *\[',
                            regex_end   = '.*\] *;.*',
                            text        =  txt)
        )


if True:  # input_buttons  *************************************************
    txt=[]
    tmp="var input_buttons = '"
    for i in [ '#'+y.name for y in filter( lambda x: x.type=='button' , h) ]:
        tmp += i+","
        if len(tmp)>130:
            tmp+="'+"
            txt.append(tmp)
            tmp=' '*20+"'"
    if len(tmp)>22:
        tmp=tmp[0:-1]
        tmp+="';"
        txt.append(tmp)
    else:
        txt[-1]=txt[-1][0:-3]+"';"
    txt=('\n'.join(txt))

html_global_configs.append(
        html_global_config( regex_start = ' *var *input_buttons *=',
                            regex_end   = '.*;.*',
                            text        =  txt)
        )


if True:  # input_number  *************************************************
    txt=[]
    tmp="var input_number=["
    for i in [ "'"+y.name+"'" for y in filter( lambda x: x.type=='number' , h) ]:
        tmp += i+","
        if len(tmp)>130:
            tmp+=" "
            txt.append(tmp)
            tmp=' '*18
    if len(tmp)>20:
        tmp=tmp[0:-1]
        tmp+="];"
        txt.append(tmp)
    else:
        txt[-1]=txt[-1][0:-2]+"];"
    txt=('\n'.join(txt))

html_global_configs.append(
        html_global_config( regex_start = ' *var *input_number *= *\[',
                            regex_end   = '.*\] *;.*',
                            text        =  txt)
        )



if True:  # LOADPARAMS  *************************************************
    txt=[]

    txt.append('// [LOLO DOCK LOADPARAMS]')

    txt.append('// Checkboxes')
    max_len=3+max([ len(y.name) for y in filter( lambda x: x.type=='checkbox' , h) ])
    for i in [ y.name for y in filter( lambda x: x.type=='checkbox' , h) ]:
        tmp="$({:<"+str(max_len)+"s}).prop('checked', (params.original.{:<"+str(max_len)+"s} ? true : false));"
        txt.append( tmp.format( "'#"+i+"'" , i ) )
    txt.append('')

    txt.append('// Numbers')
    max_len=3+max([ len(y.name) for y in filter( lambda x: x.type=='number' , h) ])
    for i in [ y.name for y in filter( lambda x: x.type=='number' , h) ]:
        tmp="$({:<"+str(max_len)+"s}).val(params.original.{:<"+str(max_len)+"s});"
        txt.append( tmp.format( "'#"+i+"'" , i ) )
    txt.append('')

    txt.append('// Switches')
    max_len=3+max([ len(y.name) for y in filter( lambda x: x.type=='select' , h) ])
    for i in [ y.name for y in filter( lambda x: x.type=='select' , h) ]:
        tmp="$({:<"+str(max_len)+"s}).val(params.original.{:<"+str(max_len)+"s});"
        txt.append( tmp.format( "'#"+i+"'" , i ) )
    txt.append('')

    txt.append('// Buttons')
    for i in [ y.name for y in filter( lambda x: x.type=='button' , h) ]:
        txt.append( ("if (params.original."+i+"){").ljust(55)+" // "+i )
        txt.append( "  $('#"+i+"').removeClass('btn-default').addClass('btn-primary').data('checked',true);" )
        txt.append( "}else{" )
        txt.append( "  $('#"+i+"').removeClass('btn-primary').addClass('btn-default').data('checked',false);" )
        txt.append( "}" )
    txt.append('')

    txt.append('// [LOLO DOCK LOADPARAMS END]')

    txt=('\n'.join(txt))
    #print(txt)

html_global_configs.append(
        html_global_config( regex_start = ' *// *\[LOLO DOCK LOADPARAMS\].*',
                            regex_end   = '.*// *\[LOLO DOCK LOADPARAMS END\].*',
                            text        =  txt)
        )




filename='dummy/index.html'

if __name__ == '__main__' and do_html:
    print('do_html')
    if not os.path.isdir(folder):
        raise ValueError('"folder" variable should be the source code folder path.')
    os.chdir(folder)
    update_html(filename,h)


py_global_config=[]

py_global_config.append(
        html_global_config( regex_start = ' *# *\[REGSET DOCK\] *',
                            regex_end   = ' *# *\[REGSET DOCK END\]',
                            text        = '# [REGSET DOCK]\n'+f.print_hugo(ret=True)+'# [REGSET DOCK END]\n' )
        )


if __name__ == '__main__' and do_py:
    print('do_py')
    if not os.path.isdir(folder):
        raise ValueError('"folder" variable should be the source code folder path.')
    os.chdir(folder)
    #update_py('resources/rp_cmds/py/ver_mem.py',py_global_config)
    #update_py('resources/rp_cmds/py/set.py',py_global_config)
    #update_py('lresources/rp_cmds/py/data_dump.py',py_global_config)
    update_py('resources/rp_cmds/py/hugo.py',py_global_config)
