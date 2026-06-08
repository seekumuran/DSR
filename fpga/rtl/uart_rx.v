module uart_rx(

    input wire clk,
    input wire rx,

    output reg [7:0] data_out,
    output reg data_valid
);

reg [3:0] bit_index;
reg [7:0] shift;

always @(posedge clk)
begin

    if(!rx)
    begin
        bit_index <= 0;
        data_valid <= 0;
    end

    else
    begin

        shift[bit_index] <= rx;

        bit_index <= bit_index + 1;

        if(bit_index == 7)
        begin
            data_out <= shift;
            data_valid <= 1;
        end

    end

end

endmodule
