# Pull the base image with python 3.10 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.10

# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
RUN python3.8 -m pip install -r requirements.txt

# Copy the earlier created app.py file to the container
COPY ./materioshka.py ./
COPY ./sam_vit_h_4b8939.pth ./

# Set the CMD to your handler
CMD ["materioshka.lambda_handler"]
