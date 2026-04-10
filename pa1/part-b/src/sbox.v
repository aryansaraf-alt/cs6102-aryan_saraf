module sbox (inp, outp);

    input [3:0] inp; // wire since not specified, MSB FIRST SINCE 3:0!
    output [3:0] outp; // wire since not specified 

    reg [3:0] outp; // now declared as a reg.
    

// implement the SBox design based on the truth table / boolean equations provided
// you can either use a high level concurrency construct or you can use continuous assignments
    always @(*) begin
        outp[3] = (inp[3]&inp[2]&inp[0]) ^ (inp[3]&inp[1]&inp[0]) ^ inp[3] ^ (inp[2]&inp[1]&inp[0]) ^ (inp[2]&inp[1]) ^ inp[1] ^ inp[0] ^ 1'b1;
        outp[2] = (inp[3]&inp[2]&inp[0]) ^ (inp[3]&inp[1]&inp[0]) ^ (inp[3]&inp[1]) ^ (inp[3]&inp[0]) ^ inp[3] ^ inp[2] ^ (inp[1]&inp[0]) ^ 1'b1;
        outp[1] = (inp[3]&inp[2]&inp[0]) ^ (inp[3]&inp[2]) ^ (inp[3]&inp[1]&inp[0]) ^ (inp[3]&inp[1]) ^ inp[3] ^ (inp[2]&inp[1]&inp[0]) ^ inp[1];
        outp[0] = inp[3] ^ (inp[2]&inp[1]) ^ inp[2] ^ inp[0];
    end

endmodule
