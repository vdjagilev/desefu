from modules import AbstractModule


class Extension(AbstractModule):

    def check(self):
        pass

    def check_arguments(self, args):
        pass

    def description(self) -> str:
        return "Extension module is responsible for filtering out files by their extension"

    def is_filter_files(self) -> bool:
        return True