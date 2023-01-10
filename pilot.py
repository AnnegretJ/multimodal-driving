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
# main_screen = xpy.io.Screen(colour=(0,0,0),open_gl=True,window_mode=True,window_size=(1550,800),no_frame=False)
# distraction-screen is the current screen/laptop screen, have projector-screen as first display in settings!

# functions for items
def auditory(q): # pass dictionary with all information (q_results)
    start = xpy.io.TextInput(message="Drücke 'Enter' auf der Tastatur um das Video zu starten")
    if type(start.get()) == str:
        # play exam video
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
    if type(confirm.get()) == str:
        e_results = exam_q(q)
        d_results = distract_q(q)
        sub = xpy.io.TextInput(message="Weiter (Drücke 'Enter')")
        if type(sub.get()) == str:
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
    if type(start.get()) == str:
        data = xpy.stimuli.Video("study_1-data/"+q["Video"],backend="mediadecoder")
        data.preload()
        data.play()
        data.present()
        cap2 = cv2.VideoCapture("study_1-data/"+q["ConditionFileVisual"])
        while cap2.isOpened() or data.is_playing:
            data.update()
            okay2 , frame2 = cap2.read()
            if okay2:
                cv2.imshow('distract' , frame2)
                cv2.setWindowProperty("distract", cv2.WND_PROP_TOPMOST, 1) # same for "distract"
                cv2.resizeWindow("distract",1510,815)
                cv2.moveWindow("distract", 1540, 0)
            if not okay2:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(1)
        cap2.release()
        data.stop()
        cv2.destroyAllWindows()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter')")
    if type(confirm.get()) == str:
        e_results = exam_q(q)
        d_results = distract_q(q)
        sub = xpy.io.TextInput("Weiter (Drücke 'Enter')")
        if type(sub.get()) == str:
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
                # elif item == "None":
                #     correct_results.append(None)
            if d_results == correct_results:
                q["ConditionCorrectness"] = True
            else:
                q["ConditionCorrectness"] = False
    return q

def audiovisual(q):
    start = xpy.io.TextInput(message="Video starten (Drücke 'Enter')")
    if type(start.get()) == str:
        data = xpy.stimuli.Video("study_1-data/"+q["Video"],backend="mediadecoder")
        sound = xpy.stimuli.Audio("study_1-data/"+q["ConditionFileAuditory"])
        sound.preload()
        sound.present()
        data.preload()
        data.play()
        data.present()
        cap2 = cv2.VideoCapture("study_1-data/"+q["ConditionFileVisual"])
        while cap2.isOpened() or data.is_playing:
            data.update()
            okay2 , frame2 = cap2.read()
            if okay2:
                cv2.imshow('distract' , frame2)
                cv2.setWindowProperty("distract", cv2.WND_PROP_TOPMOST, 1) # same for "distract"
                cv2.resizeWindow("distract",1510,815)
                cv2.moveWindow("distract", 1540, 0)
            if not okay2:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(1)
        cap2.release()
        data.stop()
        cv2.destroyAllWindows()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter'")
    if type(confirm.get()) == str:
        e_results = exam_q(q)
        d_results = distract_q(q)
        sub = xpy.io.TextInput(message="Weiter (Drücke 'Enter')")
        if type(sub.get()) == str:
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
    if type(start.get()) == str:
        # play exam video
        data = xpy.stimuli.Video("study_1-data/"+q["Video"],backend="mediadecoder")
        data.preload()
        data.play()
        data.present()
        data.wait_end()
        data.stop()
    confirm = xpy.io.TextInput(message="Ich bestätige, dass ich das gesamte Video angesehen habe. (Drücke 'Enter')")
    if type(confirm.get()) == str:
        results = exam_q(q)
        sub = xpy.io.TextInput("Weiter (Drücke 'Enter')")
        if type(sub.get()) == str:
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
    if data["Answer C"][1] != "NONE":
        questions = "\n" + data["Question"] + "\n\n 1   " + data["Answer A"][0] + "\n 2   " + data["Answer B"][0] + "\n 3  " + data["Answer C"][0]
    else:
        questions = "\n" + data["Question"] + "\n\n 1   " + data["Answer A"][0] + "\n 2   " + data["Answer B"][0]
    info = xpy.stimuli.TextBox(text = "Bitte schreibe die Nummern der richtigen Antworten in das Textfeld und bestätige mit 'Enter'.\n" + questions,size=(500,500))
    question = xpy.io.TextInput("",background_stimulus = info,gap=7)
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
    if data["Answer C"][1] != "NONE":
        if "3" in reply:
            out.append(True)
        else:
            out.append(False)
    else:
        out.append(None)
    return out

def distract_q(data): # for answering the distraction questions
    if data["DistractionAnswer C"][1] != "NONE":
        questions = "\n" + data["ConditionQuestion"] +  "\n\n 1   " + data["DistractionAnswer A"][0] + "\n 2   " + data["DistractionAnswer B"][0] + "\n 3  " + data["DistractionAnswer C"][0]
    else:
        questions = "\n" + data["ConditionQuestion"] + "\n\n 1   " + data["DistractionAnswer A"][0] + "\n 2   " + data["DistractionAnswer B"][0]
    info = xpy.stimuli.TextBox(text = "Bitte schreiben Sie die Nummern der richtigen Antworten in das Textfeld und bestätigendie Eingabe mit 'Enter'.\n" + questions,size=(500,500))
    question = xpy.io.TextInput("",background_stimulus = info,gap=7)
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
    # if data["DistractionAnswer C"][1] != "NONE":
    if "3" in reply:
        out.append(True)
    else:
        out.append(False)
    # else:
    #     out.append(None)
    return out


