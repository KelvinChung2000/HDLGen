from hdlgen.define import IO


def test_verilog_module(verilog_generator):
    """Test Verilog module creation."""
    with verilog_generator.Module("test_module"):
        pass

    # Check the string representation
    with open(verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "module test_module" in content


def test_verilog_parameter(verilog_generator):
    """Test Verilog parameter creation."""
    with verilog_generator.Module("test_module") as m:
        with m.ParameterRegion() as pr:
            pr.Parameter("WIDTH", 32)
            pr.Parameter("DEPTH", 64)

    # Check the string representation
    with open(verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "parameter WIDTH = 32" in content
    assert "parameter DEPTH = 64" in content


def test_verilog_port(verilog_generator):
    """Test Verilog port creation."""
    with verilog_generator.Module("test_module") as m:
        with m.PortRegion() as pr:
            pr.Port("clk", IO.INPUT)
            pr.Port("data_out", IO.OUTPUT, 8)
            pr.Port("data_in", IO.INPUT, 16)

    # Check the string representation
    with open(verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "input wire clk" in content
    assert "output reg[7:0] data_out" in content
    assert "input wire[15:0] data_in" in content


def test_verilog_signal(verilog_generator):
    """Test Verilog signal creation."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal = lr.Signal("test_signal", 8)
            assert str(signal) == "test_signal"
            assert signal.bits == 8

            single_bit = lr.Signal("single_bit")
            assert str(single_bit) == "single_bit"
            assert single_bit.bits == 1


def test_verilog_assign(verilog_generator):
    """Test Verilog assignment."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            assign = lr.Assign(signal_a, signal_b)
            assert "assign a = b;" in str(assign)

            # Test assignment with integer
            assign_int = lr.Assign(signal_a, 42)
            assert "assign a = 8'd42" in str(assign_int)


def test_verilog_constant(verilog_generator):
    """Test Verilog constant creation."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            lr.Constant("WIDTH", 32)

    # Check the string representation
    with open(verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "localparam WIDTH = 32'd32;" in content


def test_verilog_concat(verilog_generator):
    """Test Verilog concatenation."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            concat = lr.Concat(signal_a, signal_b)
            assert "{a ,b}" in str(concat)


def test_verilog_if_else(verilog_generator):
    """Test Verilog if-else construct."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            cond = lr.Signal("cond")

            with lr.IfElse(cond):
                lr.Signal("inside_if")

    with open(verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "if (cond)" in content


def test_verilog_initial(verilog_generator):
    """Test Verilog initial block."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            with lr.Initial():
                lr.Signal("test_init")

    with open(verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "initial" in content


def test_verilog_module_instantiation(verilog_generator):
    """Test Verilog module instantiation."""
    with verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            # Create connection pairs
            connection = lr.ConnectPair("out", "in")

            # Instantiate a module
            lr.InitModule("submodule", "inst1", [connection])

    with open(verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "submodule #() inst1" in content
