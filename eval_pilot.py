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

    for index,line in data.iterrows():
        if line["Correctness"]:
            drive_correct +=1
            if line["ConditionCorrectness"] == True:
                distract_correct += 1
                drive_c_while_distract_c += 1
            elif line["ConditionCorrectness"] == False:
                distract_incorrect += 1
                drive_c_while_distract_i += 1
        else:
            drive_incorrect +=1
            if line["ConditionCorrectness"] == True:
                distract_correct += 1
                drive_i_while_distract_c += 1
            elif line["ConditionCorrectness"] == False:
                distract_incorrect += 1
                drive_i_while_distract_i += 1
    return [(drive_correct,drive_incorrect),(distract_correct,distract_incorrect),(drive_c_while_distract_c,drive_c_while_distract_i,drive_i_while_distract_c,drive_i_while_distract_i)]

def no_distr_only(data):
    # get amount of answered correctly driving questions vs answered incorrectly
    drive_correct = 0
    drive_incorrect = 0
    for index,line in data.iterrows():
        if line["Correctness"]:
            drive_correct += 1
        else:
            drive_incorrect += 1
    return (drive_correct,drive_incorrect)

def video_item(data): # individual driving videos
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

    for index,line in data.iterrows():
        total += 1
        if line["Correctness"] and line["Condition"] != "": # when there is a condition
            drive_con_correct += 1
            if line["ConditionCorrectness"] == True:
                distr_correct += 1
                drive_c_distr_c += 1
            elif line["ConditionCorrectness"] == False:
                distr_incorrect += 1
                drive_c_distr_i += 1
        elif line["Correctness"] and line["Condition"] == "": # when there is no condition
            drive_no_con_correct += 1
        elif not line["Correctness"] and line["Condition"] != "":
            drive_con_incorrect += 1
            if line["ConditionCorrectness"] == True:
                distr_correct += 1
                drive_i_distr_c += 1
            elif line["ConditionCorrectness"] == False:
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
    distr_i_driving_c = 0
    distr_i_driving_i = 0
    # return on third tuple position

    for index,line in data.iterrows():
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
                distr_i_driving_c += 1
            else:
                distr_i_driving_i += 1
    if incorrect == total:
        return (False,(correct,incorrect),(distr_c_driving_c,distr_i_driving_c,distr_c_driving_i,distr_i_driving_i))
    return (True,(correct,incorrect),(distr_c_driving_c,distr_i_driving_c,distr_c_driving_i,distr_i_driving_i))

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

    for index,line in data.iterrows():
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
    result = 0
    comp = 0
    for index,line in data.iterrows():
        if line["Condition"] != "" and not line["Correctness"]:
            result += 1
        elif line["Condition"] != "" and line["Correctness"]:
            result -= 1
        elif line["Condition"] == "" and line["Correctness"]:
            comp += 1
        else:
            comp -= 1
    return result - comp

def second_metric(data):
    result = 0
    for index,line in data.iterrows():
        if line["Condition"] != "":
            if not line["Correctness"] and line["ConditionCorrectness"]:
                result += 1
            elif line["Correctness"] and not line["ConditionCorrectness"]:
                result -= 1
    return result

def age_range(data):
    amount = 0

    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for index,line in data.iterrows():
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

    for index,line in data.iterrows():
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
    amount = 0

    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for index,line in data.iterrows():
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

def personal_distractions(data):
    amount = 0

    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for index,line in data.iterrows():
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

def individual_participants(data): # mostly to find outliers
    correct = 0
    incorrect = 0

    correct_distr_c = 0
    correct_distr_i = 0
    incorrect_distr_c = 0
    incorrect_distr_i = 0

    for index,line in data.iterrows():
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
    return ((correct,incorrect),(correct_distr_c,correct_distr_i,incorrect_distr_c,incorrect_distr_i))

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
data["Subject Number"] = subject_number
data["Age"] = age
data["Year"] = year
data["Distractions"] = distractions
data["Experience"] = experience

participants = per_participant(data)
condition = per_condition(data)
video = per_video(data)
distraction_form = per_distraction_type(data)
age = by_age(data)
experience = by_experience(data)
year = by_year(data)
distraction = common_distraction(data)
distract_item = get_distraction_item(data)

results = dict()

results["auditory"] = dict()
results["auditory"]["drive"] = dict()
results["auditory"]["distract"] = dict()
results["auditory"]["both"] = dict()
(auditory_drive,auditory_distract,auditory_both) = condition_only(condition["auditory"])
results["auditory"]["drive"]["c"] = auditory_drive[0]
results["auditory"]["drive"]["i"] = auditory_drive[1]
results["auditory"]["distract"]["c"] = auditory_distract[0]
results["auditory"]["distract"]["i"] = auditory_distract[1]
results["auditory"]["both"]["cc"] = auditory_both[0]
results["auditory"]["both"]["ci"] = auditory_both[1]
results["auditory"]["both"]["ic"] = auditory_both[2]
results["auditory"]["both"]["ii"] = auditory_both[3]

