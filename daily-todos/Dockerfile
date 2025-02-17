# Start from an appropriate base image, such as an Alpine image with bash
FROM alpine:latest

# Install bash, curl, and cron (no need for -y flag)
RUN apk update --no-cache && apk add bash curl

# Add your bash script to the container 
COPY get_random_wikipedia.sh /usr/local/bin/get_random_wikipedia.sh

# Make your script executable
RUN chmod +x /usr/local/bin/get_random_wikipedia.sh

# Ensure the cron daemon runs when the container starts
CMD ["/usr/local/bin/get_random_wikipedia.sh"]


