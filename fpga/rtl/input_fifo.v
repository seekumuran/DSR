module input_fifo(

    input wire clk,

    input wire write_enable,
    input wire read_enable,

    input wire [7:0] data_in,

    output reg [7:0] data_out,
    output reg empty,
    output reg full
);

reg [7:0] fifo [0:31];

reg [5:0] head;
reg [5:0] tail;

always @(posedge clk)
begin

    if(write_enable && !full)
    begin
        fifo[head] <= data_in;
        head <= head + 1;
    end

    if(read_enable && !empty)
    begin
        data_out <= fifo[tail];
        tail <= tail + 1;
    end

    if(head == tail)
        empty <= 1;
    else
        empty <= 0;

    if((head + 1) == tail)
        full <= 1;
    else
        full <= 0;

end

endmodule
