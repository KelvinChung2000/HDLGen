from dataclasses import dataclass

from hdlgen.HDL_Construct._Comment import _Comment
from hdlgen.define import WriterType
from hdlgen.HDL_Construct.Region import Region
from hdlgen.HDL_Construct.Value import Value


@dataclass
class ParameterRegion(Region):
    _container: list["_Parameter"]
    _indent: int

    def __init__(self, parameters: list["_Parameter"], writer: WriterType, indent: int):
        self._container = parameters
        self._indent = indent
        self._writer = writer

    @property
    def container(self):
        return self._container

    @property
    def indent(self):
        return self._indent

    def __str__(self) -> str:
        if (
            self._writer == WriterType.VERILOG
            or self._writer == WriterType.SYSTEM_VERILOG
        ):
            lines = []

            for idx, item in enumerate(self.container):
                if isinstance(item, _Comment):
                    lines.append(f"{' ' * self.indent}{str(item)}")
                else:
                    if idx == len(self.container) - 1:
                        lines.append(f"{' ' * self.indent}{str(item)}")
                    else:
                        lines.append(f"{' ' * self.indent}{str(item)},")

            return f"#(\n{''.join([f'{line}\n' for line in lines])})\n"
        else:
            return f"generic(\n{';\n'.join([f'{" " * self.indent}{str(i)}' for i in self.container])}\n);"

    @dataclass
    class _Parameter:
        name: str
        value: Value | int
        writer: WriterType

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                return f"parameter {self.name} = {self.value}"
            else:
                return f"{self.name} : integer := {self.value}"

    def Parameter(self, name: str, value: Value | int | str) -> Value:
        if isinstance(value, str):
            value = f'"{value}"'
        _o = self._Parameter(name, value, writer=self._writer)
        self.container.append(_o)
        return Value(name, 1, isSignal=True)
