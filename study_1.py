import streamlit as st
import sys
import sqlite3
import random
import time
import pandas as pd
from playsound import playsound as ps
import numpy as np
import cv2
import os

def auditory(q): # pass dictionary with all information (q_results)
    # create item for exam question video
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/videos/")
    data = cv2.VideoCapture(q["Video"][len("videos/"):],apiPreference=0)
    s = st.button("Start Video",key="a"+q["Video"])
    if s:
        del s
        # play exam video
        while data.isOpened():
            ret, frame = data.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/")
                ps(q["ConditionFileAuditory"])
            # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        # Break the loop
            else:
                break
        data.release()
        # Closes all the frames
        cv2.destroyAllWindows()
    # form = st.form(key=q["Video"])
    confirm = st.checkbox(label="I confirm that I have watched the entire video.",value=False,key="ca"+q["Video"])
    # if confirm:
    #     del confirm
    cont = st.button("Weiter", key="wa"+q["Video"])
    if cont:
        del cont
        exam_q(q)
        distract_q(q)
    return q

def visual(q):
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/videos/")
    data = cv2.VideoCapture(q["Video"][len("videos/"):],apiPreference=0)
    # create item for distraction video
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/distraction_video/")
    vddata = cv2.VideoCapture(q["ConditionFileVisual"][len("distraction_video/"):],apiPreference=0)
    s = st.button("Start Video",key="svv"+q["Video"])
    if s:
        del s
        while data.isOpened():
            while vddata.isOpened():
                ret, frame = data.read()
                vret, vframe = vddata.read()
                if ret == True:
                    if vret == True:
                        cv2.imshow('Frame', frame)
                        cv2.imshow('Frame', vframe)
                    # Press Q on keyboard to exit
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                 # Break the loop
                    else:
                        break
                else:
                    break
                vddata.release()
                # When everything done, release
                # the video capture object
                data.release()
                # Closes all the frames
                cv2.destroyAllWindows()
    # form = st.form(key=q["Video"])
    confirm = st.checkbox(label="I confirm that I have watched the entire video.",value=False,key="cv"+q["Video"])
    # if confirm:
    #     del confirm
    cont = st.button("Weiter",key="wv"+q["Video"])
    if cont:
        del cont
        q = exam_q(q)
        q = distract_q(q)
    return q

def audiovisual(q):
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/videos/")
    data = cv2.VideoCapture(q["Video"][len("videos/"):],apiPreference=0)
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/distraction_videos/")
    vddata = cv2.VideoCapture(q["ConditionFileVisual"][len("distraction_videos/"):],apiPreference=0)
    s = st.button("Start Video",key="savv"+q["Video"])
    if s:
        del s
        while data.isOpened():
            while vddata.isOpened():
                ret, frame = data.read()
                vret, vframe = vddata.read()
                if ret == True:
                    if vret == True:
                        cv2.imshow('Frame', frame)
                        cv2.imshow('Frame', vframe)
                        ps(q["ConditionFileAuditory"])             
                    # Press Q on keyboard to exit
                        if cv2.waitKey(25) & 0xFF == ord('q'):
                            break
                 # Break the loop
                    else:
                        break
                else:
                    break
                vddata.release()
                # When everything done, release
                # the video capture object
                data.release()
                # Closes all the frames
                cv2.destroyAllWindows()
    # form = st.form(key=q["Video"])
    confirm = st.checkbox(label="I confirm that I have watched the entire video.",value=False,key="cav"+q["Video"])
    # if confirm:
    #     del confirm
    cont = st.button("Weiter",key="wav"+q["Video"])
    if cont:
        del cont
        q = exam_q(q)
        q = distract_q(q)
    return q

