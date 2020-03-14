export SAVE_FOLDER=/tmp/thoughtinator2
for key in 'pose' 'color_image' 'depth_image' 'feelings'
do
    python -m thoughtinator.parsers run-parser $key 'rabbitmq://127.0.0.1:5672' &
done