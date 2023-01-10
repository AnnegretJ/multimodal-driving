from read_sql import *
import pandas as pd
import sqlite3

def condition_only(data):
    # get amount of answered correctly driving questions vs answered incorrectly
    drive_correct = 0
    drive_incorrect = 0
    # return as first tuple in list

    # get amount of answered correctly distraction questions vs incorrectly
    distract_correct = 0
    distract_incorrect = 0
    # return as second tuple in list
    
    # get amount of answered correctly driving while distraction correctly vs driving correctly wwhile distraction incorrectly vs driving incorrectly while distraction correctly vs driving incorrectly while distraction incorrectly
    drive_c_while_distract_c = 0 # c = correct, i = incorrect
    drive_c_while_distract_i = 0
    drive_i_while_distract_c = 0
    drive_i_while_distract_i = 0
    # return as last tuple in list

    for line in data.iterrows():
        if line["Correctness"]:
            drive_correct +=1
            if line["ConditionCorrectness"]:
                distract_correct += 1
                drive_c_while_distract_c += 1
            else:
                distract_incorrect += 1
                drive_c_while_distract_i += 1
        else:
            drive_incorrect +=1
            if line["ConditionCorrectness"]:
                distract_correct += 1
                drive_i_while_distract_c += 1
            else:
                distract_incorrect += 1
                drive_i_while_distract_i += 1
    return [(drive_correct,drive_incorrect),(distract_correct,distract_incorrect),(drive_c_while_distract_c,drive_c_while_distract_i,drive_i_while_distract_c,drive_i_while_distract_i)]

def no_distr_only(data):
    # get amount of answered correctly driving questions vs answered incorrectly
    drive_correct = 0
    drive_incorrect = 0
    for line in data.iterrows():
        if line["Correctness"]:
            drive_correct += 1
        else:
            drive_incorrect += 1
    return (drive_correct,drive_incorrect)

def per_video(data): # individual driving videos
    total = 0
    # return False on first position if video has always been answered incorrectly, True otherwise

    # get amount of answered correctly driving with/without distraction vs answered incorrectly
    drive_con_correct = 0
    drive_no_con_correct = 0
    drive_con_incorrect = 0
    drive_no_con_incorrect = 0
    # return as second tuple in list

    # get amount of answered correctly distraction questions vs incorrectly
    distr_correct = 0
    distr_incorrect = 0
    # return as third tuple in list

    # get amount of answered correctly driving while distraction correctly vs driving correctly wwhile distraction incorrectly vs driving incorrectly while distraction correctly vs driving incorrectly while distraction incorrectly
    drive_c_distr_c = 0
    drive_c_distr_i = 0
    drive_i_distr_c = 0
    drive_i_distr_i = 0
    # return as last tuple in list

    for line in data.iterrows():
        total += 1
        if line["Correctness"] and line["Condition"] != "": # when there is a condition
            drive_con_correct += 1
            if line["ConditionCorrectness"]:
                distr_correct += 1
                drive_c_distr_c += 1
            else:
                distr_incorrect += 1
                drive_c_distr_i += 1
        elif line["Correctness"] and line["Condition"] == "": # when there is no condition
            drive_no_con_correct += 1
        elif not line["Correctness"] and line["Condition"] != "":
            drive_con_incorrect += 1
            if line["ConditionCorrectness"]:
                distr_correct += 1
                drive_i_distr_c += 1
            else:
                distr_incorrect += 1
                drive_i_distr_i += 1
        else:
            drive_no_con_incorrect += 1
    if total == drive_con_incorrect + drive_no_con_incorrect:
        keep = False
    else:
        keep = True
    return[keep,(drive_con_correct,drive_no_con_correct,drive_con_incorrect,drive_no_con_incorrect),(distr_correct,distr_incorrect),(drive_c_distr_c,drive_c_distr_i,drive_i_distr_c,drive_i_distr_i)]

def distraction_sample(data): # individual distraction items, remove ones that have always been answered wrong (too hard) or always been answered correctly (too easy) for second study
    total = 0 # count up for each row
    # return False on first tuple position of incorrect == total, True otherwise

    # get amount of answered correctly distraction questions vs incorrectly
    correct = 0
    incorrect = 0
    # return on second tuple position

    # get amount of answered correctly driving while distraction correctly vs driving correctly wwhile distraction incorrectly vs driving incorrectly while distraction correctly vs driving incorrectly while distraction incorrectly
    distr_c_driving_c = 0
    distr_c_driving_i = 0
    distr_i_drivint_c = 0
    distr_i_driving_i = 0
    # return on third tuple position

    for line in data.iterrows():
        total += 1 # count total amount of rows
        if line["ConditionCorrectness"]:
            correct += 1
            if line["Correctness"]:
                distr_c_driving_c += 1
            else:
                distr_c_driving_i += 1
        else:
            incorrect += 1
            if line["Correctness"]:
                distr_i_drivint_c += 1
            else:
                distr_i_driving_i += 1
    if incorrect == total:
        return (False,(correct,incorrect),(distr_c_driving_c,distr_c_driving_i,distr_i_driving_c,distr_i_driving_i))
    return (True,(correct,incorrect),(distr_c_driving_c,distr_c_driving_i,distr_i_driving_c,distr_i_driving_i))

