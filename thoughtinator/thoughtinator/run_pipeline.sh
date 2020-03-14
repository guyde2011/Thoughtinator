
python -m thoughtinator.server run-server -h '127.0.0.1' -p 8000 'rabbitmq://127.0.0.1:5672' &
python -m thoughtinator.saver run-saver 'mongodb://127.0.0.1:8081' 'rabbitmq://127.0.0.1:5672' &