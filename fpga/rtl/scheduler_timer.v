module scheduler_timer(

    input wire clk,
    input wire reset,

    output reg scheduler_tick
);

reg [31:0] counter;

always @(posedge clk or posedge reset)
begin

    if(reset)
    begin
        counter <= 0;
        scheduler_tick <= 0;
    end

    else
    begin

        counter <= counter + 1;

        if(counter == 50000)
        begin
            scheduler_tick <= 1;
            counter <= 0;
        end

        else
        begin
            scheduler_tick <= 0;
        end

    end

end

endmodule
