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
    

class Transformer(ABC):
    """Abstract base class to define transformation behaviour.
    
    ABC simplifies the creation of new transformers (eg., Dask or Apache Spark)
    """
    @abstractmethod
    def read_records(self):
        pass

    @abstractmethod
    def summarize(self):
        pass