from modules.file.type.SqliteDatabase import SqliteDatabase

def test_check_arguments():
    sd = SqliteDatabase()
    sd.extract = {
        'result': {}
    }

    assert sd.check_arguments()

def test_check_arguments_fail():
    sd = SqliteDatabase()

    assert not sd.check_arguments()
