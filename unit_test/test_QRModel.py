import json
import os
import unittest.mock
from pathlib import Path
from unittest import TestCase

from qrmvc.QRModel import QRModel

CODE_TYPES_DIR = os.path.join("..", "code_types")

TEST_FORM_FILENAME = "test_form"


class TestQRModel(TestCase):

    def setUp(self) -> None:
        pass
        self.model = unittest.mock.Mock(QRModel)
        self.model.code_folder = CODE_TYPES_DIR

    def test_save_form(self):
        test_form = {"form": 1, "type": 2}
        QRModel.save_form(TEST_FORM_FILENAME, test_form)

        loaded_test_form = QRModel.load_form(TEST_FORM_FILENAME)

        self.assertEqual(tuple(test_form.values()), loaded_test_form)

        os.remove(Path(TEST_FORM_FILENAME))

    def test_get_code_files(self):
        code_files = os.listdir(CODE_TYPES_DIR)

        code_jsons = QRModel.get_code_files(self.model)

        for code_json in code_jsons:
            print(code_json)
            if code_json not in code_files:
                self.fail(f"{code_json} not found")

    def test_load_codes(self):
        code_jsons = QRModel.get_code_files(self.model)
        self.model.get_code_files = unittest.mock.Mock(return_value=code_jsons)
        global real_code
        fake_code = {'notitle': 'nope'}

        with open(os.path.join(CODE_TYPES_DIR, code_jsons[0])) as code:
            real_code = json.load(code)

        codes = QRModel.load_codes(self.model)
        if real_code not in codes.values():
            self.fail()

        if fake_code in codes.values():
            self.fail()

