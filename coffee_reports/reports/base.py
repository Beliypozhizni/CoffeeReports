from abc import ABC, abstractmethod
from coffee_reports.models import Report


class ReportBuilder(ABC):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @abstractmethod
    def build(self, rows: list[dict[str, str]]) -> Report:
        pass
