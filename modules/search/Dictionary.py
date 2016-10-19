from kernel.kernel import Kernel
from kernel.output import Output, OutputResult
from modules import AbstractModule


class Dictionary(AbstractModule):
    def check(self):
        return True

    def check_arguments(self):
        self.dict_words = {}
        self.encoding_list = []

        if len(self.args) == 0:
            Output.err("Dictionary: Arguments should contain at least one option")
            return False

        dictionary_list = []
        try:
            dictionary_list = self.args['dictionary']
        except KeyError:
            Output.err("Mandatory argument \"dictionary\" is missing")
            return False

        try:
            arg_encoding_list = self.args['encoding']
        except KeyError:
            arg_encoding_list = ['utf-8', 'latin-1']

        self.encoding_list = arg_encoding_list

        for dict_file in dictionary_list:
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

    def is_filter_files(self) -> bool:
        return True

    def do_filter_files(self):
        self.files_criteria = []

        for dictionary in self.dict_words:
            for f in self.files:
                # The first successfully read encoding is applied
                # ToDo: Improve, try to read and compare all listed codes
                file_encoding = None
                file_content = None

                for enc in self.encoding_list:
                    Output.log("Trying file \"%s\" decode as \"%s\"" % (f, enc))

                    try:
                        file_content = open(f, 'r', encoding=enc).read()
                    except UnicodeDecodeError as e:
                        Output.log("Could not decode file \"%s\" in unicode" % f)
                        continue

                    file_encoding = enc

                    if file_content:
                        break

                if not file_content:
                    continue

                for line in self.dict_words[dictionary]:
                    if file_content.find(line) != -1:
                        if f not in self.files_criteria:
                            self.files_criteria.append(f)

                        try:
                            self.data[f]
                        except KeyError:
                            self.data[f] = []

                        self.data[f].append(line)

        return True
