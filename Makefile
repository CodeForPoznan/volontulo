make test_backend:
	docker-compose run --rm backend python3 manage.py test && pylint apps

make test_frontend:
	docker-compose run --rm frontend node_modules/.bin/ng test --single-run

make test_all:
	make test_backend
	make test_frontend
