import DEFCOM._DefComParser as dc
import unittest

class TestLoader(unittest.TestCase):
    def testLoad(self):
        print("Loading Config File")
        loaded = dc.loadConfFile("test/testConf.defcom")

        

