from examnotificator.notification.strategies import FetchCompareStrategy, AllExamsStrategy
from examnotificator.repo import MemRepo
from examnotificator.model import Exam, exam_factory
from examnotificator.fetching.builtin import DummyFetcher

from unittest import TestCase
from configurator import Config


class TestAllExamsStrategy(TestCase):
    
    def test_multiple(self):
        exams = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
                (2.0, 'def'), 
                (3.0, '3.0'), 
                (4.0, 'abc')
            ]}
        strat = AllExamsStrategy(MemRepo(exams))

        self.assertSetEqual(exams, strat.process())

    def test_single(self):
        exams = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
            ]}
        strat = AllExamsStrategy(MemRepo(exams))

        self.assertSetEqual(exams, strat.process())


class TestFetchCompareStrategy(TestCase):

    def test_single_new_on_empty(self):
        exams_before = set()
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
            ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_empty(self):
        exams_before = set()
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
                (2.0, 'def'), 
                (3.0, '3.0'), 
                (4.0, 'abc')
            ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_single_new_on_filled_single(self):
        exams_before = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
            ]}
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'), 
                (1.7, 'lll'), 
            ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_single_new_on_filled_multiple(self):
        exams_before = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
                (1.7, 'lll'),
            ]}
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
                (1.7, 'lll'),
                (2.3, 'soi'), 
            ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_filled_single(self):
        exams_before = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
            ]}
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
                (2.3, 'soi'),
                (1.7, 'lll'), 
            ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_filled_multiple(self):
        exams_before = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
                (3.3, 'ghj')
            ]}
        exams_after = { 
            exam_factory(name=_name, grade=_grade)
            for _grade, _name in [
                (1.0, 'sth'),
                (3.3, 'ghj'),
                (2.3, 'soi'),
                (1.7, 'lll'), 
            ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(Config(), exams_after))
        self.assertSetEqual(exams_new, strat.process())