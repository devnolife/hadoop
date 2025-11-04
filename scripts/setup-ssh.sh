#!/bin/bash
# Setup SSH for Hadoop (passwordless SSH)

echo "=== Setting up SSH for Hadoop ==="

# Check if SSH is installed
if ! command -v ssh &> /dev/null; then
    echo "SSH is not installed. Please install openssh-server first:"
    echo "sudo apt install openssh-server"
    exit 1
fi

# Generate SSH key if not exists
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "Generating SSH key..."
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
fi

# Copy public key to authorized_keys
echo "Setting up authorized_keys..."
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys

# Test SSH connection
echo "Testing SSH connection..."
ssh -o StrictHostKeyChecking=no localhost 'echo "SSH connection successful!"'

echo "=== SSH Setup Complete ==="
