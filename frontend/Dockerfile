# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Copy the current directory contents into the container at /usr/share/nginx/html
COPY . /usr/share/nginx/html

# Run nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]