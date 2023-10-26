# starnavi-social-network

An API service for social network written with DRF

## Feauters:

- JWT-based authentication for secure access
- An admin panel located at /admin/ for easy management
- Comprehensive documentation available at /api/doc/swagger/
- Access to user profile
- Monitoring of user activity: displays when a user last logged in and when they made their last request to the service.
- Creation of posts
- Liking and unliking
- A custom command to start the Docker app only when the database is available
- Custom middleware to trace the user's last interaction with service

### Install using GitHub:
1. Run the command below in your terminal
    - `git clone git@github.com:MarharytaSovpenko/starnavi-social-network.git`
2. Open the project folder in your IDE
3. If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements
   in it, but if not:
    - python -m venv venv
    - source venv/Scripts/activate (on Windows/Git Bash)
    - venv\Scripts\activate (on Windows/PowerShell)
    - source venv/bin/activate (on macOS)
    - pip install -r requirements.txt
4. Create .env file and fill it with variables from .env.sample.
5. Don't forget to do migrations
    - `python manage.py migrate`
6. Run your server using the command below
    - `python manage.py runserver`


### Run with Docker:
- Install Docker https://www.docker.com/
- Run `docker-compose up` command and check with `docker ps` that 2 services are up and running
- Go to `127.0.0.1:8000/api/` and check the project endpoints via DRF interface or
go to `127.0.0.1:8000/api/doc/swagger/`


### Getting access:
- Create a new user via /api/user/register/
- Obtain a user token via /api/user/token/
- Install the ModHeader extension and create a request header with the value "Bearer <Your access token>"

##  Automated Bot

### Bot Configuration:
- Number of Users: Specifies the number of users to be created.
- Max Posts per User: Defines the maximum number of posts each user can create.
- Max Likes per User: Specifies the maximum number of likes a user can give.

### Bot Activities:
- Signup Users: The bot signs up the number of users specified in the configuration.
- Create Posts: Each user randomly creates a number of posts with any content, up to the maximum defined in the configuration.
- Like Posts: After creating user accounts and posts, the bot randomly likes posts, and posts can be liked multiple times.
