import abc
from typing import Iterator


class ResponseMapper:
    @abc.abstractmethod
    def map(self, _input: Iterator) -> list:
        pass
