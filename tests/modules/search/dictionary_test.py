# Dictionary unit test file
from modules.search.Dictionary import Dictionary

def test_check_arguments():
    dic = Dictionary()
    dic.args = [
        './tests/modules/search/dictionaries/dictionary1.txt',
        './tests/modules/search/dictionaries/dictionary2.txt'
    ]


    assert dic.check_arguments()
    assert len(dic.args) == len(dic.dict_words)

    dic1 = dic.dict_words['./tests/modules/search/dictionaries/dictionary1.txt']
    dic2 = dic.dict_words['./tests/modules/search/dictionaries/dictionary2.txt']

    assert dic1[0] == 'a simple'
    assert dic2[0] == 'testing'
    assert dic1[3] == 'thesis'
    assert dic2[3] == 'hello'
