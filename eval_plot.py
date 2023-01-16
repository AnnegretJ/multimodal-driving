import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import ast

# sns.set_theme(style="whitegrid")

def by_distract(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distract = pd.DataFrame.from_dict(current.loc[[1]])
    distract = ast.literal_eval(distract.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    labels = ["drive","distraction","joined: drive correct", "joined: drive incorrect"]
    c = [drive["c"],distract["c"],both["cc"],both["ci"]] # correct driving, correct distraction, drive and distract correct, drive correct but distract incorrect
    i = [drive["i"],distract["i"],both["ic"],both["ii"]] # incorrect driving, incorrect distraction, drive incorrect distract correct, drive incorrect distract correct 
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, c, width, label='correct')
    rects2 = ax.bar(x + width/2, i, width, label='incorrect')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by question type and distraction condition: ' + column)
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()

def no_distr(current,column):
    no_distr = pd.DataFrame.from_dict(current.loc[[0]])
    no_distr = ast.literal_eval(no_distr.iloc[0][column])
    labels = ["correct, incorrect"]
    c = no_distr["c"]
    i = no_distr["i"]
    x = np.arange(len(labels))
    width = 0.35
    fig,ax = plt.subplots()
    rects1 = ax.bar(x - width/2,c,width/2,label="correct")
    rects2 = ax.bar(x + width/2,i,width/2,label="incorrect")
    ax.set_ylabel("Scores")
    ax.set_title("Scores for driving questions without distractions")
    ax.set_xticks([],[])
    ax.legend()
    ax.bar_label(rects1,padding=3)
    ax.bar_label(rects2,padding=3)
    fig.tight_layout()
    plt.show()

def video(k,d,current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distract = pd.DataFrame.from_dict(current.loc[[1]])
    distract = ast.literal_eval(distract.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    keep = pd.DataFrame.from_dict(current.loc[[3]])
    keep =  ast.literal_eval(keep.iloc[0][column])
    if keep["Y/N"] == "True":
        k.append((column,drive,distract,both)) # collect all video dictionaries to later create a scatterplot
    else:
        d.append((column,drive,distract,both))
    return k,d

def distract(k,d,current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distract = pd.DataFrame.from_dict(current.loc[[1]])
    distract = ast.literal_eval(distract.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    keep = pd.DataFrame.from_dict(current.loc[[3]])
    keep =  ast.literal_eval(keep.iloc[0][column])
    if keep["Y/N"] == "True":
        k.append((column,drive,distract,both)) # collect all video dictionaries to later create a scatterplot
    else:
        d.append((column,drive,distract,both))
    return k,d

def typ(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distract = pd.DataFrame.from_dict(current.loc[[1]])
    distract = ast.literal_eval(distract.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    labels = ["drive","distraction","joined: drive correct", "joined: drive incorrect"]
    c = [drive["c"],distract["c"],both["cc"],both["ci"]] # correct driving, correct distraction, drive and distract correct, drive correct but distract incorrect
    i = [drive["i"],distract["i"],both["ic"],both["ii"]] # incorrect driving, incorrect distraction, drive incorrect distract correct, drive incorrect distract correct 
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, c, width, label='correct')
    rects2 = ax.bar(x + width/2, i, width, label='incorrect')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by question type and distraction type: ' + column)
    ax.set_xticks(x, labels)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()

def additional(age,year,experience,participant,current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distract = pd.DataFrame.from_dict(current.loc[[1]])
    distract = ast.literal_eval(distract.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    if not column.startswith("Participant"):
        amount = pd.DataFrame.from_dict(current.loc[[4]])
        amount = ast.literal_eval(amount.iloc[0][column])
    if column.startswith("Age"):
        age.append((column,drive,distract,both,amount))
    elif column.startswith("Year"):
        year.append((column,drive,distract,both,amount))
    elif column.startswith("Experience"):
        experience.append((column,drive,distract,both,amount))
    else:
        participant.append((column,drive,distract,both))
    return age,year,experience,participant

results = pd.read_csv("eval_results.csv",sep=";",encoding="utf-8",header=[0])
videos_keep = []
videos_discard = []
distract_keep = []
distract_discard = []
age = []
year = []
experience = []
participant = []
for column in results:
    current = pd.DataFrame.from_dict(results[column])
    if column == "auditory" or column == "visual":
        by_distract(current,column)
    elif column == "no_distr": # items without distraction
        no_distr(current,column)
    elif column.startswith("Video"): # individual videos
        videos_keep,videos_discard = video(videos_keep,videos_discard,current,column)
    elif column.startswith("Distraction"):
        distract_keep,distract_discard = distract(distract_keep,distract_discard,current,column)
    elif column.startswith("Type"):
        typ(current,column)
    elif column.startswith("Age") or column.startswith("Year") or column.startswith("Experience") or column.startswith("Participant"):
        age,year,experience,participant (additional(age,year,experience,participant,current,column))
# todo: video scatterplots, distraction scatterplots, age scatterplots, year scatterplots, experience scatterplots, participant scatterplot
# video: column, {drive_c_distr,drive_c_nodistr,drive_i_distr,drive_i_nodistr},{distr},{both}

#TODO: fix video saves in eval_pilot to include if distraction played or not for drive
#TODO: do all again but filter out data with videos that have been answered incorrectly by all
# videos_keep
# drive_cd = [] # correct distract
# drive_cn = [] # correct no distract
# drive_id = []
# drive_in = []
# distr_c = []
# distr_i = []
# cc = []
# ci = []
# ic = []
# ii = []
# labels = []
# for item in videos_keep:
#     labels.append(item[0])
#     drive = item[1]
#     distr = item[2]
#     both = item[3]
#     drive_cd.append(drive[])