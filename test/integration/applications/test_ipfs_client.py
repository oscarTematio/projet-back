from unittest import TestCase

from app.core.ipfs_client import IpfsClient
import config

class IpfsClientTestCase(TestCase):

    def setUp(self):
        self.ipfs_client = IpfsClient(config)

    def test_get_json_content(self):
        content = self.ipfs_client.get_json_content("/ipns/QmWuDFnb6QUKXFApPAyZYhBAjdec1hBamnkFjT5gAiJwUL")

        self.assertTrue("string" in content)
        self.assertEqual("Hello world!", content["string"])

