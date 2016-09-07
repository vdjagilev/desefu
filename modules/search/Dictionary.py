from kernel.output import Output, OutputResult

class Dictionary:
    def check(self):
        return True

    def check_arguments(self, args):
        if len(args) == 0:
            Output.do("Dictionary: Arguments should contain at least one dictionary")
            return False

        return True
