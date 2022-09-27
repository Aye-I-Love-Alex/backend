from abc import ABC


class ConnectionInterface(ABC):
    def find_connection(self):
        "Returns connection between first and second topics"
        pass

    def keywords(self):
        "Returns keywords on current page"
        pass
