import sqlite3
import pandas as pd
from collections import defaultdict

def per_participant(discard,data): # sort data per participant
    participants = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard:
            continue # skip if Video was always answered incorrectly
        else:
            value = line["SubjectNumber"]
            participants[value].append(line)
    return participants # return dictionary of subject number mapped with the according part of the dataframe

def per_condition(discard,data): # sort data per condition
    condition = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard:
            continue
        if line["Condition"] == "auditory":
            condition["auditory"].append(line)
        elif line["Condition"] == "visual":
            condition["visual"].append(line)
        else:
            condition["no_con"].append(line)
    return condition # return dictionary of condition mapped with the according part of the dataframe

def per_video(data): # sort data per video
    video = dict()
    #video["Yqe62JAmjMI_7_31.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_7_31.mp4"] # all false
    video["Yqe62JAmjMI_30_21.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_30_21.5.mp4"]
    video["Yqe62JAmjMI_31_21.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_31_21.mp4"]
    video["Yqe62JAmjMI_38_13.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_38_13.mp4"]
    video["Yqe62JAmjMI_43_21.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_43_21.5.mp4"]
    #video["Yqe62JAmjMI_53_50.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_53_50.5.mp4"] # all false
    video["Yqe62JAmjMI_59_08.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_59_08.5.mp4"]
    video["9xY9S3LV69k_9_45.5.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_9_45.5.mp4"]
    video["9xY9S3LV69k_12_29.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_12_29.mp4"]
    video["9xY9S3LV69k_21_40.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_21_40.mp4"]
    video["9xY9S3LV69k_26_29.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_26_29.mp4"]
    video["GYhPr8RyvZU_3_03.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_3_03.5.mp4"]
    video["GYhPr8RyvZU_14_00.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_14_00.5.mp4"]
    #video["GYhPr8RyvZU_16_34.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_16_34.mp4"] # all false
    #video["GYhPr8RyvZU_19_37.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_19_37.5.mp4"] # all false
    video["GYhPr8RyvZU_21_32.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_21_32.mp4"]
    video["GYhPr8RyvZU_23_14.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_23_14.mp4"]
    video["GYhPr8RyvZU_1_03_56.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_1_03_56.5.mp4"]
    video["GYhPr8RyvZU_1_07_02.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_1_07_02.mp4"]
    return video # return dictionary of videos mapped with the according part of the dataframe

def per_distraction_type(discard,data): # sort by wether the distraction was about the weather or a restaurant
    distraction_type = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard or type(line["ConditionQuestion"]) != str:
            continue 
        if "Restaurant" in line["ConditionQuestion"]:
            distraction_type["Restaurant"].append(line)
        else:
            distraction_type["Wetter"].append(line)
    return distraction_type # return dictionary of distraction-type (restaurant or weather) mapped with the according part of the dataframe

def by_age(discard,data): # sort by participant age
    age = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard: # if current value has already been sorted by
            continue
        else:
            value = line["Age"]
            age[value].append(line)
    return age

def by_experience(discard,data): # sort by driving experience
    experience = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard:
            continue
        experience[line["Experience"]].append(line)
    #     for value in line["Experience"]:
    #         print(line["Experience"])
    #         experience[value].append(line)
    # print(experience)
    return experience

def by_year(discard,data): # sort by year when license has been received
    year = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard:
            continue
        value = line["Year"]
        year[value].append(line)
    return year

def common_distraction(discard,data): # sort by common distractions
    distraction = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard or type(line["Distractions"]) != str:
            continue
        for value in line["Distractions"].split(","):
            distraction[value].append(line)
    return distraction

def get_distraction_item(discard,data): # sort by individual distraction item (independent of distraction type)
    dis_item = defaultdict(list)
    for index,line in data.iterrows():
        if line["Video"] in discard:
            continue
        dis_item[line["ConditionQuestion"]].append(line)
    return dis_item

if __name__ == "__main__":
    conn = sqlite3.connect("results.db")
    data = pd.read_sql("SELECT * from Study1",conn)
    # Video Question Condition Correctness ConditionQuestion ConditionCorrectness
    additional_data = pd.read_csv("study_1-data/additional_results.csv",sep=";",encoding="utf-8",header=[0]) # get data for age etc.
    subject_number = []
    age = []
    year = []
    distractions = []
    experience = []
    for i in range(20): # 20 participants
        subject_number.extend([additional_data.loc[i]["Subject Number"]]*11)
        age.extend([additional_data.loc[i]["Alter"]]*11)
        year.extend([additional_data.loc[i]["Jahr"]]*11)
        distractions.extend([additional_data.loc[i]["Ablenkungen transcription"]]*11)
        experience.extend([additional_data.loc[i]["Erfahrung transcription"]]*11)
    # print(len({"Subject Number":subject_number}))
    # print(subject_number)
    # print(data)
    data.assign(SubjectNumber=subject_number)
    data.assign(Age=age)
    data.assign(Year=year)
    data.assign(Distractions=distractions)
    data.assign(Experience=experience)