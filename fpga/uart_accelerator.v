module uart_accelerator(

    input wire clk,
    input wire tx_start,
    input wire [7:0] tx_data,

    output reg tx,
    output reg busy
);

reg [3:0] bit_index;
reg [9:0] shift;

always @(posedge clk)
begin

    if(tx_start && !busy)
    begin
        shift <= {1'b1, tx_data, 1'b0};
        busy <= 1'b1;
        bit_index <= 0;
    end

    else if(busy)
    begin
        tx <= shift[0];
        shift <= shift >> 1;

        bit_index <= bit_index + 1;

        if(bit_index == 10)
        begin
            busy <= 0;
        end
    end

end

endmodule
