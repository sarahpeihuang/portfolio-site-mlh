# Line 1: Use the official CentOS Stream 8 image as the base image
FROM python:3.9-slim-buster


# Line 5: Set the working directory inside the container
WORKDIR /myportfolio

# Line 7: Copy all project files from the current directory into the container's working directory
COPY requirements.txt .

# Line 9: Install project dependencies using pip3
RUN pip3 install -r requirements.txt

COPY . .

# Line 11: Specify the command to run when a container is created from this image
CMD ["flask", "run", "--host=0.0.0.0"]

# Line 13: Specify the port that will be exposed from the container
EXPOSE 5000
