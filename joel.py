import os
import menu
import matchup
from myproject.settings import PROJECT_ROOT

path = os.path.join(PROJECT_ROOT, 'files')

def get_file_list():
    return sorted([d for d in os.listdir(path)])

def process(file):
    menu.insert_file(file)

def process_matchup():
    matchup.process_weekly_matchups()

def create_matchup_schedule():
    matchup.create_matchup_data()

def create_byes():
    menu.create_bye_weeks()

def create_locks(schedule):
    matchup.create_locks(schedule)

def recalculate_weekly_matchups():
    matchup.recalculate_weekly_matchups()