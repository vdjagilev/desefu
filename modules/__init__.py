from abc import ABC, abstractmethod
from kernel.output import Output, OutputResult


class AbstractModule(ABC):
    def __init__(self):
        # Sibling module chain, where submodules are located
        self.module_chain = None

        self.filter_files = False
        self.collect_data = False
        self.extract_data = False
        self.args = None

        # Initial value is none, can be filled during execution
        self.files = []

        self.data = {}

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def check_arguments(self):
        pass

    # Gives information if module filtering files or not
    def is_filter_files(self) -> bool:
        return self.filter_files

    # Gives information if module collecting data from analyzed files
    def is_collect_data(self) -> bool:
        return self.collect_data

    # Does module have extract options
    def is_extract_data(self) -> bool:
        return self.extract_data

    def description(self) -> str:
        return ""

    def do_filter_files(self):
        pass

    def do_collect_data(self):
        pass

    def do_extract_data(self):
        pass

    def execute(self):
        Output.do("Executing module: \"%s\"" % self.__class__.__module__.replace("modules.", "", 1))

        try:
            if self.is_filter_files():
                self.do_filter_files()
                Output.ok("Files: %d" % len(self.files))

            if self.is_collect_data():
                self.do_collect_data()

            if self.is_extract_data():
                self.do_extract_data()
        except PermissionError as e:
            Output.fail("Permission error. Could not read file \"%s\"" % e.filename)
