# Use a base image with Python
FROM python:3.9-slim

RUN apt-get update && apt-get -y install cron vim dos2unix

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the cronjob file to the cron.d directory
COPY cronjob /etc/cron.d/stock_price_cron

# Apply cron job, fix line endings and set permissions
RUN dos2unix /etc/cron.d/stock_price_cron && chmod 0644 /etc/cron.d/stock_price_cron && crontab /etc/cron.d/stock_price_cron

# Create the log files to be able to run tail
RUN touch /var/log/cron.log /var/log/cron_test.log 

# Copy and give execution rights to the start.sh
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run the command on container startup
CMD ["/app/start.sh"]