def distraction_type(data): # if distraction is restaurant or video
    # get amount of answered correctly distraction questions vs incorrectly per type
    incorrect = 0
    correct = 0
    # return as first tuple position

    # get amount of answered correctly driving while distraction correctly vs driving correctly wwhile distraction incorrectly vs driving incorrectly while distraction correctly vs driving incorrectly while distraction incorrectly per type
    drive_c_distr_c = 0
    drive_c_distr_i = 0
    drive_i_distr_c = 0
    drive_i_distr_i = 0
    # return as second tuple position

    for line in data.iterrows():
        if line["Correctness"]:
            correct += 1
            if line["ConditionCorrectness"]:
                drive_c_distr_c += 1
            else:
                drive_c_distr_i += 1
        else:
            incorrect += 1
            if line["ConditionCorrectness"]:
                drive_i_distr_c += 1
            else:
                drive_i_distr_i += 1
    return ((correct,incorrect),(drive_c_distr_c,drive_c_distr_i,drive_i_distr_c,drive_i_distr_i))

def first_metric(data):
    pass

def second_metric(data):
    pass

def age_range(data):
    amount = 0

    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for line in data.iterrows():
        amount += 1
        if line["Correctness"]:
            correct += 1
            if line["ConditionCorrectness"]:
                correct_distr_c += 1
            else:
                correct_distr_i += 1
        else:
            incorrect += 1
            if line["ConditionCorrectness"]:
                incorrect_distr_c += 1
            else:
                incorrect_distr_i += 1
    return (amount,(correct,incorrect),(correct_distr_c,correct_distr_i,incorrect_distr_c,incorrect_distr_i))

def license_year(data):
    amount = 0

    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for line in data.iterrows():
        amount += 1
        if line["Correctness"]:
            correct += 1
            if line["ConditionCorrectness"]:
                correct_distr_c += 1
            else:
                correct_distr_i += 1
        else:
            incorrect += 1
            if line["ConditionCorrectness"]:
                incorrect_distr_c += 1
            else:
                incorrect_distr_i += 1
    return (amount,(correct,incorrect),(correct_distr_c,correct_distr_i,incorrect_distr_c,incorrect_distr_i))

def experience_range(data):
    pass

def personal_distractions(data):
    pass

def individual_participants(data): # mostly to find outliers
    pass

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
# for i in range(30): # 30 participants, change for different participant numbers
for i in range(20):
    subject_number.extend([additional_data.loc[i]["Subject Number"]]*11) # 11 items per participant
    age.extend([additional_data.loc[i]["Alter"]]*11)
    year.extend([additional_data.loc[i]["Jahr"]]*11)
    distractions.extend([additional_data.loc[i]["Ablenkungen transcription"]]*11)
    experience.extend([additional_data.loc[i]["Erfahrung transcription"]]*11)
data.assign(SubjectNumber=subject_number)
# data.assign("Subject Number"==subject_number)
data.assign("Age" == age)
data.assign("Year" == year)
data.assign("Distractions" == distractions)
data.assign("Experience" == experience)

participants = per_participant(data)
condition = per_condition(data)
video = per_video(data)
distraction_type = per_distraction_type(data)
age = by_age(data)
experience = by_experience(data)
year = by_year(data)
distraction = common_distraction(data)
distract_item = get_distraction_item(data)

(auditory_drive,auditory_distract,auditory_both) = condition_only(condition["auditory"])
(visual_drive,visual_distract,visual_both) = condition_only(condition["visual"])
# spaceholder for possible audiovisual
no_distr = no_distr_only(condition["no_con"])
# call per_video(data) for each individual driving video
all_videos = dict()
for key in video.keys():
    all_videos[key] = per_video(key) # (keep,(drive),(distract),(both))
# call distraction_sample(data) for each individual distraction item
all_distractions = dict()
for key in distract_item.keys():
    all_distractions[key] = distraction_sample(key) # (keep,drive,both)
types = []
for key in distraction_type.keys():
    types[key] = distraction_type(key) # (drive,both)
# (age_amount,age_drive,age_both) = age_range(age)
# (year_amount,year_drive,year_both) = license_year(year)