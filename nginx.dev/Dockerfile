# Use the official NGINX image as the base image
FROM nginx:latest

# Install OpenSSL to generate SSL certificates and DH parameters
RUN apt-get update && apt-get install -y openssl

# Create directories for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Copy SSL certificates to the container
COPY ssl/cloudflare.crt /etc/nginx/ssl/cloudflare.crt
COPY ssl/cloudflare.key /etc/nginx/ssl/cloudflare.key

# Generate Diffie-Hellman parameter file
RUN openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048

# Set permissions for the SSL certificates and key
RUN chmod 644 /etc/nginx/ssl/cloudflare.crt && \
    chmod 600 /etc/nginx/ssl/cloudflare.key && \
    chmod 644 /etc/nginx/ssl/dhparam.pem

# Copy custom NGINX configuration file to the container
COPY .nginx.conf /etc/nginx/nginx.conf

# Expose ports 80 and 443
EXPOSE 80 443

