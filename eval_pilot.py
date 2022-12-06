from read_sql import *
import pandas as pd
import sqlite3

conn = sqlite3.connect("results.db")
data = pd.read_sql("SELECT * from Study1",conn)
# print(x)  # 13 rows per participant
# Video Question Condition Correctness ConditionQuestion ConditionCorrectness
additional_data = pd.read_csv("study_1-data/additional_results.csv",sep=";",encoding="utf-8",header=[0]) # get data for age etc.
subject_number = []
age = []
year = []
distractions = []
experience = []
for i in range(30): # 30 participants
    subject_number.extend([additional_data.loc[i]["Subject Number"]]*13)
    age.extend([additional_data.loc[i]["Alter"]]*13)
    year.extend([additional_data.loc[i]["Jahr"]]*13)
    distractions.extend([additional_data.loc[i]["Ablenkungen transcription"]]*13)
    experience.extend([additional_data.loc[i]["Erfahrung transcription"]]*13)
data.assign("Subject Number" == subject_number)
data.assign("Age" == age)
data.assign("Year" == year)
data.assign("Distractions" == distractions)
data.assign("Experience" == experience)

participants = per_participant(data)
print(participants)
condition = per_condition(data)
print(condition)
video = per_video(data)
print(video)
distraction_type = per_distraction_type(data)
print(distraction_type)
age = by_age(data)
print(age)
experience = by_experience(data)
print(experience)
year = by_year(data)
print(year)
distraction = common_distraction(data)
print(distraction)