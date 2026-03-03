<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./tgctm/static/ctm-white.png">
  <img alt="ctm logo" src="./tgctm/static/ctm.png" height="100">
</picture>

# TG-CTM

The Gatherings Common Task Management

# Setup

The best way to go about this is to use Docker. Pull this repo, then run:

```
docker compose up -d --build
docker compose exec app python manage.py migrate
```

After this, you might want to create a user for logging in:

```
docker compose exec app python manage.py createsuperuser
```

This user can be used to login in the admin panel, found here: `/admin`

## Local development

### Prerequisites
- **pyenv**: Used to manage Python versions.
- **poetry**: Dependency management and packaging tool for Python.
- **nvm**: Node Version Manager, used to manage Node.js versions.
- **.env file**: Copy the `example.env` file to `.env` and fill in the required environment variables.

### Steps

1. **Install pyenv**:
  - Follow the instructions on the [pyenv GitHub repository](https://github.com/pyenv/pyenv#installation) to install pyenv.
  - Install the required Python version for the project:
    ```sh
    pyenv install -s
    ```

2. **Install poetry**:
  - Follow the instructions on the [poetry documentation](https://python-poetry.org/docs/#installation) to install poetry.
  - Install project dependencies:
    ```sh
    poetry install
    ```

3. **Install nvm**:
  - Follow the instructions on the [nvm GitHub repository](https://github.com/nvm-sh/nvm#installing-and-updating) to install nvm.
  - Install the required Node.js version for the project:
    ```sh
    nvm install
    ```

4. **Install django-tailwind dependencies**:
  - ```sh
    poetry run python src/manage.py tailwind install
    ```

5. **Run the Project**:
  - Apply migrations and start the development server: (you need two terminals running simultaneously)
    ```sh
    # terminal 1
    poetry run python src/manage.py tailwind start
    # terminal 2
    poetry run python src/manage.py migrate
    poetry run python src/manage.py runserver
    ```

6. **Create a superuser**:
  - Create a superuser to access the Django admin panel:
    ```sh
    poetry run python src/manage.py createsuperuser
    ```
  - Log in via the admin panel at `/admin`.
