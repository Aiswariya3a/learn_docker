
# Docker

At its core, Docker is a tool that solves a classic problem for developers: "But it works on my machine!" 

It does this by packaging an application and all its dependencies (like libraries, settings, and files) into a single, standardized unit called a **container**. This container is like a real-world shipping container, it can run consistently on any computer that has Docker, no matter the underlying operating system or configuration.

Let's look at the two most important building blocks of Docker: **Images** and **Containers**.

The easiest way to think about them is with a blueprint-and-house analogy.

***

**Docker Images: The Blueprint**

A Docker Image is a read-only, unchangeable template. It's like a detailed blueprint for a house. It contains everything needed to run your application:

- The application code itself.
- A runtime environment (e.g., Python, Node.js).
- System libraries and tools.
- Specific settings and configurations.

You build an image once, and you can use it to create many running instances. Just like a blueprint, the image itself is static, it's just the set of instructions.

**Docker Containers: The House**

A Docker Container is a live, running instance of an image. It's the actual house built from the blueprint. This is where your application actually runs.

You can start, stop, move, and delete containers. From a single image (blueprint), you can create and run many identical containers (houses) at the same time. Each container is isolated from the others, running in its own little environment.

***

So, the flow looks something like this:

- You write a set of instructions in a file called a Dockerfile.
- You use that Dockerfile to build an Image (the blueprint).
- You run that Image to create a Container (the house).

***

## The `Dockerfile`: The Recipe

It's a simple text file with a list of commands that the Docker engine runs in sequence. Let's look at a simple example for a Python web app. Don't worry if the commands look new; we'll break them down.

```dockerfile
# 1. Start with an official Python blueprint
FROM python:3.9-slim

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Copy our app files into the container's folder
COPY . /app

# 4. Install the libraries our app needs
RUN pip install -r requirements.txt

# 5. Tell Docker the container will listen on port 5000
EXPOSE 5000

# 6. Set the command to run when the container starts
CMD ["python", "./app.py"]
```

Each line is a step in the recipe:

  - `FROM` specifies the base image to start from (like the foundation of the house).
  - `WORKDIR` sets the primary folder for all the commands that follow.
  - `COPY` copies files from your computer into the image.
  - `RUN` executes a command, like installing software.
  - `EXPOSE` informs Docker that the container listens on specific network ports.
  - `CMD` provides the default command to run when the container starts.

The complete flow looks like this:

`Dockerfile`  ➡️ `docker build` command ➡️ **Image** ➡️ `docker run` command ➡️ **Container**

You've got it. The next step is to use the `docker build` command.

This command reads your `Dockerfile` (the recipe) and builds the **Image** (the blueprint).

***

### The `docker build` Command

The most common way to run this command is:
`docker build -t <image_name>:<tag> .`

Let's break that down:
- `docker build`: This is the command itself.
- `-t`: This is a flag for **"tag"**. It lets us give our image a friendly, human-readable name, like `my-python-app`.
- `<image_name>:<tag>`: This is the name and version you choose. For example, `my-python-app:1.0`. Using versions (tags) is great for keeping track of changes.
- `.` : This little dot is important! It tells Docker where to find the `Dockerfile` and the files to be copied. The `.` simply means "the current directory".



So, to build the image from our previous `Dockerfile` example, we would stand in that directory and run:

`docker build -t my-python-app:1.0 .`

When you run this, Docker will go step-by-step through your `Dockerfile` and, at the end, you will have a new image on your machine called `my-python-app:1.0`.

***

### The `docker run` Command

This command tells Docker to start your application. A common way to run it for a web app looks like this:

`docker run -d -p <host_port>:<container_port> <image_name>:<tag>`

Let's look at those new flags:
- `-d`: This stands for **"detached"**. It runs the container in the background and gives you your terminal back. Without it, the container would take over your terminal, and closing it would stop your app.
- `-p`: This is for **"publish"** or "port mapping". It connects a port on your computer (the host) to a port inside the container. Our `Dockerfile` used `EXPOSE 5000`, which opened the door inside the container. This `-p` flag builds the bridge to that door from the outside world.

So, to run the `my-python-app:1.0` image we built, we would use:

`docker run -d -p 8080:5000 my-python-app:1.0`



After running this, you could open your web browser, go to `http://localhost:8080`, and you would see your Python application running!

***

