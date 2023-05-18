# Recipe
The Recipe Search website is designed to provide users with a convenient way to explore and discover various recipes. 

To deploy the project, follow the steps below:

1. Clone the project repository and navigate to the project directory:

2. Set up a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependancies:

```bash
pip install Flask Flask-Migrate SQLAlchemy Flask-Login Flask-WTF Pillow email_validator
```
4. Initialize and migrate database

```bash
flask db init
flask db migrate
flask db upgrade
```
5. run seed.py (This seed is created to add initial data to the web site like recipe categories)

```bash
python seed.py
```

5. 
    1. ### Run on local environment
        .Run application on a desire port(i use port as example 80)

    ```bash
    flask run --port 80
    ```
    2. ### Run on a vps as a baground task
        1. #### Using nohup 
            1. Pros 
                Simple and easy to deploy: It's straightforward to start a process using nohup, as it allows you to run a command or script in the background without being tied to a terminal session.
            1. Cons 
                Persistence: When the computer restarts, any processes running under nohup will be terminated. This means that if you rely solely on nohup, you'll lose your application upon a system restart.
                Manual updates: To update the application, you need to log in to the VPS (Virtual Private Server) and navigate to the project directory each time. This manual process can be cumbersome and time-consuming, especially if frequent updates are required.
        ```bash
            nohup flask run --port 80 &
        ```
        2. #### Creating a systemd service 
            1. Pros
                Automatic startup and management: Once a systemd service is configured, it will automatically start during system boot and can be easily managed using systemd commands. This eliminates the need for manual intervention, making it convenient for long-running applications.

                Easy updates and version control: With a systemd service, updating the application becomes more streamlined. You can simply update the underlying files or code and then restart the service using systemctl, ensuring that the latest version is running without the need to manually navigate to the project directory.
            2. Conse
                Complexity of configuration: Setting up a systemd service requires writing a service unit file with specific configurations. This may involve understanding and modifying parameters such as service dependencies, environment variables, and startup conditions. The initial setup process can be more complex compared to using simpler methods like nohup.

                System-specific limitations: Systemd services may have limitations or compatibility issues depending on the specific operating system or distribution. Some advanced features or configurations might not be available in older versions of systemd or on certain platforms, potentially limiting the flexibility and portability of your application.
            3. steps
                1. Create a file named recipe.service in system directory as "vim /etc/systemd/system/recipe.service" using following code
                ```bash
                [Unit]
                Description=Recipe
                After=network.target

                [Service]
                User=user_name
                Group=user_group
                WorkingDirectory=/path/to/git/cloned/recipe
                Environment="FLASK_APP=app.py"
                ExecStart=/usr/bin/bash -c "git pull && /path/to/git/cloned/recipe/venv/bin/flask run --port 80"
                ExecReload=/bin/kill -s HUP $MAINPID
                ExecStop=/bin/kill -s TERM $MAINPID
                Restart=always

                [Install]
                WantedBy=multi-user.target
                ```
                2. To apply the changes made to the systemd service, the systemd daemon shold be reloaded. This can be done by running the following command:
                ```bash
                systemctl daemon-reload
                ```
                3. Finally, run the following command to start newly created service
                ```code
                systemctl restart recipe
                ```
                4. To see the status of service, following command can be used
                ```code
                systemctl status recipe
                ```