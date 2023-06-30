build:
	docker build -t nodejs .
run:
<<<<<<< HEAD
	docker run -it -d -p 8000:8000 -v /User/MINHUI/Document/GitHub/nodejs:/app --name nodejs nodejs
=======
	docker run -it -d -p 8000:8000 --name nodejs nodejs
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
exec:
	docker exec -it nodejs /bin/bash
logs:
	docker logs nodejs
ps:
	docker ps -a
<<<<<<< HEAD
img:
=======
img:	
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
