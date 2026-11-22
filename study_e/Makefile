.PHONY: test test-full docker-test docker-test-full
PY=python3 -I -W error::ResourceWarning
test:
	$(PY) -m unittest discover -s tests -t .
test-full:
	STUDY_E_FULL=1 $(PY) -m unittest discover -s tests -t .
docker-test:
	docker compose run --rm test
docker-test-full:
	docker compose run --rm test-full
