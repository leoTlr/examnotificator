from examnotificator.repo import MemRepo
from examnotificator.model import Exam
from examnotificator.fetching.builtin import DummyFetcher
from examnotificator.notification.builtin import NoOpNotificator
from examnotificator.use_cases import NotifyNew, NotifySaved

from unittest import TestCase
from unittest.mock import Mock


class TestNotifySaved(TestCase):

    def setUp(self) -> None:
        self.notificator = Mock(NoOpNotificator)

    def test_multiple(self):
        use_case = NotifySaved()
        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
                ('def', '2.0'), 
                ('eoa', '3.0'), 
                ('abc', '4.0')
        ]}
        
        use_case.execute(MemRepo(exams), DummyFetcher(), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()


    def test_single(self):
        use_case = NotifySaved()
        exams = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}
        
        use_case.execute(MemRepo(exams), DummyFetcher(), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()


class TestFetchCompareStrategy(TestCase):

    def setUp(self) -> None:
        self.notificator = Mock(NoOpNotificator)

    def test_single_new_on_empty(self):
        exams_before = set()
        exams_after = {
            Exam(name, grade) for name, grade in [
                ('sth', '1.0'), 
        ]}
        exams_new = exams_after.difference(exams_before)

        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()

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

        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()

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

        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()

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
        
        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()

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
        
        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()

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
        
        use_case = NotifyNew()
        use_case.execute(MemRepo(exams_before), DummyFetcher(exams_new), [self.notificator])

        self.notificator.add_exams.assert_called()
        exams_added_to_notificator = set()
        for call in self.notificator.add_exams.call_args_list:
            exams_added_to_notificator.update(call.args[0])
        self.assertSetEqual(exams_new, exams_added_to_notificator)
        self.notificator.execute.assert_called_once()