# Setup :

- `python -m venv env` (validate when your IDE asks to change for virtual environment)
- `.\env\Scripts\activate` (Win) / `source env/bin/activate` (Mac/Lin)
- `pip install -r requirements.txt`

# Launch :

OUTDATED

You'll need terminals to run the whole project, one for the simulation, and one for the dashboard :
- `python simulation.py` for the simulation
- `streamlit run dashboard.py` for the dashboard

Remember to stop the dashboard from the browser when exiting.
Use Ctrl+C in the terminals to kill the scripts.

# Modification :

Don't forget to always `git pull <remote> <branch>` before editing the code to make sure you're working on the latest version.
Then use : `git add -A`, `git commit -m "<commit message>"`, `git push -u <remote> <branch>`.