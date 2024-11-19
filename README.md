# Farabin-API

## To Run the Project, You Have the Following Choices:

### 1. Run the Project with Docker:
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

### 2. Run the Project with Django Itself:
You can either use `pipenv` or Python's `venv`. Follow the steps for your chosen method:

#### **To Use `pipenv`:**
1. Ensure you have `pipenv` installed. If not, install it with:
   ```bash
   pip install pipenv
   ```
2. Activate the `pipenv` shell and install dependencies automatically:
   ```bash
    pipenv shell
   ```

#### **To Use `venv`:**
1. Create a new virtual environment in your project folder:
   ```bash
    python -m venv yourvenvname
   ```
2. Activate the virtual environment and install dependencies:
- **Linux/Max**:
  ```bash
  source yourvenvname/bin/activate
  pip install -r requirements.txt
  ```
- **Windows**:
   ```bash
    yourvenvname\Scripts\activate
    pip install -r requirements.txt   
    ```

---
### 3. Running the Project:
After setting up the environment, execute the following commands to initialize and run the project:
   ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver
   ```