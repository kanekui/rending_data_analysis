import abc
from RendingDTO import RendingDataSet


class IExecutable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, dto: RendingDataSet) -> RendingDataSet:
        raise NotImplementedError()
