from abc import ABC, abstractmethod


class AbstractModule(ABC):
    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def check_arguments(self, args: list):
        pass

    # Gives information if module filtering files or not
    def is_filter_files(self) -> bool:
        return False

    # Gives information if module collecting data from analyzed files
    def is_collect_data(self) -> bool:
        return False

    # Does module have extract options
    def is_extract_data(self) -> bool:
        return False

    def description(self) -> str:
        return ""
