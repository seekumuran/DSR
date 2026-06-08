module input_timestamp(

    input wire clk,

    output reg [31:0] timestamp
);

always @(posedge clk)
begin

    timestamp <= timestamp + 1;

end

endmodule
