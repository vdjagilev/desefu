from kernel.output import Output, OutputResult
from kernel.kernel import Kernel
import sys
import ruamel.yaml

class Config:

    def __init__(self, config_file):
        self.config_file = config_file

        try:
            self.file_resource = open(config_file, 'r')
        except:
            Output.do("Failed to open config file \"%s\", unexpected error: \"%s\"" % (config_file, sys.exc_info()[0]), OutputResult.Fail)
            Kernel.end()

        Output.do("File was successfully opened", OutputResult.OK)

    def analyze(self):
        Output.do("Starting config file analysis")
        
        read_data = self.file_resource.read();
        config = ruamel.yaml.load(read_data, ruamel.yaml.RoundTripLoader)
        
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
                analysis = self.analyze_module(module)
        
        return analysis

    def analyze_module(self, module_config):
        analysis = False
        Output.log("Analyzing module: %s" % module_config['mod'])
        Output.log("Analyzing arguments: %s" % module_config['args'])
        
        try:
            module_config['sub']
            Output.log("Analyzing submodule")

            for sub in module_config['sub']:
                analysis = self.analyze_module(sub)
        except KeyError:
            Output.log("No submodules detected")

        return analysis

    def close(self):
        if self.file_resource:
            self.file_resource.close()
