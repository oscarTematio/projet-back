from unittest import TestCase

import os
import json

class AbstractUnitTest(TestCase):

    def load_json_resource(self, file):
        # given
        path = os.path.dirname(__file__)

        fileName = path + "/resources/"+file
        with open(fileName, 'r') as content_file:
            content = content_file.read()

            return json.loads(content)

