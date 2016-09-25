from modules import AbstractModule


class FileHeader(AbstractModule):
    def is_collect_data(self) -> bool:
        return False

    def check(self):
        return True

    def is_extract_data(self) -> bool:
        return False

    def check_arguments(self, args):
        # ToDo: Make a check
        return True

    def description(self) -> str:
        return "FileHeader module is used to filter files by their header"

    def is_filter_files(self) -> bool:
        return True
