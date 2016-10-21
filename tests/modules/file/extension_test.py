from modules.file.Extension import Extension

def test_check_arguments():
    ext = Extension()
    ext.args = ['', 'db', 'sqlite', 'sqlite3']

    assert ext.check()
    assert ext.check_arguments()

    ext.args = None

    try:
        ext.check_arguments()
    except SystemExit:
        assert True

def test_dict_values():
    ext = Extension()
    ext.args = ['', 'db']

    assert len(ext.description()) > 0
    assert ext.is_filter_files()
    assert not ext.is_collect_data()
    assert not ext.is_extract_data()

def test_filter_files():
    ext = Extension()
    ext.args = ['']

    files = [
        './tests/modules/file/extension_mocks/database.sqlite',
        './tests/modules/file/extension_mocks/database2.db',
        './tests/modules/file/extension_mocks/noextfile',
        './tests/modules/file/extension_mocks/some.jpg'
    ]

    ext.files = files

    assert ext.do_filter_files()
    assert len(ext.files) == 1

    ext.files = files
    ext.args = ['', 'db', 'jpg']

    assert ext.do_filter_files()
    assert len(ext.files) == 3
