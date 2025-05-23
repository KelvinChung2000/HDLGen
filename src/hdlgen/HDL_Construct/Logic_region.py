from contextlib import contextmanager
from dataclasses import dataclass
from textwrap import indent
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
            comp: list[str] = []
            repeat = set()
            for i in self.container:
                if isinstance(i, (self._signal, self._Constant)):
                    signal.append(i)
                elif isinstance(i, self._InitModule):
                    if i.module in repeat:
                        continue
                    repeat.add(i.module)
                    comp.append(i.getVHDL_comp())
                    other.append(i)
                else:
                    other.append(i)

            indentCount = (self.indent + self.indentCount) * " "
            return (
                f"{indent(f'{"\n".join([str(i) for i in signal])}', indentCount)}\n"
                # f"{indent(f'{"\n".join([i for i in comp])}', indentCount)}"
                "\n"
                f"begin\n{indent(f'{"\n".join([str(i) for i in other])}', indentCount)}"
            )

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

    def Signal_default(self, name: str, bits: int | Value = 1, defaultValue: int = 0):
        _o = self._signal_default(name, bits, self._writer, defaultValue)
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
    def IfElse(self, cond: Value | bool):
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
                if isinstance(self.src, int):
                    return f'{self.dst} => "{self.src}"'
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
                        f"{self.module} #(\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.parameter])}\n"
                        f") {self.initName} (\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                        f");\n"
                    )
                else:
                    r = (
                        f"{self.module} #() {self.initName} (\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                        f");\n"
                    )
            else:
                if self.parameter:
                    r = (
                        f"{self.initName} : entity work.{self.module}\ngeneric map(\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.parameter])}\n"
                        f"{' ' * self.indent})\nport map(\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                        f");\n"
                    )
                else:
                    r = (
                        f"{self.initName} : entity work.{self.module}()\ngeneric map(\n"
                        f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                        f");\n"
                    )

            return r

        def getVHDL_comp(self) -> str:
            if self.parameter:
                r = (
                    f"component {self.module} is\n"
                    f"{' ' * self.indentCount} generic(\n"
                    f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.parameter])}\n"
                    f"{' ' * self.indentCount}) port(\n"
                    f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                    f"{' ' * self.indentCount});\n"
                    f"end component;\n"
                )
            else:
                r = (
                    f"component {self.module} is\n"
                    f"{' ' * (self.indentCount)} {self.initName} : {self.module} port(\n"
                    f"{',\n'.join([f'{" " * (self.indentCount)}{i}' for i in self.ports])}\n"
                    f"{' ' * self.indentCount});\n"
                    f"end component;\n"
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
                    return f"wire {self.name};"
                elif isinstance(self.bits, int):
                    return f"wire [{self.bits - 1}:0] {self.name};"
                else:
                    return f"wire [{self.bits}:0] {self.name};"
            elif self.writer == WriterType.SYSTEM_VERILOG:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"logic {self.name};"
                elif isinstance(self.bits, int):
                    return f"logic [{self.bits - 1}:0] {self.name};"
                else:
                    return f"logic [{self.bits}:0] {self.name};"
            else:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"signal {self.name} : std_logic;"
                elif isinstance(self.bits, int):
                    return f"signal {self.name} : std_logic_vector({self.bits - 1} downto 0);"
                else:
                    return (
                        f"signal {self.name} : std_logic_vector({self.bits} downto 0);"
                    )

    @dataclass
    class _signal_default:
        name: str
        bits: Value | int = 1
        writer: WriterType = WriterType.VERILOG
        defaultValue: int = 0

        def __str__(self) -> str:
            if self.writer == WriterType.VERILOG:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"wire {self.name} = {self.bits}'d{self.defaultValue};"
                elif isinstance(self.bits, int):
                    return f"wire [{self.bits - 1}:0] {self.name} = {self.bits}'d{self.defaultValue};"
                else:
                    return f"wire [{self.bits}:0] {self.name} = {self.bits}'d{self.defaultValue};"
            elif self.writer == WriterType.SYSTEM_VERILOG:
                if self.bits == 1 and isinstance(self.bits, int):
                    return f"logic {self.name} = {self.bits}'d{self.defaultValue};"
                elif isinstance(self.bits, int):
                    return f"logic [{self.bits - 1}:0] {self.name} = {self.bits}'d{self.defaultValue};"
                else:
                    return f"logic [{self.bits}:0] {self.name} = {self.bits}'d{self.defaultValue};"
            else:
                v = bin(self.defaultValue)[2:]
                if self.bits == 1 and isinstance(self.bits, int):
                    return f'signal {self.name} : std_logic := "{v}";'
                elif isinstance(self.bits, int):
                    return f'signal {self.name} : std_logic_vector({self.bits - 1} downto 0) := "{v}";'
                else:
                    return f'signal {self.name} : std_logic_vector({self.bits} downto 0) := "{v}";'

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
