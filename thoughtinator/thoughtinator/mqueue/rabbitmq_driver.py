from ._rabbitmq import Connection as _Connection
from typing import Iterable as _Iterable


class _RabbitMQDriver:

    def __init__(self, host, port):
        self._host = host
        self._port = port

    @property
    def connection(self):
        return _Connection(self._host, self._port)

    def publish_data(self, data: str, exchange: str):
        with self.connection as channel:
            channel.exchange_declare(exchange)
            channel.basic_publish(exchange, '', data)

    def publish_work(self, data: str, exchange: str, route: str):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'fanout')
            channel.basic_publish(exchange, route, data)

    def consume_work(self, handler, *, exchange: str, route: str):
        with self.connection as channel:
            channel.exchange_declare(exchange, 'fanout')

            queue = channel.queue_declare(route).method.queue
            channel.queue_bind(exchange, queue, route)

            def callback(channel, method, props, body):
                handler(method.routing_key, body)
                channel.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            channel.start_consuming()

    def consume_data(self, handler, *, exchange: str, routes: _Iterable[str]):
        with self.connection as channel:
            queue = channel.queue_declare(queue='').method.queue
            for route in routes:
                channel.queue_bind(exchange, queue, route)

            def callback(channel, method, props, body):
                handler(method.routing_key, body)
                channel.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=queue, on_message_callback=callback)
            channel.start_consuming()


rabbitmq = _RabbitMQDriver
