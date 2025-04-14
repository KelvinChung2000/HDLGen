from abc import ABC, abstractmethod
from contextlib import contextmanager
from hdlgen.HDL_Construct._Comment import _Comment


class Region(ABC):
    _indentCount: int = 4

    @property
    @abstractmethod
    def container(self) -> list: ...

    @property
    @abstractmethod
    def indent(self) -> int: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @property
    def indentCount(self):
        return self._indentCount

    @indentCount.setter
    def indentCount(self, value):
        self._indentCount = value

    def Comment(self, comment: str):
        _o = _Comment(comment)
        self.container.append(_o)
        return _o

    def NewLine(self):
        self.container.append("")

    @contextmanager
    def IfDef(self, marco: str):
        from hdlgen.HDL_Construct.IfDef_region import IfDefRegion

        r = IfDefRegion(marco, [], self.indent + self.indentCount)
        try:
            yield r
        finally:
            self.container.append(r)
