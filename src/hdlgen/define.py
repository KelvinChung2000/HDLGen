from enum import StrEnum


class WriterType(StrEnum):
    VERILOG = "verilog"
    SYSTEM_VERILOG = "sv"
    VHDL = "vhdl"


class IO(StrEnum):
    INPUT = "input"
    OUTPUT = "output"
    INOUT = "inout"
