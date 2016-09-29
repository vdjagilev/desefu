from abc import ABC, abstractmethod
from kernel.output import Output, OutputResult


class AbstractModule(ABC):
    def __init__(self):
        self.is_sub_module = False
        self.parent_module = None

        # Current module chain, where module is located
        self.module_chain = None
        
        # Sibling module chain, "sub"
        self.sibling_module_chain = None

        self.filter_files = False
        self.collect_data = False
        self.extract_data = False
        self.args = None

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def check_arguments(self, args):
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
        Output.log("Executing module: %s.%s" % (self.__class__.__module__, self.__class__.__name__))
        if self.is_filter_files():
            self.do_filter_files()

        if self.is_collect_data():
            self.do_collect_data()

        if self.is_extract_data():
            self.do_extract_data()
