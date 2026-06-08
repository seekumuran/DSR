module timing_controller(

    input wire clk,

    output reg tick_1khz
);

reg [15:0] counter;

always @(posedge clk)
begin

    counter <= counter + 1;

    if(counter == 50000)
    begin
        tick_1khz <= ~tick_1khz;
        counter <= 0;
    end

end

endmodule
