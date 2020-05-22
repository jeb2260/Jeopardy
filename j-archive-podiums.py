from bs4 import BeautifulSoup
import requests
import time
import lxml
import sys
import os
import re
import csv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(CURRENT_DIR, 'podium-data')
J_ARCHIVE_DIR = os.path.join(CURRENT_DIR, 'j-archive-csv')
SITE_FOLDER = os.path.join(CURRENT_DIR, "j-archive archive")


def main():
    #allEpisodes = get_episode_range(36,36)
    #create_save_folder()
    listfile = os.path.join(FOLDER, 'episode-list.csv')
    #write_to_csv(listfile, allEpisodes)
    cluefile = os.path.join(J_ARCHIVE_DIR,'j-archive-season-36.csv')
    tournfile = os.path.join(FOLDER, 'tournament-episodes.csv')
    podiumData = get_podium_data(listfile,tournfile, cluefile)
    datafile = os.path.join(FOLDER, 'podium-data.csv')
    write_to_csv(datafile,podiumData)

#Calculate how many correct/incorrect responses each contestant gave
#Optimize this in future by just reading it from BeautifulSoup page
def get_accuracy_data(episodeNum, cluefile):
    #Accuracies[0] = # of Jeopardy questions left contestant got correct 
    #Accuracies[1] = # of Jeopardy questions left contestant got incorrect
    #Accuracies[2] = # of Double Jeopardy questions left contestant got correct
    #Accuracies[3] = # of Double Jeopardy questions left contestant got incorrect
    #Accuracies[4] = # of Final Jeopardy questions left contestant got correct
    #Accuracies[5] = # of Final Jeopardy questions left contestant got incorrect
    #Accuracies[6] = # of Tiebreaker Jeopardy questions left contestant got correct
    #Accuracies[7] = # of Tiebreaker Jeopardy questions left contestant got incorrect
    #etc
    accuracies = [0] * 27
    #Open csv file in read mode with utf-8 encoding
    with open(cluefile,'r',newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        #Traverse row by row
        for row in csv_reader:
            if int(row[0])==episodeNum:
                #Check which round it is
                if row[3]=='Jeopardy':
                    #Right contestant
                    if int(row[-1]) < 0:
                        accuracies[17] = accuracies[17] + 1
                    if int(row[-1]) > 0:
                        accuracies[16] = accuracies[16] + 1
                    #Middle contestant
                    if int(row[-2]) < 0:
                        accuracies[9] = accuracies[9] + 1
                    if int(row[-2]) > 0:
                        accuracies[8] = accuracies[8] + 1
                    #LeftContestant
                    if int(row[-3]) < 0:
                        accuracies[1] = accuracies[1] + 1
                    if int(row[-3]) > 0:
                        accuracies[0] = accuracies[0] + 1

                elif row[3]=='Double Jeopardy':
                    #Right contestant
                    if int(row[-1]) < 0:
                        accuracies[19] = accuracies[19] + 1
                    if int(row[-1]) > 0:
                        accuracies[18] = accuracies[18] + 1
                    #Middle contestant
                    if int(row[-2]) < 0:
                        accuracies[11] = accuracies[11] + 1
                    if int(row[-2]) > 0:
                        accuracies[10] = accuracies[10] + 1
                    #LeftContestant
                    if int(row[-3]) < 0:
                        accuracies[3] = accuracies[3] + 1
                    if int(row[-3]) > 0:
                        accuracies[2] = accuracies[2] + 1

                elif row[3]=='Final Jeopardy':
                    #Right contestant
                    if int(row[-1]) < 0:
                        accuracies[21] = accuracies[21] + 1
                    if int(row[-1]) > 0:
                        accuracies[20] = accuracies[20] + 1
                    #Middle contestant
                    if int(row[-2]) < 0:
                        accuracies[13] = accuracies[13] + 1
                    if int(row[-2]) > 0:
                        accuracies[12] = accuracies[12] + 1
                    #LeftContestant
                    if int(row[-3]) < 0:
                        accuracies[5] = accuracies[5] + 1
                    if int(row[-3]) > 0:
                        accuracies[4] = accuracies[4] + 1
                #Tiebreaker
                else:
                    #Right contestant
                    if int(row[-1]) < 0:
                        accuracies[23] = accuracies[23] + 1
                    if int(row[-1]) > 0:
                        accuracies[22] = accuracies[22] + 1
                    #Middle contestant
                    if int(row[-2]) < 0:
                        accuracies[15] = accuracies[15] + 1
                    if int(row[-2]) > 0:
                        accuracies[14] = accuracies[14] + 1
                    #LeftContestant
                    if int(row[-3]) < 0:
                        accuracies[7] = accuracies[7] + 1
                    if int(row[-3]) > 0:
                        accuracies[6] = accuracies[6] + 1
            if int(row[0])>episodeNum:
                break
        total_accuracies = [accuracies[0]+accuracies[2]+accuracies[4]+accuracies[6],accuracies[1]+accuracies[3]+accuracies[5]+accuracies[7],
        accuracies[8]+accuracies[10]+accuracies[12]+accuracies[14], accuracies[9]+accuracies[11]+accuracies[13]+accuracies[15],
        accuracies[16]+accuracies[18]+accuracies[20]+accuracies[22], accuracies[17]+accuracies[19]+accuracies[21]+accuracies[23]]
    return accuracies, total_accuracies

def get_scores(episodeNum):
    #[0] = score at end of Jeopardy round (for left contestant)
    #[1] = score at end of DJ round (for left contestant)
    #[2] = score at end of FJ round (for left contestant)
    #[3] = score at end of FJ round (for middle contestant)
    #etc
    print(episodeNum)
    round_scores = []

    season = 36

    season_folder = os.path.join(SITE_FOLDER, 'season {}'.format(season))
    #this list comprehension doesn't preseve episode order so I'll sort it manually
    episode_file = os.path.join(season_folder, '{}.html'.format(episodeNum))
    #Get episode page
    episode = open(episode_file, encoding="utf-8")
    soupEpisode = BeautifulSoup(episode, 'lxml')
    episode.close()

    #Because of inconsistencies in titles of how many clues at the first commercial break, we need this workaround
    for h3 in soupEpisode.find_all('h3'):
        if 'Scores at the first commercial break' in h3.text:
            commercial_break_table = str(soupEpisode).split(str(h3))[1]
            break

    table = BeautifulSoup(commercial_break_table, "lxml")

    first_commercial_break = [int(score.text.replace('$','').replace(',','')) for score in table.find('table').find_all('tr')[1].find_all('td')]

    first_round_scores = [int(score.text.replace('$','').replace(',','')) for score in soupEpisode.find('h3', string='Scores at the end of the Jeopardy! Round:').findNext('table').find_all('tr')[1].find_all('td')]

    second_round_scores = [int(score.text.replace('$','').replace(',','')) for score in soupEpisode.find('h3', string='Scores at the end of the Double Jeopardy! Round:').findNext('table').find_all('tr')[1].find_all('td')]

    final_scores = [int(score.text.replace('$','').replace(',','')) for score in soupEpisode.find('h3', string='Final scores:').findNext('table').find_all('tr')[1].find_all('td')]

    coryat_scores = [int(score.text.replace('$','').replace(',','')) for score in soupEpisode.find('a', href="http://www.j-archive.com/help.php#coryatscore").findNext('table').find_all('tr')[1].find_all('td')]

    round_scores = first_commercial_break

    round_scores.extend(first_round_scores)
    round_scores.extend(second_round_scores)
    round_scores.extend(final_scores)
    round_scores.extend(coryat_scores)

    return round_scores


#Create that file with all the podiums
def get_podium_data(episodesFile,tournamentsFile, cluefile):
    allEpisodes = read_from_csv(episodesFile)[::-1]
    tournEps = get_tourn_ep_list(tournamentsFile)
    results = []
    episode_i = 0
    #Traverses all episodes
    #CHANGE: -1 to -2 because of the whole "next episode still hasn't happened and thus doens't appear" thing
    while episode_i < len(allEpisodes)-2:
        sys_print("Episode {} out of {}, id no. {}, game no. {}".format(episode_i,len(allEpisodes),allEpisodes[ episode_i ]['gameId'],allEpisodes[ episode_i ]['epNum']))
        offset = 1
        currentEp = allEpisodes[ episode_i ]
        nextEp = allEpisodes[ episode_i+offset ]
        # Why the offset?
        # Increase offset until next episode is non-tournament (this is why)
        while (int(nextEp['epNum']) in tournEps):
            offset += 1
            nextEp = allEpisodes[ episode_i+offset ]
        #Split the contestants by the "vs"
        currentContestants = re.split(r' vs\. ', currentEp['contestants'])


        round_accuracies, total_accuracies = get_accuracy_data(int(currentEp['epNum']), cluefile)

        round_scores = get_scores(int(currentEp['epNum']))


        ######################CHECK WHO WON (by either analyzing next game or by brute force)##########################
        winnerIndices = []
        # Check if episodes are immediately before/after each other
        # If they are, can use list of contestant names to determine winner(s)
        # If not, need to request game page and parse winner(s)
        # NOTE: There may be gaps in between games, shouldn't be an issue for newer games
        if int(nextEp['epNum']) == int(currentEp['epNum'])+offset:
            nextContestants = re.split(r' vs\. ', nextEp['contestants'])
            #Use set intersection to find the winner, since winner is the only next person
            champSet = set(currentContestants).intersection(nextContestants)
            #Handles the edge case where you have more than one winner?
            winnerIndices = [i for i, contestant in enumerate(currentContestants) if contestant in champSet]
        else:
            winnerIndices = parse_winners(currentEp['gameId'])
            time.sleep(5)
        results.append({
            "gameId": int(currentEp['gameId']),
            "season": int(currentEp['season']),
            "epNum": int(currentEp['epNum']),
            "date": currentEp['date'],
            "left": currentContestants[0],
            "middle": currentContestants[1],
            "right": currentContestants[2],
            "winnerIndices": winnerIndices,
            "LeftCorrect": total_accuracies[0],
            "LeftIncorrect": total_accuracies[1],
            "MiddleCorrect": total_accuracies[2],
            "MiddleIncorrect": total_accuracies[3],
            "RightCorrect": total_accuracies[4],
            "RightIncorrect": total_accuracies[5],
            "FinalLeft":round_scores[-6],
            "FinalMiddle":round_scores[-5],
            "FinalRight": round_scores[-4],
            "CoryatLeft": round_scores[-3],
            "CoryatMiddle": round_scores[-2],
            "CoryatRight": round_scores[-1],
            "CommercialLeft": round_scores[0],
            "CommercialMiddle": round_scores[1],
            "CommercialRight": round_scores[2],
            "JLeft": round_scores[3],
            "JMiddle": round_scores[4],
            "JRight": round_scores[5],
            "DJLeft": round_scores[6],
            "DJMiddle": round_scores[7],
            "DJRight": round_scores[8],
            "LeftJCorrect": round_accuracies[0],
            "LeftJIncorrect": round_accuracies[1],
            "LeftDJCorrect": round_accuracies[2],
            "LeftDJIncorrect": round_accuracies[3],
            "LeftFJCorrect": round_accuracies[4],
            "LeftFJIncorrect": round_accuracies[5],
            "LeftTieCorrect": round_accuracies[6],
            "LeftTieIncorrect": round_accuracies[7],
            "MiddleJCorrect": round_accuracies[8],
            "MiddleJIncorrect": round_accuracies[9],
            "MiddleDJCorrect": round_accuracies[10],
            "MiddleDJIncorrect": round_accuracies[11],
            "MiddleFJCorrect": round_accuracies[12],
            "MiddleFJIncorrect": round_accuracies[13],
            "MiddleTieCorrect": round_accuracies[14],
            "MiddleTieIncorrect": round_accuracies[15],
            "RightJCorrect": round_accuracies[16],
            "RightJIncorrect": round_accuracies[17],
            "RightDJCorrect": round_accuracies[18],
            "RightDJIncorrect": round_accuracies[19],
            "RightFJCorrect": round_accuracies[20],
            "RightFJIncorrect": round_accuracies[21],
            "RightTieCorrect": round_accuracies[22],
            "RightTieIncorrect": round_accuracies[23]
        })
        episode_i += offset
    return results

def create_save_folder():
    if not os.path.isdir(FOLDER):
        print('Creating %s folder' % FOLDER)
        os.mkdir(FOLDER)

#Brute force method of finding winner for a specific episode
def parse_winners(episodeId):
    page = requests.get("http://www.j-archive.com/showgame.php?game_id={}".format(episodeId))
    pageSoup = BeautifulSoup(page.text, 'lxml')
    try:
        #Seems like "score" is a variable embedded in the page
        #First part removes dollar signs and commas, so $3,000-->3000
        #idk what find_all('tr')
        finalScores = [int(score.text.replace('$','').replace(',','')) for score in pageSoup.find('h3', string='Final scores:').findNext('table').find_all('tr')[1].find_all('td')]
    except:
        print("No final scores section for game with ID {}".format(episodeId))
        return []
    adjustedScores = [score if score >= 0 else 0 for score in finalScores]
    maxScore = max(adjustedScores)
    #Why not just return maxScore?
    #^Because you want to return the index (contestant #) of the winner, not their score
    return [i for i, score in enumerate(adjustedScores) if score == maxScore and score != 0]


def get_episode_list(season):
    seasonPage = requests.get('http://j-archive.com/showseason.php?season={}'.format(season))
    seasonSoup = BeautifulSoup(seasonPage.text, 'lxml')
    #\d{1,4} captures up to 4 digits
    epNumRe = re.compile(r'\#(\d{1,4})')
    #Date format (year-month-day)
    epDateRe = re.compile(r'\d{4}-\d{2}-\d{2}')
    gameIdRe = re.compile(r'game_id=(\d+)')
    episodes = [row.find_all('td') for row in seasonSoup.find_all('tr')]
    return [{
                "season": season,
                "epNum": epNumRe.search(episode[0].text.strip()).group(1),
                "gameId": gameIdRe.search(episode[0].a['href']).group(1),
                "date": epDateRe.search(episode[0].text.strip()).group(0),
                "contestants": episode[1].text.strip(),
                "info": episode[2].text.strip()
            }
            for episode in episodes]

def get_episode_range(start,end):
    episodes = []
    for season in range(start,end+1):
        sys_print("Season {}".format(season))
        episodes = get_episode_list(season) + episodes
        time.sleep(5)
    return episodes

def get_tourn_ep_list(filename):
    result = []
    with open(filename,'r',newline='',encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            result = result + list(range(int(row[0]),int(row[1])+1))
    return result

def sys_print(string):
    sys.stdout.write("{}\n".format(string))
    sys.stdout.flush()

def write_to_csv(filename, data):
    with open(filename,'w+',newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = data[0].keys()
        writer.writerow(list(keys))
        for d in data:
            writer.writerow([d[key] for key in keys])

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

if __name__=="__main__":
    main()