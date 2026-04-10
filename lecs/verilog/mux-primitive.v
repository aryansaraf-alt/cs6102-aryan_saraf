// mux w 2 lines

module mux(sel, f, a, b);
    input a, b, sel;
    output f;
    wire f1, f2;
    
    not g0(nsel, sel);

    and g1 (f1, a, nsel), g2 (f2, b, sel);
    or g3 (f, f1, f2);

endmodule;




