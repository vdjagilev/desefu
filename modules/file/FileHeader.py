from modules import AbstractModule
from kernel.output import Output, OutputResult
from kernel.kernel import Kernel


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
                Output.err("Amount of listed types should be at least one, or more")
                Kernel.end()

            for i in range(len(types)):
                for j in range(len(types[i])):
                    types[i][j] = str(types[i][j])

            Output.log("Amount of types: %d" % len(types))
        except IndexError:
            Output.err("FileHeader module should have \"types\" argument")
            Kernel.end()

        return True

    def description(self) -> str:
        return "FileHeader module is used to filter files by their header"

    def is_filter_files(self) -> bool:
        return True

    def do_filter_files(self):
        files = self.files
        files_criteria = []
        types = self.args['types']

        for t in types:
            hex_str = ' '.join(t)

            for f in files:
                if f in files_criteria:
                    continue

                file_data = open(f, 'r+b').read(len(t))
                # ToDo: Do more effective way of comparison (binary) instead of string
                header = ' '.join(["{:02X}".format(x) for x in file_data])

                if hex_str == header:
                    files_criteria.append(f)

        self.files = files_criteria
