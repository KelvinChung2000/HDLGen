# HDLGen

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/rtlgen.svg)](https://pypi.org/project/hdlgen/)
<!-- [![Build Status](https://img.shields.io/github/actions/workflow/status/username/RTLGen/main.yml?branch=master)](https://github.com/username/RTLGen/actions) -->
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/en/latest/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library for programmatically generating HDL (Hardware Description Language) code including Verilog, SystemVerilog, and VHDL.

## Features

- Intuitive context manager-based API
- Support for multiple HDL languages
- Clean, readable HDL output generation
- Python-native approach to hardware description

## Installation

```bash
pip install hdlgen
```

## Quick Start

```python
from rtlgen import CodeGen

# Create a Verilog generator
gen = CodeGen("conditional_module.v", "verilog")

# Create a module with ports and logic
with gen.Module("conditional_module") as m:
    # Define internal logic
    with m.LogicRegion() as lr:
        # Create signals
        clk = lr.Signal("clk")
        reset = lr.Signal("reset")
        counter = lr.Signal("counter", 8)
        
        # Create an always block for synchronous logic
        with lr.BeginEnd("always @(posedge clk)"):
            with lr.IfElse("reset"):
                lr.Assign(counter, 0, blocking=True)
            with lr.Else():
                lr.Assign(counter, counter + 1, blocking=True)

# file auto written when gen.Module out of context
```

## Side-by-Side Examples

Here are examples showing HDLGen Python code and the resulting HDL output for Verilog, SystemVerilog, and VHDL.

### Module and Signal Declaration

**Verilog**
<table>
<tr><th>Python Code (Verilog)</th><th>Generated Verilog</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("module.v", "verilog")

with gen.Module("test_module") as m:
    with m.LogicRegion() as lr:
        signal = lr.Signal("test_signal", 8)
        single_bit = lr.Signal("single_bit")
```

</td><td>

```verilog
module test_module (
);

    // Logic
    reg [7:0] test_signal;
    reg single_bit;

endmodule
```

</td></tr></table>

**SystemVerilog**
<table>
<tr><th>Python Code (SystemVerilog)</th><th>Generated SystemVerilog</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("module.sv", "systemverilog") # Target SystemVerilog

with gen.Module("test_module") as m:
    with m.LogicRegion() as lr:
        # SystemVerilog typically uses 'logic' type
        test_signal = lr.Signal("test_signal", 8, type="logic")
        single_bit = lr.Signal("single_bit", type="logic")
```

</td><td>

```systemverilog
module test_module (
);

    // Logic
    logic [7:0] test_signal; // 'logic' type
    logic single_bit;       // 'logic' type

endmodule
```

</td></tr></table>

**VHDL**
<table>
<tr><th>Python Code (VHDL)</th><th>Generated VHDL</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("module.vhd", "vhdl") # Target VHDL
gen.Library("ieee")
gen.Use("ieee.std_logic_1164.all")

with gen.Module("test_module") as m:
    # In VHDL, signals are part of an architecture
    with m.Architecture("rtl") as arch:
        test_signal = arch.Signal("test_signal", "std_logic_vector(7 downto 0)")
        single_bit = arch.Signal("single_bit", "std_logic")
```

</td><td>

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity test_module is
    -- Ports would be defined here if any
end entity test_module;

architecture rtl of test_module is
    -- Signals
    signal test_signal : std_logic_vector(7 downto 0);
    signal single_bit  : std_logic;
begin
    -- Concurrent statements or processes
end architecture rtl;
```

</td></tr></table>

### If-Else Conditions

**Verilog**
<table>
<tr><th>Python Code (Verilog)</th><th>Generated Verilog</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("conditional_module.v", "verilog")

with gen.Module("conditional_module") as m:
    with m.LogicRegion() as lr:
        clk = lr.Signal("clk")
        reset = lr.Signal("reset")
        counter = lr.Signal("counter", 8)
        
        with lr.BeginEnd("always @(posedge clk)"): # Synchronous block
            with lr.IfElse("reset"):
                lr.Assign(counter, 0, blocking=False) # Non-blocking
            with lr.Else():
                lr.Assign(counter, counter + 1, blocking=False) # Non-blocking
```

</td><td>

```verilog
module conditional_module (
);

    // Logic
    reg clk;
    reg reset;
    reg [7:0] counter;
    
    always @(posedge clk) begin
        if (reset) begin
            counter <= 0; // Non-blocking assignment
        end else begin
            counter <= counter + 1; // Non-blocking assignment
        end
    end

endmodule
```

</td></tr></table>

**SystemVerilog**
<table>
<tr><th>Python Code (SystemVerilog)</th><th>Generated SystemVerilog</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("conditional_module.sv", "systemverilog")

with gen.Module("conditional_module") as m:
    with m.LogicRegion() as lr:
        clk = lr.Signal("clk", type="logic")
        reset = lr.Signal("reset", type="logic")
        counter = lr.Signal("counter", 8, type="logic")

        # Using always_ff for synchronous logic
        with lr.AlwaysFF("@(posedge clk or posedge reset)") as ff_block: # Async reset
            with ff_block.If("reset"): # Active-high reset
                ff_block.Assign(counter, "\'0\'", blocking=False) # SV literal assignment
            with ff_block.Else():
                ff_block.Assign(counter, counter + 1, blocking=False)
```

</td><td>

```systemverilog
module conditional_module (
);

    // Logic
    logic clk;
    logic reset;
    logic [7:0] counter;
    
    always_ff @(posedge clk or posedge reset) begin // Assuming asynchronous reset
        if (reset) begin
            counter <= \'0\';
        end else begin
            counter <= counter + 1;
        end
    end

endmodule
```

</td></tr></table>

**VHDL**
<table>
<tr><th>Python Code (VHDL)</th><th>Generated VHDL</th></tr>
<tr><td>

```python
from rtlgen import CodeGen

gen = CodeGen("conditional_module.vhd", "vhdl")
gen.Library("ieee")
gen.Use("ieee.std_logic_1164.all")
gen.Use("ieee.numeric_std.all") # For arithmetic

with gen.Module("conditional_module") as m:
    # Define Entity Ports
    clk = m.Port("clk_i", "in", "std_logic")
    reset = m.Port("reset_i", "in", "std_logic")
    counter_out = m.Port("counter_o", "out", "std_logic_vector(7 downto 0)")

    with m.Architecture("rtl") as arch:
        # Internal signal for counter logic, using 'unsigned' for arithmetic
        counter_reg = arch.Signal("counter_s", "unsigned(7 downto 0)")

        with arch.Process([clk, reset]) as p: # Process sensitive to clk and reset
            with p.If(f"{reset} = \'1\'"): # Asynchronous reset
                p.Assign(counter_reg, "(others => \'0\')")
            with p.ElsIf(f"rising_edge({clk})"):
                p.Assign(counter_reg, f"{counter_reg} + 1")
        
        # Assign internal signal to output port
        arch.Assign(counter_out, f"std_logic_vector({counter_reg})")
```

</td><td>

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity conditional_module is
    port (
        clk_i     : in  std_logic;
        reset_i   : in  std_logic;
        counter_o : out std_logic_vector(7 downto 0)
    );
end entity conditional_module;

architecture rtl of conditional_module is
    signal counter_s : unsigned(7 downto 0);
begin
    process (clk_i, reset_i)
    begin
        if reset_i = \'1\' then
            counter_s <= (others => \'0\');
        elsif rising_edge(clk_i) then
            counter_s <= counter_s + 1;
        end if;
    end process;

    counter_o <= std_logic_vector(counter_s);
end architecture rtl;
```

</td></tr></table>

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