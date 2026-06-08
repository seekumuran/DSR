module packet_crc(

    input wire clk,
    input wire [7:0] data_in,

    output reg [15:0] crc
);

always @(posedge clk)
begin

    crc <= crc ^ data_in;

end

endmodule
