# fastapi-template

FastAPI is a modern, batteries-included Python web framework that's perfect for building RESTful APIs. It can handle both synchronous and asynchronous requests and has built-in support for data validation, JSON serialization, authentication and authorization, and OpenAPI documentation.

This template provides a convenient way to quickly start working with FastAPI. It comes with a sample API that serves as a foundation for your own projects. Additionally, it offers authentication capabilities using Fief and supports MongoDB as the underlying database.

## Features

- Authentication: [Fief](https://docs.fief.dev/)
- Database: [MongoDB](https://www.mongodb.com/)
- Object Document Mapper: [Beanie-ODM](https://beanie-odm.dev/)
- Endpoints: Create, Read, Update, and Delete for Cats

## Getting Started

If you intend to run this project or deploy it to a Cloud Service Provider, it is recommended to set up a local development environment. If you're unfamiliar with the process of setting up such an environment, consider exploring the following resources as a starting point:

- [AlmaLinux 9](https://thevriends.com/technology/operating-systems/linux/almalinux/)

- [Windows Subsystem for Linux](https://thevriends.com/technology/operating-systems/windows/wsl/)

- [Podman](https://thevriends.com/technology/containers/podman/)

### Local Development Environment

- Clone this repo to your local development machine

  ```bash
  git clone https://github.com/jasonvriends/fastapi-template.git
  cd fastapi-template/app
  ```

- Create a Python Virtual Environment

  ```bash
  python3.11 -m venv .venv
  ```

- Activate the Python Virtual Environment

  ```bash
  source .venv/bin/activate
  ```

- Upgrade pip

  ```bash
  pip install --upgrade pip
  ```

- Install packages via file

  ```bash
  pip install -r requirements.txt
  ```

- Create a file called `podman-compose.yml` and populate it with the following:

  ```bash
  version: "3.8"

  services:
    mongodb:
      image: mongo:latest
      container_name: mongodb
      environment:
        MONGO_INITDB_ROOT_USERNAME: mongodb
        MONGO_INITDB_ROOT_PASSWORD: mongodb
      ports:
        - "27017:27017"
      volumes:
        - mongodb_data:/data/db

  volumes:
    mongodb_data:
  ```

- Start the MongoDB container

  ```bash
  podman-compose up
  ```

- Create a `.env` file

  ```bash
  mv .env.example .env
  ```

- Populate the variables in the `.env` file.

- Run the application
  ```bash
  python main.py
  ```

## References

- [Beanie-ODM](https://beanie-odm.dev/)

- [Fief](https://docs.fief.dev/)

- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)

- [FastAPI Production Template](https://github.com/zhanymkanov/fastapi_production_template)
