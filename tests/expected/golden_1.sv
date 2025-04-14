module test_module #(
    parameter param1 = 10,
    parameter param2 = 20
)
(
    input logic input1,
    output logic output1
);

assign output1 = input1;
localparam const1 = 32'd42;
logic [7:0] signal1;
test #(
    .p(param1)
) init (
    .a(1'd0),
    .b(input1)
);

endmodule
