module adder #(
    parameter DATA_WIDTH = 4
) (
    input   logic [DATA_WIDTH-1 : 0] A,
    input   logic [DATA_WIDTH-1 : 0] B,
    output  logic [DATA_WIDTH   : 0] X
);

    // Add the two inputs and assign the result to output X
    assign X = A + B;

    // Optional: You can add a comment here to explain the functionality
    // This module performs a simple addition of two DATA_WIDTH-bit numbers.
    
endmodule