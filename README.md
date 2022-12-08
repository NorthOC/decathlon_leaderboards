# Decathlon CSV contestant data to JSON leaderboards

Takes a CSV file with contestant data, calculates scores, generates leaderboards, stores all of it
in `<timestamp>/output.json` and returns a view for the generated file.

Built using Flask.

## Directory documentation

`scripts/` - Stores the main logic of app.
`static/` - Stores css file.
`temp/` - Location to where generated JSON file will be saved.
`templates/` - Views.

## Install

TODO

You can test the app using `test.csv` file for upload.

## Algorithm

This is the algorithm file of the whole app:

https://drive.google.com/file/d/1QOojk-vfAnndBE1fQbrYvCbx_S-NynPm/view?usp=sharing

Download it and open it using https://app.diagrams.net/