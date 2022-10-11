import streamlit as st
import sys
import sqlite3
import random
import time
import pandas as pd
from playsound import playsound as ps
import numpy as np
import cv2

# TODO data gathering, testing

connection = sqlite3.connect("results.db") # databench for collected data
cursor = connection.cursor()
s_sql = "CREATE TABLE IF NOT EXISTS Study1( " \
    "Age INT, " \
    "YearOfLicense INT, " \
    "RegularityDriving TEXT, " \
    "PersonalDistractors TEXT, " \
    "Video TEXT, " \
    "Question TEXT, " \
    "Condition TEXT, " \
    "Correctness BOOL, " \
    "ConditionQuestion TEXT, " \
    "ConditionCorrectness BOOL, " \
    "Time FLOAT, )"
cursor.execute(s_sql)

filepath = "study_1-data/"
exam_questions = pd.read_csv(filepath+"videoquestions.csv",header=1)
distraction_questions = pd.read_csv(filepath+"distractionquestions.csv",header=1)
current_results = []
condition = sys.argv[-1] # write condition when calling the file (auditory, visual, audiovisual)
order = random(exam_questions.iterrows()) # randomize order of questions
distraction_order = random(distraction_questions.iterrows())
# maybe take distraction-determination out of this file and do separately, mirror participant-screen and start distraction when participant clicks "play"
condition_values = random([True,True,True,True,True,True,True,False,False,False,False,False,False,False,False]) # make it more likely to get a False than to get a True
for index,row in order:
    condition_value = condition_values[0]
    del condition_values[0]
    q_results = dict()
    q_results["Age"] = 0
    q_results["YearOfLicense"] = 0
    q_results["RegularityDriving"] = ""
    q_results["PersonalDistractors"] = ""
    q_results["Video"] = row["Filename"]
    q_results["Question"] = row["Question"]
    if condition_value:
        q_results["Condition"] = condition
        q_results["ConditionFileAuditory"] = distraction_order[0][1]["Filename Auditory"]
        q_results["ConditionFileVisual"] = distraction_order[0][1]["Filename Visual"]
        q_results["ConditionQuestion"] = distraction_order[0][1]["Question"]
    else:
        q_results["Condition"] = ""
        q_results["ConditionQuestion"] = None
    q_results["Correctness"] = None
    q_results["ConditionCorrectness"] = None
    q_results["Time"] = 0.0
    # video_file = open(item, 'rb')
    data = cv2.VideoCapture(q_results["Video"])
    if condition == "visual" or condition == "audiovisual":
        vddata = cv2.VideoCapture(q_results["ConditionFileVisual"])
    # data = video_file.read()
    s = st.button("Start Video")
    if s:
        while data.isOpened():
            ret, frame = data.read()
            if ret == True:
                cv2.imshow('Frame', frame)                
            # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        # Break the loop
            else:
                break
        # When everything done, release
        # the video capture object
        data.release()
        # Closes all the frames
        cv2.destroyAllWindows()
        # autoplay video st.video(data, format="video/mp4", start_time=0)
        if condition_value:
            if condition == "auditory":
                ps(q_results["ConditionFileAuditory"])
            elif condition == "audiovisual" or condition == "visual":
                if condition == "audiovisual":
                    ps(q_results["ConditionFileAuditory"])
                # autoplay visual distraction on second screen
                while vddata.isOpened():
                    ret, frame = vddata.read()
                    if ret == True:
                        cv2.imshow('Frame', frame)
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                    else:
                        break
                vddata.release()
                cv2.destroyAllWindows()
    confirm = st.checkbox(label="I confirm that I have watched the entire video.",value=False)
    if confirm:
        cont = st.button("Weiter")
        if cont:
            start=time.time()
            st.write(row["Question"])
            a = st.checkbox(label=row["Answer A"],value=False)
            b = st.checkbox(label=row["Answer B"],value=False)
            if row["Answer C"] != "None":
                c = st.checkbox(label=row["Answer C"],value=False)
            else:
                c = None
            st.write(q_results["ConditionQuestion"])
            x = st.checkbox(label=distraction_order[0][1]["Answer A"],value=False)
            y = st.checkbox(label=distraction_order[0][1]["Answer B"],value=False)
            if distraction_order[0][1]["Answer C"] != "None":
                z = st.checkbox(label=distraction_order[0][1]["Answer C"],value=False)
            else:
                z = None
            submit = st.button("Weiter")
            if submit:
                end=time.time()
                q_results["Time"] = end-start
                correct_results = []
                correct_distraction_results = []
                for item in [row["Correctness A"],row["Correctness B"],row["Correctness C"]]:
                    if item == "TRUE":
                        correct_results.append(True)
                    elif item == "FALSE":
                        correct_results.append(False)
                    elif item == "None":
                        correct_results.append(None)
                if [a,b,c] == correct_results:
                    q_results["Correctness"] = True
                else:
                    q_results["Correctness"] = False
                for item in [distraction_order[0][1]["Correctness A"], distraction_order[0][1]["Correctness B"], distraction_order[0][1]["Correctness C"]]:
                    if item == "TRUE":
                        correct_distraction_results.append(True)
                    elif item == "FALSE":
                        correct_distraction_results.append(False)
                    elif item == None:
                        correct_distraction_results.append(None)
                if [x,y,z] == correct_distraction_results:
                    q_results["ConditionCorrectness"] = True
                else:
                    q_results["ConditionCorrectness"] = False
                continue
    current_results.append(q_results)
done = st.button("Fertig")
if done:
    st.title("Bitte antworten Sie noch auf ein paar Fragen zu Ihrer Person.")
    age = int(st.text_input("Wie alt sind Sie?","0"))
    year_of_license = int(st.text_input("In welchem Jahr haben Sie ihren Führerschein erhalten?","0000"))
    regularity_driving = st.text_input("Wie häufig fahren Sie selbst Auto?","")
    personal_distractors = st.text_input("Wovon werden Sie leicht abgelenkt? (z.B. beim Auto fahren, beim Lernen, beim Arbeiten)","")

    for item in current_results:
        item["Age"] = age
        item["YearOfLicense"] = year_of_license
        item["RegularityDriving"] = regularity_driving
        item["PersonalDistractors"] = personal_distractors
        params = (item["Age"],item["YearOfLicense"],item["RegularityDriving"],item["PersonalDistractors"],item["Video"],item["Question"],item["Condition"],item["Correctness"],item["Time"])
        cursor.execute("INSERT INTO Study1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

    submit = st.button("Submit")
    if submit:
        st.write("Vielen Dank für Ihre Teilnahme an der Studie. Bitte geben Sie der Studienleitung Bescheid.")
        connection.commit()
        connection.close()