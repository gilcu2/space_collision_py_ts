#!/bin/sh

set -e

# Replace the placeholder in config.js with the environment variable
sed -i "s/localhost/${API_HOST}/g" /usr/share/nginx/html/config.js

# Start the Nginx server
nginx -g "daemon off;"