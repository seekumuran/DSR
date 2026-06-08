module button_matrix(

    input wire clk,
    input wire [7:0] gpio_in,

    output reg [7:0] button_state
);

always @(posedge clk)
begin
    button_state <= gpio_in;
end

endmodule
