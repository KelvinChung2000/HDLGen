from hdlgen.define import IO


def test_system_verilog_module(system_verilog_generator):
    """Test system_verilog module creation."""
    with system_verilog_generator.Module("test_module"):
        pass

    # Check the string representation
    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "module test_module" in content


def test_system_verilog_parameter(system_verilog_generator):
    """Test system_verilog parameter creation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.ParameterRegion() as pr:
            pr.Parameter("WIDTH", 32)
            pr.Parameter("DEPTH", 64)

    # Check the string representation
    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "parameter WIDTH = 32" in content
    assert "parameter DEPTH = 64" in content


def test_system_verilog_port(system_verilog_generator):
    """Test system_verilog port creation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.PortRegion() as pr:
            pr.Port("clk", IO.INPUT)
            pr.Port("data_out", IO.OUTPUT, 8)
            pr.Port("data_in", IO.INPUT, 16)

    # Check the string representation
    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "input logic clk" in content
    assert "output logic[7:0] data_out" in content
    assert "input logic[15:0] data_in" in content


def test_system_verilog_signal(system_verilog_generator):
    """Test system_verilog signal creation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal = lr.Signal("test_signal", 8)
            assert str(signal) == "test_signal"
            assert signal.bits == 8

            single_bit = lr.Signal("single_bit")
            assert str(single_bit) == "single_bit"
            assert single_bit.bits == 1


def test_system_verilog_assign(system_verilog_generator):
    """Test system_verilog assignment."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            assign = lr.Assign(signal_a, signal_b)
            assert "assign a = b;" in str(assign)

            # Test assignment with integer
            assign_int = lr.Assign(signal_a, 42)
            assert "assign a = 8'd42" in str(assign_int)


def test_system_verilog_constant(system_verilog_generator):
    """Test system_verilog constant creation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            lr.Constant("WIDTH", 32)

    # Check the string representation
    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()
    assert "localparam WIDTH = 32'd32;" in content


def test_system_verilog_concat(system_verilog_generator):
    """Test system_verilog concatenation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            concat = lr.Concat(signal_a, signal_b)
            assert "{a ,b}" in str(concat)


def test_system_verilog_if_else(system_verilog_generator):
    """Test system_verilog if-else construct."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            cond = lr.Signal("cond")

            with lr.IfElse(cond):
                lr.Signal("inside_if")

    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "if (cond)" in content


def test_system_verilog_initial(system_verilog_generator):
    """Test system_verilog initial block."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            with lr.Initial():
                lr.Signal("test_init")

    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "initial" in content


def test_system_verilog_module_instantiation(system_verilog_generator):
    """Test system_verilog module instantiation."""
    with system_verilog_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            # Create connection pairs
            connection = lr.ConnectPair("out", "in")

            # Instantiate a module
            lr.InitModule("submodule", "inst1", [connection])

    with open(system_verilog_generator.filePath, "r") as f:
        content = f.read()

    assert "submodule #() inst1" in content
