from kernel.config import Config
from kernel.module_chain import ModuleChain
from modules import AbstractModule


def test_get_module():
    module_config = {
        'mod': 'file.Extension',
        'args': ['db', 'etc', 'abc', ''],
        'sub': [
            {
                'mod': 'file.Extension',
                'args': ['db'],
                'sub': [
                    {
                        'mod': 'file.Extension',
                        'args': [''],
                        'sub': [
                            {
                                'mod': 'file.FileHeader',
                                'args': {
                                    'types': [['00', '00', '00']]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }

    mod = Config.get_module(module_config)
    assert isinstance(mod, AbstractModule)
    assert mod.check()
    assert mod.check_arguments()
    assert module_config['args'] == mod.args

    assert mod.module_chain
    assert isinstance(mod.module_chain.modules[0], AbstractModule)
    assert module_config['sub'][0]['args'] == mod.module_chain.modules[0].args

    mod_chain1 = mod.module_chain
    assert mod_chain1.modules[0].module_chain
    mod_chain2 = mod_chain1.modules[0].module_chain
    assert mod_chain2.modules[0].module_chain
    mod_chain3 = mod_chain2.modules[0].module_chain
    assert isinstance(mod_chain3, ModuleChain)
    assert isinstance(mod_chain3.modules[0], AbstractModule)

    file_header = mod_chain3.modules[0]

    assert {'types': [['00', '00', '00']]} == file_header.args
    assert file_header.__class__.__name__ == 'FileHeader'

def test_config_init():
    conf = Config('./examples/phone_msg.yml', './tests/config/')

    assert conf.config_file == './examples/phone_msg.yml'
    assert conf.evidence_folder == './tests/config/'

def config_test_init_fail():
    try:
        Config('./examples/nonexistent', './tests/config/')
    except SystemExit:
        assert True

    try:
        Config('./examples/phone_msg.yml', './tests/nonexistent_folder/')
    except SystemExit:
        assert True

def test_config_analyze():
    conf = Config('./examples/phone_msg.yml', './tests/config/')

    mod_chain_list = conf.analyze()

    assert mod_chain_list
    assert isinstance(mod_chain_list, list)
    assert len(mod_chain_list) > 0
    assert mod_chain_list[0]
    assert isinstance(mod_chain_list[0], ModuleChain)
    assert isinstance(mod_chain_list[0].modules[0], AbstractModule)
