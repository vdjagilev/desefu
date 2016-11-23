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
                Output.err("Could not read file \"%s\". %s" % (dict_file, e))
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

                #for enc in self.encoding_list:
                #    Output.log("Trying file \"%s\" decode as \"%s\"" % (f, enc))

                try:
                    file_content = open(f, 'rb').read()
                except Exception as e:
                    Output.err("File \"%s\" could not be opened: %s" % (f, e))
                    Kernel.end()

                if not file_content or len(file_content) == 0:
                    Output.log("A file \"%s\" is empty. Skipping it" % f)
                    continue

                for line in self.dict_words[dictionary]:
                    if file_content.lower().find(line.lower()) != -1:
                        if f not in self.files_criteria:
                            self.files_criteria.append(f)

                        # Data collection part, which is responsible for collecting data.
                        # For each file there is a set of words, which were found in
                        # that file. In this case do_filter_files() function does
                        # do_collect_data(), but that is needed for optimization
                        # in order to avoid file content search procedure again
                        try:
                            self.data[f]
                        except KeyError:
                            self.data[f] = []

                        self.data[f].append(line)

        self.files = self.files_criteria
