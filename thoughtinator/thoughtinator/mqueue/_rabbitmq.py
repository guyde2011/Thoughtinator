from pika import BlockingConnection, ConnectionParameters


class Connection:

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def __enter__(self):
        self._connection = BlockingConnection(
            ConnectionParameters(host=self._host, port=self._port))
        return self._connection.channel()

    def __exit__(self, cls, exception, tb):
        self._connection.close()
