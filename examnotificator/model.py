from abc import ABC

from pydantic import BaseModel, ValidationError, validator


class Exam(BaseModel, ABC):
    name: str

    class Config:
        frozen=True
        anystr_strip_whitespace=True


class GradedExam(Exam):
    """ An exam with a grade in range 1,0..5,0. Considered passed if grade <= 4.0 """
    grade: float

    @validator('grade')
    def grade_in_valid_range(cls, grade):
        if grade < 1.0 or grade > 5.0:
            raise ValueError(f'grade has to be in 1,0..5,0: "{grade}"')
        return grade

    @property
    def passed(self):
        if self.grade <= 4.0:
            return True
        return False


class OnlyPassExam(Exam):
    """ An exam that one can pass or not but is not graded """
    passed: bool

    def __str__(self):
        if self.passed:
            return f'{self.name}: passed'
        return f'{self.name}: not passed'


_exam_types = (
    GradedExam, 
    OnlyPassExam
)

def exam_factory(**kwargs):
    for exam_type in _exam_types:
        try:
            return exam_type.parse_obj(kwargs)
        except ValidationError as e:
            continue

    raise ValueError(f'could not parse Exam from data: {kwargs}')