results["visual"] = dict()
results["visual"]["drive"] = dict()
results["visual"]["distract"] = dict()
results["visual"]["both"] = dict()
(visual_drive,visual_distract,visual_both) = condition_only(condition["visual"])
results["visual"]["drive"]["c"] = visual_drive[0]
results["visual"]["drive"]["i"] = visual_drive[1]
results["visual"]["distract"]["c"] = visual_distract[0]
results["visual"]["distract"]["i"] = visual_distract[1]
results["visual"]["both"]["cc"] = visual_both[0]
results["visual"]["both"]["ci"] = visual_both[1]
results["visual"]["both"]["ic"] = visual_both[2]
results["visual"]["both"]["ii"] = visual_both[3]

results["no_distr"] = dict()
results["no_distr"]["drive"] = dict()
no_distr = no_distr_only(condition["no_con"])
results["no_distr"]["drive"]["c"] = no_distr[0]
results["no_distr"]["drive"]["i"] = no_distr[1]

# call per_video(data) for each individual driving video
for key in video:
    results["Video " + key] = dict()
    results["Video " + key]["drive"] = dict()
    results["Video " + key]["distract"] = dict()
    results["Video " + key]["both"] = dict()
    results["Video " + key]["keep"] = dict()
    current = video_item(video[key]) # (keep,(drive),(distract),(both))
    results["Video " + key]["keep"]["Y/N"] = current[0]
    results["Video " + key]["drive"]["c"] = current[1][0]
    results["Video " + key]["drive"]["i"] = current[1][1]
    results["Video " + key]["distract"]["c"] = current[2][0]
    results["Video " + key]["distract"]["i"] = current [2][1]
    results["Video " + key]["both"]["cc"] = current[3][0]
    results["Video " + key]["both"]["ci"] = current[3][1]
    results["Video " + key]["both"]["ic"] = current[3][2]
    results["Video " + key]["both"]["ii"] = current[3][3]

# call distraction_sample(data) for each individual distraction item
for key in distract_item.keys():
    if key != None:
        results["Distraction " + key] = dict()
        results["Distraction " + key]["keep"] = dict()
        results["Distraction " + key]["drive"] = dict()
        results["Distraction " + key]["distract"] = dict()
        results["Distraction " + key]["both"] = dict()
        (keep,drive,both) = distraction_sample(distract_item[key]) # (keep,drive,both)
        results["Distraction " + key]["keep"]["Y/N"] = keep
        results["Distraction " + key]["drive"]["c"] = drive[0]
        results["Distraction " + key]["drive"]["i"] = drive[1]
        results["Distraction " + key]["distract"]["c"] = both[0] + both[2]
        results["Distraction " + key]["distract"]["i"] = both[1] + both[3]
        results["Distraction " + key]["both"]["cc"] = both[0]
        results["Distraction " + key]["both"]["ci"] = both[1]
        results["Distraction " + key]["both"]["ic"] = both[2]
        results["Distraction " + key]["both"]["ii"] = both[3]

for key in distraction_form.keys():
    results["Type " + key] = dict()
    results["Type " + key]["drive"] = dict()
    results["Type " + key]["distract"] = dict()
    results["Type " + key]["both"] = dict()
    (drive,both) = distraction_type(distraction_form[key]) # (drive,both)
    results["Type " + key]["drive"]["c"] = drive[0]
    results["Type " + key]["drive"]["i"] = drive[1]
    results["Type " + key]["distract"]["c"] = both[0] + both[2]
    results["Type " + key]["distract"]["i"] = both[1] + both[3]
    results["Type " + key]["both"]["cc"] = both[0]
    results["Type " + key]["both"]["ci"] = both[1]
    results["Type " + key]["both"]["ic"] = both[2]
    results["Type " + key]["both"]["ii"] = both[3]

for key in age.keys():
    key = str(key)
    results["Age " + key] = dict()
    results["Age " + key]["amount"] = dict()
    results["Age " + key]["drive"] = dict()
    results["Age " + key]["distract"] = dict()
    results["Age " + key]["both"] = dict()
    (amount,drive,both) = age_range(age[int(key)]) # (amount,drive,both)
    results["Age " + key]["amount"]["num"] = amount
    results["Age " + key]["drive"]["c"] = drive[0]
    results["Age " + key]["drive"]["i"] = drive[1]
    results["Age " + key]["distract"]["c"] = both[0] + both[2]
    results["Age " + key]["distract"]["i"] = both[1] + both[3]
    results["Age " + key]["both"]["cc"] = both[0]
    results["Age " + key]["both"]["ci"] = both[1]
    results["Age " + key]["both"]["ic"] = both[2]
    results["Age " + key]["both"]["ii"] = both[3]

