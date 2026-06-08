module axis_filter(

    input wire clk,
    input wire [7:0] axis_in,

    output reg [7:0] axis_out
);

reg [7:0] last;

always @(posedge clk)
begin

    axis_out <= (axis_in + last) >> 1;

    last <= axis_out;

end

endmodule
