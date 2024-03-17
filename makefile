include .env
export

run:
	python main.py

migrate:
	atlas schema apply --url "mysql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}" --to "file://schema.hcl"