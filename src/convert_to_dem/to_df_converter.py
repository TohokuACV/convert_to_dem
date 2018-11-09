from abc import *

class ToDfConverter:
    @abstractmethod
    def read(self, *args, **kwargs):
        """
        Reads in some stuff and convert to a pandas DataFrame
        :return: pandas DataFrame
        """
        raise NotImplementedError()
