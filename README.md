# Farabin-API

## To Run the Project, You Have the Following Choices

-> Please note that the Docker configurations arent updated and therefore are not usefull

### 1. Run the Project with Docker

- First, make sure Docker is installed on your system.

- In the project directory, run the `docker compose` command appropriate for your operating system:
  - **For Ubuntu**:

    ```bash
    sudo docker compose up --build
    ```

  - **For Windows**:

    ```bash
    docker-compose up --build
    ```

---

### 2. Run the Project with Django Itself

You can either use `pipenv`, `poetry` or Python's `venv`. Follow the steps for your chosen method:

#### - **To Use `pipenv`:**

1. Ensure you have `pipenv` installed. If not, install it with:

   ```bash
   pip install pipenv
   ```

2. Activate the `pipenv` shell and install dependencies automatically:

   ```bash
    pipenv shell
   ```

#### - **To Use `poetry`:**

1. Ensure you have `poetry` installed. If not, install it with:

   ```bash
   pip install poetry
   
   or

   sudo apt install python3-poetry
   ```

2. Install the dependencies and activate shell:

   ```bash
   poetry install --no-root
   
   poetry shell
   ```

#### - **To Use `venv`:**

1. Create a new virtual environment in your project folder:

   ```bash
    python -m venv yourvenvname
   ```

2. Activate the virtual environment and install dependencies:

- **Linux/Mac**:

  ```bash
  source yourvenvname/bin/activate
  pip install -r requirements.txt
  ```

- **Windows**:

   ```bash
    yourvenvname\Scripts\activate
    pip install -r requirements.txt   
    ```

**After the installation and activating the environments, you either can run the project manually ot just use the scripts that are prepared like following:**

#### - **To use `supervisor`:**

##### - **To source the `command scripts`:**

- **Linux/Mac**:
   With `source load.sh`, the scripts directory temporarily gets added to the `PATH` of your terminal and you'll be able to use the provided commands:

Below command will run the supervisor:

```bash
start.sh
```

Below command will show the status of the supervisor:

```bash
status.sh
```

And finally, command below will stop the supervisor service:

```bash
stop.sh
```

(P.S.: there are other scripts as well which are either for loading the tools or enviroment variables but can be used seperatley and independentaley)

After the `supervisor` started the services you'll be able to access the predefined URLs. the supervisor will automatically starts `Gunicorn web server`, `Celery Worker`, `Celery Beat` and `Flower`. Default ports are lister below:

```bash
- **Gunicorn**: 8000  
- **Flower**: 5555
```

### 3. Accessing the Project  

Projets default web service is set to `8000` port, but you can modify it in the `supervisor.conf` or the scripts that are responsible for serving the project.

Also, to see the asynchronous processes using the `flower`, you only need to navigate to the `5555` port.

And That's it! You'r all set🙂.
