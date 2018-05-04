`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
//
// Protección contra saturación.
//
// A menudo se recortan un bus de datos para adaptarlo a otro. satprotect permite
// realizar ese empalme teniendo en cuenta los bits que se descartan para 
// saturar la salida cuando sea necesario
//
//////////////////////////////////////////////////////////////////////////////////

/* Descripción:

Parámetros:

  - Ri  : resolucion de la entrada en bits
  - Ro  : resolucion de la salida en bits
  - SAT : valor de saturación en bits

Límites de valores de salida para cada valor de SAT

 SAT  |    min  |   max 
   0  |     -1  |     0
   1  |     -2  |     1
   2  |     -4  |     3
   3  |     -8  |     7
   4  |    -16  |    15
   5  |    -32  |    31
   6  |    -64  |    63
   7  |   -128  |   127
   8  |   -256  |   255
   9  |   -512  |   511
  10  |  -1024  |  1023
  11  |  -2048  |  2047
  12  |  -4096  |  4095
  13  |  -8192  |  8191


*/


//(* keep_hierarchy = "yes" *) 
module satprotect #(
   parameter     Ri  = 15, 
   parameter     Ro  = 14,
   parameter     SAT = 14
)
(
    //input clk,rst,
    input  signed [Ri-1:0] in,    // input signal
    output signed [Ro-1:0] out    // output signal
    );
    
    wire pos_sat, neg_sat;
    
    assign pos_sat = ( ~in[Ri-1] ) & (     |in[Ri-2:SAT-1]  );
    assign neg_sat = (  in[Ri-1] ) & ( ~ ( &in[Ri-2:SAT-1] ) );
    
    generate
      if (SAT<Ro)
        assign out = (pos_sat|neg_sat) ? { in[Ri-1] , {Ro-SAT+1{in[Ri-1]}} , {SAT-2{~in[Ri-1]}} }  :  in[Ro-1:0] ;
      else
        assign out = (pos_sat|neg_sat) ? { in[Ri-1] , {Ro-1{~in[Ri-1]}} }  :  in[Ro-1:0] ;
    endgenerate
    
endmodule

/* 
Instantiation example:

satprotect #(.Ri(15),.Ro(14),.SAT(14)) i_satprotect ( .in(IN), .out(OUT) );


*/


