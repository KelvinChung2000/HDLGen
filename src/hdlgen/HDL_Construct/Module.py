from contextlib import contextmanager

from hdlgen.define import WriterType
from hdlgen.HDL_Construct.Logic_region import LogicRegion
from hdlgen.HDL_Construct.Parameter_region import ParameterRegion
from hdlgen.HDL_Construct.Port_region import PortRegion
from hdlgen.HDL_Construct.Region import Region


class Module(Region):
    _container: list[Region]
    _indent: int
    name: str
    attributes: list | None = None
    libraries: list[str] = [""]

    def __init__(
        self,
        name: str,
        container: list[Region],
        writer: WriterType,
        indent: int,
        attributes=None,
        libraries=[""],
    ):
        self.name = name
        self.attributes = attributes
        self._container = container
        self._indent = indent
        self._writer = writer
        self.libraries = libraries
        # self._parameters = ParameterRegion([], self.indent)
        # self._ports = PortRegion([], self.indent)
        # self._logics = LogicRegion([], self.indent)

    @property
    def container(self):
        return self._container

    @property
    def indent(self):
        return self._indent

    def __str__(self) -> str:
        # self.container.append(self._parameters)
        # self.container.append(self._ports)
        # self.container.append(self._logics)
        if (
            self._writer == WriterType.VERILOG
            or self._writer == WriterType.SYSTEM_VERILOG
        ):
            if self.attributes:
                return f"(* {', '.join([str(i) for i in self.attributes])} *)\nmodule {self.name} {''.join([str(i) for i in self.container])}\nendmodule\n\n"
            else:
                return f"module {self.name} {''.join([str(i) for i in self.container])}\nendmodule\n\n"
        else:
            t: dict = {
                "param": "",
                "port": "",
                "logic": "",
            }
            for i in self.container:
                if isinstance(i, ParameterRegion):
                    t["param"] = i
                elif isinstance(i, PortRegion):
                    t["port"] = i
                elif isinstance(i, LogicRegion):
                    t["logic"] = i

            return (
                f"library ieee;\n"
                f"use ieee.std_logic_1164.all;\n"
                f"use work.all;\n"
                f"{''.join([f'use {i};\n' for i in self.libraries if i])}\n"
                f"entity {self.name} is\n{t['param']}\n{t['port']}end entity {self.name};\n"
                f"architecture Behavioral of {self.name} is \n{t['logic']}\nend architecture Behavioral;\n"
            )

    @contextmanager
    def ParameterRegion(self):
        pr = ParameterRegion([], self._writer, self.indent + self.indentCount)
        try:
            yield pr
        finally:
            self.container.append(pr)

    @contextmanager
    def PortRegion(self):
        pr = PortRegion([], self._writer, self.indent + self.indentCount)
        try:
            yield pr
        finally:
            self.container.append(pr)

    @contextmanager
    def LogicRegion(self):
        lr = LogicRegion([], self._writer, self.indent)
        try:
            yield lr
        finally:
            self.container.append(lr)
