#!/bin/bash

# Step 1: Change to the project folder
cd ~/portfolio-site-mlh

# Step 2: Fetch and reset the git repository
git fetch && git reset origin/main --hard

# Step 3: Enter the python virtual environment and install dependencies
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Step -: Restart the myportfolio service 
# systemctl restart myportfolio   

# Step 4: Stop and remove existing containers using docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml down

# Step 5: Build and start the containers again
docker-compose -f docker-compose.prod.yml up -d --build
