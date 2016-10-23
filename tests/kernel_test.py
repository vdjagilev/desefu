from kernel.kernel import Kernel
from modules import AbstractModule
from kernel.module_chain import ModuleChain
import glob
import os

def test_get_module():
    mod = Kernel.get_module('modules', 'file.Extension')

    assert isinstance(mod, AbstractModule)

    try:
        mod = Kernel.get_module('modules', 'not.Exists')
    except SystemExit:
        assert True

    try:
        mod = Kernel.get_module('tests.modules', 'file.WrongModule')
    except KeyError:
        assert True

def test_main_exec_search():
    remove_files = glob.glob('abcetc_*.json')

    for rf in remove_files:
        os.remove(rf)

    mc = ModuleChain()
    mc.id = "abcetc"
    mc.files = [
        './tests/modules/file/extension_mocks/database.sqlite',
        './tests/modules/file/extension_mocks/database2.db'
    ]

    module = Kernel.get_module('modules', 'file.Extension')
    module.files = mc.files
    module.args = ['db']

    mc.modules.append(module)

    Kernel.exec_search([mc])

    files = glob.glob('abcetc_*.json')

    assert len(files) == 1
