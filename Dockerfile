# Set the base image to Ubuntu
FROM ubuntu

# Update the sources list
RUN apt-get update

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

#Copy my Code into the Container
ADD code /code

# Get pip to download and install requirements:
RUN pip install -r /code/requirements.txt

# Set the default directory where CMD will execute
WORKDIR /code

CMD ./run.sh