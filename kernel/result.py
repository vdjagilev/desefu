from kernel.config import Config
import jsonpickle

class Result:
    def __init__(self, config: Config):
        self.config = config
        self.files_count = 0
        self.config = {
            "file": config.config_file,
            "sha256": config.config_file_sha256
        }
        self.meta = config.meta
        self.author = config.author
        self.evidence_folder = config.evidence_folder
        self.files_count = config.files_count_initial

        self.result = []

    def get_json(self):
        return jsonpickle.encode(self.__dict__)
