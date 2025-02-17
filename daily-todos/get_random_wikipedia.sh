#!/bin/bash
# set -e  # Exit immediately if a command fails

# Function to handle errors
error_handler() {
  echo "An error occurred while fetching the URL."
  exit 1  # Exit the script with a non-zero status
}

# Trap errors and call error_handler on any command failure
trap 'error_handler' ERR

URL="https://en.wikipedia.org/wiki/Special:Random"

LOCAL_ADD_TODO_URL=""

if [ -n "$ADD_TODO_URL" ]; then
    LOCAL_ADD_TODO_URL="$ADD_TODO_URL"
else
    LOCAL_ADD_TODO_URL="http://127.0.0.1:8081"
fi

# echo "$LOCAL_ADD_TODO_URL"

# Send GET request to "Special:Random" and capture the response header
response=$(curl -s -I $URL)


# Check if the response is valid
if [[ $? -ne 0 ]]; then
  echo "Failed to fetch the response."
  exit 1
fi

# Extract the Location header (the final redirected URL)
real_url=$(echo "$response" | grep -i "^Location:" | awk '{print $2}' | tr -d '\r')

# Check if the Location header is found
if [ -z "$real_url" ]; then
  echo "Failed to extract the URL from the response."
  exit 1
fi

json_data="{\"todo\": \"READ $real_url\"}"


# Send POST request to the URL of choice with the real_url inside the JSON payload
response=$(curl -s -X POST "$LOCAL_ADD_TODO_URL/add_todo" -H "Content-Type: application/json" -H "User-Agent: MyCustomClient/1.0" -d "$json_data")

# Check if the response is empty or failed
if [ -z "$response" ]; then
  echo "Failed to get a response from the POST request."
  exit 1
fi

# Output the response
# echo "Response from the POST request:"
# echo "$response"