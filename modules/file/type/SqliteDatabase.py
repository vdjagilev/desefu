from modules import AbstractModule
from kernel.output import Output
import sqlite3
from sqlite3 import OperationalError


class SqliteDatabase(AbstractModule):
    potential_timestamps = [
        'date', 'time', 'timestamp'
    ]

    def is_collect_data(self) -> bool:
        return False

    def check(self):
        return True

    def is_extract_data(self) -> bool:
        return True

    def build_query(self, e_result, e_query_fields, e_query_where, e_query_order):
        pass

    def do_extract_data(self):
        # Traverse each database
        for db_file in self.files:
            db = sqlite3.connect('file:%s?mode=ro' % db_file, uri=True)
            tables = {}

            for row in db.execute('SELECT tbl_name FROM sqlite_master WHERE type = "table"'):
                timestamp_columns = []
                id_columns = []

                try:
                    tables[row[0]] = db.execute('PRAGMA table_info(%s);' % row[0]).fetchall()
                except OperationalError:
                    Output.warn("Could not fetch table info from table \"%s\"" % row[0])

            db.close()

    def check_arguments(self):
        self.e_result = None
        self.e_query_where = None
        self.e_query_order = None
        self.e_query_select = None

        # Check "extract" field as well
        try:
            result = self.extract['result']
        except KeyError:
            Output.err("\"extract\" mandatory option \"result\" is missing")
            return False

        self.e_result = result

        where_query = None
        try:
            where_query = self.extract['where']
        except KeyError:
            where_query = False

        self.e_query_where = where_query

        order_query = None
        try:
            order_query = self.extract['order']
        except KeyError:
            order_query = False

        self.e_query_order = order_query

        select_query = None
        try:
            select_query = self.extract['columns']
        except KeyError:
            select_query = False

        self.e_query_select = select_query

        return True

    def description(self) -> str:
        description = "SqliteDatabase module is used to extract certain data from SQLite databases in certain way\n"
        description += "This module has \"extract\" option with different options:\n"
        description += "* columns (Columns to be extracted) [array]\n"
        description += "** result - Those columns which match request conditions (related to \"where\" option)\n"
        description += "** timestamps - Different kind of timestamps, dates and other columns\n"
        description += "** id - Fetch fields containing ID keyword\n"
        description += "** all - Fetch all columns\n"
        description += "* where (Search criteria) [array]\n"
        description += "** ~mod.3.data.1 - Makes reference to data collection result from module #3 and column #1 (count start from 1)\n"
        description += "* order (how to order output result)\n"
        description += "** timestamps: DESC (Will make descending order by timestamps)\n"
        description += "* result (Export result)\n"
        description += "** columns (A simple list of columns which should be extracted)\n"
        description += "** rows (Export rows containing data)\n"

        return description

    def is_filter_files(self) -> bool:
        return False
