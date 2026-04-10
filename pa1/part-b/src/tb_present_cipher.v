`timescale 1ns / 1ps
module tb_present_cipher;

reg clk;
reg rst;
reg [63:0] plaintext;
reg [79:0] key;
reg en;
reg krdy;
reg prdy;

wire [63:0] ciphertext;
wire done;
wire start;


always begin
    #5 clk = ~clk;
end

present_cipher dut ( .clk(clk), .rst(rst), .plaintext(plaintext), .key(key), .en(en), .prdy(prdy), .krdy(krdy),
                        .done(done), .start(start), .ciphertext(ciphertext) );

initial begin
    $display ("time\t, clk\t, rst\t plaintext\t, key\t, ciphertext\t, en\t, krdy\t, prdy\t, start\t, done\t" );
    $monitor ("%g\t %b\t, %b\t %x\t   %x\t  %x\t  %b\t \%b\t  %b\t %b\t %b\t",
                $time, clk, rst, plaintext, key, ciphertext, en, krdy, prdy, start, done);

    clk = 1;
    #10 rst = 1;
    #10 rst = 0;
    #10 plaintext <= 64'hffffffffffffffff;      // ciphertext = ad7d5befea5c6dea
    // plaintext <= 64'h1000000000000000;      // ciphertext = b5cafa95bee34f40
    key <= 80'h10000000000000000000;

    #10 en = 1;
    #10 krdy <= 1;
    #10 prdy <= 1;

    #10 krdy <= 0;
    #10 prdy <= 0;

    #500 $finish;
end

initial begin
    $dumpfile ("present_dump.vcd");
    $dumpvars (1, tb_present_cipher);
end

endmodule
