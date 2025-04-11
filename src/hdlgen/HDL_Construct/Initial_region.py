from dataclasses import dataclass

from hdlgen.HDL_Construct.Logic_region import LogicRegion
from hdlgen.HDL_Construct.Region import Region
from hdlgen.define import WriterType


@dataclass
class InitialRegion(LogicRegion, Region):
    _container: list[Region]
    _writer: WriterType
    _indent: int

    def __init__(self, container: list[Region], writer: WriterType, indent: int):
        self._container = container
        self._writer = writer
        self._indent = indent

    @property
    def container(self):
        return self._container

    @property
    def indent(self):
        return self._indent

    def __str__(self) -> str:
        match self._writer:
            case WriterType.VERILOG | WriterType.SYSTEM_VERILOG:
                return (
                    f"initial begin\n{'\n'.join([str(i) for i in self.container])}\nend"
                )
            case WriterType.VHDL:
                return f"process\n{'\n'.join([str(i) for i in self.container])}\nwait;\nend process;"
            case _:
                raise ValueError("Unsupported WriterType")
