from modules import AbstractModule
from kernel.output import Output


class SqliteDatabase(AbstractModule):
    def is_collect_data(self) -> bool:
        return True

    def check(self):
        return True

    def is_extract_data(self) -> bool:
        return True

    def check_arguments(self):
        # Check "extract" field as well
        try:
            result = self.extract['result']
        except KeyError:
            Output.err("\"extract\" mandatory option \"result\" is missing")
            return False

        return True

    def description(self) -> str:
        return "SqliteDatabase module is used to collect and extract certain data from SQLite databases"

    def is_filter_files(self) -> bool:
        return False

    def do_extract_data(self):
        pass
