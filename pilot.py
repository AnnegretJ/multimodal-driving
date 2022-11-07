import sys
import sqlite3
import random
import time
import pandas as pd
import numpy as np
import os
import expyriment as xpy
import cv2

# initialize experiment
exp = xpy.design.Experiment(name="Pilot Study")
xpy.control.initialize(exp)


# functions for items
def auditory(q): # pass dictionary with all information (q_results)
    start = xpy.io.TextInput(message="Drücke 'Enter' auf der Tastatur um das Video zu starten")
    if start.get() == "":
        # play exam video
        # os.chdir("C:/Users/janzso/Desktop/multimodal-driving/study_1-data/videos")
        # data = cv2.VideoCapture(q["Video"][len("videos/"):],apiPreference=0)
        data = xpy.stimuli.Video("study_1-data/"+q["Video"],backend="mediadecoder")
        data.preload()
        # play audio
        sound = xpy.stimuli.Audio("study_1-data/"+q["ConditionFileAuditory"])
        sound.preload()
        sound.present()
        data.play()
        data.present()
        data.wait_end()
        data.stop()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter')")
    if confirm.get() == "":
        exam_q(q)
        distract_q(q)
        sub = xpy.io.TextInput(message="Weiter (Drücke 'Enter')")
        if sub.get() == "":
            correct_results = []
            for item in [q["Answer A"][1],q["Answer B"][1],q["Answer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if e_results == correct_results:
                q["Correctness"] = True
            else:
                q["Correctness"] = False
            correct_results = []
            for item in [q["DistractionAnswer A"][1],q["DistractionAnswer B"][1],q["DistractionAnswer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if d_results == correct_results:
                q["ConditionCorrectness"] = True
            else:
                q["ConditionCorrectness"] = False
    return q

def visual(q):
    start = xpy.io.TextInput(message="Video starten (Drücke 'Enter')")
    if start.get() == "":
        data = xpy.stimuli.Video("study_1-data/"+q["Video"])
        vdata = xpy.stimuli.Video("study_1-data/"+q["ConditionFileVisual"])
        data.preload()
        vdata.preload()
        data.play()
        vdata.play()
        data.present()
        vdata.present()
        data.wait_end()
        vdata.wait_end()
        data.stop()
        vdata.stop()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter')")
    if confirm.get() == "":
        exam_q(q)
        distract_q(q)
        sub = xpy.io.TextInput("Weiter (Drücke 'Enter')")
        if sub.get() == "":
            correct_results = []
            for item in [q["Answer A"][1],q["Answer B"][1],q["Answer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if e_results == correct_results:
                q["Correctness"] = True
            else:
                q["Correctness"] = False
            correct_results = []
            for item in [q["DistractionAnswer A"][1],q["DistractionAnswer B"][1],q["DistractionAnswer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if d_results == correct_results:
                q["ConditionCorrectness"] = True
            else:
                q["ConditionCorrectness"] = False
    return q

def audiovisual(q):
    start = xpy.io.TextInput(message="Video starten (Drücke 'Enter')")
    if start.get() == "":
        data = xpy.stimuli.Video("study_1-data/"+q["Video"])
        vdata = xpy.stimuli.Video("study_1-data/"+q["ConditionFileVisual"])
        sound = xpy.stimuli.Audio("study_1-data/"+q["ConditionFileAuditory"])
        data.preload()
        vdata.preload()
        sound.preload()
        sound.present()
        data.play()
        vdata.play()
        data.present()
        vdata.present()
        data.wait_end()
        vdata.wait_end()
        data.stop()
        vdata.stop()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter'")
    if confirm.get() == "":
        e_results = exam_q(q)
        d_results = distract_q(q)
        sub = xpy.io.TextInput(message="Weiter (Drücke 'Enter')")
        if sub.get() == "":
            correct_results = []
            for item in [q["Answer A"][1],q["Answer B"][1],q["Answer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if e_results == correct_results:
                q["Correctness"] = True
            else:
                q["Correctness"] = False
            correct_results = []
            for item in [q["DistractionAnswer A"][1],q["DistractionAnswer B"][1],q["DistractionAnswer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if d_results == correct_results:
                q["ConditionCorrectness"] = True
            else:
                q["ConditionCorrectness"] = False
    return q

def baseline(q): # without distractions
    # create item for exam question video
    start = xpy.io.TextInput(message="Drücke 'Enter' auf der Tastatur um das Video zu starten")
    if start.get() == "":
        # play exam video
        data = xpy.stimuli.Video("study_1-data/"+q["Video"],backend="mediadecoder")
        data.preload()
        data.play()
        data.present()
        data.wait_end()
        data.stop()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter')")
    if confirm.get() == "":
        results = exam_q(q)
        sub = xpy.io.TextInput("Weiter (Drücke 'Enter')")
        if sub.get() == "":
            correct_results = []
            for item in [q["Answer A"][1],q["Answer B"][1],q["Answer C"][1]]:
                if item == "TRUE":
                    correct_results.append(True)
                elif item == "FALSE":
                    correct_results.append(False)
                elif item == "None":
                    correct_results.append(None)
            if results == correct_results:
                q["Correctness"] = True
            else:
                q["Correctness"] = False
    return q

# questionnaire
def exam_q(data): # for answering the exam questions
    if data["Answer C"][0] != None:
        questions = "\n 1   " + data["Answer A"][0] + "\n 2   " + data["Answer B"][0] + "\n 3  " + data["Answer C"][0]
    else:
        questions = "\n 1   " + data["Answer A"][0] + "\n 2   " + data["Answer B"][0]
    info = xpy.stimuli.TextBox(text = "Bitte schreibe die Nummern der richtigen Antworten in das Textfeld und bestätige mit 'Enter'." + questions,size=(500,500))
    info.preload()
    question = xpy.io.TextInput("")
    info.present()
    exp.clock.wait(10000)
    reply = question.get()
    out = []
    if "1" in reply:
        out.append(True)
    else:
        out.append(False)
    if "2" in reply:
        out.append(True)
    else:
        out.append(False)
    if data["Answer C"][0] != None:
        if "3" in reply:
            out.append(True)
        else:
            out.append(False)
    else:
        out.append(None)
    return out

def distract_q(data): # for answering the distraction questions
    question = xpy.stimuli.TextScreen("",data["ConditionQuestion"])
    answer_x = xpy.stimuli.TextScreen("",data["DistractionAnswer A"][0])
    x = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP"))
    answer_y = xpy.stimuli.TextScreen("",data["DistractionAnswer B"][0])
    y = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP"))
    if data["DistractionAnswer C"] != "None":
        answer_z = xpy.stimuli.TextScreen("",data["DistractionAnswer C"][0])
        z = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP"))
    else:
        z = None
    n = xpy.stimuli.TextScreen("","Weiter")
    n_button = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP"))
    if n_button != None:
        return [x,y,z]


# create databench
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
xpy.control.start()
# read and sort data
# os.chdir("C:/Users/janzso/Desktop/multimodal-driving/study_1-data")
exam_questions = pd.read_csv("study_1-data/videoquestions.csv",sep=";",encoding="utf-8",header=[0])
distraction_questions = pd.read_csv("study_1-data/distractionquestions.csv",sep=";",encoding="utf-8",header=[0])
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
condition_values = [True,False,True,False] + condition_values # four items (2 with 2 without distraction) for initialization
for index in order:   
    current_results = []
    condition_value = condition_values.pop()
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

    # call functions for samples
    if condition_value and condition == "auditory":
        q_results = auditory(q_results)
    elif condition_value and condition == "visual":
        q_results = visual(q_results)
    elif condition_value and condition == "audiovisual":
        q_results = audiovisual(q_results)
    else: # when condition_value is False
        q_results = baseline(q_results)
    current_results.append(q_results)

# button when Done
done = xpy.stimuli.TextScreen("","Drücken Sie '1', wenn Sie fertig sind.")
# done_button = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP")) # alternatively try xpy.io.ParallelPort
done_button = exp.keyboard.check(1)
# if done_button.check() != None:
if done_button == 1:
    exp.keyboard.clear()
    title = xpy.stimuli.TextScreen("","Bitte antworten Sie noch auf ein paar Fragen zu Ihrer Person.")
    age = xpy.io.TextInput(message="Wie alt sind Sie?",default_input=int)
    year_of_license = xpy.io.TextInput(message="In welchem Jahr haben Sie ihren Führerschein erhalten?",default_input=int)
    regularity_driving = xpy.io.TextInput(message="Wie häufig fahren Sie selbst Auto?",default_input=str)
    personal_distractors = xpy.io.TextInput("Wovon werden Sie leicht abgelenkt? (z.B. beim Auto fahren, beim Lernen, beim Arbeiten)",default_input=str)
    for item in current_results:
        item["Age"] = age
        item["YearOfLicense"] = year_of_license
        item["RegularityDriving"] = regularity_driving
        item["PersonalDistractors"] = personal_distractors
        params = (item["Age"],item["YearOfLicense"],item["RegularityDriving"],item["PersonalDistractors"],item["Video"],item["Question"],item["Condition"],item["Correctness"],item["Time"])
        cursor.execute("INSERT INTO Study1 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
    submit = xpy.stimuli.TextScreen("","Drücken Sie '1', um die Studie zu beenden.")
    # submit_button = xpy.io.EventButtonBox(interface=xpy.io.SerialPort("TCP")) # alternatively try xpy.io.ParallelPort
    submit_button = exp.keyboard.check(1)
    # if submit_button.check() != None:
    if submit_button == 1:
        exp.keyboard.clear()
        final = xpy.stimuli.TextScreen("","Vielen Dank für Ihre Teilnahme an der Studie. Bitte geben Sie der Studienleitung Bescheid.")
        connection.commit()
        connection.close()
        xpy.control.end()