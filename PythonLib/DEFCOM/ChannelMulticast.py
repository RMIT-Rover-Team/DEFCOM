from . import _DefComParser

class MulticastSender:
    def __init__(self, defcomFilePath: str):
        self._config = _DefComParser.loadConfFile(defcomFilePath)

    