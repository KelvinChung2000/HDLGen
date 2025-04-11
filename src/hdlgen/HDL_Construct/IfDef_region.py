from dataclasses import dataclass

from hdlgen.HDL_Construct.Logic_region import LogicRegion
from hdlgen.HDL_Construct.Parameter_region import ParameterRegion
from hdlgen.HDL_Construct.Port_region import PortRegion
from hdlgen.HDL_Construct.Region import Region


@dataclass
class IfDefRegion(ParameterRegion, PortRegion, LogicRegion, Region):
    macro: str
    _container: list[Region]
    _indent: int

    def __init__(self, macro, container: list[Region], indent: int):
        self.macro = macro
        self._container = container
        self._indent = indent

    @property
    def container(self):
        return self._container

    @property
    def indent(self):
        return self._indent

    def __str__(self) -> str:
        return f"`ifdef {self.macro}\n{'\n'.join([f'{str(i)}' for i in self.container])}\n`endif"
