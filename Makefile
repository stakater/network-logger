
DOCKER_ACCOUNT ?=

buildimage:
	docker build -t $(DOCKER_ACCOUNT)/network-logger .

runimage:
	docker run $(DOCKER_ACCOUNT)/network-logger

buildrunimage:
	docker build -t $(DOCKER_ACCOUNT)/network-logger . && docker run $(DOCKER_ACCOUNT)/network-logger

buildpushimage:
	docker build -t $(DOCKER_ACCOUNT)/network-logger . && docker push $(DOCKER_ACCOUNT)/network-logger

kindloadimage:
	kind load docker-image $(DOCKER_ACCOUNT)/network-logger

installmanifest:
	kubectl apply -f manifests

deletemanifest:
	kubectl delete -f manifests