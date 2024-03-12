# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV MONGO_URI='mongodb+srv://andrewmalley:Queloque!72599@cluster0.fgkgdss.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ENV API_KEY='70b50751ee1db558cca4365d7451f42b811a0284fc8c1a8211470a3980c4e3b4'

# Run app.py when the container launches
CMD ["flask", "run"]
