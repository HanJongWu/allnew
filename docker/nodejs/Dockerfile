<<<<<<< HEAD
=======
<<<<<<< HEAD
# step 1 : Base Images
FROM node:16.20.0

# step 2 : Package Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# step 3 : Specify a working directory
WORKDIR '/root'

# step 4 : Config file copy
COPY .bashrc .
COPY .exrc .
COPY hello.js .

# step 5 : install express
RUN npm init -y
RUN npm install express
RUN npm install -g nodemon

# Step 6 : open port
EXPOSE 8000

# Step 7 : Execution Program
CMD ["nodemon", "hello.js"]
=======
>>>>>>> f18a9679d25451c754f8ed8290474aa22e15adf2
# Step 1 : Base Images
FROM node:16.20.0

# Step 2 : Packge Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# Step 3 : Specify a working directory
WORKDIR '/root'

# Step 4 : Config file copy
COPY .bashrc .
COPY .exrc .
COPY hello.js .
RUN npm install express

# Step 5 : open port
EXPOSE 8000

# Step 6 : Execution Program
CMD ["node","hello.js"]
<<<<<<< HEAD
=======
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
>>>>>>> f18a9679d25451c754f8ed8290474aa22e15adf2
