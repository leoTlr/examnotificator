from examnotificator.notification.strategies import FetchCompareStrategy, AllExamsStrategy
from examnotificator.repo import MemRepo
from examnotificator.model import Exam
from examnotificator.fetching.builtin import DummyFetcher

from unittest import TestCase


class TestAllExamsStrategy(TestCase):
    
    def test_multiple(self):
        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        
        strat = AllExamsStrategy(MemRepo(exams))

        self.assertSetEqual(exams, strat.process())

    def test_single(self):
        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}

        strat = AllExamsStrategy(MemRepo(exams))

        self.assertSetEqual(exams, strat.process())


class TestFetchCompareStrategy(TestCase):

    def test_single_new_on_empty(self):
        exams_before = set()
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_empty(self):
        exams_before = set()
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_single_new_on_filled_single(self):
        exams_before = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
        ]}
        exams_new = exams_after.difference(exams_before)

        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_single_new_on_filled_multiple(self):
        exams_before = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
        ]}
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
        ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_filled_single(self):
        exams_before = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
        ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())

    def test_multiple_new_on_filled_multiple(self):
        exams_before = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
        ]}
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        exams_new = exams_after.difference(exams_before)
        
        strat = FetchCompareStrategy(MemRepo(exams_before), DummyFetcher(exams_after))
        self.assertSetEqual(exams_new, strat.process())