from kernel.kernel import Kernel
from modules.file.type.SqliteDatabase import SqliteDatabase
from modules.search.Dictionary import Dictionary
from kernel.module_chain import ModuleChain
from nose.tools import assert_raises

class ResultMock:
    def __init__(self):
        self.result = []

def test_check_arguments():
    sd = SqliteDatabase()
    sd.extract = {
        'result': {},
        'where': 'test'
    }

    assert sd.check_arguments()

def test_check_arguments_fail():
    sd = SqliteDatabase()

    assert not sd.check_arguments()

    sd.extract = {
        'result': {}
    }

    assert_raises(SystemExit, lambda : sd.check_arguments())

def test_extract_data_main():
    Kernel.result = ResultMock()

    mc = ModuleChain()
    mc.files = ["tests/modules/file/type/sqlitedatabase_mocks/test1.db"]
    mc.id = "Test01"

    dm = Dictionary()
    dm.files = mc.files
    dm.current_module_chain = mc
    dm.args = {'dictionary': ["tests/modules/search/dictionaries/dictionary1.txt"]}

    dm.check()
    dm.check_arguments()

    mc.modules.append(dm)

    mc_s = ModuleChain()
    mc_s.files = mc.files
    mc_s.id = "[sub]"

    dm.module_chain = mc_s

    sd = SqliteDatabase()
    sd.extract = {
        'columns':  ['result', 'timestamps', 'id'],
        'where': '~mod.1.data',
        'order': {
            'timestamps': 'DESC'
        },
        'result': ['data']
    }

    sd.check()
    sd.check_arguments()

    sd.parent_module_chain = mc
    sd.current_module_chain = mc_s

    mc_s.modules.append(sd)

    Kernel.exec_search([mc])

    result = Kernel.collect_result(mc)

    assert len(result['modules']) == 1

    dm_result = result['modules'][0]
    dm_chain = dm_result['module_chain']

    assert dm_chain['module_chain_id'] == '[sub]'

    smod = dm_chain['modules'][0]
    assert smod['files_count'] == 1

    edata = smod['extract_data']

    db = edata['tests/modules/file/type/sqlitedatabase_mocks/test1.db']
    assert list(db.keys()) == ['mega_messenger_test']
    table = db['mega_messenger_test']
    columns = table[0]
    data = table[1]

    assert columns == ['id', 'timestamp', 'text']
    assert data[0][2] == 'Hello there'
