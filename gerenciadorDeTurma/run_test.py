import unittest
import os

def load_test():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='*_test.py')
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_test())
