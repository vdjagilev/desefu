from kernel.module_chain import ModuleChain
from kernel.output import Output
from kernel.kernel import Kernel
import sys
import ruamel.yaml
import os
import hashlib

from modules import AbstractModule


class Config:
    def __init__(self, config_file, evidence_folder):
        self.config_file = config_file
        self.config_file_sha256 = None
        self.evidence_folder = evidence_folder
        self.files_count_initial = 0
        self.module_chain = []
        self.author = None
        self.meta = None

        try:
            self.file_resource = open(config_file, 'r')
        except:
            Output.err("Failed to open config file \"%s\", unexpected error: \"%s\"" % (config_file, sys.exc_info()[0]))
            Kernel.end()

        try:
            if not os.path.isdir(evidence_folder):
                Output.err("Provided evidence folder \"%s\" is not a folder or does not exists" % evidence_folder)
                Kernel.end()
        except PermissionError:
            Output.err("There is no permission reading directory \"%s\"" % evidence_folder)
            Kernel.end()

    """
    Get module chain list, for each search record
    """
    def analyze(self) -> list:
        Output.do("Starting config file analysis")

        read_data = self.file_resource.read()

        try:
            config = ruamel.yaml.load(read_data, ruamel.yaml.RoundTripLoader)
        except:
            Output.err("Could not parse config file due to error: %s" % sys.exc_info()[0])
            Output.log(sys.exc_info())
            Kernel.end()

        # After config file has been loaded
        self.file_resource.close()

        # Print hash file of the config file
        sha256 = hashlib.sha256(open(self.config_file, 'rb').read()).hexdigest()
        self.config_file_sha256 = sha256
        Output.do("Config file SHA256: %s" % sha256)

        try:
            self.author = config['author']
        except KeyError:
            Output.err("Missing \"author\" value in config file")
            Kernel.end()

        # Meta key is optional
        try:
            self.meta = config['meta']
        except KeyError:
            pass

        Output.do("Author: %s" % self.author)

        mod_chain_list = []

        evidence_files = []
        Output.do("Starting evidence folder scan")
        for root, dir, files in os.walk(self.evidence_folder):
            for file in files:
                evidence_files.append(os.path.join(root, file))

        self.files_count_initial = len(evidence_files)
        Output.do("Total amount of files: %d" % len(evidence_files))

        for record_id in config['search']:
            mod_chain_list.append(Config.get_chain(record_id, evidence_files, config['search'][record_id]))

        return mod_chain_list

    @staticmethod
    def get_chain(chain_id: str, files: list, mod_list_config: list) -> ModuleChain:
        chain = ModuleChain()
        chain.id = chain_id
        chain.files = files

        for mod_record in mod_list_config:
            mod = Config.get_module(mod_record)
            chain.modules.append(mod)

        return chain

    @staticmethod
    def get_module(module_config) -> AbstractModule:
        mod = None
        Output.log("Analyzing module: %s" % module_config['mod'])

        try:
            mod = Kernel.get_module('modules', module_config['mod'])
            mod_check = mod.check()

            if not mod_check:
                Output.err("Module check has failed.")
                Kernel.end()

            try:
                args = module_config['args']
            except KeyError:
                args = []

            extract_option = False

            try:
                module_config['extract']
                extract_option = True
            except KeyError:
                extract_option = False

            if not mod.is_extract_data() and extract_option:
                Output.err("Module \"%s\" cannot have \"extract\" option")
                Kernel.end()

            if extract_option:
                mod.extract = module_config['extract']

            mod.args = args
            mod_check_args = mod.check_arguments()

            if not mod_check_args:
                Output.err("Error, arguments check have not been passed")
                Kernel.end()

        except (SystemError, AttributeError) as e:
            Output.err("Could not import module \"%s\" due to errors." % module_config['mod'])
            Output.log(e)
            Kernel.end()

        try:
            module_config['sub']
            sub_exists = True
        except KeyError:
            sub_exists = False

        if sub_exists:
            sub_list = module_config['sub']
            Output.log("Analyzing submodule of \"%s\"" % module_config['mod'])
            chain = Config.get_chain("[sub[%s]]" % (module_config['mod']), [], sub_list)
            mod.module_chain = chain
        else:
            Output.log("No submodules detected")

        return mod

    def close(self):
        if self.file_resource:
            self.file_resource.close()
