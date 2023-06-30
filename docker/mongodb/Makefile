build:
	docker build -t mongo .
run:
<<<<<<< HEAD
	docker run -d -p 27017:27017 -v /Users/MINHUI/Documents/GitHub/docker/mongo:/app -v /Users/MINHUI/Documents/GitHub/docer/mongo/data:/data/db --name mongo mongo
=======
	docker run -d -p 27017:27017 -v /Users/BTC-N26/Documents/GitHub/mongo:/app -v /Users/BTC-N26/Documents/GitHub/docker/mongo/data:/data/db --name mongo mongo
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
exec:
	docker exec -it mongo /bin/bash
logs:
	docker logs mongo
<<<<<<< HEAD
ps:
=======
ps:	
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
<<<<<<< HEAD
=======

>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
rmi:
	docker rmi $$(docker images -q)
