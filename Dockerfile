# Start from a base image with Ubuntu
FROM ubuntu:20.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install Python, pip, LibreOffice, unoconv, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip libreoffice unoconv \
    imagemagick ghostscript fonts-dejavu fonts-liberation

# Install CairoSVG for SVG to PNG conversion
RUN apt-get install -y python3-cairosvg

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Clean up to reduce layer size
RUN rm -rf /var/lib/apt/lists/*

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py using Gunicorn when the container launches
CMD ["gunicorn", "--log-level", "debug", "--workers=3", "--worker-class=gthread", "--threads=4", "--bind", "0.0.0.0:8080", "app:app"]
