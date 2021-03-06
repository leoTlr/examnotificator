import unittest

from examnotificator.repo import ShelveRepo
from examnotificator.model import Exam

from tempfile import TemporaryDirectory
from uuid import uuid4
from os import remove
from pathlib import Path


class TestShelveRepo(unittest.TestCase):

    def setUp(self):
        self.td = TemporaryDirectory()
        self.tf = Path(self.td.name) / Path('tmptstshelf')

    def tearDown(self) -> None:
        self.td.cleanup()

    def test_non_existent_file_creates_empty_shelf(self):

        rnd_file = Path(str(uuid4()))
        sr = ShelveRepo(rnd_file)

        self.assertTrue(rnd_file.exists)
        self.assertSetEqual(set(), sr.get())

        remove(rnd_file)

    def test_add_one(self):

        sr = ShelveRepo(self.tf)
        exam = Exam('sth', '1.0')
        sr.save({exam})
        
        self.assertSetEqual({exam}, sr.get())
            

    def test_add_multiple_at_once(self):
        sr = ShelveRepo(self.tf)
        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        sr.save(exams)

        self.assertSetEqual(exams, sr.get())
    
    def test_add_one_update_one(self):
        sr = ShelveRepo(self.tf)
        exam_0 = Exam('sth', '1.0')
        sr.save({exam_0})

        exam_1 = Exam('abc', '1.3')
        sr.save({exam_1})
        
        self.assertSetEqual({exam_0, exam_1}, sr.get())

    def test_add_one_update_multiple(self):
        sr = ShelveRepo(self.tf)
        exam_0 = Exam('hdk', '5.0')
        sr.save({exam_0})

        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        sr.save(exams)

        self.assertSetEqual(exams | {exam_0}, sr.get())

    def test_add_one_override(self):
        sr = ShelveRepo(self.tf)
        exam_0 = Exam('sth', '1.0')
        sr.save({exam_0})

        exam_1 = Exam('abc', '1.3')
        sr.save({exam_1}, override=True)
        
        self.assertSetEqual({exam_1}, sr.get())



