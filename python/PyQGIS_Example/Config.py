
import os


class ServerConfig:
    def __init__(self):
        current_path = os.path.abspath(__file__)
        self.rootPath=os.path.dirname(os.path.dirname(current_path))

globalConfig = ServerConfig()