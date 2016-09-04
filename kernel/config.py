from kernel.output import Output, OutputResult
from kernel.kernel import Kernel
import sys
import ruamel.yaml
import importlib


class Config:
    def __init__(self, config_file):
        self.config_file = config_file

        try:
            self.file_resource = open(config_file, 'r')
        except:
            Output.do("Failed to open config file \"%s\", unexpected error: \"%s\"" % (config_file, sys.exc_info()[0]),
                      OutputResult.Error)
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

        # Starting to check for fields
        # Author, meta (optional)
        # then go for "search" field
        # analyze in loop, sub elements as well
        # while analyzing search modules do:
        # * Check their existance
        # * Check by using check() function
        # * Do check_arguments() function
        self.author = config['author']

        # Meta key is optional
        try:
            self.meta = config['meta']
        except KeyError:
            self.meta = ""

        Output.do("Author: %s" % self.author)

        analysis = False

        for record_id in config['search']:
            Output.log("Analyzing record_id: %s" % record_id)
            for module in config['search'][record_id]:
                analysis = self.analyze_module(module, 'search')

        return analysis

    def analyze_module(self, module_config, module_type):
        analysis = False
        Output.log("Analyzing module: %s" % module_config['mod'])

        try:
            mod_import = importlib.import_module(module_type + '.' + module_config['mod'])
            mod_class = getattr(mod_import, module_config['mod'])

            # Module object initialization
            mod = mod_class()

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


        except (SystemError, ImportError, AttributeError) as e:
            Output.do("Could not load module \"%s\" due to errors." % module_config['mod'],
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
