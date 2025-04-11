import pytest

from hdlgen.code_gen import CodeGenerator
from hdlgen.define import WriterType


@pytest.fixture()
def verilog_generator(tmp_path):
    """Fixture for Verilog code generator."""
    p = tmp_path / "verilog.v"
    return CodeGenerator(p, WriterType.VERILOG)


@pytest.fixture()
def system_verilog_generator(tmp_path):
    """Fixture for SystemVerilog code generator."""
    p = tmp_path / "system_verilog.sv"
    return CodeGenerator(p, WriterType.SYSTEM_VERILOG)


@pytest.fixture()
def vhdl_generator(tmp_path):
    """Fixture for VHDL code generator."""
    p = tmp_path / "vhdl.vhdl"
    return CodeGenerator(p, WriterType.VHDL)
