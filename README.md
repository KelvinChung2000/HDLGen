# RTLGen

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/rtlgen.svg)](https://pypi.org/project/rtlgen/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/username/RTLGen/main.yml?branch=main)](https://github.com/username/RTLGen/actions)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/en/latest/)
[![Documentation](https://img.shields.io/badge/docs-numpy%20style-brightgreen.svg)](https://numpydoc.readthedocs.io/en/latest/format.html)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library for programmatically generating HDL (Hardware Description Language) code including Verilog, SystemVerilog, and VHDL.

## Features

- Intuitive context manager-based API
- Support for multiple HDL languages
- Clean, readable HDL output generation
- Python-native approach to hardware description

## Installation

```bash
pip install rtlgen
```

## Quick Start

```python
from rtlgen import CodeGen

# Create a Verilog generator
gen = CodeGen("output.v", "verilog")

# Create a module with ports and logic
with gen.Module("example_counter") as m:
    # Define module parameters
    with m.ParameterRegion() as params:
        params.Parameter("WIDTH", 8)
    
    # Define ports
    with m.PortRegion() as ports:
        ports.Input("clk")
        ports.Input("rst_n")
        ports.Output("count", "WIDTH")
    
    # Define internal logic
    with m.LogicRegion() as lr:
        # Create signals
        counter = lr.Signal("counter", "WIDTH")
        
        # Create an always block for synchronous logic
        with lr.BeginEnd("always @(posedge clk or negedge rst_n)"):
            with lr.IfElse("!rst_n"):
                lr.Assign(counter, 0, blocking=True)
            with lr.Else():
                lr.Assign(counter, counter + 1, blocking=True)
        
        # Continuous assignment
        lr.Assign("count", counter)

# file auto written when gen.Module out of context
```

## Side-by-Side Examples

Here are examples showing RTLGen Python code and the resulting Verilog output:

### Module and Signal Declaration

<table>
<tr>
<th>Python Code</th>
<th>Generated Verilog</th>
</tr>
<tr>
<td>

```python
from rtlgen import CodeGen

gen = CodeGen("module.v", "verilog")

with gen.Module("test_module") as m:
    with m.LogicRegion() as lr:
        signal = lr.Signal("test_signal", 8)
        single_bit = lr.Signal("single_bit")
```

</td>
<td>

```verilog
module test_module (
);

    // Logic
    reg [7:0] test_signal;
    reg single_bit;

endmodule
```

</td>
</tr>
</table>

### Assignment Operations

<table>
<tr>
<th>Python Code</th>
<th>Generated Verilog</th>
</tr>
<tr>
<td>

```python
with gen.Module("assign_module") as m:
    with m.LogicRegion() as lr:
        signal_a = lr.Signal("a", 8)
        signal_b = lr.Signal("b", 8)
        
        # Signal to signal assignment
        lr.Assign(signal_a, signal_b)
        
        # Constant assignment
        lr.Assign(signal_a, 42)
```

</td>
<td>

```verilog
module assign_module (
);

    // Logic
    reg [7:0] a;
    reg [7:0] b;
    
    assign a = b;
    assign a = 8'd42;

endmodule
```

</td>
</tr>
</table>

### If-Else Conditions

<table>
<tr>
<th>Python Code</th>
<th>Generated Verilog</th>
</tr>
<tr>
<td>

```python
with gen.Module("conditional_module") as m:
    with m.LogicRegion() as lr:
        clk = lr.Signal("clk")
        reset = lr.Signal("reset")
        counter = lr.Signal("counter", 8)
        
        with lr.BeginEnd("always @(posedge clk)"):
            with lr.IfElse("reset"):
                lr.Assign(counter, 0, blocking=True)
            with lr.Else():
                lr.Assign(counter, counter + 1, blocking=True)
```

</td>
<td>

```verilog
module conditional_module (
);

    // Logic
    reg clk;
    reg reset;
    reg [7:0] counter;
    
    always @(posedge clk) begin
        if (reset) begin
            counter = 0;
        end else begin
            counter = counter + 1;
        end
    end

endmodule
```

</td>
</tr>
</table>

### Module Instantiation

<table>
<tr>
<th>Python Code</th>
<th>Generated Verilog</th>
</tr>
<tr>
<td>

```python
with gen.Module("top_module") as m:
    with m.LogicRegion() as lr:
        clk = lr.Signal("clk")
        reset = lr.Signal("reset")
        data_out = lr.Signal("data_out", 8)
        
        # Create connections
        clk_conn = lr.ConnectPair("clk", clk)
        rst_conn = lr.ConnectPair("reset", reset)
        out_conn = lr.ConnectPair("result", data_out)
        
        # Instantiate a module
        lr.InitModule("counter", "counter_inst", 
                     [clk_conn, rst_conn, out_conn])
```

</td>
<td>

```verilog
module top_module (
);

    // Logic
    reg clk;
    reg reset;
    reg [7:0] data_out;
    
    counter #() counter_inst (
        .clk(clk),
        .reset(reset),
        .result(data_out)
    );

endmodule
```

</td>
</tr>
</table>

## Supported HDL Languages

- Verilog
- SystemVerilog
- VHDL

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.