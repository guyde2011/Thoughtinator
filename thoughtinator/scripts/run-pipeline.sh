#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	echo '[Thoughtinator] loading ...'
	sudo docker-compose up -d
	up=$(HEAD 127.0.0.1:5000/users | grep '200\ OK' | wc -l)
	while [ "$up" -eq "0" ]; do
		up=$(HEAD 127.0.0.1:5000/users | grep '200\ OK' | wc -l)
		sleep 1
	done
	up=$(HEAD 127.0.0.1:8080 | grep '200\ OK' | wc -l)
	while [ "$up" -eq "0" ]; do
		up=$(HEAD 127.0.0.1:8080 | grep '200\ OK' | wc -l)
		sleep 1
	done
	echo '[Thoughtinator] Successfully loaded!'
}


main "$@"