And with that, we've completed the entire journey:
1.  **`Dockerfile`**: We wrote the recipe.
2.  **`docker build`**: We used the recipe to create the blueprint (**Image**).
3.  **`docker run`**: We used the blueprint to launch the house (**Container**).


***

To view this in a more familiar way, open your web browser (like Chrome, Firefox, or Safari) and go to the following address:

`http://localhost:8080`

You should see the text "Server is up and running." displayed on the web page. This means you have successfully:

1.  Started your server inside the container.
2.  Mapped the container's internal port to your local machine's port 8080.
3.  Accessed it from your computer.

-----

### How to Show an Actual Web Page

Right now, your Python script is likely just sending plain text. To serve a real web page with HTML, you'll need to use a simple web framework like **Flask**.

Here’s how to modify your project to display a proper heading.

#### 1\. Update `requirements.txt`

Your application now depends on Flask, so add it to your `requirements.txt` file. The file should contain:

```
Flask
```

#### 2\. Update Your Python App (`main.py`)

Replace the content of your Python file with this simple Flask application.

```python
from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the default URL ("/")
@app.route('/')
def home():
    # Return an HTML heading as the response
    return '<h1>Hello from inside a Docker Container!</h1>'

# Run the app
if __name__ == '__main__':
    # Listen on all network interfaces and on port 5000
    app.run(host='0.0.0.0', port=5000)
```

**Key Changes:**

  - `host='0.0.0.0'`: This is crucial. It tells the Flask server to listen for connections from outside the container, which allows Docker's port mapping to work.
  - `port=5000`: This runs the app on port 5000 *inside* the container, matching what you likely have in your `Dockerfile`'s `EXPOSE 5000` command.

#### 3\. Rebuild and Rerun

Now that you've changed your code, you need to build a new image and run a new container.

1.  **Stop the old container:**
    `docker stop <container_name_or_id>`
2.  **Rebuild your image:**
    `docker build -t your-app-name .`
3.  **Run a new container:**
    `docker run -d -p 8080:5000 your-app-name`

Now, when you refresh `http://localhost:8080` in your browser, you will see your new HTML heading.

***

### See What's Running: `docker ps`
First, you'll probably want to see a list of all your active containers. The command for this is `docker ps`.

The `ps` stands for "process status," a common term in other systems. Think of it as asking Docker, "What processes are you currently running?"



When you run it, you'll see a table with info about your container, including:
- `CONTAINER ID`: A unique ID for your container.
- `IMAGE`: The image it was created from (`my-python-app:1.0`).
- `PORTS`: The port mapping we set up (`0.0.0.0:8080->5000/tcp`).
- `NAMES`: A random, funny name Docker gives your container (like `goofy_einstein`).

### Stop a Container: `docker stop`
Once you can see your container, you can stop it using the `docker stop` command. You just need to tell it *which* container to stop by giving it either the `CONTAINER ID` or the random `NAME` from the `docker ps` command.

So, the workflow is:
1.  Run `docker ps` to find the container's name or ID.
2.  Run `docker stop` using that name or ID.

***

## Local `venv` vs. Docker's Environment

Think of it this way:

  * **Virtual Environment (`venv`)**: This isolates your project's Python dependencies from *other Python projects on your local computer*. It's a toolbox for your workshop.
  * **Docker Container**: This isolates your *entire application* (the code, the Python installation itself, and all dependencies) from your *entire local computer*. It's a complete, self-contained, portable workshop.

When your `Dockerfile` runs the command `RUN pip install -r requirements.txt`, it is installing those packages fresh into the container's own isolated Python environment. It has no knowledge of, and should not be polluted by, your local `venv`.

-----

## How to Exclude It: The `.dockerignore` File

To prevent Docker from copying your `venv` folder and other unnecessary files, you should create a file named `.dockerignore` in the same directory as your `Dockerfile`. It works exactly like a `.gitignore` file.

This is a **critical best practice** because it:

1.  **Keeps your image small**: Virtual environment folders can be huge.
2.  **Speeds up the build**: Docker doesn't have to waste time sending all those files to the builder.
3.  **Avoids conflicts**: Your local `venv` might have binaries built for your OS (like Windows or macOS), which would fail inside the Linux-based container.

A typical `.dockerignore` file for a Python project would look like this:

```
# Ignore the local virtual environment
venv/
env/

# Ignore Python cache files
__pycache__/
*.pyc

# Ignore editor and git files
.git/
.vscode/
.idea/
```

