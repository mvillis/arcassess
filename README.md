# ArcAssess

ArcAssess provides a simple survey tool.

## Project Setup

1. Clone the project locally
2. Create a virtual python environment and process the `requirements.txt` file to pull in any dependencies. Python 2.7.5 has been used in tests.
3. Set some environment variables:
- `TEAMTEMP_SECRET_KEY=fsdafds2342`  (this key can be whatever you like)
- `DATABASE_URL=sqlite:////Users/mvillis/Dev/archassess/db.sqlite`
Note that the database url is an absolute path to a file. You will need to update this path to match a location on your desktop.

4. Run the following commands from the root directory of your project using the virtual environment you created above:
- `python manage.py syncdb` When running this command there is no need to set up an initial super user.
- `python manage.py migrate`
- `manage.py loaddata initial_load.yaml` This loads some basic setup data

5. Run the app
- `python manage.py runserver`
- go to http://127.0.0.1:8000/
- Register a new user
- Go for it!
