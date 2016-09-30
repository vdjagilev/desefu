from kernel.module_chain import ModuleChain
from kernel.output import Output, OutputResult
from kernel.kernel import Kernel
import sys
import ruamel.yaml
import importlib
import os

from modules import AbstractModule


class Config:
    def __init__(self, config_file, evidence_folder):
        self.config_file = config_file
        self.evidence_folder = evidence_folder
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

        try:
            evidence_files = []
            Output.do("Starting evidence folder scan")
            for root, dir, files in os.walk(self.evidence_folder):
                for file in files:
                    evidence_files.append(os.path.join(root, file))

            Output.do("Total amount of files: %d" % len(evidence_files))

            for record_id in config['search']:
                mod_chain = ModuleChain()
                mod_chain.files = evidence_files
                mod_chain.id = record_id

                Output.log("Analyzing record_id: %s" % record_id)
                for module_record in config['search'][record_id]:
                    mod = self.analyze_module(module_record, 'modules')

                    mod.module_chain = mod_chain
                    mod_chain.modules.append(mod)

                mod_chain_list.append(mod_chain)
        except KeyError:
            Output.err("Error getting \"search\" entry from config file")
            Kernel.end()
        except TypeError:
            Output.err("Search entry does not contain any values")
            Kernel.end()

        return mod_chain_list

    def analyze_module(self, module_config, module_type) -> AbstractModule:
        mod = None
        Output.log("Analyzing module: %s" % module_config['mod'])

        try:
            mod = Kernel.get_module(module_type, module_config['mod'])
            mod_check = mod.check()

            if not mod_check:
                Output.err("Module check has failed.")
                Kernel.end()

            args = []
            try:
                args = module_config['args']
            except KeyError:
                pass

            Output.log("Analyzing arguments: %s" % module_config['args'])
            mod_check_args = mod.check_arguments(args)

            if not mod_check_args:
                Output.err("Error, arguments check have not been passed")
                Kernel.end()

            mod.args = args

        except (SystemError, AttributeError) as e:
            Output.err("Could not import module \"%s\" due to errors." % module_config['mod'])
            Output.log(e)
            Kernel.end()

        try:
            sub_list = module_config['sub']
            Output.log("Analyzing submodule")
            
            if len(sub_list) > 0:
                sibling_module_chain = ModuleChain()

                for sub in sub_list:
                    sub_mod = None
                    sub_mod = self.analyze_module(sub, module_type)

                    sub_mod.parent_module = mod
                    sub_mod.is_sub_module = True

                    # Module chain of "sub" section should have a list of modules
                    sibling_module_chain.modules.append(sub_mod)

                    # Each module should have reference, 
                    sub_mod.module_chain = sibling_module_chain

                mod.sibling_module_chain = sibling_module_chain
                
                return sub_mod
        except KeyError:
            Output.log("No submodules detected")
        
        return mod

    def close(self):
        if self.file_resource:
            self.file_resource.close()
