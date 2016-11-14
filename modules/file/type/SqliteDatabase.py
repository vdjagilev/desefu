from modules import AbstractModule
from kernel.output import Output
from kernel.kernel import Kernel
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

    def do_extract_data(self):
        self.extract_data = {}
        search_criteria_data = None
        search_criteria_index = None

        # ToDo: Add other variants (file, custom string support, ... etc)
        if len(self.e_query_where) != 0:
            where_str = self.e_query_where

            # Reference to a mod
            # ToDo: Make possible to have an array instead of key:value pair
            if where_str[0:4] == '~mod':
                where_elem_list = where_str[5:].split('.')

                # Support only data for now
                where_mod = self.parent_module_chain.modules[int(where_elem_list[0]) - 1]
                search_criteria_data = where_mod.data

                try:
                    search_criteria_index = int(where_elem_list[2])
                except IndexError:
                    search_criteria_index = None

        # Traverse each database file
        for db_file in self.files:

            if search_criteria_data:
                # For simple array data, without any index
                # "file" => [1, 2, 3]
                if not search_criteria_index:
                    # ToDo: Check if file does not exist in module data
                    collected_file_data = search_criteria_data[db_file]
                else:
                    # For more complex list
                    # "file" => [(123, 456), (123, 789)]
                    Output.log("No index approach yet implemented")

            db = sqlite3.connect('file:%s?mode=ro' % db_file, uri=True)
            db.row_factory = sqlite3.Row
            tables = {}

            for table in db.execute('SELECT tbl_name FROM sqlite_master WHERE type = "table"'):
                timestamp_columns = []
                id_columns = []
                result_columns = []
                #data_result = []

                result = None
                cursor = None

                try:
                    cursor = db.execute('SELECT * FROM %s;' % table[0])
                    result = cursor.fetchall()
                except OperationalError:
                    Output.warn("Could not fetch table info from table \"%s\"" % table[0])
                    continue

                table_columns = [desc[0] for desc in cursor.description]

                if 'timestamps' in self.extract['columns']:
                    for substring in self.potential_timestamps:
                        timestamp_columns.extend([s for s in table_columns if substring.lower() in s.lower()])

                if 'id' in self.extract['columns']:
                    for substring in ['id']:
                        id_columns.extend([s for s in table_columns if substring.lower() in s.lower()])

                for file_data_elem in collected_file_data:
                    for row in result:
                        for col, value in enumerate(row):
                            if str(file_data_elem).lower() in str(value).lower():
                                if table_columns[col] not in result_columns:
                                    result_columns.append(table_columns[col])

                if len(result_columns) > 0:
                    #export_columns = id_columns + timestamp_columns + result_columns
                    export_columns = []
                    export_columns.extend(id_columns)
                    export_columns.extend(timestamp_columns)
                    export_columns.extend(result_columns)
                    export_data = []

                    # ToDo: Make ORDER BY query here.
                    result_cursor = db.cursor()
                    result_data = db.execute("SELECT %s FROM %s;" % (", ".join(export_columns), table[0]))

                    for c in export_columns:
                        for row in result_data:
                            #print("Col: %s, data: %s" % (c, row[c]))
                            print(row[c])
                            #export_data.append([row[c]])

                    #for c in export_columns:
                    #    data = []
                    #    print("Idx: %s, Col: %s" % (export_columns.index(c), c))
                    #    print(row[export_columns.index(c)])
                    #    print("------")

                    #    for row in result:
                    #        data.append(row[export_columns.index(c)])

                    #    export_data = data

                    tables[table[0]] = (export_columns, export_data)
                #print("Table: %s" % table[0])
                #print("TimeCol: %s" % timestamp_columns)
                #print("IdCol: %s" % id_columns)
                #print("Col: %s" % result_columns)
                #print("---------------------------------")

            db.close()

            if len(tables) > 0:
                self.extract_data[db_file] = tables

        print(self.extract_data)

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

        if not where_query:
            Output.err("Option \"where\" is mandatory.")
            Kernel.end()

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
