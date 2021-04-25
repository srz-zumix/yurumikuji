#
# help
#
help: ## show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e 's/^GNUmakefile://' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: yurumikuji/*.py ## install self
	python setup.py install

install-test-deps: ## install test dependencies
	pip install -e.[test]

test: install ## commands test
	kamidana --additionals=yurumikuji.yurumikuji sample/profile.j2

info:
	kamidana -a=yurumikuji.yurumikuji --list-info

pytest: ## python test
	python setup.py test

tox: install-test-deps
	tox .

flake8: install-test-deps
	tox -e flake8 .

docker:
	docker run -it --rm -v ${PWD}:/work -w /work python:3.8-alpine sh
	# apk add make
