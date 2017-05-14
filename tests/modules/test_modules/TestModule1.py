from modules import AbstractModule


class TestModule1(AbstractModule):
    def check_arguments(self):
        return True

    def check(self):
        return False
