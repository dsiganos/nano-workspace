TAG := dsiganos/nanoworkspace:1.0

shell:
	docker run -it $(TAG) bash

rootshell:
	docker run -u 0 -it $(TAG) bash

build:
	docker build -t $(TAG) .

.PHONY: default shell build
