from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Value:
    _value: str
    _bitWidth: int | Self | None
    isSignal: bool

    @property
    def value(self):
        return self._value

    @property
    def bits(self):
        return self._bitWidth

    def customEq(self, a, b):
        return a.value == b.value and a.bits == b.bits and a.isSignal == b.isSignal

    def __repr___(self):
        return f"[{self.isSignal=} {self.bits=}]{self.value}"

    def __bool__(self):
        return True

    def __str__(self):
        return self.value

    def __getitem__(self, key: slice | int | Self):
        if self.bits is None:
            raise ValueError("Cannot slice or get value with unknown bit width")
        if isinstance(key, int):
            return Value(f"{self.value}[{key}]", 1, self.isSignal)
        elif isinstance(key, slice):
            if key.step is not None:
                raise ValueError("Cannot slice with step")
            if self.isSignal:
                if key.start is None:
                    return Value(
                        f"{self.value}[{self.bits - 1}:{key.stop}]",
                        self.bits,
                        self.isSignal,
                    )
                if key.stop is None:
                    return Value(
                        f"{self.value}[{key.start}:0]", self.bits, self.isSignal
                    )
                if (
                    key.start == key.stop
                    and isinstance(key.start, int)
                    and isinstance(key.stop, int)
                ):
                    return Value(f"{self.value}[{key.start}]", 1, self.isSignal)
                return Value(
                    f"{self.value}[{key.start}:{key.stop}]",
                    self.bits,
                    self.isSignal,
                )
            else:
                raise ValueError("Can only slice port and signal type")
        elif isinstance(key, Value):
            return Value(f"{self.value}[{key.value}]", self.bits, self.isSignal)
        else:
            raise ValueError("Invalid index")

    def __add__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} + {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} + {other}", self.bits, self.isSignal)

    def __sub__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} - {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} - {other}", self.bits, self.isSignal)

    def __mul__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} * {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} * {other}", self.bits, self.isSignal)

    def __truediv__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} / {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} / {other}", self.bits, self.isSignal)

    def __floordiv__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} // {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} // {other}", self.bits, self.isSignal)

    def __mod__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} % {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} % {other}", self.bits, self.isSignal)

    def __pow__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} ** {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} ** {other}", self.bits, self.isSignal)

    def __lshift__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} << {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} << {other}", self.bits, self.isSignal)

    def __rshift__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} >> {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} >> {other}", self.bits, self.isSignal)

    def __and__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} & {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} & {other}", self.bits, self.isSignal)

    def __xor__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} ^ {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} ^ {other}", self.bits, self.isSignal)

    def __or__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} | {other.value}", self.bits, self.isSignal)
        else:
            return Value(f"{self.value} | {other}", self.bits, self.isSignal)

    def __neg__(self):
        return Value(f"-{self.value}", self.bits, self.isSignal)

    def __pos__(self):
        return Value(f"+{self.value}", self.bits, self.isSignal)

    def __abs__(self):
        raise NotImplementedError("Absolute value is not supported")

    def __invert__(self):
        return Value(f"~{self.value}", self.bits, self.isSignal)

    def __lt__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} < {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} < {other}", 1, self.isSignal)

    def __le__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} <= {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} <= {other}", 1, self.isSignal)

    def __eq__(self, other):
        if isinstance(other, Value):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} != {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} != {other}", 1, self.isSignal)

    def __gt__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} > {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} > {other}", 1, self.isSignal)

    def __ge__(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} >= {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} >= {other}", 1, self.isSignal)

    def __len__(self):
        return self.bits

    def logical_and(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} && {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} && {other}", 1, self.isSignal)

    def logical_or(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} || {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} || {other}", 1, self.isSignal)

    def logical_not(self):
        return Value(f"!{self.value}", 1, self.isSignal)

    def __radd__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} + {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} + {self.value}", self.bits, self.isSignal)

    def __rsub__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} - {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} - {self.value}", self.bits, self.isSignal)

    def __rmul__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} * {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} * {self.value}", self.bits, self.isSignal)

    def __rtruediv__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} / {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} / {self.value}", self.bits, self.isSignal)

    def __rfloordiv__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} // {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} // {self.value}", self.bits, self.isSignal)

    def __rmod__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} % {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} % {self.value}", self.bits, self.isSignal)

    def __rlshift__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} << {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} << {self.value}", self.bits, self.isSignal)

    def __rrshift__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} >> {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} >> {self.value}", self.bits, self.isSignal)

    def __rand__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} & {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} & {self.value}", self.bits, self.isSignal)

    def __rxor__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} ^ {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} ^ {self.value}", self.bits, self.isSignal)

    def __ror__(self, other):
        if isinstance(other, Value):
            return Value(f"{other.value} | {self.value}", self.bits, self.isSignal)
        else:
            return Value(f"{other} | {self.value}", self.bits, self.isSignal)

    def full_eq(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} === {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} === {other}", 1, self.isSignal)

    def full_ne(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} !== {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} !== {other}", 1, self.isSignal)

    def eq(self, other):
        if isinstance(other, Value):
            return Value(f"{self.value} == {other.value}", 1, self.isSignal)
        else:
            return Value(f"{self.value} == {other}", 1, self.isSignal)
