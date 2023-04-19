import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import ast
import seaborn as sns
from collections import defaultdict

# sns.set_theme(style="whitegrid")

def by_distract(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distraction = pd.DataFrame.from_dict(current.loc[[1]])
    distraction = ast.literal_eval(distraction.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    labels = ["drive","distraction","joined: drive correct", "joined: drive incorrect"]
    c = [drive["c"],distraction["c"],both["cc"],both["ci"]] # correct driving, correct distraction, drive and distract correct, drive correct but distract incorrect
    i = [drive["i"],distraction["i"],both["ic"],both["ii"]] # incorrect driving, incorrect distraction, drive incorrect distract correct, drive incorrect distract correct 
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

def distr(current,column):
    distr = pd.DataFrame.from_dict(current.loc[[0]])
    distr = ast.literal_eval(distr.iloc[0][column])
    labels = ["correct, incorrect"]
    c = distr["c"]
    i = distr["i"]
    x = np.arange(len(labels))
    width = 0.35
    fig,ax = plt.subplots()
    rects1 = ax.bar(x - width/2,c,width/2,label="correct")
    rects2 = ax.bar(x + width/2,i,width/2,label="incorrect")
    ax.set_ylabel("Scores")
    ax.set_title("Scores for distraction question: " + column)
    ax.set_xticks([],[])
    ax.legend()
    ax.bar_label(rects1,padding=3)
    ax.bar_label(rects2,padding=3)
    fig.tight_layout()
    plt.show()

def video(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    try:
        distraction = pd.DataFrame.from_dict(current.loc[[1]])
        distraction = ast.literal_eval(distraction.iloc[0][column])
        both = pd.DataFrame.from_dict(current.loc[[2]])
        both = ast.literal_eval(both.iloc[0][column])
    except ValueError: # value is nan when no distract
        distraction = dict()
        both = dict()
    return (column,drive,distraction,both)

def distract(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distraction = pd.DataFrame.from_dict(current.loc[[1]])
    distraction = ast.literal_eval(distraction.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    return (column,drive,distraction,both)

def scatter_items(typ,items): # items = [(current,column),...] # type "drive"/"distract"
    labels = ["correct","incorrect","both: correct","both: drive correct", "both: distract correct", "both: incorrect"]
    videos = []
    c = []
    i = []
    cc = []
    ci = []
    ic = []
    ii = []
    # y = np.arange(len(items))
    x = np.arange(len(labels))
    # plt.yticks(y,range(len(items)))
    for column,drive,distraction,both in items:
        videos.append(column)
        if typ == "drive":
            c.append(drive["c"])
            i.append(drive["i"])
        elif typ == "distract":
            c.append(distraction["c"])
            i.append(distraction["i"])
        cc.append(both["cc"])
        ci.append(both["ci"])
        ic.append(both["ic"])
        ii.append(both["ii"])
    plt.xticks(x,labels)
    if typ == "drive":
        colors = ["c","b","g","y","k","tab:brown","tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:pink","tab:gray","blueviolet","lime"]
    elif typ == "distract":
        colors = ["c","b","g","y","k","tab:brown","tab:blue"]
    n = 0
    sns.swarmplot(x=["correct" for x in c],y=c,dodge=True,color=colors,s=10)
    sns.swarmplot(x=["incorrect" for x in i],y=i,dodge=True,color=colors,s=10)
    sns.swarmplot(x=["both: correct" for x in cc],y=cc,dodge=True,color=colors,s=10)
    sns.swarmplot(x=["both: drive correct" for x in ci],y=ci,dodge=True,color=colors,s=10)
    sns.swarmplot(x=["both: distract correct" for x in ic],y=ic,dodge=True,color=colors,s=10)
    sns.swarmplot(x=["both: incorrect" for x in ii],y=ii,dodge=True,color=colors,s=10)
    handles = []
    for item in colors:
        p = mpatches.Patch(color=item,label=videos[n])
        handles.append(p)
        n+=1
    # for key in videos.keys():
    #     plt.scatter(labels,videos[key],color=colors[n],label=key)
    #     n += 1
    if typ == "drive":
        plt.legend(handles=handles,bbox_to_anchor=(0.5,0.7,1.,.102),loc=3,ncol=2,borderaxespad=0.)
    elif typ == "distract":
        plt.legend(handles=handles,bbox_to_anchor=(0.175,0.85,1.,.102),loc=3,ncol=2,borderaxespad=0.)
    plt.xlabel('Correctness')
    plt.ylabel('Amount Answered')
    plt.title('Answers to individual ' + typ + " items",loc="left")
    plt.show()

def scatter_additional(typ,items): # item = [(column,drive,distraction,both)]
    labels = ["drive: correct","drive: incorrect","distract: correct","distract: incorrect","both: correct","both: drive correct", "both: distract correct", "both: incorrect"]
    type_items = []
    correctness = defaultdict(list)
    # y = np.arange(len(items))
    x = np.arange(len(labels))
    # plt.yticks(y,range(len(items)))
    if typ != "participant":
        for (column,drive,distraction,both,_) in items:
            type_items.append(column) # list of i.e. all ages
            correctness["drive: correct"].append(drive["c"])
            correctness["drive: incorrect"].append(drive["i"])
            correctness["distract: correct"].append(distraction["c"])
            correctness["distract: incorrect"].append(distraction["i"])
            correctness["both: correct"].append(both["cc"])
            correctness["both: drive correct"].append(both["ci"])
            correctness["both: distract correct"].append(both["ic"])
            correctness["both: incorrect"].append(both["ii"])
    else:
        for (column,drive,distraction,both) in items:
            type_items.append(column) # list of i.e. all ages
            correctness["drive: correct"].append(drive["c"])
            correctness["drive: incorrect"].append(drive["i"])
            correctness["distract: correct"].append(distraction["c"])
            correctness["distract: incorrect"].append(distraction["i"])
            correctness["both: correct"].append(both["cc"])
            correctness["both: drive correct"].append(both["ci"])
            correctness["both: distract correct"].append(both["ic"])
            correctness["both: incorrect"].append(both["ii"])
    colors = ["c","b","g","y","k","tab:brown","tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:pink","tab:gray","blueviolet","lime","lightcoral","chocolate","burlywood","yellow","greenyellow","springgreen","fuchsia","aquamarine"]
    colors = colors[:len(type_items)]
    plt.xticks(x,labels)
    n = 0
    for item in labels:
        sns.swarmplot(x=[item for x in correctness[item]],y=correctness[item],dodge=True,color=colors,s=10)
    handles = []
    for item in type_items:
        p = mpatches.Patch(color=colors[n],label=item)#[8:])
        handles.append(p)
        n+=1
    
    plt.legend(handles=handles)
    # print(type_items)
    # plt.legend(handles=handles,bbox_to_anchor=(0.75,0.65,1.,.102),loc=3,ncol=2,borderaxespad=0.)
    plt.xlabel('Correctness')
    plt.ylabel('Amount Answered')
    plt.title('Answers by participant ' + typ,loc="left")
    plt.show()

def typ(current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distraction = pd.DataFrame.from_dict(current.loc[[1]])
    distraction = ast.literal_eval(distraction.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    labels = ["drive","distraction","joined: drive correct", "joined: drive incorrect"]
    c = [drive["c"],distraction["c"],both["cc"],both["ci"]] # correct driving, correct distraction, drive and distract correct, drive correct but distract incorrect
    i = [drive["i"],distraction["i"],both["ic"],both["ii"]] # incorrect driving, incorrect distraction, drive incorrect distract correct, drive incorrect distract correct 
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

def additional(age,abl,year,experience,participant,current,column):
    drive = pd.DataFrame.from_dict(current.loc[[0]])
    drive = ast.literal_eval(drive.iloc[0][column])
    distraction = pd.DataFrame.from_dict(current.loc[[1]])
    distraction = ast.literal_eval(distraction.iloc[0][column])
    both = pd.DataFrame.from_dict(current.loc[[2]])
    both = ast.literal_eval(both.iloc[0][column])
    if not column.startswith("Participant"):
        amount = pd.DataFrame.from_dict(current.loc[[4]])
        amount = ast.literal_eval(amount.iloc[0][column])
    if column.startswith("Age"):
        age.append((column,drive,distraction,both,amount))
    elif column.startswith("Year"):
        year.append((column,drive,distraction,both,amount))
    elif column.startswith("Experience"):
        experience.append((column,drive,distraction,both,amount))
    elif column.startswith("PersDis"):
        abl.append((column,drive,distraction,both,amount))
    else:
        participant.append((column,drive,distraction,both))
    return age,abl,year,experience,participant

results = pd.read_csv("eval_results.csv",sep=";",encoding="utf-8",header=[0])
videos = []
distracts = []
age = []
year = []
experience = []
participant = []
abl = [] # ablenkungen
for column in results:
    current = pd.DataFrame.from_dict(results[column])
    if column == "auditory" or column == "visual":
        continue
        by_distract(current,column)
    elif column == "no_distr": # items without distraction
        continue
        no_distr(current,column)
    elif column.startswith("Distraction"):
        distracts.append(video(current,column)) # column,drive,distract,both
        continue
        distr(current,column)
    elif column.startswith("Video"):
        videos.append(video(current,column)) # column,drive,distract,both
    elif column.startswith("Type"):
        continue
        typ(current,column)
    elif column.startswith("Age") or column.startswith("Year") or column.startswith("Experience") or column.startswith("Participant") or column.startswith("PersDis"):
        age,abl,year,experience,participant = additional(age,abl,year,experience,participant,current,column)

# video scatterplot

# scatter_items("drive",videos)
# scatter_items("distract",distracts)

# age scatterplots: how many videos/distractions correct/incorrect dependent on age
scatter_additional("age",age)
scatter_additional("year",year)
scatter_additional("experience",experience)
# scatter_additional("participant",participant)
scatter_additional("abl",abl)


