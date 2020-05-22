import time
import lxml
import sys
import os
import re
import csv
import progressbar
import concurrent.futures as futures
from ast import literal_eval

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(CURRENT_DIR, 'podium-data')
J_ARCHIVE_DIR = os.path.join(CURRENT_DIR, 'j-archive-csv')


def main():
    cluefile = os.path.join(J_ARCHIVE_DIR,'j-archive-season-36.csv')
    tournfile = os.path.join(FOLDER, 'tournament-episodes.csv')
    categorydata = get_game_category_data(cluefile,tournfile)
    category_data_file = os.path.join(FOLDER, 'category-data.csv')
    write_to_csv(category_data_file,categorydata)

    categories = get_categories(category_data_file)
    categories_file = os.path.join(FOLDER, 'categories.csv')
    write_to_csv(categories_file,categories)

def get_categories(categoryFile):
    categories = []
    #{Category_name: [Games appeared, correct answers, incorrect attempts, daily double frequency, Final Jeopardy frequency,
    #                   unselected clues, average order]}
    category_dict = dict()

    with open(categoryFile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        category_indices = [1,5,9,13,17,21,25,29,33,37,41,45,49,52]

        #Fix last two indices because there's no "order" column for FJ/Tiebreaker
        correct_indices = [x+2 for x in category_indices]
        correct_indices[-1]=correct_indices[-1]-1
        correct_indices[-2]=correct_indices[-2]-1
        incorrect_indices = [x+3 for x in category_indices]
        incorrect_indices[-1]=incorrect_indices[-1]-1
        incorrect_indices[-2]=incorrect_indices[-2]-1

        clue_orders = [57,58,59,60,61,62,63,64,65,66,67,68]

        #len(row)=69
        for row in csv_reader:
            daily_doubles = literal_eval(row[55])
            unanswered_clues = literal_eval(row[56])
            for column_num, index in enumerate(category_indices):
                if row[index] == "N/A":
                    continue
                elif row[index] in category_dict:
                    #Update games appeared
                    category_dict[row[index]][0]=category_dict[row[index]][0]+1
                    #Update correct answers
                    category_dict[row[index]][1]=category_dict[row[index]][1]+int(row[correct_indices[column_num]])
                    #Update incorrect attempts
                    category_dict[row[index]][2]=category_dict[row[index]][2]+int(row[incorrect_indices[column_num]])
                    #Update daily double frequency
                    category_dict[row[index]][3]=category_dict[row[index]][3]+1 if column_num+1 in daily_doubles else category_dict[row[index]][3]
                    #Update Final Jeopardy frequency
                    category_dict[row[index]][4]=category_dict[row[index]][4]+1 if column_num==12 else category_dict[row[index]][4]
                    #Update tiebreaker frequency 
                    category_dict[row[index]][5]=category_dict[row[index]][5]+1 if column_num==13 else category_dict[row[index]][5]
                    #Update number of unselected clues
                    category_dict[row[index]][6]=category_dict[row[index]][6]+unanswered_clues[column_num] if column_num < 12 else category_dict[row[index]][5]
                    #Update total pick order (divide by total number of regular jeopardy games appeared later, since you can't
                    #continuously divide by a number and keep adding as you go. It becomes nonsensical then)
                    pick_order = literal_eval(row[clue_orders[column_num]]) if column_num<12 else []
                    category_dict[row[index]][7]=category_dict[row[index]][7]+float(sum(pick_order)) if column_num<12 else category_dict[row[index]][7]
                else:
                    category_dict[row[index]]=[0]*8
                    category_dict[row[index]][0]=1
                    category_dict[row[index]][1]=int(row[correct_indices[column_num]])
                    category_dict[row[index]][2]=int(row[incorrect_indices[column_num]])
                    category_dict[row[index]][3]=1 if column_num+1 in daily_doubles else 0
                    category_dict[row[index]][4]=1 if column_num==12 else 0
                    category_dict[row[index]][5]=1 if column_num==13 else 0
                    category_dict[row[index]][6]=unanswered_clues[column_num] if column_num < 12 else 0
                    pick_order = literal_eval(row[clue_orders[column_num]]) if column_num<12 else []
                    category_dict[row[index]][7]=float(sum(pick_order)) if column_num<12 else 0


    for category_name, data in category_dict.items():
        categories.append({
            "Category": category_name,
            "Games Appeared": data[0],
            "Correct-Attempts": data[1],
            "Incorrect-Attempts": data[2],
            "Daily-Double Count": data[3],
            "Final-Jeopardy-Count": data[4],
            "Tiebreaker-Count": data[5],
            "Unselected-Clues": data[6],
            #Dividing total pick order by total number of clues in regular Jeopardy play 
            "Average-Pick-Order": data[7]/((data[0]-data[4]-data[5])*5) if data[0]-data[4]-data[5]>0 else 0
        })
    return categories

#This creates a csv file that has each episode on a row and the categories next to it (in order)
def get_game_category_data(clueFile, tournamentsFile):
    tournEps = get_tourn_ep_list(tournamentsFile)
    game_data = []
    episode_list = []
    #List of dictionaries for each game 
    j_rounds = []
    dj_rounds = []
    fj_rounds = []
    tb_rounds = []

    
    with open(clueFile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for row in csv_reader:
            
            #We are iterating through a new episode
            if len(episode_list)<1 or episode_list[-1]!=int(row[0]):
                episode_list.append(int(row[0]))
                j_rounds.append(dict())
                dj_rounds.append(dict())
                fj_rounds.append(dict())
                tb_rounds.append(dict())

            if row[3]=="Jeopardy":
                current_round = j_rounds[-1]
                #Check if we need to traverse this row
                if len(current_round)<6:
                    coordinates = literal_eval(row[4])
                    column_number = coordinates[0]
                    current_round[column_number]=row[5]

            elif row[3]=="Double Jeopardy":
                current_round = dj_rounds[-1]
                #Check if we need to traverse this row
                if len(current_round)<6:
                    coordinates = literal_eval(row[4])
                    column_number = coordinates[0]
                    current_round[column_number]=row[5]

            elif row[3]=="Final Jeopardy":
                current_round = fj_rounds[-1]
                #Check if we need to traverse this row
                if len(current_round)==0:
                    current_round[0]=row[5]

            else:
                current_round = tb_rounds[-1]
                #Check if we need to traverse this row
                if len(current_round)==0:
                    current_round[0]=row[5]


    #Convert data to csv file
    for index, epNum in enumerate(episode_list):

        categories = [j_rounds[index][1],j_rounds[index][2],j_rounds[index][3],j_rounds[index][4],j_rounds[index][5],
                dj_rounds[index][1],dj_rounds[index][2],dj_rounds[index][3],dj_rounds[index][4],dj_rounds[index][5], fj_rounds[0]]
        if len(tb_rounds[index])>0:
            categories.append(tb_rounds[index][0])

        selection_orders, num_unpicked_clues, modified_selection_orders = get_selection_orders(clueFile,categories,epNum)

        correctAttempts,incorrectAttempts = get_category_accuracies(clueFile,categories,epNum)

        daily_doubles = get_daily_doubles(clueFile,categories,epNum)
        
        game_data.append({
                "epNum": epNum,
                "J-Category-1": j_rounds[index][1],
                "Pick-Order1": selection_orders[0],
                "Correct-Attempts1": correctAttempts[0],
                "Incorrect-Attempts1": incorrectAttempts[0],
                "J-Category-2": j_rounds[index][2],
                "Pick-Order2:": selection_orders[1],
                "Correct-Attempts2": correctAttempts[1],
                "Incorrect-Attempts2": incorrectAttempts[1],
                "J-Category-3": j_rounds[index][3],
                "Pick-Order3:": selection_orders[2],
                "Correct-Attempts3": correctAttempts[2],
                "Incorrect-Attempts3": incorrectAttempts[2],
                "J-Category-4": j_rounds[index][4],
                "Pick-Order4:": selection_orders[3],
                "Correct-Attempts4": correctAttempts[3],
                "Incorrect-Attempts4": incorrectAttempts[3],
                "J-Category-5": j_rounds[index][5],
                "Pick-Order5:": selection_orders[4],
                "Correct-Attempts5": correctAttempts[4],
                "Incorrect-Attempts5": incorrectAttempts[4],
                "J-Category-6": j_rounds[index][6],
                "Pick-Order6:": selection_orders[5],
                "Correct-Attempts6": correctAttempts[5],
                "Incorrect-Attempts6": incorrectAttempts[5],
                "DJ-Category-1": dj_rounds[index][1],
                "Pick-Order7:": selection_orders[6],
                "Correct-Attempts7": correctAttempts[6],
                "Incorrect-Attempts7": incorrectAttempts[6],
                "DJ-Category-2": dj_rounds[index][2],
                "Pick-Order8:": selection_orders[7],
                "Correct-Attempts8": correctAttempts[7],
                "Incorrect-Attempts8": incorrectAttempts[7],
                "DJ-Category-3": dj_rounds[index][3],
                "Pick-Order9:": selection_orders[8],
                "Correct-Attempts9": correctAttempts[8],
                "Incorrect-Attempts9": incorrectAttempts[8],
                "DJ-Category-4": dj_rounds[index][4],
                "Pick-Order10:": selection_orders[9],
                "Correct-Attempts10": correctAttempts[9],
                "Incorrect-Attempts10": incorrectAttempts[9],
                "DJ-Category-5": dj_rounds[index][5],
                "Pick-Order11:": selection_orders[10],
                "Correct-Attempts11": correctAttempts[10],
                "Incorrect-Attempts11": incorrectAttempts[10],
                "DJ-Category-6": dj_rounds[index][6],
                "Pick-Order12:": selection_orders[11],
                "Correct-Attempts12": correctAttempts[11],
                "Incorrect-Attempts12": incorrectAttempts[11],
                "FJ-Category": fj_rounds[index][0],
                "Correct-Attempts13": correctAttempts[12],
                "Incorrect-Attempts13": incorrectAttempts[12],
                "Tiebreaker": "N/A" if len(tb_rounds[index])<1 else tb_rounds[index][0],
                "Correct-Attempts14": "N/A" if len(tb_rounds[index])<1 else correctAttempts[13],
                "Incorrect-Attempts14": "N/A" if len(tb_rounds[index])<1 else incorrectAttempts[13],
                "Daily-Doubles": daily_doubles,
                "Unpicked-Clues": num_unpicked_clues,
                "Modified-Pick-Order1": modified_selection_orders[0],
                "Modified-Pick-Order2": modified_selection_orders[1],
                "Modified-Pick-Order3": modified_selection_orders[2],
                "Modified-Pick-Order4": modified_selection_orders[3],
                "Modified-Pick-Order5": modified_selection_orders[4],
                "Modified-Pick-Order6": modified_selection_orders[5],
                "Modified-Pick-Order7": modified_selection_orders[6],
                "Modified-Pick-Order8": modified_selection_orders[7],
                "Modified-Pick-Order9": modified_selection_orders[8],
                "Modified-Pick-Order10": modified_selection_orders[9],
                "Modified-Pick-Order11": modified_selection_orders[10],
                "Modified-Pick-Order12": modified_selection_orders[11]
            })
    return game_data

def get_daily_doubles(clueFile,categories,epNum):
    daily_doubles = []
    with open(clueFile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if int(row[0])==epNum:
                coordinates = literal_eval(row[4])
                column_number = int(coordinates[0])
                round_name = row[3]

                if round_name == "Jeopardy":
                    if row[8]=="True":
                        daily_doubles.append(column_number)

                if round_name == "Double Jeopardy":
                    if row[8]=="True":
                        daily_doubles.append(column_number+6)

            if int(row[0])>epNum:
                break
    daily_doubles.sort()
    return daily_doubles

def get_category_accuracies(clueFile,categories,epNum):
    correctAttempts = [0]*14
    incorrectAttempts = [0]*14
    with open(clueFile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if int(row[0])==epNum:
                coordinates = literal_eval(row[4])
                column_number = coordinates[0]
                round_name = row[3]
                if round_name == "Jeopardy":
                    correctAttempts[column_number-1] =correctAttempts[column_number-1]+ int(row[11])
                    incorrectAttempts[column_number-1] =incorrectAttempts[column_number-1]+ int(row[12])

                elif round_name == "Double Jeopardy":
                    correctAttempts[column_number+5] =correctAttempts[column_number+5]+ int(row[11])
                    incorrectAttempts[column_number+5] =incorrectAttempts[column_number+5]+ int(row[12])
                elif round_name == "Final Jeopardy":
                    correctAttempts[column_number+11] =correctAttempts[column_number+11]+ int(row[11])
                    incorrectAttempts[column_number+11] =incorrectAttempts[column_number+11]+ int(row[12])
                else:
                    correctAttempts[column_number+12] =correctAttempts[column_number+12]+ int(row[11])
                    incorrectAttempts[column_number+12] =incorrectAttempts[column_number+12]+ int(row[12])
            if int(row[0])>epNum:
                break
    return correctAttempts,incorrectAttempts

def get_selection_orders(clueFile, categories,epNum):
    #Initialize selection order as empty for now so that in the end, we can see if any category had unpicked clues
    selection_orders = [["_"]*5 for i in range(12)]
    num_unpicked_clues = [0]*12

    j_clues_picked = 0
    dj_clues_picked = 0

    #Get pick orders for each category
    with open(clueFile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if int(row[0])==epNum:
                order = int(row[6])
                coordinates = literal_eval(row[4])
                column_number = coordinates[0]
                row_number = coordinates[1]

                round_name = row[3]
                if round_name == "Jeopardy":
                    selection_orders[column_number-1][row_number-1]=order
                    j_clues_picked = max(j_clues_picked,order)
                if round_name == "Double Jeopardy":
                    selection_orders[column_number+5][row_number-1]=order
                    dj_clues_picked = max(dj_clues_picked,order)
            if int(row[0])>epNum:
                break
    #Count how many clues were unpicked in each category
    for index, category in enumerate(selection_orders):
        for x in category:
            if x=="_":
                num_unpicked_clues[index]=num_unpicked_clues[index]+1

    modified_selection_orders = selection_order_formula(selection_orders, j_clues_picked, dj_clues_picked)

    return selection_orders, num_unpicked_clues, modified_selection_orders

def selection_order_formula(selection_orders, j_clues_picked, dj_clues_picked):
    modified_selection_orders = selection_orders
    for index,category in enumerate(selection_orders):
        #Single Jeopardy
        if index<7:
            for idx,order in enumerate(category):
                if order == "_":
                    category[idx]=float(j_clues_picked+1+30)/2
        #Double Jeopardy
        else:
            for idx,order in enumerate(category):
                if order == "_":
                    category[idx]=float(dj_clues_picked+1+30)/2
    return modified_selection_orders

def get_tourn_ep_list(filename):
    result = []
    with open(filename,'r',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            result = result + list(range(int(row[0]),int(row[1])+1))
    return result

def read_from_csv(filename):
    result = []
    with open(filename,'r',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        for row in reader:
            d = {}
            for h, v in zip(headers, row):
                d[h] = v
            result.append(d)
    return result

def write_to_csv(filename, data):
    with open(filename,'w+',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = data[0].keys()
        writer.writerow(list(keys))
        for d in data:
            writer.writerow([d[key] for key in keys])

if __name__ == "__main__":
    main()