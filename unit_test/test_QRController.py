import os
import unittest.mock
from pathlib import Path
from unittest import TestCase

from qrmvc.QRController import QRController
from qrmvc.QRView import QRView


class TestQRController(TestCase):
    def setUp(self) -> None:
        self.ctrl = unittest.mock.Mock(QRController)
        self.ctrl.input_forms = {0: {"code_format": "{0}"}, 1: {"code_format": "{0}, {1}"},
                                 2: {"code_format": "{0}, {1}, {2}"}}
        self.ctrl.form_types = [0, 1, 2, 3]
        self.ctrl.temp_picture = "x"
        self.ctrl.view = unittest.mock.Mock(QRView)

    def tearDown(self) -> None:
        os.remove(Path(self.ctrl.temp_picture))

    def test_generate(self):
        try:
            QRController.generate(self.ctrl, None, 3)
            self.fail()
        except KeyError:
            pass

        try:
            QRController.generate(self.ctrl, None, 4)
            self.fail()
        except AssertionError:
            pass

        try:
            QRController.generate(self.ctrl, {"1": 1}, 0)
        except AttributeError:
            self.fail()

        try:
            QRController.generate(self.ctrl, {"1": 1, "2": 2}, 1)
        except AttributeError:
            self.fail()
        try:
            QRController.generate(self.ctrl, {"1": 1, "2": 2}, 0)
            self.fail()
        except AttributeError:
            pass
