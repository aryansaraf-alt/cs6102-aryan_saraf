`timescale 1ns / 1ps
module tb_sbox;

// testbench signals
reg [3:0] inp;
wire [3:0] outp;

// instantiate the S-box module

sbox DUT (
    .inp(inp),
    .outp(outp)
);

initial begin
    // display header
    $display("Time\t Input\t Output");
    // monitor changes in inp and outp
    $monitor("%0dns\t %b\t %b", $time, inp, outp);

    inp = 0;
    // stimulate the inp signal after a certain delay
    // test all possible values for inp signal
    
    inp = 4'h0; #10;
    if (outp !== 4'hC) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h1; #10;
    if (outp !== 4'h5) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h2; #10;
    if (outp !== 4'h6) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h3; #10;
    if (outp !== 4'hB) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h4; #10;
    if (outp !== 4'h9) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h5; #10;
    if (outp !== 4'h0) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h6; #10;
    if (outp !== 4'hA) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h7; #10;
    if (outp !== 4'hD) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h8; #10;
    if (outp !== 4'h3) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'h9; #10;
    if (outp !== 4'hE) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hA; #10;
    if (outp !== 4'hF) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hB; #10;
    if (outp !== 4'h8) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hC; #10;
    if (outp !== 4'h4) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hD; #10;
    if (outp !== 4'h7) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hE; #10;
    if (outp !== 4'h1) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    inp = 4'hF; #10;
    if (outp !== 4'h2) $display("FAIL at inp=%h", inp);
    else $display("PASS at inp=%h", inp);

    #10;
    $display("\nsimulation over.");


    // finish simulation
    $finish;
end

initial begin
    $dumpfile("sbox_dump.vcd");
    $dumpvars(1, tb_sbox);
end

endmodule
