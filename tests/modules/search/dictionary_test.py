# Dictionary unit test file
from modules.search.Dictionary import Dictionary

def test_check_arguments():
    dic = Dictionary()
    dic.args = {
        'dictionary': [
            './tests/modules/search/dictionaries/dictionary1.txt',
            './tests/modules/search/dictionaries/dictionary2.txt'
        ]
    }


    assert dic.check_arguments()
    assert len(dic.args['dictionary']) == len(dic.dict_words)

    dic1 = dic.dict_words['./tests/modules/search/dictionaries/dictionary1.txt']
    dic2 = dic.dict_words['./tests/modules/search/dictionaries/dictionary2.txt']

    assert dic1[0] == 'a simple'
    assert dic2[0] == 'testing'
    assert dic1[3] == 'thesis'
    assert dic2[3] == 'hello'

def test_check_arguments_fail():
    dic = Dictionary()
    dic.args = {}

    assert not dic.check_arguments()

    dic.args = {'random': [1, 2, 3]}

    assert not dic.check_arguments()

    dic.args = {'dictionary': ['./tests/modules/search/dictionaries/nonexistentfile_dictionary.txt']}

    try:
        assert dic.check_arguments()
    except SystemExit:
        assert True

def test_data_collection():
    dic = Dictionary()
    dic.args = {
        'dictionary': [
            './tests/modules/search/dictionaries/dictionary1.txt',
            './tests/modules/search/dictionaries/dictionary2.txt'
        ]
    }

    assert dic.check_arguments()

    dic.files = [
        './tests/modules/search/dictionary_mocks/test1.sqlite',
        './tests/modules/search/dictionary_mocks/empty'
    ]

    dic.do_filter_files()

    assert len(dic.data) == 1
    assert list(dic.data)[0] == './tests/modules/search/dictionary_mocks/test1.sqlite'
    assert dic.data['./tests/modules/search/dictionary_mocks/test1.sqlite'].sort() == ['stash', 'thesis', 'test', 'object'].sort()

    dic.files.append('./tests/modules/search/dictionary_mocks/nonexistentfile')

    try:
        dic.do_filter_files()
        assert False
    except SystemExit:
        assert True

def test_dict_values():
    dic = Dictionary()
    assert len(dic.description()) > 0
    assert dic.is_filter_files()
    assert dic.check()
