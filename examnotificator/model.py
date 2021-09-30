from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen = True)
class Exam:
    name: str
    grade: Optional[str] = field(default = None)
    passed: Optional[bool] = field(default = None)

    def __str__(self) -> str:
        retval = self.name
        if self.grade:
            retval += f', {self.grade}'
        if self.passed is not None:
            if self.passed == True:
                retval += f', passed'
            else:
                retval += ', failed'
        return retval
