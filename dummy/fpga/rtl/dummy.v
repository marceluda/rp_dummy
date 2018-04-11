`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 08.02.2017 17:17:16
// Design Name:
// Module Name: lock
// Project Name:
// Target Devices:
// Tool Versions:
// Description:
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////

//(* dont_touch = "true" *)
//(* keep = "true" *)
//(* use_dsp48 = "yes" *)
//(* fsm_encoding = "gray" *)


//(* keep_hierarchy = "yes" *)
module dummy(
    input clk,rst,
    // inputs
    input  signed   [14-1:0] in1,in2,
    input                    external_trigger,   // External triger input

    // outputs
    output signed   [14-1:0] out1,out2,
    output signed   [14-1:0] osc1,osc2,
    output                   trigger,            // Oscilloscope trigger output
    output                   digital_modulation, // Modulation for digital otuput
    output reg      [24-1:0] pwm_cfg_a,pwm_cfg_b,pwm_cfg_c,pwm_cfg_d,
    output reg      [32-1:0] osc_ctrl,

    // system bus
    input           [32-1:0] sys_addr        ,  //!< bus address
    input           [32-1:0] sys_wdata       ,  //!< bus write data
    input           [ 4-1:0] sys_sel         ,  //!< bus write byte select
    input                    sys_wen         ,  //!< bus write enable
    input                    sys_ren         ,  //!< bus read enable
    output reg      [32-1:0] sys_rdata       ,  //!< bus read data
    output reg               sys_err         ,  //!< bus error indicator
    output reg               sys_ack            //!< bus acknowledge signal
    );

    // Module starts here  *********************************************


    // [WIREREG DOCK]
    // aux_signals --------------------------
    reg         [ 3-1:0] read_ctrl;
    wire        [32-1:0] cnt_clk,cnt_clk2;
    
    // inout --------------------------
    wire        [12-1:0] slow_out1,slow_out2,slow_out3,slow_out4;
    wire signed [14-1:0] oscA,oscB;
    
    // mix --------------------------
    reg  signed [14-1:0] aux_A,aux_B;
    
    // outputs --------------------------
    reg         [ 4-1:0] out1_sw,out2_sw,slow_out1_sw,slow_out2_sw,slow_out3_sw,slow_out4_sw;
    
    // scope --------------------------
    reg         [ 5-1:0] oscA_sw,oscB_sw;
    reg         [ 8-1:0] trig_sw;
    
    // [WIREREG DOCK END]



    reg  signed [28-1:0] X_28_reg,Y_28_reg,F1_28_reg,F2_28_reg,F3_28_reg,sqX_28_reg,sqY_28_reg,sqF_28_reg;
    reg  signed [14-1:0] error_reg,ctrl_A_reg,ctrl_B_reg;
    reg         [50-1:0] cnt,cnt_reg;


    always @(posedge clk) begin
        if(rst) begin
            X_28_reg    <=  28'b0;
            Y_28_reg    <=  28'b0;
            F1_28_reg   <=  28'b0;
            F2_28_reg   <=  28'b0;
            F3_28_reg   <=  28'b0;
            sqX_28_reg  <=  28'b0;
            sqY_28_reg  <=  28'b0;
            sqF_28_reg  <=  28'b0;
            error_reg   <=  14'b0;
            ctrl_A_reg  <=  14'b0;
            ctrl_B_reg  <=  14'b0;
            cnt         <=  50'b0;
            cnt_reg     <=  50'b0;
        end
        else begin
            X_28_reg    <=  28'b0;
            Y_28_reg    <=  28'b0;
            F1_28_reg   <=  28'b0;
            F2_28_reg   <=  28'b0;
            F3_28_reg   <=  28'b0;
            sqX_28_reg  <=  28'b0;
            sqY_28_reg  <=  28'b0;
            sqF_28_reg  <=  28'b0;
            error_reg   <=  14'b0;
            ctrl_A_reg  <=  14'b0;
            ctrl_B_reg  <=  14'b0;
            cnt         <=  50'b0;
            cnt_reg     <=  50'b0;
        end
    end




    // Configuration for slow_outputs
    always @(posedge clk)
    if (rst) begin
        pwm_cfg_a  <= 24'h0 ;
        pwm_cfg_b  <= 24'h0 ;
        pwm_cfg_c  <= 24'h0 ;
        pwm_cfg_d  <= 24'h0 ;
    end
    else begin
        pwm_cfg_a  <= pwm_cfg_a_w ;
        pwm_cfg_b  <= pwm_cfg_b_w ;
        pwm_cfg_c  <= pwm_cfg_c_w ;
        pwm_cfg_d  <= pwm_cfg_d_w ;
    end

    wire signed [14-1:0] slow_out1_14,slow_out2_14,slow_out3_14,slow_out4_14 ;
    wire        [16-1:0] slow_out1_au,slow_out2_au,slow_out3_au,slow_out4_au ;
    wire        [24-1:0] slow_out1_aux,slow_out2_aux,slow_out3_aux,slow_out4_aux ;


   // Slow DACs decoders
    aDACdecoder i_aDACdecoder_a (  .clk(clk), .rst(rst), .in(slow_out1),  .out(pwm_cfg_a_w)  );
    aDACdecoder i_aDACdecoder_b (  .clk(clk), .rst(rst), .in(slow_out2),  .out(pwm_cfg_b_w)  );
    aDACdecoder i_aDACdecoder_c (  .clk(clk), .rst(rst), .in(slow_out3),  .out(pwm_cfg_c_w)  );
    aDACdecoder i_aDACdecoder_d (  .clk(clk), .rst(rst), .in(slow_out4),  .out(pwm_cfg_d_w)  );





    // Muxers  *********************************************************

    // Scopes outputs *************
    muxer_reg5  #(.RES(14)) i_muxer5_scope1 (
        // input
        .clk(clk), .rst(rst),
        .sel  ( oscA_sw ), // select cable
        .in0  ( 14'b0 ),
        .in1  ( in1     ),   .in2  ( in2     ),
        .in3  ( 14'b0  ),
        .in4  ( 14'b0  ),   .in5  ( 14'b0  ),
        .in6  ( 14'b0  ),   .in7  ( 14'b0  ),
        .in8  ( 14'b0 ),   .in9  ( 14'b0 ),
        .in10 ( 14'b0 ),    .in11 ( 14'b0  ),
        .in12 ( 14'b0 ),   .in13 ( 14'b0 ),
        .in14 ( 14'b0 ),    .in15 ( 14'b0 ),   .in16 ( 14'b0  ),
        .in17 ( 14'b0  ),   .in18 ( 14'b0  ), .in19 ( 14'b0 ),
        .in20 ( 14'b0 ),   .in21 ( 14'b0 ),
        .in22 ( 14'b0      ),   .in23 ( 14'b0    ),
        .in24 ( 14'b0     ),   .in25 ( 14'b0   ),  .in26 ( 14'b0   ),
        .in27 ( 14'b0    ),   .in28 ( 14'b0  ),  .in29 ( 14'b0  ),
        .in30 ( 14'b0 ), // in30
        .in31 ( 14'b0 ), // in31
        // output
        .out ( oscA  )
    );

    muxer_reg5  #(.RES(14)) i_muxer5_scope2 (
        // input
        .clk(clk), .rst(rst),
        .sel  ( oscB_sw ), // select cable
        .in0  ( 14'b0 ),
        .in1  ( in1     ),   .in2  ( in2     ),
        .in3  ( 14'b0  ),
        .in4  ( 14'b0  ),   .in5  ( 14'b0  ),
        .in6  ( 14'b0  ),   .in7  ( 14'b0  ),
        .in8  ( 14'b0 ),   .in9  ( 14'b0 ),
        .in10 ( 14'b0 ),    .in11 ( 14'b0  ),
        .in12 ( 14'b0 ),   .in13 ( 14'b0 ),
        .in14 ( 14'b0 ),    .in15 ( 14'b0 ),   .in16 ( 14'b0  ),
        .in17 ( 14'b0  ),   .in18 ( 14'b0  ), .in19 ( 14'b0 ),
        .in20 ( 14'b0 ),   .in21 ( 14'b0 ),
        .in22 ( 14'b0      ),   .in23 ( 14'b0    ),
        .in24 ( 14'b0     ),   .in25 ( 14'b0   ),  .in26 ( 14'b0   ),
        .in27 ( 14'b0    ),   .in28 ( 14'b0  ),  .in29 ( 14'b0  ),
        .in30 ( 14'b0 ), // in30
        .in31 ( 14'b0 ), // in31
        // output
        .out ( oscB  )
    );

    assign osc1 = oscA;
    assign osc2 = oscB;


    //  External Trigger  selection ******************

    //assign trigger          = trig_time ? ramp_trig : external_trigger ;
    // items=['Pin','Ramp floor','Ramp ceil','harmonic mod.','Square mod.','Out of lock','Param. change'],

    assign  trigger_signals = {  1'b0   ,
                                 1'b0      ,
                                 1'b0       ,
                                 1'b0       ,
                                 1'b0     ,
                                 1'b0    ,
                                 1'b0   ,
                                 external_trigger
                              } ;

    trigger_input  #(.R(8),.N(3)) i_trigger_input (
        // input
        .clk(clk), .rst(rst),
        .trig_in ( trigger_signals ),
        .trig_sel( trig_sw         ),
        // output
        .trig_tick(trigger)
    ) ;


    // Fast DAC outputs *************

    muxer4  #(.RES(14)) out1_sw_m (
        // input
        .sel  ( out1_sw           ), // select cable
        .in0  ( 14'b0             ), // in0
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( 14'b0 ), // in3
        .in4  ( 14'b0           ), // in4
        .in5  ( 14'b0            ), // in5
        .in6  ( 14'b0            ), // in6
        .in7  ( 14'b0            ), // in7
        .in8  ( 14'b0            ), // in8
        .in9  ( 14'b0           ), // in9
        .in10 ( 14'b0           ), // in10
        .in11 ( 14'b0          ), // in11
        .in12 ( 14'b0            ), // in12
        .in13 ( 14'b0            ), // in13
        .in14 ( 14'b0             ), // in14
        .in15 ( 14'b0             ), // in15

        // output
        .out ( out1   )
    );


    muxer4  #(.RES(14)) out2_sw_m (
        // input
        .sel  ( out2_sw          ), // select cable
        .in0  ( 14'b0             ), // in0
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( 14'b0 ), // in3
        .in4  ( 14'b0           ), // in4
        .in5  ( 14'b0            ), // in5
        .in6  ( 14'b0            ), // in6
        .in7  ( 14'b0            ), // in7
        .in8  ( 14'b0           ), // in8
        .in9  ( 14'b0           ), // in9
        .in10 ( 14'b0            ), // in10
        .in11 ( 14'b0          ), // in11
        .in12 ( 14'b0            ), // in12
        .in13 ( 14'b0            ), // in13
        .in14 ( 14'b0             ), // in14
        .in15 ( 14'b0             ), // in15
        // output
        .out ( out2  )
    );



    // Slow DACs outputs *************
    // map to 0 - 1.8 V

    //assign slow_out1_au  =  $signed(slow_out1_14) + $signed(15'd8192)  ;
    //assign slow_out2_au  =  $signed(slow_out2_14) + $signed(15'd8192)  ;
    assign slow_out3_au  =  $signed(slow_out3_14) + $signed(15'd8192)  ;
    assign slow_out4_au  =  $signed(slow_out4_14) + $signed(15'd8192)  ;

    //assign slow_out1_aux = slow_out1_au * 8'd156 ;
    //assign slow_out2_aux = slow_out2_au * 8'd156 ;

    pipe_mult #(.R(16),.level(4)) i_mult_slow_out3_aux (.clk(clk), .a(slow_out3_au) , .b(16'd156), .pdt(slow_out3_aux));
    pipe_mult #(.R(16),.level(4)) i_mult_slow_out4_aux (.clk(clk), .a(slow_out4_au) , .b(16'd156), .pdt(slow_out4_aux));
    //assign slow_out3_aux = slow_out3_au * 8'd156 ;
    //assign slow_out4_aux = slow_out4_au * 8'd156 ;

    //assign slow_out1     = slow_out1_aux[22-1:10];
    //assign slow_out2     = slow_out2_aux[22-1:10];
    assign slow_out3     = slow_out3_aux[22-1:10];
    assign slow_out4     = slow_out4_aux[22-1:10];




    /*
    assign slow_out1 = 12'b0;
    assign slow_out2 = 12'b0;
    assign slow_out4 = 12'b0;
    */
    /* DISABLED BY LOLO -- Reapir
    muxer4  #(.RES(14)) slow_out1_sw_m (
        // input
        .sel  ( slow_out1_sw ), // select cable
        .in0  ( 14'b10000000000000),
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( in1_m_in2[14-1:0] ), // in3
        .in4  ( sin_ref           ), // in4
        .in5  ( cos_1f            ), // in5
        .in6  ( cos_2f            ), // in6
        .in7  ( cos_3f            ), // in7
        .in8  ( sq_ref            ), // in8
        .in9  ( sq_phas           ), // in9
        .in10 ( ramp_A            ), // in10
        .in11 ( pidA_out          ), // in11
        .in12 ( ctrl_A            ), // in12
        .in13 ( ctrl_B            ), // in13
        .in14 ( error             ), // in14
        .in15 ( aux_A             ), // in15
        // output
        .out ( slow_out1_14  )
    );

    muxer4  #(.RES(14)) slow_out2_sw_m (
        // input
        .sel  ( slow_out2_sw ), // select cable
        .in0  ( 14'b10000000000000),
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( in1_m_in2[14-1:0] ), // in3
        .in4  ( cos_ref           ), // in4
        .in5  ( cos_1f            ), // in5
        .in6  ( cos_2f            ), // in6
        .in7  ( cos_3f            ), // in7
        .in8  ( sq_quad           ), // in8
        .in9  ( sq_phas           ), // in9
        .in10 ( ramp_B            ), // in10
        .in11 ( pidA_out          ), // in11
        .in12 ( ctrl_A            ), // in12
        .in13 ( ctrl_B            ), // in13
        .in14 ( error             ), // in14
        .in15 ( aux_B             ), // in15
        // output
        .out ( slow_out2_14  )
    );
    */
    assign     slow_out1_14 = 14'b10000000000000 ;
    assign     slow_out2_14 = 14'b10000000000000 ;


    muxer_reg4  #(.RES(14)) slow_out3_sw_m (
        // input
        .clk(clk), .rst(rst),
        .sel  ( slow_out3_sw ), // select cable
        .in0  ( 14'b10000000000000),
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( 14'b0 ), // in3
        .in4  ( 14'b0           ), // in4
        .in5  ( 14'b0            ), // in5
        .in6  ( 14'b0            ), // in6
        .in7  ( 14'b0            ), // in7
        .in8  ( 14'b0            ), // in8
        .in9  ( 14'b0           ), // in9
        .in10 ( 14'b0            ), // in10
        .in11 ( 14'b0          ), // in11
        .in12 ( 14'b0            ), // in12
        .in13 ( 14'b0            ), // in13
        .in14 ( 14'b0             ), // in14
        .in15 ( 14'b0             ), // in15
        // output
        .out ( slow_out3_14  )
    );


    muxer_reg4  #(.RES(14)) slow_out4_sw_m (
        // input
        .clk(clk), .rst(rst),
        .sel  ( slow_out4_sw ), // select cable
        .in0  ( 14'b10000000000000),
        .in1  ( in1               ), // in1
        .in2  ( in2               ), // in1-in2
        .in3  ( 14'b0 ), // in3
        .in4  ( 14'b0           ), // in4
        .in5  ( 14'b0            ), // in5
        .in6  ( 14'b0            ), // in6
        .in7  ( 14'b0            ), // in7
        .in8  ( 14'b0           ), // in8
        .in9  ( 14'b0           ), // in9
        .in10 ( 14'b0            ), // in10
        .in11 ( 14'b0          ), // in11
        .in12 ( 14'b0            ), // in12
        .in13 ( 14'b0            ), // in13
        .in14 ( 14'b0             ), // in14
        .in15 ( 14'b0             ), // in15
        // output
        .out ( slow_out4_14  )
    );



    // [FPGA MEMORY DOCK]
    //---------------------------------------------------------------------------------
    //
    //  System bus connection
    
    // SO --> MEMORIA --> FPGA
    
    always @(posedge clk)
    if (rst) begin
        oscA_sw                <=   5'd1     ; // switch for muxer oscA
        oscB_sw                <=   5'd2     ; // switch for muxer oscB
        osc_ctrl               <=   2'd3     ; // oscilloscope control // [osc2_filt_off,osc1_filt_off]
        trig_sw                <=   8'd0     ; // Select the external trigger signal
        out1_sw                <=   4'd0     ; // switch for muxer out1
        out2_sw                <=   4'd0     ; // switch for muxer out2
        slow_out1_sw           <=   4'd0     ; // switch for muxer slow_out1
        slow_out2_sw           <=   4'd0     ; // switch for muxer slow_out2
        slow_out3_sw           <=   4'd0     ; // switch for muxer slow_out3
        slow_out4_sw           <=   4'd0     ; // switch for muxer slow_out4
        read_ctrl              <=   3'd0     ; // [unused,start_clk,Freeze]
        aux_A                  <=  14'd0     ; // auxiliar value of 14 bits
        aux_B                  <=  14'd0     ; // auxiliar value of 14 bits
    end else begin
        if (sys_wen) begin
            if (sys_addr[19:0]==20'h00000)  oscA_sw               <=  sys_wdata[ 5-1: 0] ; // switch for muxer oscA
            if (sys_addr[19:0]==20'h00004)  oscB_sw               <=  sys_wdata[ 5-1: 0] ; // switch for muxer oscB
            if (sys_addr[19:0]==20'h00008)  osc_ctrl              <=  sys_wdata[ 2-1: 0] ; // oscilloscope control // [osc2_filt_off,osc1_filt_off]
            if (sys_addr[19:0]==20'h0000C)  trig_sw               <=  sys_wdata[ 8-1: 0] ; // Select the external trigger signal
            if (sys_addr[19:0]==20'h00010)  out1_sw               <=  sys_wdata[ 4-1: 0] ; // switch for muxer out1
            if (sys_addr[19:0]==20'h00014)  out2_sw               <=  sys_wdata[ 4-1: 0] ; // switch for muxer out2
            if (sys_addr[19:0]==20'h00018)  slow_out1_sw          <=  sys_wdata[ 4-1: 0] ; // switch for muxer slow_out1
            if (sys_addr[19:0]==20'h0001C)  slow_out2_sw          <=  sys_wdata[ 4-1: 0] ; // switch for muxer slow_out2
            if (sys_addr[19:0]==20'h00020)  slow_out3_sw          <=  sys_wdata[ 4-1: 0] ; // switch for muxer slow_out3
            if (sys_addr[19:0]==20'h00024)  slow_out4_sw          <=  sys_wdata[ 4-1: 0] ; // switch for muxer slow_out4
          //if (sys_addr[19:0]==20'h00028)  in1                   <=  sys_wdata[14-1: 0] ; // Input signal IN1
          //if (sys_addr[19:0]==20'h0002C)  in2                   <=  sys_wdata[14-1: 0] ; // Input signal IN2
          //if (sys_addr[19:0]==20'h00030)  out1                  <=  sys_wdata[14-1: 0] ; // signal for RP RF DAC Out1
          //if (sys_addr[19:0]==20'h00034)  out2                  <=  sys_wdata[14-1: 0] ; // signal for RP RF DAC Out2
          //if (sys_addr[19:0]==20'h00038)  slow_out1             <=  sys_wdata[12-1: 0] ; // signal for RP slow DAC 1
          //if (sys_addr[19:0]==20'h0003C)  slow_out2             <=  sys_wdata[12-1: 0] ; // signal for RP slow DAC 2
          //if (sys_addr[19:0]==20'h00040)  slow_out3             <=  sys_wdata[12-1: 0] ; // signal for RP slow DAC 3
          //if (sys_addr[19:0]==20'h00044)  slow_out4             <=  sys_wdata[12-1: 0] ; // signal for RP slow DAC 4
          //if (sys_addr[19:0]==20'h00048)  oscA                  <=  sys_wdata[14-1: 0] ; // signal for Oscilloscope Channel A
          //if (sys_addr[19:0]==20'h0004C)  oscB                  <=  sys_wdata[14-1: 0] ; // signal for Oscilloscope Channel B
          //if (sys_addr[19:0]==20'h00050)  cnt_clk               <=  sys_wdata[32-1: 0] ; // Clock count
          //if (sys_addr[19:0]==20'h00054)  cnt_clk2              <=  sys_wdata[32-1: 0] ; // Clock count
            if (sys_addr[19:0]==20'h00058)  read_ctrl             <=  sys_wdata[ 3-1: 0] ; // [unused,start_clk,Freeze]
            if (sys_addr[19:0]==20'h0005C)  aux_A                 <=  sys_wdata[14-1: 0] ; // auxiliar value of 14 bits
            if (sys_addr[19:0]==20'h00060)  aux_B                 <=  sys_wdata[14-1: 0] ; // auxiliar value of 14 bits
        end
    end
    //---------------------------------------------------------------------------------
    // FPGA --> MEMORIA --> SO
    wire sys_en;
    assign sys_en = sys_wen | sys_ren;
    
    always @(posedge clk, posedge rst)
    if (rst) begin
        sys_err <= 1'b0  ;
        sys_ack <= 1'b0  ;
    end else begin
        sys_err <= 1'b0 ;
        
        casez (sys_addr[19:0])
            20'h00000 : begin sys_ack <= sys_en;  sys_rdata <= {  27'b0                   ,          oscA_sw  }; end // switch for muxer oscA
            20'h00004 : begin sys_ack <= sys_en;  sys_rdata <= {  27'b0                   ,          oscB_sw  }; end // switch for muxer oscB
            20'h00008 : begin sys_ack <= sys_en;  sys_rdata <= {  30'b0                   ,         osc_ctrl  }; end // oscilloscope control // [osc2_filt_off,osc1_filt_off]
            20'h0000C : begin sys_ack <= sys_en;  sys_rdata <= {  24'b0                   ,          trig_sw  }; end // Select the external trigger signal
            20'h00010 : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,          out1_sw  }; end // switch for muxer out1
            20'h00014 : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,          out2_sw  }; end // switch for muxer out2
            20'h00018 : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,     slow_out1_sw  }; end // switch for muxer slow_out1
            20'h0001C : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,     slow_out2_sw  }; end // switch for muxer slow_out2
            20'h00020 : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,     slow_out3_sw  }; end // switch for muxer slow_out3
            20'h00024 : begin sys_ack <= sys_en;  sys_rdata <= {  28'b0                   ,     slow_out4_sw  }; end // switch for muxer slow_out4
            20'h00028 : begin sys_ack <= sys_en;  sys_rdata <= {  {18{in1[13]}}           ,              in1  }; end // Input signal IN1
            20'h0002C : begin sys_ack <= sys_en;  sys_rdata <= {  {18{in2[13]}}           ,              in2  }; end // Input signal IN2
            20'h00030 : begin sys_ack <= sys_en;  sys_rdata <= {  {18{out1[13]}}          ,             out1  }; end // signal for RP RF DAC Out1
            20'h00034 : begin sys_ack <= sys_en;  sys_rdata <= {  {18{out2[13]}}          ,             out2  }; end // signal for RP RF DAC Out2
            20'h00038 : begin sys_ack <= sys_en;  sys_rdata <= {  20'b0                   ,        slow_out1  }; end // signal for RP slow DAC 1
            20'h0003C : begin sys_ack <= sys_en;  sys_rdata <= {  20'b0                   ,        slow_out2  }; end // signal for RP slow DAC 2
            20'h00040 : begin sys_ack <= sys_en;  sys_rdata <= {  20'b0                   ,        slow_out3  }; end // signal for RP slow DAC 3
            20'h00044 : begin sys_ack <= sys_en;  sys_rdata <= {  20'b0                   ,        slow_out4  }; end // signal for RP slow DAC 4
            20'h00048 : begin sys_ack <= sys_en;  sys_rdata <= {  {18{oscA[13]}}          ,             oscA  }; end // signal for Oscilloscope Channel A
            20'h0004C : begin sys_ack <= sys_en;  sys_rdata <= {  {18{oscB[13]}}          ,             oscB  }; end // signal for Oscilloscope Channel B
            20'h00050 : begin sys_ack <= sys_en;  sys_rdata <=                                       cnt_clk   ; end // Clock count
            20'h00054 : begin sys_ack <= sys_en;  sys_rdata <=                                      cnt_clk2   ; end // Clock count
            20'h00058 : begin sys_ack <= sys_en;  sys_rdata <= {  29'b0                   ,        read_ctrl  }; end // [unused,start_clk,Freeze]
            20'h0005C : begin sys_ack <= sys_en;  sys_rdata <= {  {18{aux_A[13]}}         ,            aux_A  }; end // auxiliar value of 14 bits
            20'h00060 : begin sys_ack <= sys_en;  sys_rdata <= {  {18{aux_B[13]}}         ,            aux_B  }; end // auxiliar value of 14 bits
            default   : begin sys_ack <= sys_en;  sys_rdata <=  32'h0        ; end
        endcase
    end
    // [FPGA MEMORY DOCK END]

endmodule
