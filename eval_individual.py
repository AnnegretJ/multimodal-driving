import pandas as pd
from collections import defaultdict
import matplotlib.pylab as plt
import seaborn as sns

data = pd.read_csv("study_2-data/results.csv",sep=";",encoding="utf-8",header=[0])

participant_voice = defaultdict(dict)
participant_button = defaultdict(dict)

for index,line in data.iterrows():
    if line["Participant"] == "gold":
        continue
    else:
        key = line["Participant"]
    if line["Condition"] == "button":
        if line["Reactiontime"] != "none" and line["Reaction"] != "self":
            participant_button[key][line["Scene"]] = line["Reactiontime"]
    else:
        if line["Reactiontime"] != "none" and line["Reaction"] != "self":
            participant_voice[key][line["Scene"]] = line["Reactiontime"]

for key in participant_voice.keys():
    labels = list(participant_voice[key].keys())
    c = "g"
    sns.swarmplot(x=labels,y=[float(value.replace(",",".")) for _,value in participant_voice[key].items()],dodge=True,color=c,size=10)#,label="")
    plt.title("Reaction times by item for voice participant " + str(key))
    plt.show()
for key in participant_button.keys():
    labels=list(participant_button[key].keys())
    c = "b"
    sns.swarmplot(x=labels,y=[float(value.replace(",",".")) for _,value in participant_button[key].items()],dodge=True,color=c,size=10)#,label="")
    plt.title("Reaction times by item for button participant " + str(key))
    plt.show()
# plt.title("Individual Distraction Time per Item and Participant")
# plt.show()