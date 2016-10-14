from modules import AbstractModule


class SqliteDatabase(AbstractModule):
    def is_collect_data(self) -> bool:
        return True

    def check(self):
        return True

    def is_extract_data(self) -> bool:
        return True

    def check_arguments(self):
        # ToDo: Check args
        return True

    def description(self) -> str:
        return "SqliteDatabase module is used to collect and extract certain data from SQLite databases"

    def is_filter_files(self) -> bool:
        return False
