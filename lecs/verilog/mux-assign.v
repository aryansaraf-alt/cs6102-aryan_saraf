module mux(a, b, f, sel);
    input a, b, sel;
    output f;

    assign f = sel?b:a;
endmodule
