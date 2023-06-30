<<<<<<< HEAD
# step 1
FROM node:16

# step 2
WORKDIR /usr/src/app

# step 3
RUN git clone http://github.com/westmini427/docker-publish
WORKDIR docker-publish/worldcup
RUN npm install

# step 4
EXPOSE 8000

# step 6
=======
FROM node:16

# Step 2
WORKDIR /usr/src/app

# Step 3
RUN git clone http://github.com/HanJongWu/docker-publish
WORKDIR docker-publish/worldcup
RUN npm install

# Step 4
EXPOSE 8000

# Step 5
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
CMD ["node", "app.js"]
