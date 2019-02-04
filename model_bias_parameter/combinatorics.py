import os.path
import pandas as pd
import itertools
import numpy as np

DATA_PATH = '../'

def combinatoric(agent_scores):
	#Finds all possible choices of 3 agent scores from these 6
	agent_scores = list(agent_scores.values())
	combinations = list(itertools.combinations(agent_scores, 3))
	#Find the sums of each of these combinations and rank them
	sums = []
	for item in combinations:
		summed = item[0] + item[1] + item[2]
		sums.append(summed)
	sums = sorted(sums)
	return sums

def maximize_homophily(my_rating, agent_scores):
	agent_scores = list(agent_scores.values())
	scores = []
	#Find top 3 closest
	for i in range(3):
		closest = min(agent_scores, key=lambda x:abs(x - my_rating))
		scores.append(closest)
		agent_scores.remove(closest)
	return sum(scores)

def find_z(picked, forced_mean, stdev):
	z = (picked - forced_mean)/stdev
	return z

def simulation(subjID):
	me_path = DATA_PATH + subjID + '.csv'
	me = pd.read_csv(me_path)

	results = pd.DataFrame()

	for i in range(len(me)):
		#Get all *seen* agent scores for this stimulus
		agent_scores = dict()
		for j in range(1, 7):
			agent_scores[me['a%s_name'%j][i]] = me['a%s_rating'%j][i]
		# print("Seen agents:")
		# print(agent_scores)

		#Find all combinatoric possiblities
		possible_sums = combinatoric(agent_scores)
		# print("Possible sums:")
		# print(possible_sums)

		#Find picked possibility
		picked_agents = dict()
		for j in range(1, 4):
			picked_agents[me['kept_%s_name'%j][i]] = me['kept_%s_rating'%j][i]

		picked_scores = list(picked_agents.values())
		picked_sum = 0
		for j in range(len(picked_scores)):
			picked_sum += picked_scores[j]
		# print("Picked agents:")
		# print(picked_agents)
		# print("Picked sum:")
		# print(picked_sum)

		#Find what would have picked if maximizing homophily
		my_rating = me['subject_rating'][i]
		# print("My rating:")
		# print(my_rating)
		maxhomo_score = maximize_homophily(my_rating, agent_scores)
		# print("If trying to maximize homophily:")
		# print(maxhomo_score)

		#Find ranking in comparison to minimum
		min_rank = possible_sums.index(picked_sum)
		# print("Ranking wrt minimum:")
		# print(min_rank)

		#Find ranking in comparison to maximizing homophily
		maxhomo_index = possible_sums.index(maxhomo_score)
		maxhomo_rank = min_rank - maxhomo_index #this is the index of the picked sum
		# print("Ranking wrt maximizing homophily:")
		# print(maxhomo_rank)

		#Find z score wrt maximizing homophily as forced mean
		stdev = np.std(possible_sums)
		mean = np.mean(possible_sums)
		z = find_z(picked_sum, maxhomo_score, stdev)
		# print("Z Score wrt maximizing homophily:")
		# print(z)

		results = results.append(pd.Series([mean, stdev, my_rating, picked_sum, possible_sums[0], min_rank, maxhomo_score, maxhomo_index, maxhomo_rank, z]), ignore_index = True)

	results.columns = ["Mean of Possible Sums", "Stdev of Possible Sums", "Participant Rating", "Picked Sum", "Minimum Possible Sum", "Ranking From Min", "Maximizing Homophily Sum", "Maximizing Homophily Rank", "Ranking from Max. Homo.", "Z Score from Max. Homo."]
	results.to_csv("output/%s_bias.csv"%subjID, index = False)
	# print(results)

#Can iterate through all subjects to produce some output sheet, but check above first
if __name__ == '__main__':
	# simulation('13')
	for i in range(91):
	    if os.path.isfile(DATA_PATH+str(i)+'.csv'):
	        simulation(str(i))

