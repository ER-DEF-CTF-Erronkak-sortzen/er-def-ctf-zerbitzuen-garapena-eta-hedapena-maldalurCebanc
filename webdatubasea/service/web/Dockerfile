FROM php:7.4-cli

# Install required packages (SSH server and MySQL client)
RUN apt-get update && apt-get install -y \
    openssh-server \
    default-mysql-client \
    && mkdir /var/run/sshd

# Copy application files
WORKDIR /var/www/html
COPY . .

# Add and configure SSH user
RUN useradd -m dev1 && echo "dev1:dev1_password" | chpasswd

# Expose necessary ports
EXPOSE 80 22

# Copy and set the entrypoint script
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]