#
# help
#
help: ## show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e 's/^GNUmakefile://' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: sample

setup: ## first setup
	python3 -m venv .
	./bin/pip3 install -r requirements.txt

sample:
	./bin/kamidana --additionals=./yurumikuji.py sample/profile.j2
