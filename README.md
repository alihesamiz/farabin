# Farabin-API

## To Run the Project, You Have the Following Choices

> [!WARNING]
> **The Docker configurations aren't updated and therefore are not useful.**

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

You can use `pipenv`, `poetry`, or Python's `venv`. Follow the steps for your chosen method:

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

2. Install the dependencies and activate the shell:

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

**After the installation and activating the environments, you can either run the project manually ot use the scripts that are prepared as follows:**

#### - **To use `supervisor`:**

> [!TIP]
> With `source load.sh`, the scripts directory temporarily gets added to the `PATH` of your terminal, and you'll be able to use the provided commands:

The below command will run the supervisor:

```bash
start.sh
```

The below command will show the status of the supervisor:

```bash
status.sh
```

And finally, the command below will stop the supervisor service:

```bash
stop.sh
```
> [!NOTE]
> There are other scripts as well, which are either for loading the tools or environment variables, but can be used separately and independently

After the `supervisor` starts the services, you can access the predefined URLs. The supervisor will automatically start `Gunicorn web server`, `Celery Worker`, `Celery Beat`, and `Flower`. The default ports are listed below:


- **Gunicorn**: 8000  
- **Flower**: 5555

---

### 3. Accessing the Project  

Project's default web service is set to `8000` port, but you can modify it in the `supervisor.conf` or the scripts which responsible for serving the project.

Also, to see the asynchronous processes using the `flower`, you only need to navigate to the `5555` port.

And that's it! You're all set🙂.

> [!CAUTION]
> The default settings are set to `development`; for deployment, you need to set it to `production` in the following scripts:
> - manage.py
> - asgi.py
> - wsgi.py
> - celery.py
