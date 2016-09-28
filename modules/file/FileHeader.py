from modules import AbstractModule
from kernel.output import Output, OutputResult

class FileHeader(AbstractModule):
    def is_collect_data(self) -> bool:
        return False

    def check(self):
        return True

    def is_extract_data(self) -> bool:
        return False

    def check_arguments(self, args):
        try:
            types = args['types']

            if 0 == len(types):
                Output.do("Amount of listed types should be at least one, or more", OutputResult.Error)
                Kernel.end()

            Output.log("Amount of types: %d" % len(types))
        except IndexError:
            Output.do("FileHeader module should have \"types\" argument", OutputResult.Error)
            Kernel.end()

        return True

    def description(self) -> str:
        return "FileHeader module is used to filter files by their header"

    def is_filter_files(self) -> bool:
        return True

    def do_filter_files(self):
        files = self.module_chain.files
        files_criteria = []
        types = self.args['types']

        for t in types:
            for f in files:
                if f in files_criteria:
                    continue

                file_data = open(f, 'r+b').read(len(t))

                # ToDo
