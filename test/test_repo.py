import unittest

from examnotificator.repo import ShelveRepo
from examnotificator.model import Exam, exam_factory

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
        exam = exam_factory(grade=1.0, name='sth')
        sr.save({exam})
        
        self.assertSetEqual({exam}, sr.get())
            

    def test_add_multiple_at_once(self):
        sr = ShelveRepo(self.tf)
        exams = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
                (2.0, 'def'), 
                (3.0, '3.0'), 
                (4.0, 'abc')
            ]}
        sr.save(exams)

        self.assertSetEqual(exams, sr.get())
    
    def test_add_one_update_one(self):
        sr = ShelveRepo(self.tf)
        exam_0 = exam_factory(grade=1.0, name='sth')
        sr.save({exam_0})

        exam_1 = exam_factory(grade=1.3, name='abc')
        sr.save({exam_1})
        
        self.assertSetEqual({exam_0, exam_1}, sr.get())

    def test_add_one_update_multiple(self):
        sr = ShelveRepo(self.tf)
        exam_0 = exam_factory(grade=5.0, name='hdk')
        sr.save({exam_0})

        exams = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
                (2.0, 'def'), 
                (3.0, '3.0'), 
                (4.0, 'abc')
            ]}
        sr.save(exams)

        self.assertSetEqual(exams | {exam_0}, sr.get())

    def test_add_one_override(self):
        sr = ShelveRepo(self.tf)
        exam_0 = exam_factory(grade=1.0, name='sth')
        sr.save({exam_0})

        exam_1 = exam_factory(grade=1.3, name='abc')
        sr.save({exam_1}, override=True)
        
        self.assertSetEqual({exam_1}, sr.get())



