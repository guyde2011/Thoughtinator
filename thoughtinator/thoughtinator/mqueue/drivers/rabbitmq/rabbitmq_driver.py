from typing import Iterable
from pika import BlockingConnection, ConnectionParameters


class RabbitConnection:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._connection = None

    def __enter__(self):
        self._connection = BlockingConnection(
            ConnectionParameters(host=self._host, port=self._port))
        return self._connection.channel()

    def __exit__(self, cls, exception, tb):
        self._connection.close()


class RabbitMQDriver:

    def __init__(self, host, port):
        self._host = host
        self._port = port

    @property
    def connection(self) -> RabbitConnection:
        return RabbitConnection(self._host, self._port)

    def publish_data(self, data: str, exchange: str, route: str):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'direct')
            channel.basic_publish(exchange, route, data)

    def publish_work(self, data: str, exchange: str):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'fanout')
            channel.basic_publish(exchange, '', data)

    def consume_work(self, handler, exchange: str, route: str):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'fanout')

            queue = channel.queue_declare(route).method.queue
            channel.queue_bind(queue, exchange, route)

            def callback(channel, method, props, body):
                handler(method.routing_key, body)
                channel.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            channel.start_consuming()

    def consume_data(self, handler, exchange: str, routes: Iterable[str]):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'direct')
            for route in routes:
                queue = channel.queue_declare(queue='').method.queue
                channel.queue_bind(queue, exchange, routing_key=route)

                def callback(channel, method, props, body):
                    handler(method.routing_key, body)
                    channel.basic_ack(delivery_tag=method.delivery_tag)

                channel.basic_consume(queue=queue,
                                      on_message_callback=callback)
            channel.start_consuming()
