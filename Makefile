GIT_SHA := $(shell git rev-parse --short HEAD)

NAME = sso-helper

docker:
	docker build . --target prod -t eu.gcr.io/xamaral/$(NAME):$(GIT_SHA) -t $(NAME):latest

push: docker
	docker push eu.gcr.io/xamaral/$(NAME):$(GIT_SHA)

docker-dev:
	docker build . --target dev -t $(NAME)-dev:latest

.PHONY: docker push docker-dev
