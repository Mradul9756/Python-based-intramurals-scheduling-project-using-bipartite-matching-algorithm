import random 
import string
import pandas as pd
import xlsxwriter


# function to get the keys from dictionary (which are lists in this case)
def getList(dict):
    return dict.keys()

# Importing data from csv file (U-REC real qualdratics input)
# read data and make a df
data = pd.read_csv("/Users/mmourya23/Downloads/Team+Time+Preference+-+Fall+Indoor_December+6,+2021_14.59.csv")

# Q4_1 to Q4_7 represents Monday - Sunday
# Q7 = name of the sport 
# Q1 = Data of the teams
# work with only these columns
columns = ["Q7","Q1","Q4_1","Q4_2","Q4_3","Q4_4","Q4_5","Q4_6","Q4_7"]

# condense the data (remove every column except above mentioned)
data2 = pd.DataFrame(data= data, columns=columns)

data2 = data2.drop([0,1])

# list of unique games
list_unique = data2.Q7.unique()
list_unique

# inside game there are dataframes of data grouped by game
game = [] # create list for storing specific games data
for i in list_unique:
    game.append(data2[data2["Q7"] == i])

# rename the days columns for the ease of user input (it's in int)
for i in range(0,len(game)): 
    game[i] = game[i].rename(columns={"Q4_1":1,"Q4_2":2,"Q4_3":3,"Q4_4":4,"Q4_5":5,"Q4_6":6,"Q4_7":7})

# Return =
# { "a":["3:30","4:30"],
#   "b":["6:00","7:00"],
#   "c":["5:30","6:30","7:30","8:00"],
#   "d":["3:00","4:00","4:30","5:00","5:30","6:00"]}
# value - teams name, keys - available times
def timeList(team, day):
    list_teams = list(game[team]['Q1']) # convert the column with team names into list
    list_times = list(game[team][day]) # convert the column with team times into list
    list_times = list(map(lambda i:[i], list_times)) # convert list to list of lists 
    dictofteams = {}

    for i in range(len(list_teams)):
        dictofteams[list_teams[i]] = str(list_times[i][0]).split(",")
    return dictofteams

print("Enter Game:")
gameNumber = int(input())
print("Enter Day:")
dayNumber = int(input())

# creates the object that has dictionary with teams and times
newTimeList = timeList(gameNumber,dayNumber)

# keys = lists
teams1 = list(getList(newTimeList))

# find the common time between two teams
def common(list1,list2):
    for value in list1:
        if value in list2 and value !='nan': # don't want the nan values
            return value,True
    return False

# Returns  =  {{0, 1, 1, 0, 0, 0},
#              {1, 0, 0, 1, 0, 0},
#              {0, 0, 1, 0, 0, 0},
#              {0, 0, 1, 1, 0, 0},
#              {0, 0, 0, 0, 0, 0},
#              {0, 0, 0, 0, 0, 1}}
def check (newTimeList, teams1):
    noOfTeams = len(newTimeList)
    graph = [[0 for i in range(noOfTeams)] for j in range(noOfTeams)]
    for i in range(0, len(graph)):
        for j in range(0, len(graph[0])):
            if i > j and common(newTimeList[teams1[i]], newTimeList[teams1[j]]):
                graph[i][j] = graph[j][i] = 1
    return graph 


# Bipartite Matching algorithm
# Arguments:
#            1.Graph    : Consist of 2D lists that store the possible matches between all team
#                        size of list= n*n (where n is the number of teams)
#            2.Team     : index of the number of the team
#            3.matches  : default = -1, reprents index of the team. (If they have match, then -1 will 
#                        change to the number of the team they are playing against)
#                        EX: [-1,3,-1,1] => Team no.1 will be playing with team no.3
#            4.isPlaying: Checking if one team has played another team or not
#                        Then it will check if a team can play another team or not
def findPossibleMatch(graph, team, matches, isPlaying):
    for i in range(len(graph)):
        if (graph[team][i] == 1) and (isPlaying[i] == False) and (team != i):
            isPlaying[i] = True
            if matches[i] == -1 or matches[i] == team or findPossibleMatch(graph, matches[i], matches, isPlaying):
                matches[team] = i
                matches[i] = team
                return True
    return False


# return the pairings in a list
def filter(graph):
    noOfTeams = len(graph)
    matches = [-1] * noOfTeams

    for team in range(len(graph)):
        isPlaying = [False] * noOfTeams
        isPlaying[team] = True
        findPossibleMatch(graph, team, matches, isPlaying)
    # get the index of the keys in dict
    list_index = list(newTimeList)
    pairing = []
    for i in matches:
        pairing.append('No match') if i == -1 else pairing.append(list_index[i])
    
    return pairing

# find all the common times between two teams
def common_time (a,b):
    #This is sorted
    gametime = [c for c in a if c in b]
    return (gametime)

final_matches = (filter(check(newTimeList, teams1)))

for i in range(len(final_matches)):
    if final_matches[i]!="No match":
        print(teams1[i], " Vs. ", final_matches[i])
        print (common_time(newTimeList[teams1[i]], newTimeList[final_matches[i]]),"\n")

# print the entire schedule to excel
count = 1
for a in range (0,5):
    for days in range (1,8):
        newTimeList = timeList(a,days)
        teams1 = list(getList(newTimeList))
        def filter(graph):
            noOfTeams = len(graph)
            matches = [-1] * noOfTeams
            for team in range(len(graph)):
                isPlaying = [False] * noOfTeams
                isPlaying[team] = True
                findPossibleMatch(graph, team, matches, isPlaying)
            # get the index of the keys in dict
            list_index = list(newTimeList)
            pairing = []
            for i in matches:
                pairing.append('No match') if i == -1 else pairing.append(list_index[i])
            return pairing
        final_matches = (filter(check(newTimeList, teams1)))
        workbook = xlsxwriter.Workbook('Result'+str(count)+'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write (0,0, "Team Name")
        worksheet.write (0,1, "Time")
        row = 1
        for i in range(((len(final_matches))+1//2)):
            if final_matches[i]!="No match":
                worksheet.write (row,0, str(teams1[i])+" vs "+ str(final_matches[i]))
                listoftime = common_time(newTimeList[teams1[i]], newTimeList[final_matches[i]])
                worksheet.write (row,1, str(listoftime))
                row+=1
        count+=1
        workbook.close()