import os

# Set a dummy SLACK_TOKEN so the module can be imported without a real token
os.environ.setdefault('SLACK_TOKEN', 'xoxb-test-dummy-token')

try:
    import unittest2 as unittest
except Exception:
    import unittest

from yurumikuji.yurumikuji import on_error


class test_on_error(unittest.TestCase):

    def setUp(self):
        self._original_env = os.environ.copy()

    def tearDown(self):
        # Restore original environment
        os.environ.clear()
        os.environ.update(self._original_env)

    def test_on_error_without_env_var(self):
        """on_error returns the error when SLACK_API_ERROR_RAISE is not set"""
        os.environ.pop('SLACK_API_ERROR_RAISE', None)
        e = Exception('test error')
        result = on_error(e)
        self.assertIs(result, e)

    def test_on_error_env_var_false(self):
        """on_error returns the error when SLACK_API_ERROR_RAISE=false"""
        os.environ['SLACK_API_ERROR_RAISE'] = 'false'
        e = Exception('test error')
        result = on_error(e)
        self.assertIs(result, e)

    def test_on_error_env_var_true(self):
        """on_error raises the error when SLACK_API_ERROR_RAISE=true"""
        os.environ['SLACK_API_ERROR_RAISE'] = 'true'
        e = Exception('test error')
        with self.assertRaises(Exception) as ctx:
            on_error(e)
        self.assertIs(ctx.exception, e)

    def test_on_error_env_var_true_uppercase(self):
        """on_error raises the error when SLACK_API_ERROR_RAISE=True (case insensitive)"""
        os.environ['SLACK_API_ERROR_RAISE'] = 'True'
        e = Exception('test error')
        with self.assertRaises(Exception) as ctx:
            on_error(e)
        self.assertIs(ctx.exception, e)


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