So, the key takeaway is: your local `venv` is for developing on **your machine**. The `Dockerfile` and `requirements.txt` are the recipe for Docker to build a brand new, clean environment for the **container**.

***

The main purpose of **Docker Compose** is to make running your container easier by writing down the configuration in a file, instead of typing a long command every time.

-----

## The Problem We Are Solving

Remember our `docker run` command?
`docker run -d -p 8080:5000 your-app-name`

This command is getting a bit long. What if we wanted to add more options? It would become very hard to remember and type correctly.

Docker Compose solves this by letting us save that configuration into a file.

-----

## A Simple Example (Just Our Web App)

Let's use Docker Compose for **only our single web app container**.

1.  **Create the `docker-compose.yml` file:**
    This file describes the *exact same things* our `docker run` command did.

    ```yaml

    # 'services' is the list of containers we want to run
    services:
      # 'webapp' is the name WE CHOOSE for our one service.
      webapp:
        # This replaces 'docker build .'
        # It tells Compose to build the image from the
        # Dockerfile in the current folder ('.').
        build: .

        # This replaces the '-p 8080:5000' part of our run command.
        # It maps port 8080 on our computer to port 5000 in the container.
        ports:
          - "8080:5000"
    ```
-----

## How to Run It

Now, instead of `docker build` and `docker run`, you only need one command in your terminal:

`docker-compose up -d`

This single command reads your `docker-compose.yml` file and does everything for you. To stop it, you just press `Ctrl + C`.

Add the `-d` flag to your command. The `-d` stands for "detached". Now, Docker Compose will start your containers and immediately return you to your command prompt. Your application is running in the background.

So, the only thing we've done here is move our `run` command options into a clean file. Once we're comfortable with this, we can later add a second service like a database.

You've run into a common and useful feature\! By default, `docker-compose up` runs in **foreground mode**. This attaches your terminal directly to the container's logs, which is great for seeing real-time output and errors.

-----

## How to See Logs in Detached Mode

Once your containers are running in the background, you can view their logs at any time with the `logs` command:

```bash
docker-compose logs
```

To see the logs in real-time, add the `-f` flag, which means "follow":

```bash
docker-compose logs -f
```

You can press `Ctrl + C` to stop watching the logs at any time, and your containers will **keep running** in the background.

To stop the containers, use 

```bash
docker-compose down
```

Now that you're comfortable with how Docker Compose works for a single service, we can go back to its main purpose: running a web app and a api together.

-----

## Running two containers

Let's create a second, very simple Python app. We'll call it an `api` service. Our main `webapp` will simply ask this `api` service for a message.

This is a great example of a **microservices** architecture, where different parts of your application run as separate services.

-----

### Step 1: Create a New `api` Service

First, let's create the files for our second, simpler web service.

1.  Inside your project folder, create a new folder named `api`.
2.  Inside this new `api` folder, create a file named `api.py`:
    ```python
    # file: api/api.py
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def get_message():
        # This service just returns a simple string.
        return "Hello from the API container!"

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5001)
    ```
3.  Inside the `api` folder, create its `requirements.txt`:
    ```
    # file: api/requirements.txt
    Flask
    ```
4.  Finally, create a `Dockerfile` inside the `api` folder:
    ```dockerfile
    # file: api/Dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY . /app
    RUN pip install -r requirements.txt
    CMD ["python", "./api.py"]
    ```

-----

### Step 2: Update `docker-compose.yml`

Now, let's tell Docker Compose about both services.

```yaml
services:
  webapp:
    # This builds from the Dockerfile in the main folder
    build: .
    ports:
      - "8080:5000"

  api:
    # This builds from the Dockerfile in the './api' folder
    build: ./api
    # Notice: NO ports here. We don't need to access the api
    # from our browser, only from our webapp.
```

-----

### Step 3: Update the Main `webapp`

Now, let's change our main web app to call the new `api` service.

1.  Add the `requests` library to your main `requirements.txt` file (the one not in the `api` folder):
    ```
    # file: requirements.txt
    Flask
    requests
    ```
