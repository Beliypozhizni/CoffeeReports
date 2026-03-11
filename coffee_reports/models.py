from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class Report:
    headers: Sequence[str]
    rows: Sequence[Sequence[Any]]
