try:
    import unittest2 as unittest
except:
    import unittest
import os

def test_suite():
    test_loader = unittest.TestLoader()
    # test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('./tests')
    return test_suite
