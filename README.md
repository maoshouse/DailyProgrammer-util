# DailyProgrammer-util
## Intro
The first prompt of 2015 was to write something that will be useful for this year's Daily Progammer prompts. As such, I decided to write a utility to grab new assignments and organize them into separate project folders. This became a slightly better idea when I realized that the programming prompts posted on reddit are formatted in Markdown, which is perfect for starting README.md files for version control on github. 
## Prereqs
This project uses the PRAW package to grab stuff from reddit's API. Installation should be easy. With pip, simply enter `pip install praw` and everything should be good to go after a clean installation.

There's a textfile, config.cfg that should be modified to point to the root project directory where you wish to store Daily Programmer projects.
## Usage
`python daily_programmer_util.py` should do the trick.
