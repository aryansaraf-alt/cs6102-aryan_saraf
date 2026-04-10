// mux w 2 lines

module mux(f, a, b, sel);
    input a, b, sel;
    output f;

    reg f;

    always @(a or b or sel) begin
       if (sel) 
           f = b;
       else 
           f = a;
    end
endmodule
