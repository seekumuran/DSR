module uart_tb;

reg clk;
reg rx;

initial
begin

    clk = 0;

    forever #5 clk = ~clk;

end

initial
begin

    rx = 1;

    #100;

    rx = 0;

end

endmodule
