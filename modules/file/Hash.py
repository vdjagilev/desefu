from modules import AbstractModule
from kernel.output import Output
import hashlib


class Hash(AbstractModule):
    def is_collect_data(self) -> bool:
        return True

    def check(self):
        return True

    def description(self) -> str:
        return "A module which collects data about file hashes"

    def check_arguments(self):
        allowed_values = [
            'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'
        ]

        if len(self.args) == 0:
            self.args = ['md5', 'sha1', 'sha256']
            Output.do("Will calculate only default list of hashes \"%s\"" % self.args)

        for hash_name in self.args:
            if hash_name not in allowed_values:
                Output.err("Unknown hash \"%s\"" % hash_name)
                return False

        return True

    def do_collect_data(self):
        for f in self.files:
            self.data[f] = []

            for h in self.args:
                self.data[f].append((h, self.get_file_hash(f, h)))

    def get_file_hash(self, file_path, hash_name):
        hash_func = None

        if hash_name == 'md5':
            hash_func = hashlib.md5()
        elif hash_name == 'sha1':
            hash_func = hashlib.sha1()
        elif hash_name == 'sha224':
            hash_func = hashlib.sha224()
        elif hash_name == 'sha256':
            hash_func = hashlib.sha256()
        elif hash_name == 'sha384':
            hash_func = hashlib.sha384()
        elif hash_name == 'sha512':
            hash_func = hashlib.sha512()

        with open(file_path, 'rb') as f:
            for data_chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(data_chunk)

        return hash_func.hexdigest()