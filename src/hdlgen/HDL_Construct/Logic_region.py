from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable

from hdlgen.define import WriterType
from hdlgen.HDL_Construct.Region import Region
from hdlgen.HDL_Construct.Value import Value


class LogicRegion(Region):
    _container: list
    _indent: int
    _writer: WriterType

    def __init__(self, container: list, writer: WriterType, indent: int):
        self._container = container
        self._writer = writer
        self._indent = indent

    def __str__(self) -> str:
        if (
            self._writer == WriterType.VERILOG
            or self._writer == WriterType.SYSTEM_VERILOG
        ):
            return f"\n{'\n'.join([str(i) for i in self.container])}"
        else:
            signal = []
            other = []
            for i in self.container:
                if isinstance(i, self._signal):
                    signal.append(i)
                else:
                    other.append(i)
            return f"{''.join([str(i) for i in signal])}begin\n{''.join([str(i) for i in other])}"

    @property
    def container(self):
        return self._container

    @property
    def indent(self):
        return self._indent

    def ConnectPair(self, dst: str, src: Value | int):
        return self._ConnectPair(dst, src, self._writer)

    def Signal(self, name: str, bits: int | Value = 1):
        _o = self._signal(name, bits, self._writer)
        self.container.append(_o)
        return Value(name, bits, isSignal=True)

    def Assign(self, dst: Value, src: Value | int):
        _o = self._Assign(dst, src, self._writer)
        self.container.append(_o)
        return _o

    def Constant(self, name: str, value: int):
        _o = self._Constant(name, value, self._writer)
        self.container.append(_o)
        return Value(name, value, isSignal=False)

    def Concat(self, *args):
        return self._Concat(args, writer=self._writer)

    def ReadMem(
        self,
        file: Value | str,
        dst: str,
        width: int,
        depth: int,
        start: int = 0,
        end: int = 0,
    ):
        _o = self._ReadMem(file, dst, self._writer, width, depth, start, end)
        self.container.append(_o)
        return Value(dst, depth, isSignal=True)

    def InitModule(
        self,
        module: str,
        initName: str,
        ports: list["LogicRegion._ConnectPair"],
        parameters: list["LogicRegion._ConnectPair"] = [],
    ):
        _o = self._InitModule(
            module,
            initName,
            parameters,
            ports,
            self._writer,
            self.indent,
            self.indentCount,
        )
        self.container.append(_o)
        return _o

    @contextmanager
    def Generate(self):
        from hdlgen.HDL_Construct.Generate_region import GenerateRegion

        r = GenerateRegion([], self._writer, self.indent + self.indentCount)
        try:
            yield r
        finally:
            self.container.append(r)

    @contextmanager
    def IfElse(self, cond: Value):
        from hdlgen.HDL_Construct.IfElse_region import IfElseRegion

        r = IfElseRegion(cond, [], [], self._writer, self.indent)
        try:
            yield r
        finally:
            self.container.append(r)

    @contextmanager
    def Initial(self):
        from hdlgen.HDL_Construct.Initial_region import InitialRegion

        r = InitialRegion([], self._writer, self.indent + self.indentCount)
        try:
            yield r
        finally:
            self.container.append(r)

    @dataclass
    class _ConnectPair:
        dst: str
        src: Value | int
        writer: WriterType

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                if isinstance(self.src, int):
                    return f".{self.dst}({max(self.src.bit_length(), 1)}'d{self.src})"
                else:
                    return f".{self.dst}({self.src})"
            else:
                return f"{self.dst} => {self.src}"

    @dataclass
    class _InitModule:
        module: str
        initName: str
        parameter: list["LogicRegion._ConnectPair"]
        ports: list["LogicRegion._ConnectPair"]
        writer: WriterType
        indent: int
        indentCount: int

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                if self.parameter:
                    r = (
                        f"{' ' * self.indent}{self.module} #(\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.parameter])}\n"
                        f"{' ' * self.indent}) {self.initName} (\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.ports])}\n"
                        f"{' ' * self.indent});\n"
                    )
                else:
                    r = (
                        f"{' ' * self.indent}{self.module} #() {self.initName} (\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.ports])}\n"
                        f"{' ' * self.indent});\n"
                    )
            else:
                if self.parameter:
                    r = (
                        f"{' ' * self.indent} {self.initName} : {self.module} generic map(\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.parameter])}\n"
                        f"{' ' * self.indent}) port map(\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.ports])}\n"
                        f"{' ' * self.indent});\n"
                    )
                else:
                    r = (
                        f"{' ' * self.indent} {self.initName} : {self.module} port map(\n"
                        f"{',\n'.join([f'{" " * (self.indent + self.indentCount)}{i}' for i in self.ports])}\n"
                        f"{' ' * self.indent});\n"
                    )

            return r

    @dataclass
    class _Assign:
        dst: Value
        src: Value | int
        writer: WriterType

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                if isinstance(self.src, int):
                    return (
                        f"assign {self.dst} = {max(int(self.dst.bits), 1)}'d{self.src};"
                    )
                return f"assign {self.dst} = {self.src};"
            else:
                return f"{self.dst} <= {self.src};"

    @dataclass
    class _signal:
        name: str
        bits: Value | int = 1
        writer: WriterType = WriterType.VERILOG

        def __str__(self) -> str:
            if self.writer == WriterType.VERILOG:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"reg {self.name};"
                elif isinstance(self.bits, int):
                    return f"reg [{self.bits - 1}:0] {self.name};"
                else:
                    return f"reg [{self.bits}:0] {self.name};"
            elif self.writer == WriterType.SYSTEM_VERILOG:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"logic {self.name};"
                elif isinstance(self.bits, int):
                    return f"logic [{self.bits - 1}:0] {self.name};"
                else:
                    return f"logic [{self.bits}:0] {self.name};"
            else:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"{self.name} : std_logic;"
                elif isinstance(self.bits, int):
                    return f"{self.name} : std_logic_vector({self.bits - 1} downto 0);"
                else:
                    return f"{self.name} : std_logic_vector({self.bits} downto 0);"

    @dataclass
    class _Constant:
        name: str
        value: int
        writer: WriterType

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                return f"localparam {self.name} = 32'd{self.value};"
            else:
                return f"constant {self.name} : integer := {self.value};"

    @dataclass(frozen=True)
    class _Concat:
        item: Iterable[Value]
        writer: WriterType

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                return f"{{{' ,'.join(str(i) for i in self.item)}}}"
            else:
                return f"{' & '.join(str(i) for i in self.item)}"

        @property
        def value(self) -> str:
            return self.__str__()

    @dataclass
    class _ReadMem:
        file: Value | str
        dst: str
        writer: WriterType
        width: int
        depth: int
        start: int = 0
        end: int = 0

        def __str__(self) -> str:
            if (
                self.writer == WriterType.VERILOG
                or self.writer == WriterType.SYSTEM_VERILOG
            ):
                if isinstance(self.file, str):
                    return (
                        f"reg [{self.width - 1}:0] {self.dst} [0:{self.depth - 1}];\n"
                        f'initial $readmemh("{self.file}", {self.dst});'
                    )
                else:
                    return (
                        f"reg [{self.width - 1}:0] {self.dst} [0:{self.depth - 1}];\n"
                        f"initial $readmemh({self.file}, {self.dst});"
                    )
            else:
                raise NotImplementedError
