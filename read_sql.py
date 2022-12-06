import sqlite3
import pandas as pd

def per_participant(data): # sort data per participant
    participants = dict()
    for value in data["Subject Number"]:
        if value in participants.keys():
            continue
        participants[value] = data.loc[data["Subject Number"] == value]
    return participants # return dictionary of subject number mapped with the according part of the dataframe
    # participants = dict()
    # for i in range(1,31): # 30 participants, starting with number 1
    #     participants[i] = data.loc[data["Subject Number"] == str(i)]
    # return participants 

def per_condition(data): # sort data per condition
    condition = dict()
    condition[auditory] = data.loc[data['Condition'] == "auditory"] # get all rows with auditory distraction
    condition[visual] = data.loc[data['Condition'] == "visual"]
    condition[audiovisual] = data.loc[data['Condition'] == "audiovisual"]
    condition[no_con] = data.loc[data['Condition'] == ""]
    return condition # return dictionary of condition mapped with the according part of the dataframe

def per_video(data): # sort data per video
    video = dict()
    video["Yqe62JAmjMI_7_31.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_7_31.mp4"]
    video["Yqe62JAmjMI_30_21.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_30_21.5.mp4"]
    video["Yqe62JAmjMI_31_21.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_31_21.mp4"]
    video["Yqe62JAmjMI_38_13.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_38_13.mp4"]
    video["Yqe62JAmjMI_43_21.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_43_21.5.mp4"]
    video["Yqe62JAmjMI_53_50.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_53_50.5.mp4"]
    video["Yqe62JAmjMI_59_08.5.mp4"] = data.loc[data['Video'] == "videos/Yqe62JAmjMI_59_08.5.mp4"]
    video["9xY9S3LV69k_9_45.5.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_9_45.5.mp4"]
    video["9xY9S3LV69k_12_29.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_12_29.mp4"]
    video["9xY9S3LV69k_21_40.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_21_40.mp4"]
    video["9xY9S3LV69k_26_29.mp4"] = data.loc[data['Video'] == "videos/9xY9S3LV69k_26_29.mp4"]
    video["GYhPr8RyvZU_3_03.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_3_03.5.mp4"]
    video["GYhPr8RyvZU_14_00.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_14_00.5.mp4"]
    video["GYhPr8RyvZU_16_34.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_16_34.mp4"]
    video["GYhPr8RyvZU_19_37.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_19_37.5.mp4"]
    video["GYhPr8RyvZU_21_32.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_21_32.mp4"]
    video["GYhPr8RyvZU_23_14.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_23_14.mp4"]
    video["GYhPr8RyvZU_1_03_56.5.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_1_03_56.5.mp4"]
    video["GYhPr8RyvZU_1_07_02.mp4"] = data.loc[data['Video'] == "videos/GYhPr8RyvZU_1_07_02.mp4"]
    return video # return dictionary of videos mapped with the according part of the dataframe

def per_distraction_type(data): # sort by wether the distraction was about the weather or a restaurant
    distraction_type = dict()
    distraction_type["Restaurant"] = data.loc[data["ConditionQuestion"].str.contains("Restaurant")] # all questions that contain the word "Restaurant"
    distraction_type["Wetter"] = data.loc[~data["ConditionQuestion"].str.contains("Restaurant")] # all questions that do not contain the word "Restaurant"
    return distraction_type # return dictionary of distraction-type (restaurant or weather) mapped with the according part of the dataframe

def by_age(data): # sort by participant age
    age = dict()
    for value in data["Age"]:
        if value in age.keys(): # if current value has already been sorted by
            continue
        age[value] = data.loc[data["Age"] == value]
    return age

def by_experience(data): # sort by driving experience
    experience = dict()
    for value in data["Experience"]:
        if value in experience.keys():
            continue
        experience[value] = data.loc[data["Experience"] == value]
    return experience

def by_year(data): # sort by year when license has been received
    year = dict()
    for value in data["Year"]:
        if value in year.keys():
            continue
        year[value] = data.loc[data["Year"] == value]
    return year

def common_distraction(data): # sort by common distractions
    distraction = dict()
    for value in data["Distractions"]:
        if value in distraction.keys():
            continue
        distraction[value] = data.loc[data["Distractions"] == value]
    return distraction

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
    for i in range(12):# range(30): # 30 participants
        subject_number.extend([additional_data.loc[i]["Subject Number"]]*13)
        age.extend([additional_data.loc[i]["Alter"]]*13)
        year.extend([additional_data.loc[i]["Jahr"]]*13)
        distractions.extend([additional_data.loc[i]["Ablenkungen transcription"]]*13)
        experience.extend([additional_data.loc[i]["Erfahrung transcription"]]*13)
    print(type({"Subject Number":subject_number}))
    print(list(data["ConditionCorrectness"]))
    print(list(data["Correctness"]))
    print(list(data["Condition"]))
    data.assign({"Subject Number":subject_number})
    data.assign({"Age":age})
    data.assign({"Year":year})
    data.assign({"Distractions":distractions})
    data.assign({"Experience":experience})