# Decathlon Leaderboards

Built with Flask.

Takes a CSV file with contestant data, calculates scores, generates leaderboards, parses it
in `temp/<timestamp>/output.json` and returns a view of the generated file.

## Directory documentation

`scripts/` - Stores the main logic of app.

`static/` - Stores css file.

`temp/` - Location to where generated JSON file will be saved.

`templates/` - Views.

## Install

### With Docker

```bash
git clone https://github.com/NorthOC/decathlon_leaderboards
cd decathlon_leaderboards
docker build --tag decathlon-leaderboards .
docker run decathlon-leaderboards
```

### Manual (no Docker)

```bash
git clone https://github.com/NorthOC/decathlon_leaderboards
cd decathlon_leaderboards
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask run
```

You can test the app using `test.csv` file for upload.

## Algorithm

This is the algorithm file of the whole app:

https://drive.google.com/file/d/1QOojk-vfAnndBE1fQbrYvCbx_S-NynPm/view?usp=sharing

Download it and open it using https://app.diagrams.net/