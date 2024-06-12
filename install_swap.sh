#!/bin/bash

# Set the size of the swap file. This example creates a 4GB swap file.
swap_size=4G

# Create the swap file. Replace '/swapfile' with your desired file path if needed.
sudo fallocate -l $swap_size /swapfile

# Set the correct permissions for the swap file.
sudo chmod 600 /swapfile

# Set up the swap area.
sudo mkswap /swapfile

# Enable the swap file.
sudo swapon /swapfile

# Make the swap file permanent by adding it to /etc/fstab.
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Verify the swap is active.
sudo swapon --show