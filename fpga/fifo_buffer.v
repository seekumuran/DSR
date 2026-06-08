module fifo_buffer(

    input wire clk,
    input wire write_enable,
    input wire read_enable,

    input wire [7:0] data_in,

    output reg [7:0] data_out
);

reg [7:0] mem [0:15];

reg [3:0] head;
reg [3:0] tail;

always @(posedge clk)
begin

    if(write_enable)
    begin
        mem[head] <= data_in;
        head <= head + 1;
    end

    if(read_enable)
    begin
        data_out <= mem[tail];
        tail <= tail + 1;
    end

end

endmodule
