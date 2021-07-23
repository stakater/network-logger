
buildimage:
	docker build -t network-logger .

runimage:
	docker run network-logger

buildrunimage:
	docker build -t network-logger . && docker run network-logger