from modules import AbstractModule
from kernel.output import Output, OutputResult
from os.path import splitext

class Extension(AbstractModule):

    def check(self):
        return True

    def check_arguments(self):
        if len(self.args) == 0:
            Output.err("Extension should have at least one element in arguments")
            return False

        return True

    def description(self) -> str:
        return "Extension module is responsible for filtering out files by their extension"

    def is_filter_files(self) -> bool:
        return True

    def do_filter_files(self):
        files = self.files
        files_criteria = []

        for ext in self.args:
            for f in files:
                if f in files_criteria:
                    continue

                if splitext(f)[1][1:] == ext:
                    files_criteria.append(f)

        self.files = files_criteria
