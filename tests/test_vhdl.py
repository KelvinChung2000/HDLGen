from hdlgen.define import IO


def test_vhdl_module(vhdl_generator):
    """Test vhdl module creation."""
    with vhdl_generator.Module("test_module"):
        pass

    # Check the string representation
    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()
    assert "entity test_module is" in content


def test_vhdl_parameter(vhdl_generator):
    """Test vhdl parameter creation."""
    with vhdl_generator.Module("test_module") as m:
        with m.ParameterRegion() as pr:
            pr.Parameter("WIDTH", 32)
            pr.Parameter("DEPTH", 64)

    # Check the string representation
    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()

    assert "generic(" in content
    assert "WIDTH : integer := 32" in content
    assert "DEPTH" in content


def test_vhdl_port(vhdl_generator):
    """Test vhdl port creation."""
    with vhdl_generator.Module("test_module") as m:
        with m.PortRegion() as pr:
            pr.Port("clk", IO.INPUT)
            pr.Port("data_out", IO.OUTPUT, 8)

    # Check the string representation
    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()
    assert "port(" in content
    assert "data_out: out std_logic_vector(7 downto 0)" in content
    assert "clk: in std_logic" in content


def test_vhdl_signal(vhdl_generator):
    """Test vhdl signal creation."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal = lr.Signal("test_signal", 8)
            assert str(signal) == "test_signal"
            assert signal.bits == 8

            single_bit = lr.Signal("single_bit")
            assert str(single_bit) == "single_bit"
            assert single_bit.bits == 1


def test_vhdl_assign(vhdl_generator):
    """Test vhdl assignment."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            assign = lr.Assign(signal_a, signal_b)
            assert "a <= b;" in str(assign)

            # Test assignment with integer
            assign_int = lr.Assign(signal_a, 42)
            assert "a <= 42;" in str(assign_int)


def test_vhdl_constant(vhdl_generator):
    """Test vhdl constant creation."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            lr.Constant("WIDTH", 32)

    # Check the string representation
    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()
    assert "constant WIDTH : integer := 32;" in content


def test_vhdl_concat(vhdl_generator):
    """Test vhdl concatenation."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            signal_a = lr.Signal("a", 8)
            signal_b = lr.Signal("b", 8)

            concat = lr.Concat(signal_a, signal_b)
            assert "a & b" in str(concat)


def test_vhdl_if_else(vhdl_generator):
    """Test vhdl if-else construct."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            cond = lr.Signal("cond")

            with lr.IfElse(cond):
                lr.Signal("inside_if")

    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()

    assert "if (cond)" in content


def test_vhdl_initial(vhdl_generator):
    """Test vhdl initial block."""
    with vhdl_generator.Module("test_module") as m:
        with m.LogicRegion() as lr:
            with lr.Initial():
                lr.Signal("test_init")

    with open(vhdl_generator.filePath, "r") as f:
        content = f.read()

    assert "process" in content
    assert "end process;" in content
    assert "wait;" in content
