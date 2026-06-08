module button_matrix_tb;

reg clk;
reg [7:0] gpio_in;

wire [7:0] button_state;

button_matrix uut(

    .clk(clk),
    .gpio_in(gpio_in),
    .button_state(button_state)
);

always #5 clk = ~clk;

initial
begin

    clk = 0;

    gpio_in = 8'b00000000;

    #20;

    gpio_in = 8'b11110000;

    #50;

    $finish;

end

endmodule
