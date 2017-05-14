from kernel.kernel import Kernel
from modules import AbstractModule
from kernel.config import Config
from kernel.result import Result
from kernel.module_chain import ModuleChain
import glob
import os
import json

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

def test_check():
    Kernel.check("modules")

def test_main_exec_search():
    config = Config('./examples/phone_msg.yml', './tests/modules/file/extension_mocks')
    result = Result(config)

    Kernel.result = result

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

    data = Kernel.result.result[0]

    assert data['module_chain_id'] == 'abcetc'
    assert len(data['modules']) == 1
    assert data['modules'][0]['mod'] == 'file.Extension'
    assert data['modules'][0]['files_count'] == 1
    assert len(data['modules'][0]['files']) == 1
