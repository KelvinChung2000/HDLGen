def integration_1(generator):
    with generator.Module("test_module") as m:
        with m.ParameterRegion() as pr:
            p = pr.Parameter("param1", 10)
            pr.Parameter("param2", 20)
        with m.PortRegion() as pr:
            i1 = pr.InputPort("input1")
            i2 = pr.OutputPort("output1")
        with m.LogicRegion() as lr:
            lr.Assign(i2, i1)
            lr.Constant("const1", 42)
            lr.Signal("signal1", 8)
            lr.InitModule(
                "test",
                "init",
                [lr.ConnectPair("a", 0), lr.ConnectPair("b", i1)],
                [lr.ConnectPair("p", p)],
            )


def test_integration_1_verilog(verilog_generator):
    integration_1(verilog_generator)
    with open(verilog_generator.filePath, "r") as f:
        generated_code = f.read()

    # Read the golden file for comparison
    with open("tests/expected/golden_1.v", "r") as f:
        golden_code = f.read()

    # Compare the generated code with the golden file
    assert generated_code.strip() == golden_code.strip(), (
        "Generated code doesn't match the golden file"
    )


def test_integration_1_vhdl(vhdl_generator):
    integration_1(vhdl_generator)
    with open(vhdl_generator.filePath, "r") as f:
        generated_code = f.read()

    # Read the golden file for comparison
    with open("tests/expected/golden_1.vhdl", "r") as f:
        golden_code = f.read()

    # Compare the generated code with the golden file
    assert generated_code.strip() == golden_code.strip(), (
        "Generated code doesn't match the golden file"
    )


def test_integration_1_system_verilog(system_verilog_generator):
    integration_1(system_verilog_generator)
    with open(system_verilog_generator.filePath, "r") as f:
        generated_code = f.read()

    # Read the golden file for comparison
    with open("tests/expected/golden_1.sv", "r") as f:
        golden_code = f.read()

    # Compare the generated code with the golden file
    assert generated_code.strip() == golden_code.strip(), (
        "Generated code doesn't match the golden file"
    )
