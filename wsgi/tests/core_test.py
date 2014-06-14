import sys

sys.path.append("../")
sys.path.append("../../")

import unittest
import random

import zombietweet


class ZombietweetTest(unittest.TestCase):

    # making test names
    db_testname = "zombietweet_"
    db_testname += str(random.randint(1000, 9999))

    def setUp(self):
        self.app = zombietweet.app.test_client()

    # common tests
    def test_version(self):
        """ Testing basic call that get current app version """
        res = self.app.get('/version')

        assert res.status_code == 200


if __name__ == '__main__':
    unittest.main()
