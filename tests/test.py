import sys
from yurumikuji.yurumikuji import slack_users_name


try:
    import unittest2 as unittest
except:
    import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class yurumikuji_test_base(unittest.TestCase):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture
        return super(yurumikuji_test_base, self).setUp()

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.capture.close()
        return super(yurumikuji_test_base, self).tearDown()

    def stdoout(self):
        value = self.capture.getvalue()
        return value


class test_yurumikuji(yurumikuji_test_base):

    def setUp(self):
        return super(test_yurumikuji, self).setUp()

    def tearDown(self):
        return super(test_yurumikuji, self).tearDown()

    def test_simple(self):
        self.assertNotEqual("", slack_users_name())


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
