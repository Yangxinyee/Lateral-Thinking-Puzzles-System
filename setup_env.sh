#!/bin/bash

# Set virtual environment name
ENV_NAME="LTP_env"

echo "Creating virtual environment: $ENV_NAME ..."
python3 -m venv $ENV_NAME

echo "Virtual environment created!"

echo "Activating environment and installing dependencies..."
source $ENV_NAME/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "All dependencies installed!"
echo "To use the environment, run: source $ENV_NAME/bin/activate"