import pandas as pd
from collections import defaultdict
import matplotlib.pylab as plt
import seaborn as sns

additional_data = pd.read_csv("study_2-data/additional_results_main.csv",sep=";",encoding="utf-8",header=[0]) # get data for age etc.
#general_results = pd.read_csv("study_2-data/results.csv",sep=";",encoding="utf-8",header=[0])

age = dict()
year = dict()
experience = dict()
pilot = dict()
handedness = dict()
condition = defaultdict(list)
distractions = dict()
mean_distr_no_distr = dict() # difference in mean reaction time with distraction in comparison to without distraction
median_distr_no_distr = dict() # difference in median reaction time
mean_weather_no_distr = dict() # difference in mean reaction time for weather distractions
median_weather_no_distr = dict() # difference in median
mean_restaurant_no_distr = dict() # difference in mean reaction time for restaurant distractions
median_restaurant_no_distr = dict() # difference in median
mean_previous_self = dict() # difference in mean reaction time with previous reaction self in comparison to previous reaction none
median_previous_self = dict()
mean_previous_avoid = dict()
median_previous_avoid = dict()
mean_previous_hit = dict()
median_previous_hit = dict()
mean_previous_distract = dict() # difference in mean reaction time with previous item with distraction in comparison to previous reaction without distraction
median_previous_distract = dict()


for index,line in additional_data.iterrows(): # per participant
    n = line["Subject Number"]
    age[n] = line["Alter"]
    if "/" in str(line["Jahr"]):
        year[n] = float(str(line["Jahr"])[:4])
    else:
        year[n] = float(line["Jahr"])
    try:
        experience[n] = line["Erfahrung transcription"]
    except AttributeError:
        pass
    pilot[n] = line["Pilot?"]
    handedness[n] = line["Händigkeit"]
    condition[line["Condition"]].append(n)
    distractions[n] = str(line["Ablenkungen transcription"]).split()
    mean_distr_no_distr[n] = float(str(line["average_distract"]).replace(",",".")) - float(str(line["average_non"]).replace(",",".")) # positive number if distraction has higher reaction time, negative number if distraction has lower reaction time
    median_distr_no_distr[n] = float(str(line["median_distract"]).replace(",",".")) - float(str(line["median_non"]).replace(",","."))
    mean_weather_no_distr[n] = float(str(line["average_weather"]).replace(",",".")) - float(str(line["average_non"]).replace(",","."))
    median_weather_no_distr[n] = float(str(line["median_weather"]).replace(",",".")) - float(str(line["median_non"]).replace(",","."))
    try:
        mean_restaurant_no_distr[n] = float(str(line["average_restaurant"]).replace(",",".")) - float(str(line["average_non"]).replace(",","."))
        median_restaurant_no_distr[n] = float(str(line["median_restaurant"]).replace(",",".")) - float(str(line["median_non"]).replace(",","."))
    except ValueError:
        pass
    try:
        mean_previous_self[n] = float(str(line["MEANprevious: self"]).replace(",",".")) - float(str(line["MEANprevious: none"]).replace(",","."))
        median_previous_self[n] = float(str(line["MEDIANprevious: self"]).replace(",",".")) - float(str(line["MEDIANprevious: none"]).replace(",","."))
    except ValueError:
        pass
    mean_previous_avoid[n] = float(str(line["MEANprevious: avoid"]).replace(",",".")) - float(str(line["MEANprevious: none"]).replace(",","."))
    median_previous_avoid[n] = float(str(line["MEDIANprevious: avoid"]).replace(",",".")) - float(str(line["MEDIANprevious: none"]).replace(",","."))
    try:
        mean_previous_hit[n] = float(str(line["MEANprevious: hit"]).replace(",",".")) - float(str(line["MEANprevious: none"]).replace(",","."))
        median_previous_hit[n] = float(str(line["MEDIANprevious: hit"]).replace(",",".")) - float(str(line["MEDIANprevious: none"]).replace(",","."))
    except ValueError:
        pass
    mean_previous_distract[n] = float(str(line["MEANprevious: distract"]).replace(",",".")) - float(str(line["MEANprevious: no_distr"]).replace(",","."))
    median_previous_distract[n] = float(str(line["MEDIANprevious: distract"]).replace(",",".")) - float(str(line["MEDIANprevious: no_distr"]).replace(",","."))

labels = condition["button"]
b_mean = "b"
b_median = "tab:blue"
v_mean = "g"
v_median = "tab:green"
button_participants = []
voice_participants = []
button_items_mean = []
voice_items_mean = []
button_items_median = []
voice_items_median = []
additional_data_button = []
additional_data_voice = []
# x: participant, y: value
# graph for distraction, for distraction type, for previous action, for previous distraction
for p in condition["button"]:
    try:
        button_items_mean.append(mean_distr_no_distr[p])
        button_items_median.append(median_distr_no_distr[p])
        # button_items_mean.append(mean_restaurant_no_distr[p])
        # button_items_median.append(median_restaurant_no_distr[p])
        # button_items_mean.append(mean_previous_distract[p])
        # button_items_median.append(median_previous_distract[p])
        # for item in distractions[p]:
        #     if "," in item:
        #         item = item[:-1]
        #     button_items_mean.append(mean_distr_no_distr[p])
        #     button_items_median.append(median_distr_no_distr[p])
        #     button_participants.append(p)
        #     additional_data_button.append(item)
        button_participants.append(p)
        additional_data_button.append(handedness[p])
    except KeyError:
        continue
for p in condition["voice"]:
    try:
        # for item in distractions[p]:
        #     if "," in item:
        #         item = item[:-1]
        #     voice_items_mean.append(mean_distr_no_distr[p])
        #     voice_items_median.append(median_distr_no_distr[p])
        #     voice_participants.append(p)
        #     additional_data_voice.append(item)
        voice_items_mean.append(mean_distr_no_distr[p])
        voice_items_median.append(median_distr_no_distr[p])
        # voice_items_mean.append(mean_restaurant_no_distr[p])
        # voice_items_median.append(median_restaurant_no_distr[p])
        # voice_items_mean.append(mean_previous_distract[p])
        # voice_items_median.append(median_previous_distract[p])
        voice_participants.append(p)
        additional_data_voice.append(handedness[p])
    except KeyError:
        continue
# plt.scatter(button_participants,button_items_mean,c=b_mean,label="mean button")
# plt.scatter(button_participants,button_items_median,c=b_median,label="median button")
# plt.scatter(voice_participants,voice_items_mean,c=v_mean,label="mean voice")
# plt.scatter(voice_participants,voice_items_median,c=v_median,label="median voice")
sns.swarmplot(x=additional_data_button,y=button_items_mean,dodge=True,color=b_mean,size=10)#,label="mean button")
sns.swarmplot(x=additional_data_button,y=button_items_median,dodge=True,color=b_median,size=10)#,label="median button")
sns.swarmplot(x=additional_data_voice,y=voice_items_mean,dodge=True,color=v_mean,size=10)#,label="mean voice")
sns.swarmplot(x=additional_data_voice,y=voice_items_median,dodge=True,color=v_median,size=10)#,label="median voice")
#plt.legend()
# plt.title("Difference between Distraction and no-Distraction items")
plt.title("Difference between Distraction and no-Distraction items dependent on Participant Handedness")
# plt.title("Difference between Restaurant-Distraction and no-Distraction items")
# plt.title("Difference between previous item with Distraction and previous item without Distraction")
plt.show()