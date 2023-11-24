# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8

RUN yum -y install git

# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
RUN python3.8 -m pip install -r requirements.txt

# Copy the earlier created app.py file to the container
COPY sam_vit_h_4b8939.pth ./
COPY app.py ${LAMBDA_TASK_ROOT}

WORKDIR /var/task
CMD [ "app.lambda_handler" ]
