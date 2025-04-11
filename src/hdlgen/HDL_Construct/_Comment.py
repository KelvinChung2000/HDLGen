from dataclasses import dataclass


@dataclass
class _Comment:
    comment: str

    def __str__(self):
        return f"// {self.comment}"