def comp(q): # without distractions
    # create item for exam question video
    os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/videos/")
    data = cv2.VideoCapture(q["Video"][len("videos/"):],apiPreference=0)
    s = st.button("Start Video",key="scv"+q["Video"])
    if s:
        del s
        # play exam video
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
    # form = st.form(key=q["Video"])
    confirm = st.checkbox(label="I confirm that I have watched the entire video.",value=False,key="cc"+q["Video"])
    if confirm:
        results = exam_q(q)
        submit = st.button("Weiter",key="wes"+data["Video"])
        if submit:
            del submit
            correct_results = []
            for item in [data["Answer A"][1],data["Answer B"][1],data["Answer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if results == correct_results:
                data["Correctness"] = True
            else:
                data["Correctness"] = False
    return q

def exam_q(data): # for answering the exam questions
    # form = st.form(key=data["Question"])
    st.write(data["Question"])
    a = st.checkbox(label=data["Answer A"][0],value=False,key="qa"+data["Video"])
    b = st.checkbox(label=data["Answer B"][0],value=False,key="qb"+data["Video"])
    if data["Answer C"] != "None":
        c = st.checkbox(label=data["Answer C"][0],value=False,key="qc"+data["Video"])
    else:
        c = None
    return [a,b,c]

def distract_q(data): # for answering the distraction questions
    # form = st.form(key=data["ConditionQuestion"])
    st.write(data["ConditionQuestion"])
    x = st.checkbox(label=data["DistractionAnswer A"][0],value=False,key="da"+data["Video"])
    y = st.checkbox(label=data["DistractionAnswer B"][0],value=False,key="db"+data["Video"])
    if data["DistractionAnswer C"][0] != "None":
        z = st.checkbox(label=data["DistractionAnswer C"][0],value=False,key="dc"+data["Video"])
    else:
        z = None
    submit = st.button("Weiter",key="wds")
    if submit:
        del submit
        correct_distraction_results = []
        for item in [data["DistractionAnswer A"][1], data["DistractionAnswer B"][1], data["DistractionAnswer C"][1]]:
            if item == "TRUE":
                correct_distraction_results.append(True)
            elif item == "FALSE":
                correct_distraction_results.append(False)
            elif item == "None":
                correct_distraction_results.append(None)
        if [x,y,z] == correct_distraction_results:
            data["ConditionCorrectness"] = True
        else:
            data["ConditionCorrectness"] = False
        del x
        del y
        del z
    return data

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
    "Time FLOAT )"
cursor.execute(s_sql)

os.chdir("C:/Users/Tili/Desktop/Uni/Master/study_1-data/")
exam_questions = pd.read_csv("videoquestions.csv",sep=";",encoding="utf-8",header=[0])
distraction_questions = pd.read_csv("distractionquestions.csv",sep=";",encoding="utf-8",header=[0])
with st.form(key="form"):
    condition = sys.argv[-1] # write condition when calling the file (auditory, visual, audiovisual)
    order = random.sample([x for x,y in exam_questions.iterrows()],len([x for x,y in exam_questions.iterrows()])) # randomize order of questions
    distractions = [x for x,y in distraction_questions.iterrows()]
    res = [(i,j) for i, j in zip(distractions[::2], distractions[1::2])] # pair rows with same question but different truth values in answers
    new = []
    for item in res:
        result = random.sample(list(item),2) # only keep one of the items, so that no participant has the same question twice
        new.append(result)
    distraction_order = random.sample(new,len(new))
    con = [True,True,True,True,True,True,True,True,False,False,False,False,False,False,False]
    condition_values = random.sample(con,len(con)) # 8 with distraction, 7 without
    condition_values = [False,True,False,True] + condition_values # four items (2 with 2 without distraction) for initialization
    for index in order:   
        current_results = []
        condition_value = condition_values[0]
        del condition_values[0]
        q_results = dict()
        q_results["Age"] = 0
        q_results["YearOfLicense"] = 0
        q_results["RegularityDriving"] = ""
        q_results["PersonalDistractors"] = ""
        q_results["Video"] = exam_questions.loc[index]["Filename"]
        q_results["Question"] = exam_questions.loc[index]["Question"]
        q_results["Answer A"] = (exam_questions.loc[index]["Answer A"], exam_questions.loc[index]["Correctness A"])
        q_results["Answer B"] = (exam_questions.loc[index]["Answer B"], exam_questions.loc[index]["Correctness B"])
        q_results["Answer C"] = (exam_questions.loc[index]["Answer C"], exam_questions.loc[index]["Correctness C"])
        if condition_value:
            q_results["Condition"] = condition
            q_results["ConditionFileAuditory"] = distraction_questions.loc[distraction_order[0][1]]["Filename Auditory"]
            q_results["ConditionFileVisual"] = distraction_questions.loc[distraction_order[0][1]]["Filename Visual"]
            q_results["ConditionQuestion"] = distraction_questions.loc[distraction_order[0][1]]["Question"]
            q_results["DistractionAnswer A"] = (distraction_questions.loc[distraction_order[0][1]]["Answer A"], distraction_questions.loc[distraction_order[0][1]]["Correctness A"])
            q_results["DistractionAnswer B"] = (distraction_questions.loc[distraction_order[0][1]]["Answer B"], distraction_questions.loc[distraction_order[0][1]]["Correctness B"])
            q_results["DistractionAnswer C"] = (distraction_questions.loc[distraction_order[0][1]]["Answer C"], distraction_questions.loc[distraction_order[0][1]]["Correctness C"])
        else:
            q_results["Condition"] = ""
            q_results["ConditionQuestion"] = None
        q_results["Correctness"] = None
        q_results["ConditionCorrectness"] = None
        q_results["Time"] = 0.0

        if condition_value and condition == "auditory":
            q_results = auditory(q_results)
        elif condition_value and condition == "visual":
            q_results = visual(q_results)
        elif condition_value and condition == "audiovisual":
            q_results = audiovisual(q_results)
        else: # when condition_value is False
            q_results = comp(q_results)
        # form = st.form(key=str(index))
        current_results.append(q_results)
    done = st.button("Fertig",key="done")
    if done: # at the end of the study after seeing all items
        del done
        # form = st.form(key="final")
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

        submit = st.form_submit_button("Submit") #,key="submit")
        if submit:
            del submit
            st.write("Vielen Dank für Ihre Teilnahme an der Studie. Bitte geben Sie der Studienleitung Bescheid.")
            connection.commit()
            connection.close()