import abc

class MarketData(abc.ABC):

    @abc.abstractmethod
    def get_candles(self):
        pass
