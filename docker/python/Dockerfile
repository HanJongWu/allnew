<<<<<<< HEAD
# step 1 : Base Images
FROM python:3.9

# step 2 : Package Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# step 3 : Specify a working directory
WORKDIR '/root'

# step 4 : Config file copy
=======
# Step 1 : Base Images
FROM python:3.9

# Step 2 : Packge Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# Step 3 : Specify a working directory
WORKDIR '/root'

# Step 4 : Config file copy
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
COPY .bashrc .
COPY .exrc .
COPY hello.py .
RUN pip install bottle

<<<<<<< HEAD
# step 5 : open port
EXPOSE 8000

# step 6 : Execution Program
CMD ["python", "hello.py"]
=======
# Step 5 : open port
EXPOSE 8000

# Step 6 : Execution Program
CMD ["python","hello.py"]
>>>>>>> de95fd84f296b27228e7f62bd03f37e0da494ece
