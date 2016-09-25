from modules import AbstractModule


class Extension(AbstractModule):

    def check(self):
        return True

    def check_arguments(self, args):
        return True

    def description(self) -> str:
        return "Extension module is responsible for filtering out files by their extension"

    def is_filter_files(self) -> bool:
        return True
