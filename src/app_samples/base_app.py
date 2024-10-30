from abc import ABC, abstractmethod

class BaseLanggraphApp(ABC):

    @abstractmethod
    def create_graph(self):
        pass
