# Use the official Python image as a base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install wget (if needed for any additional setup)
RUN apt-get update && apt-get install -y wget

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Set up Chrome options
RUN CHROME_BIN=$(which google-chrome-stable) \
    && echo "CHROME_BIN=$CHROME_BIN" >> /etc/environment

# Configure Chrome options
ENV CHROME_PATH /usr/bin/google-chrome-stable
ENV CHROME_BIN /usr/bin/google-chrome-stable
ENV CHROME_DRIVER /usr/local/bin/chromedriver

# Copy the rest of the application code
COPY . /app

# Expose the port FastAPI will run on (not necessary for Cloud Run)
# EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app"]
