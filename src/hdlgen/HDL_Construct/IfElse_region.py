from contextlib import contextmanager
from dataclasses import dataclass

from hdlgen.define import WriterType
from hdlgen.HDL_Construct.BeginEnd_region import BeginEndRegion
from hdlgen.HDL_Construct.Logic_region import LogicRegion
from hdlgen.HDL_Construct.Region import Region
from hdlgen.HDL_Construct.Value import Value


@dataclass
class IfElseRegion(LogicRegion, Region):
    _cond: Value
    _tRegion: list[Region]
    _fRegion: list[Region]
    _writer: WriterType
    _indent: int

    def __init__(
        self,
        cond: Value,
        tRegion: list[Region],
        fRegion: list[Region],
        writer: WriterType,
        indent: int,
    ):
        self._cond = cond
        self._tRegion = tRegion
        self._fRegion = fRegion
        self._writer = writer
        self._indent = indent

    @property
    def container(self):
        return (self._tRegion, self._fRegion)

    @property
    def indent(self):
        return self._indent

    @contextmanager
    def TrueRegion(self):
        be = BeginEndRegion([], self._writer, self.indent)
        try:
            yield be
        finally:
            self._tRegion.append(be)

    @contextmanager
    def FalseRegion(self):
        be = BeginEndRegion([], self._writer, self.indent)
        try:
            yield be
        finally:
            self._fRegion.append(be)

    def __str__(self) -> str:
        return f"if ({str(self._cond)}) {'\n'.join([str(i) for i in self._tRegion])}\nelse {'\n'.join([str(i) for i in self._fRegion])}\n"
