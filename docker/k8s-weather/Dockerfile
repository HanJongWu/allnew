# Step 1 : Base Images
FROM node:18.16.0

# Step 2 : Package Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# Step 3 : Specify a working directory
WORKDIR '/root'

# Step 4 : Config file copy
COPY weather.tar.gz .

# Step 5 : install express
RUN tar xvzf weather.tar.gz
WORKDIR '/root/weather'
RUN npm install
RUN npm install -g nodemon

# Step 5 : Open port
EXPOSE 8000

# Step 7: Execution Program
CMD ["nodemon", "app.js"]
