from kernel.output import Output, OutputResult
from modules import AbstractModule


class Dictionary(AbstractModule):
    def check(self):
        return True

    def check_arguments(self):
        if len(self.args) == 0:
            Output.err("Dictionary: Arguments should contain at least one dictionary")
            return False

        return True

    def do_filter_files(self):
        return True