2.  Update your `main.py` file to fetch the message:
    ```python
    # file: main.py
    from flask import Flask
    import requests

    app = Flask(__name__)

    @app.route('/')
    def home():
        # This sends a request to our api service.
        # The hostname 'api' matches the service name in docker-compose.yml.
        # The port '5001' matches the port our api.py is running on.
        try:
            response = requests.get('http://api:5001')
            message = response.text
        except requests.exceptions.ConnectionError as e:
            message = f"Error connecting to the API: {e}"
        
        return f'<h1>The API says: "{message}"</h1>'

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

-----

### Step 4: Run It

Now, run the same command:

```bash
docker-compose up -d --build
```

(The `--build` flag tells Compose to rebuild the images since we changed the code.)

Go to `http://localhost:8080`. Your `webapp` will now call the `api` container, get the message, and display it. You have two containers talking to each other\!

-----

## Connecting a DataBase

Let's connect our PostgreSQL database.

The process has three main steps:

1.  We'll add the new `db` service to our `docker-compose.yml` file.
2.  We'll update our `webapp`'s Python code to talk to this new database.
3.  We'll run it and see it in action.

-----

### Step 1: Update `docker-compose.yml`

Let's replace our `api` service with a new service named `db` for our database.

```yaml
version: '3.8'
services:
  webapp:
    build: .
    ports:
      - "8080:5000"
    # This tells Compose to start the db before the webapp
    depends_on:
      - db

  db:
    # Use the official PostgreSQL image
    image: "postgres:13-alpine"
    # These are settings passed to the PostgreSQL container on startup
    environment:
      - POSTGRES_USER=myuser
      - POSTGRES_PASSWORD=mypassword
      - POSTGRES_DB=mydatabase
```

The **`environment`** section is how we configure the database, setting the default user, password, and database name.

-----

### Step 2: Update the Web App

Now we'll change the Python code to connect to PostgreSQL.

1.  First, update your main `requirements.txt` file. We need to add the PostgreSQL driver, `psycopg2-binary`, and we can remove `requests`.

    ```
    Flask
    psycopg2-binary
    ```
2.  Next, replace the code in your `main.py` file with this:

    ```python
    from flask import Flask
    import psycopg2
    import time

    app = Flask(__name__)

    @app.route('/')
    def home():
        # Let's try to connect to the database
        try:
            conn = psycopg2.connect(
                host="db",
                database="mydatabase",
                user="myuser",
                password="mypassword"
            )
            # If we get here, the connection was successful!
            conn.close() # Close the connection right away
            return "<h1>Success! I connected to the database.</h1>"

        except psycopg2.OperationalError as e:
            # If we get here, something went wrong
            return f"<h1>Error: Could not connect. Is the database running?</h1><p>{e}</p>"

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

-----

### Step 3: Run It

Now, run the command to build the new `webapp` image and start both services:

```bash
docker-compose up --build -d
```

Go to `http://localhost:8080` in your browser. You will see, "Success! I connected to the database."

***

## how Docker containers handle data?

It proves your `webapp` container can successfully find and communicate with your `db` container over the private network Docker Compose created.

Now that we know the connection works, let's do a quick experiment to discover a very important concept about how Docker containers handle data.

-----

### The Experiment: What Happens When Containers Stop?

1.  First, let's put the slightly bigger code back into your `main.py` file. This is the version that creates a table and saves a timestamp for each visit.

    ```python
    import time
    from flask import Flask
    import psycopg2

    app = Flask(__name__)

    def get_db_connection():
        while True:
            try:
                conn = psycopg2.connect(
                    host="db",
                    database="mydatabase",
                    user="myuser",
                    password="mypassword")
                return conn
            except psycopg2.OperationalError:
                print("Connection failed, retrying...")
                time.sleep(1)

    @app.route('/')
    def home():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, timestamp timestamp);")
        cur.execute("INSERT INTO visits (timestamp) VALUES (NOW());")
        conn.commit()
        cur.execute("SELECT timestamp FROM visits ORDER BY timestamp DESC;")
        visits = cur.fetchall()
        cur.close()
        conn.close()
        
        response = "<h1>Visitor Timestamps:</h1>"
        for visit in visits:
            response += f"<p>{visit[0]}</p>"
        
        return response

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```
2.  Now, in your terminal, run `docker-compose up --build -d` to update your running application.
3.  Go to `http://localhost:8080` and refresh the page 3-4 times. You should see a new timestamp appear with each refresh.
4.  Once you have a few timestamps, go back to your terminal and completely stop and **remove** the containers with this command:
    ```bash
    docker-compose down
    ```
5.  Finally, start everything again:
    ```bash
    docker-compose up -d
    ```

Now for the important question: refresh your browser one last time. What do you see? What happened to the list of timestamps you created?