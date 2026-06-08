module debounce_engine(

    input wire clk,
    input wire noisy,

    output reg clean
);

reg [15:0] counter;

always @(posedge clk)
begin

    if(noisy != clean)
    begin
        counter <= counter + 1;

        if(counter == 16'hFFFF)
        begin
            clean <= noisy;
            counter <= 0;
        end
    end

    else
    begin
        counter <= 0;
    end

end

endmodule
