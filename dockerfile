# 1. Start with an official Python blueprint
FROM python:3.9-slim

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Copy our app files into the container's folder
COPY . /app

# 4. Install the libraries our app needs
RUN pip install -r requirements.txt

# 5. Tell Docker the container will listen on port 5000
EXPOSE 5000

# 6. Set the command to run when the container starts
CMD ["python", "./app.py"]