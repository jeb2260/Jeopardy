import time
import lxml
import sys
import os
import re
import csv
import progressbar
import concurrent.futures as futures

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(CURRENT_DIR, 'podium-data')
J_ARCHIVE_DIR = os.path.join(CURRENT_DIR, 'j-archive-csv')

def main():
	podiumfile = os.path.join(FOLDER,'podium-data.csv')
	tournfile = os.path.join(FOLDER, 'tournament-episodes.csv')
	contestantfile = os.path.join(FOLDER, 'contestant-profiles.csv')
	contestantData = create_contestant_profiles(podiumfile,tournfile)
	write_to_csv(contestantfile,contestantData)

#Create that file with all of the contestants
#Stuff currently implemented: appearances/victories, accuracy %
#Maybe use a dictionary? for appearances
#NOT IMPLEMENTED: How to represent champions across tournament gaps
def create_contestant_profiles(podiumFile,tournamentsFile):
	#Dictionary format: {contestant_name: [start_date,end_date, #wins]}
	#Note: Wins are not straightforward, as tournament contestants can
	#advance to semifinals via wild-card. 
	appearances = dict()
	#Dictionary format: {contestant_name: [num_correct, num_incorrect, num_j_correct, num_j_incorrect,
	#								       num_dj_correct, num_dj_incorrect, num_fj_correct, num_fj_incorrect,
	#								       num_tiebreak_correct, num_tiebreak_incorrect]}
	accuracies = dict()

	profiles = []

	with open(podiumFile,'r',newline='',encoding='utf-8') as csvfile:
		csv_reader = csv.reader(csvfile)
		next(csv_reader)

		for row in csv_reader:
			date = row[3]
			winner_index = int(str(row[7]).strip('[]'))

			contestant1_name = row[4]
			contestant1_correct = int(row[8])
			contestant1_incorrect = int(row[9])
			contestant1_J_correct = int(row[14])
			contestant1_J_incorrect = int(row[15])
			contestant1_DJ_correct = int(row[16])
			contestant1_DJ_incorrect = int(row[17])
			contestant1_FJ_correct = int(row[18])
			contestant1_FJ_incorrect = int(row[19])
			contestant1_Tie_correct = int(row[20])
			contestant1_Tie_incorrect = int(row[21])

			contestant2_name = row[5]
			contestant2_correct = int(row[10])
			contestant2_incorrect = int(row[11])
			contestant2_J_correct = int(row[22])
			contestant2_J_incorrect = int(row[23])
			contestant2_DJ_correct = int(row[24])
			contestant2_DJ_incorrect = int(row[25])
			contestant2_FJ_correct = int(row[26])
			contestant2_FJ_incorrect = int(row[27])
			contestant2_Tie_correct = int(row[28])
			contestant2_Tie_incorrect = int(row[29])

			contestant3_name = row[6]
			contestant3_correct = int(row[12])
			contestant3_incorrect = int(row[13])
			contestant3_J_correct = int(row[30])
			contestant3_J_incorrect = int(row[31])
			contestant3_DJ_correct = int(row[32])
			contestant3_DJ_incorrect = int(row[33])
			contestant3_FJ_correct = int(row[34])
			contestant3_FJ_incorrect = int(row[35])
			contestant3_Tie_correct = int(row[36])
			contestant3_Tie_incorrect = int(row[37])

			#Being in appearances automatically means they'll be in accuracies
			if contestant1_name in appearances:
				#Update date
				appearances[contestant1_name][1]=date
				#Update number of wins (if they did win)
				if winner_index==0:
					appearances[contestant1_name][2]=appearances[contestant1_name][2]+1
				#Update accuracies
				accuracies[contestant1_name][0]=accuracies[contestant1_name][0]+contestant1_correct
				accuracies[contestant1_name][1]=accuracies[contestant1_name][1]+contestant1_incorrect
				accuracies[contestant1_name][2]=accuracies[contestant1_name][2]+contestant1_J_correct
				accuracies[contestant1_name][3]=accuracies[contestant1_name][3]+contestant1_J_incorrect
				accuracies[contestant1_name][4]=accuracies[contestant1_name][4]+contestant1_DJ_correct
				accuracies[contestant1_name][5]=accuracies[contestant1_name][5]+contestant1_DJ_incorrect
				accuracies[contestant1_name][6]=accuracies[contestant1_name][6]+contestant1_FJ_correct
				accuracies[contestant1_name][7]=accuracies[contestant1_name][7]+contestant1_FJ_incorrect
				accuracies[contestant1_name][8]=accuracies[contestant1_name][8]+contestant1_Tie_correct
				accuracies[contestant1_name][9]=accuracies[contestant1_name][9]+contestant1_Tie_incorrect


			else:
				#Assume start and end date are same (update if not)
				#Check if they won
				if winner_index==0:
					appearances[contestant1_name]=[date,date,1]
				else:
					appearances[contestant1_name]=[date,date,0]
				accuracies[contestant1_name]=[contestant1_correct,contestant1_incorrect,contestant1_J_correct,contestant1_J_incorrect,
												contestant1_DJ_correct,contestant1_DJ_incorrect,contestant1_FJ_correct,contestant1_FJ_incorrect,
												contestant1_Tie_correct,contestant1_Tie_incorrect]

			if contestant2_name in appearances:
				appearances[contestant2_name][1]=date
				#Update number of wins (if they did win)
				if winner_index==1:
					appearances[contestant2_name][2]=appearances[contestant2_name][2]+1
				#Update accuracies
				accuracies[contestant2_name][0]=accuracies[contestant2_name][0]+contestant2_correct
				accuracies[contestant2_name][1]=accuracies[contestant2_name][1]+contestant2_incorrect
				accuracies[contestant2_name][2]=accuracies[contestant2_name][2]+contestant2_J_correct
				accuracies[contestant2_name][3]=accuracies[contestant2_name][3]+contestant2_J_incorrect
				accuracies[contestant2_name][4]=accuracies[contestant2_name][4]+contestant2_DJ_correct
				accuracies[contestant2_name][5]=accuracies[contestant2_name][5]+contestant2_DJ_incorrect
				accuracies[contestant2_name][6]=accuracies[contestant2_name][6]+contestant2_FJ_correct
				accuracies[contestant2_name][7]=accuracies[contestant2_name][7]+contestant2_FJ_incorrect
				accuracies[contestant2_name][8]=accuracies[contestant2_name][8]+contestant2_Tie_correct
				accuracies[contestant2_name][9]=accuracies[contestant2_name][9]+contestant2_Tie_incorrect
			else:
				if winner_index==1:
					appearances[contestant2_name]=[date,date,1]
				else:
					appearances[contestant2_name]=[date,date,0]
				accuracies[contestant2_name]=[contestant2_correct,contestant2_incorrect,contestant2_J_correct,contestant2_J_incorrect,
												contestant2_DJ_correct,contestant2_DJ_incorrect,contestant2_FJ_correct,contestant2_FJ_incorrect,
												contestant2_Tie_correct,contestant2_Tie_incorrect]

			if contestant3_name in appearances:
				appearances[contestant3_name][1]=date
				#Update number of wins (if they did win)
				if winner_index==2:
					appearances[contestant3_name][2]=appearances[contestant3_name][2]+1
				#Update accuracies
				accuracies[contestant3_name][0]=accuracies[contestant3_name][0]+contestant3_correct
				accuracies[contestant3_name][1]=accuracies[contestant3_name][1]+contestant3_incorrect
				accuracies[contestant3_name][2]=accuracies[contestant3_name][2]+contestant3_J_correct
				accuracies[contestant3_name][3]=accuracies[contestant3_name][3]+contestant3_J_incorrect
				accuracies[contestant3_name][4]=accuracies[contestant3_name][4]+contestant3_DJ_correct
				accuracies[contestant3_name][5]=accuracies[contestant3_name][5]+contestant3_DJ_incorrect
				accuracies[contestant3_name][6]=accuracies[contestant3_name][6]+contestant3_FJ_correct
				accuracies[contestant3_name][7]=accuracies[contestant3_name][7]+contestant3_FJ_incorrect
				accuracies[contestant3_name][8]=accuracies[contestant3_name][8]+contestant3_Tie_correct
				accuracies[contestant3_name][9]=accuracies[contestant3_name][9]+contestant3_Tie_incorrect
			else:
				if winner_index==2:
					appearances[contestant3_name]=[date,date,1]
				else:
					appearances[contestant3_name]=[date,date,0]
				accuracies[contestant3_name]=[contestant3_correct,contestant3_incorrect,contestant3_J_correct,contestant3_J_incorrect,
												contestant3_DJ_correct,contestant3_DJ_incorrect,contestant3_FJ_correct,contestant3_FJ_incorrect,
												contestant3_Tie_correct,contestant3_Tie_incorrect]

		for contestant in appearances:
			print(contestant)
			#Special cases because they may not play in Final Jeopardy/Tiebreaker
			finalJeopardyAccuracy = 100*float(accuracies[contestant][6])/(float(accuracies[contestant][6])+float(accuracies[contestant][7])) if accuracies[contestant][6]+accuracies[contestant][7]!=0 else "Did Not Play"
			tiebreakerAccuracy = 100*float(accuracies[contestant][8])/(float(accuracies[contestant][8])+float(accuracies[contestant][9])) if accuracies[contestant][8]+accuracies[contestant][9]!=0 else "N/A"
			#Special cases where they did not buzz in at all (losers)
			j_accuracy = 100*float(accuracies[contestant][2])/(float(accuracies[contestant][2])+float(accuracies[contestant][3])) if accuracies[contestant][2]+accuracies[contestant][3]!=0 else "Did Not Buzz"
			dj_accuracy = 100*float(accuracies[contestant][4])/(float(accuracies[contestant][4])+float(accuracies[contestant][5])) if accuracies[contestant][4]+accuracies[contestant][5]!=0 else "Did Not Buzz"
			profiles.append({
				"contestant": contestant,
				"firstAppearance": appearances[contestant][0],
				"lastAppearance": appearances[contestant][1],
				"Wins": appearances[contestant][2],
				"numberCorrect": accuracies[contestant][0],
				"numberIncorrect": accuracies[contestant][1],
				"overallAccuracy": 100*float(accuracies[contestant][0])/(float(accuracies[contestant][0])+float(accuracies[contestant][1])),
				"J-Accuracy": j_accuracy,
				"DJ-Accuracy": dj_accuracy,
				"FJ-Accuracy": finalJeopardyAccuracy,
				"Tiebreak-Accuracy": tiebreakerAccuracy,
				"Correct/Game": float(accuracies[contestant][0])/float(appearances[contestant][2]+1),
				"J-Correct": accuracies[contestant][2],
				"J-Incorrect": accuracies[contestant][3],
				"DJ-Correct": accuracies[contestant][4],
				"DJ-Incorrect": accuracies[contestant][5],
				"FJ-Correct": accuracies[contestant][6],
				"FJ-Incorrect": accuracies[contestant][7],
				"Tiebreak-Correct": accuracies[contestant][8],
				"Tiebreak-Incorrect": accuracies[contestant][9]
			})
	return profiles


def write_to_csv(filename, data):
	with open(filename,'w+',newline='',encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		keys = data[0].keys()
		writer.writerow(list(keys))
		for d in data:
			writer.writerow([d[key] for key in keys])

if __name__=="__main__":
    main()