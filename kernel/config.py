from kernel.output import Output, OutputResult
from kernel.kernel import Kernel
import sys
import ruamel.yaml
import importlib
import os


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
            Output.do("Failed to open config file \"%s\", unexpected error: \"%s\"" % (config_file, sys.exc_info()[0]),
                      OutputResult.Error)
            Kernel.end()

        try:
            if not os.path.isdir(evidence_folder):
                Output.do("Provided evidence folder \"%s\" is not a folder or does not exists" % evidence_folder,
                          OutputResult.Error)
                Kernel.end()
        except PermissionError:
            Output.do("There is no permission reading directory \"%s\"" % evidence_folder, OutputResult.Error)
            Kernel.end()

    def analyze(self):
        Output.do("Starting config file analysis")

        read_data = self.file_resource.read()

        try:
            config = ruamel.yaml.load(read_data, ruamel.yaml.RoundTripLoader)
        except:
            Output.do("Could not parse config file due to error: %s" % sys.exc_info()[0], OutputResult.Error)
            Output.log(sys.exc_info())
            Kernel.end()

        try:
            self.author = config['author']
        except KeyError:
            Output.do("Missing \"author\" value in config file", OutputResult.Error)
            Kernel.end()

        # Meta key is optional
        try:
            self.meta = config['meta']
        except KeyError:
            pass

        Output.do("Author: %s" % self.author)

        analysis = False

        try:
            for record_id in config['search']:
                Output.log("Analyzing record_id: %s" % record_id)
                for module in config['search'][record_id]:
                    analysis = self.analyze_module(module, 'modules')
        except KeyError:
            Output.do("Error getting search entry from config file", OutputResult.Error)
            Kernel.end()
        except TypeError:
            Output.do("Search entry does not contain any values", OutputResult.Error)
            Kernel.end()

        return analysis

    def analyze_module(self, module_config, module_type):
        analysis = False
        Output.log("Analyzing module: %s" % module_config['mod'])

        try:
            mod = Kernel.get_module(module_type, module_config['mod'])
            mod_check = mod.check()

            if not mod_check:
                Kernel.end()

            args = []
            try:
                args = module_config['args']
            except KeyError:
                pass

            mod_check_args = mod.check_arguments(args)

            if not mod_check_args:
                Kernel.end()


        except (SystemError, AttributeError) as e:
            Output.do("Could not import module \"%s\" due to errors." % module_config['mod'],
                      result=OutputResult.Error)
            Output.log(e)
            Kernel.end()

        Output.log("Analyzing arguments: %s" % module_config['args'])

        try:
            module_config['sub']
            Output.log("Analyzing submodule")

            for sub in module_config['sub']:
                analysis = self.analyze_module(sub, module_type)
        except KeyError:
            Output.log("No submodules detected")

        return analysis

    def close(self):
        if self.file_resource:
            self.file_resource.close()
