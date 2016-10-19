from kernel.kernel import Kernel
from kernel.output import Output, OutputResult
from modules import AbstractModule


class Dictionary(AbstractModule):
    def check(self):
        return True

    def check_arguments(self):
        self.dict_words = {}

        if len(self.args) == 0:
            Output.err("Dictionary: Arguments should contain at least one dictionary")
            return False

        for dict_file in self.args:
            try:
                with open(dict_file, 'r') as file_words:
                    self.dict_words[dict_file] = []

                    for line in file_words:
                        if len(line) > 0:
                            self.dict_words[dict_file].append(line.strip())

            except Exception as e:
                Output.err("Could not read file \"%s\". %s" % (dict_file, e.with_traceback()))
                Kernel.end()

        Output.do("Total amount of word dictionaries: %d" % len(self.dict_words))

        return True

    def description(self) -> str:
        return "A module which is responsible for filtering files by their contents, which can be found in dictionaries (aka files with keywords)"

    def do_filter_files(self):
        return True
