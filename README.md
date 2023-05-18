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
            1. Pros: Simple and easy to deploy
            1. Cons: This will lose the application when the computer is restarting.
            2. Cons: You have to login to vps and navigate to the project directory at each time you need to update.
        ```bash
            nohup flask run --port 80 &
        ```