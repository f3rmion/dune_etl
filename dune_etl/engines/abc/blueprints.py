from abc import ABC
from abc import abstractmethod


class Extractor(ABC):
    """Abstract base class to define extraction behaviour into a staging area.
    
    ABC simplifies the creation of new extractors to change staging areas quickly (eg., AWS S3).
    """
    @abstractmethod
    def query_records(self):
        pass

    @abstractmethod
    def store_records(self):
        pass
    