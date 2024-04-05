# **Social Media Project**

This project is a social media platform built using Django and Django REST Framework.

## Installation

**Clone the repository:**

git clone https://github.com/psgareja/social_network_project_AccuKnox.git

**Navigate to the project directory:**

cd social_network_project_AccuKnox

**Install the required dependencies:**

pip install -r requirements.txt

**Apply migrations:**

python manage.py migrate

**Run the development server.**

python manage.py runserver

**The server will start running at 'http://localhost:8000/'**

## Usage

**Use Postman to test the API endpoints.**

**API Endpoints**

**Signup**: /api/signup/ (POST)

**Login**: /api/login/ (POST)

**Search Users**: /api/search/ (GET)

**Send Friend Request**: /api/send-friend-request/ (POST)

**Accept Friend Request**: /api/accept-friend-request/ (POST)

**Reject Friend Request**: /api/reject-friend-request/ (POST)

**List Friends**: /api/list-friends/ (GET)

**List Pending Friend Requests**: /api/list-pending-requests/ (GET)

# Example

**Signup**: /api/signup/

**URL**:http://localhost:8000/api/singup/

**Body**: {

    "username": "example_user",
    
    "email": "user@example.com",
    
    "password": "password123"
    
}


## Postman Collection Link:
https://www.postman.com/lunar-module-explorer-98808198/workspace/socialmediaproject/collection/34066709-0b562726-2d7d-40ae-b3e9-b4b8eceaca3a?action=share&creator=34066709

## Docker

To containerize the application using Docker , follow these steps:

**1.Install Docker on your machine**

**2.Create 'Dockerfile' and 'docker-compose.yml' for the project**

**3.Build the Docker image:**

docker-compose build

**4.Run the Docker container:**

docker-compose up






