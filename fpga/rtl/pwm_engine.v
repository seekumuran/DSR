module pwm_engine(

    input wire clk,
    input wire [7:0] duty_cycle,

    output reg pwm_out
);

reg [7:0] counter;

always @(posedge clk)
begin

    counter <= counter + 1;

    if(counter < duty_cycle)
        pwm_out <= 1;
    else
        pwm_out <= 0;

end

endmodule
