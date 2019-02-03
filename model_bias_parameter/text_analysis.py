import pandas as pd
import os
from collections import Counter

DATA_PATH = "../"

#for each participant, develop a list of kept vs. eliminated words ranked in order of number of times
#output into a csv with all participants: participant / condition / my words / kept words / eliminated words
#see if differs at all from person to person/systematic differences

def text_each(subjID):
	me_path = DATA_PATH + subjID + '.csv'
	me = pd.read_csv(me_path)

	condition = me['condition'][0]

	mine = []
	kept = []
	elim = []

	for i in range(len(me)):
		mine += me['subject_title'][i].split()
		kept += me['kept_1_title'][i].split()
		kept += me['kept_2_title'][i].split()
		kept += me['kept_3_title'][i].split()
		elim += me['elim_1_title'][i].split()
		elim += me['elim_2_title'][i].split()
		elim += me['elim_3_title'][i].split()

	my_words = Counter(mine)
	most_occur_m = my_words.most_common(50)

	kept_words = Counter(kept)
	most_occur_k = kept_words.most_common(50)

	elim_words = Counter(elim)
	most_occur_e = elim_words.most_common(50)

	return pd.Series([subjID, condition, most_occur_m, most_occur_k, most_occur_e])

def run_all():
	text = pd.DataFrame()

	for i in range(91):
		if os.path.isfile(DATA_PATH+str(i)+'.csv'):
			result = text_each(str(i))
			text = text.append(result, ignore_index = True)
	text.columns = ["subj_ID", "condition", "own_words", "kept_words", "elim_words"]
	text.to_csv("output/text_anaysis.csv", index = False)

	#add result from text_each to text dataframe
run_all()
