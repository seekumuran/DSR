module packet_framer(

    input wire clk,
    input wire [7:0] btn1,
    input wire [7:0] btn2,

    output reg [87:0] packet
);

always @(posedge clk)
begin

    packet[87:80] <= 8'hAA;
    packet[79:72] <= 8'h01;
    packet[71:64] <= 8'h01;

    packet[63:56] <= btn1;
    packet[55:48] <= btn2;

    packet[47:0] <= 48'h808080808000;

end

endmodule