# create databench
connection = sqlite3.connect("results.db") # databench for collected data
cursor = connection.cursor()
s_sql = "CREATE TABLE IF NOT EXISTS Study1( " \
    "Video TEXT, " \
    "Question TEXT, " \
    "Condition TEXT, " \
    "Correctness BOOL, " \
    "ConditionQuestion TEXT, " \
    "ConditionCorrectness BOOL )"
cursor.execute(s_sql)
xpy.control.start()
exam_questions = pd.read_csv("study_1-data/videoquestions.csv",sep=";",encoding="utf-8",header=[0])
distraction_questions = pd.read_csv("study_1-data/distractionquestions.csv",sep=";",encoding="utf-8",header=[0])
condition = sys.argv[-1] # write condition when calling the file (auditory, visual, audiovisual)
distractions = [x for x,y in distraction_questions.iterrows()]
res = [(i,j) for i, j in zip(distractions[::2], distractions[1::2])] # pair rows with same question but different truth values in answers
new = []
for item in res:
    result = random.sample(list(item),1) # only keep one of the items, so that no participant has the same question twice
    new.extend(result)
distraction_order = random.sample(new,len(new))
# con = [True,True,True,True,True,True,True,False,False,False,False,False,False]
con = [True,True,True,True,True,False,False,False,False,False,False]
condition_values = random.sample(con,len(con)) # 6 without distraction, 5 with
condition_values = [False,True,False,True] + condition_values # four items (2 with 2 without distraction) for initialization
# condition_values = [False,True] # for testing
order = random.sample([x for x,y in exam_questions.iterrows()],len(condition_values)) # randomize order of questions, just as many questions as there are condition values
current_results = []
for index in order:
    try:
        condition_value = condition_values[0]
        del condition_values[0]
    except IndexError:
        condition_value = False
    q_results = dict()
    q_results["Video"] = exam_questions.loc[index]["Filename"]
    q_results["Question"] = exam_questions.loc[index]["Question"]
    q_results["Answer A"] = (exam_questions.loc[index]["Answer A"], str(exam_questions.loc[index]["Correctness A"]).upper())
    q_results["Answer B"] = (exam_questions.loc[index]["Answer B"], str(exam_questions.loc[index]["Correctness B"]).upper())
    q_results["Answer C"] = (exam_questions.loc[index]["Answer C"], str(exam_questions.loc[index]["Correctness C"]).upper())
    if condition_value and distraction_order != []:
        q_results["Condition"] = condition
        q_results["ConditionFileAuditory"] = distraction_questions.loc[distraction_order[0]]["Filename Auditory"]
        q_results["ConditionFileVisual"] = distraction_questions.loc[distraction_order[0]]["Filename Visual"]
        q_results["ConditionQuestion"] = distraction_questions.loc[distraction_order[0]]["Question"]
        q_results["DistractionAnswer A"] = (distraction_questions.loc[distraction_order[0]]["Answer A"], str(distraction_questions.loc[distraction_order[0]]["Correctness A"]).upper())
        q_results["DistractionAnswer B"] = (distraction_questions.loc[distraction_order[0]]["Answer B"], str(distraction_questions.loc[distraction_order[0]]["Correctness B"]).upper())
        q_results["DistractionAnswer C"] = (distraction_questions.loc[distraction_order[0]]["Answer C"], str(distraction_questions.loc[distraction_order[0]]["Correctness C"]).upper())
        del distraction_order[0] # remove the first value
    else:
        q_results["Condition"] = ""
        q_results["ConditionQuestion"] = None
    q_results["Correctness"] = None
    q_results["ConditionCorrectness"] = None

    # call functions for samples
    if q_results["Condition"] == "auditory":
    # if condition_value and condition == "auditory" and distraction_order != []:
        q_results = auditory(q_results)
    elif q_results["Condition"] == "visual":
    # elif condition_value and condition == "visual" and distraction_order != []:
        q_results = visual(q_results)
    elif q_results["Condition"] == "audiovisual":
    # elif condition_value and condition == "audiovisual" and distraction_order != []:
        q_results = audiovisual(q_results)
    else: # when condition_value is False
        q_results = baseline(q_results)
    last = q_results.copy()
    current_results.append(last) # create a copy of results to save

# button when Done
done = xpy.io.TextInput("Drücken Sie 'Enter', wenn Sie fertig sind.")
if type(done.get()) == str:
    for item in current_results[4:]: # ignore the first four items as they are for initialization
        params = (item["Video"],item["Question"],item["Condition"],item["Correctness"],item["ConditionQuestion"],item["ConditionCorrectness"])
        cursor.execute("INSERT INTO Study1 VALUES (?, ?, ?, ?, ?, ?)", params)
    submit = xpy.io.TextInput("Drücken Sie 'Enter' um die Studie zu beenden.")
    if type(submit.get()) == str:
        connection.commit()
        connection.close()
        xpy.control.end()