for key in year.keys():
    key = str(key)
    results["Year " + key] = dict()
    results["Year " + key]["amount"] = dict()
    results["Year " + key]["drive"] = dict()
    results["Year " + key]["distract"] = dict()
    results["Year " + key]["both"] = dict()
    (amount,drive,both) = license_year(year[int(key)])
    results["Year " + key]["amount"]["num"] = amount
    results["Year " + key]["drive"]["c"] = drive[0]
    results["Year " + key]["drive"]["i"] = drive[1]
    results["Year " + key]["distract"]["c"] = both[0] + both[2]
    results["Year " + key]["distract"]["i"] = both[1] + both[3]
    results["Year " + key]["both"]["cc"] = both[0]
    results["Year " + key]["both"]["ci"] = both[1]
    results["Year " + key]["both"]["ic"] = both[2]
    results["Year " + key]["both"]["ii"] = both[3]

for key in experience.keys():
    results["Experience " + key] = dict()
    results["Experience " + key]["amount"] = dict()
    results["Experience " + key]["drive"] = dict()
    results["Experience " + key]["distract"] = dict()
    results["Experience " + key]["both"] = dict()
    (amount,drive,both) = experience_range(experience[key])
    results["Experience " + key]["amount"]["num"] = amount
    results["Experience " + key]["drive"]["c"] = drive[0]
    results["Experience " + key]["drive"]["i"] = drive[1]
    results["Experience " + key]["distract"]["c"] = both[0] + both[2]
    results["Experience " + key]["distract"]["i"] = both[1] + both[3]
    results["Experience " + key]["both"]["cc"] = both[0]
    results["Experience " + key]["both"]["ci"] = both[1]
    results["Experience " + key]["both"]["ic"] = both[2]
    results["Experience " + key]["both"]["ii"] = both[3]

for key in participants.keys():
    key = str(key)
    results["Participant " + key] = dict()
    results["Participant " + key]["drive"] = dict()
    results["Participant " + key]["distract"] = dict()
    results["Participant " + key]["both"] = dict()
    (drive,both) = individual_participants(participants[int(key)])
    results["Participant " + key]["drive"]["c"] = drive[0]
    results["Participant " + key]["drive"]["i"] = drive[1]
    results["Participant " + key]["distract"]["c"] = both[0] + both[2]
    results["Participant " + key]["distract"]["i"] = both[1] + both[2]
    results["Participant " + key]["both"]["cc"] = both[0]
    results["Participant " + key]["both"]["ci"] = both[1]
    results["Participant " + key]["both"]["ic"] = both[2]
    results["Participant " + key]["both"]["ii"] = both[3]
    
for key in distraction.keys():
    if type(key) == str: # avoid nan
        results["PersDis " + key] = dict()
        results["PersDis " + key]["amount"] = dict()
        results["PersDis " + key]["drive"] = dict()
        results["PersDis " + key]["distract"] = dict()
        results["PersDis " + key]["both"] = dict()
        (amount,drive,both) = personal_distractions(distraction[key])
        results["PersDis " + key]["amount"]["num"] = amount
        results["PersDis " + key]["drive"]["c"] = drive[0]
        results["PersDis " + key]["drive"]["i"] = drive[1]
        results["PersDis " + key]["distract"]["c"] = both[0] + both[2]
        results["PersDis " + key]["distract"]["i"] = both[1] + both[3]
        results["PersDis " + key]["both"]["cc"] = both[0]
        results["PersDis " + key]["both"]["ci"] = both[1]
        results["PersDis " + key]["both"]["ic"] = both[2]
        results["PersDis " + key]["both"]["ii"] = both[3]

results["metric_one"] = dict()
results["metric_two"] = dict()
results["metric_one"]["auditory"] = {"a1":first_metric(condition["auditory"])}
results["metric_one"]["visual"] =  {"v1":first_metric(condition["visual"])}
results["metric_one"]["all"] = {"all1":first_metric(data)}
results["metric_two"]["auditory"] = {"a2":second_metric(condition["auditory"])}
results["metric_two"]["visual"] = {"v2":second_metric(condition["visual"])}
results["metric_two"]["all"] = {"all2":second_metric(data)}

frame = pd.DataFrame.from_dict(results)
frame.to_csv("eval_results.csv",sep=";",encoding="utf-8")