# Test commands
test_backend:
	docker-compose run --rm backend python3 manage.py test
	docker-compose run --rm backend pylint apps

test_frontend:
	docker-compose run --rm frontend node_modules/.bin/ng test --single-run

test_all: test_backend test_frontend


# Lint commands
lint_backend:
	docker-compose run --rm backend /bin/bash -c \
	"echo -e '\n\nRunning pycodestyle...';\
	pycodestyle --exclude='apps/volontulo/migrations/*,node_modules,.ropeproject' .;\
	echo -e '\nRunning pylint...';\
	pylint apps;"

lint_frontend:
	docker-compose run --rm frontend node_modules/.bin/ng lint

lint_all: lint_backend lint_frontend


# Docker commands
docker_remove_containers:
	docker rm $$(docker ps -qa --filter name='volontulo_*')

docker_remove_images:
	docker rmi $$(docker images -qa --filter reference='*/volontulo*')

docker_remove_all: docker_remove_containers docker_remove_images


# Other commands
populate_database:
	docker-compose run --rm backend python3 manage.py populate_database
