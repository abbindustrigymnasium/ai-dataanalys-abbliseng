import csv
import matplotlib.pyplot as plt
from matplotlib import colors

#tour_de_spartacusData

# Global Variables
rawData = []
overallData = [] #Data for the whole of the training, mostly averages
allData = [] #Arrays for plotting
baseValue = []
ui_width = 40
k = 1
name = ''
phc = {'p':0,'h':0,'c':0}
avehrZone = 0
maxPulse = 189 #Let user enter or calculate ~(220-age)
averageStep = 11
newDataPoint = None
indexes = {}
heartRateZones = [
    {'Intensity': 'Unlisted', 'PercentageOfMax': [0,50], 'Level':0,"Comment":"It's called unlisted for a reason..."},
    {'Intensity': 'Very light', 'PercentageOfMax': [50,60], 'Level':1,"Comment":"We're getting somewhere! Push alittle harder next time!"},
    {'Intensity': 'Light', 'PercentageOfMax': [60,70], 'Level':2,"Comment":"Good, not great but not bad. Just good."},
    {'Intensity': 'Moderate', 'PercentageOfMax': [70,80], 'Level':3,"Comment":"Well done! I'm very proud!"},
    {'Intensity': 'Hard', 'PercentageOfMax': [80,90], 'Level':4,"Comment":"Nice! Next time try pushing alittle harder!"},
    {'Intensity': 'Maximum', 'PercentageOfMax': [90,100], 'Level':5,"Comment":"Try hard..."}
]
# Define functions
def calculateTime(start, now):
    diff = []
    for i in range(len(start)):
        diff.append(int(now[i])-int(start[i]))
    for i in range(len(diff)):
        if diff[-(i+1)] < 0: #check if the time is invalid/negative
            diff[-(i+1)] += 60
            diff[-(i+2)] -= 1
    for i in range(len(diff)):
        diff[i] = str(diff[i])
        if len(diff[i]) < 2:
            diff[i] ='0'+diff[i]
        if i == 0:
            diff[i] += '.'
    return float(''.join(diff))

def getHRZone(cPulse,mPulse):
    percentage = round((cPulse/mPulse)*100,2)
    for zone in heartRateZones:
        if percentage>=zone['PercentageOfMax'][0] and percentage<=zone['PercentageOfMax'][1]:
            return zone

def transform(inputData):
    transformData = []
    for dataPointIndex in range(len(inputData)):
        averageValue = inputData[dataPointIndex]
        for step in range(int((averageStep-1)/2)):
            try:
                averageValue += (inputData[dataPointIndex+step]*(k**step))
                averageValue += (inputData[dataPointIndex-step]*(k**step))
            except:
                pass
        averageValue = averageValue/averageStep
        newDataPoint = averageValue
        transformData.append(newDataPoint)
    return transformData

def filter(times,inputData):
    transformedData = None
    for i in range(times):
        if i == 0:
            transformedData = transform(inputData)
        else:
            transformedData = transform(transformedData)
    return transformedData
    
def getMaxPulse():
    placeholder = input("Enter maxpulse, leave blank for automatic > ")
    try:
        return int(placeholder)
    except ValueError:
        age = input("Enter your age > ")
        try:
            return 220-int(age)
        except ValueError:
            print("ERROR: Invalid input")
            exit()

def graph(xGraph,yGraph,x,y,label = ""):
    axs[xGraph,yGraph].plot(x,y)
    axs[xGraph,yGraph].set_title(label)

# Read in and format data to the desired structure
try:
    with open('./'+input('Enter file name > ')+'.csv', newline='') as csvfile:
        maxPulse = getMaxPulse()
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for index, row in enumerate(spamreader):
            if index != 0: #The 0th element holds titels
                # Add the location values to rawData
                location = [float(row[indexes["lat"]]),float(row[indexes["lon"]]),float(row[indexes["ele"]])]
                # Get base values and format the timestamp
                timestamp = row[indexes["time2"]].replace('Z','').split('T')
                if index == 1:
                    currentDate = timestamp[0]
                    startTime = timestamp[1].split(':')
                    name = row[indexes["name"]]
                # Add the current time trained to rawData
                timestamp = calculateTime(startTime,timestamp[1].split(':')) #Instead of current time calculate total training time
                # Add the PHC values to rawData
                phc = [float(row[indexes["power"]]),float(row[indexes["hr"]]),float(row[indexes["cad"]])]
                # Calculate the current heart rate zone
                hrZone = getHRZone(phc[1], maxPulse)
                avehrZone += hrZone['Level']
                # Add the actual values to the rawData array
                rawData.append({'location':location,'timestamp':timestamp,'phc':phc, 'heartRateZone': hrZone})
            else:
                for i, item in enumerate(row):
                    indexes[item] = i
except FileNotFoundError:
    print('-'*ui_width)
    print('An error occured when attempting to open\nthe file, please make sure the file is\nin same directory and try again.')
    print('-'*ui_width)
    input()
    exit()

overallData = {'time':str(rawData[-1]['timestamp']),'aveHRZone':round(avehrZone/len(rawData),2)}
allData = {'locations': [[],[],[]],'timestamps':[],'heartRateZones':[],'PHCs':[[],[],[]]} #Prepare the variable

for row in rawData: #Insert all data into the allData variable
    allData['locations'][0].append(row['location'][0]) #
    allData['locations'][1].append(row['location'][1]) #
    allData['locations'][2].append(row['location'][2]) #
    allData['timestamps'].append(row['timestamp']) 
    allData['heartRateZones'].append(row['heartRateZone']['Level']) #
    allData['PHCs'][0].append(row['phc'][0]) #
    allData['PHCs'][1].append(row['phc'][1]) #
    allData['PHCs'][2].append(row['phc'][2]) #



print('-'*ui_width)
print('Calculating...')
print('-'*ui_width)

averageData = {'PHCs':[filter(30,allData['PHCs'][0]),[],filter(30,allData['PHCs'][2])]} #Prepare the variable

# plt.hist([10,10,20,35,10,12],bins=[10,20,30,40])
# plt.show()
fig, axs = plt.subplots(4,2)
graph(0,0,allData['locations'][0],allData['locations'][1],"Map")
graph(1,0,range(len(allData['locations'][2])),allData['locations'][2],"Elevation")
graph(2,0,range(len(allData['PHCs'][0])),allData['PHCs'][0],'Power')
graph(3,0,range(len(allData['PHCs'][2])),allData['PHCs'][2],"Cadence")

# graph(0,1,range(len(allData['heartRateZones'])),allData['heartRateZones'],"Heart Rate Zone")
graph(1,1,range(len(allData['PHCs'][1])),allData['PHCs'][1],"Heart Rate")

graph(2,1,range(len(averageData['PHCs'][0])),averageData['PHCs'][0], "Average Power")
graph(3,1,range(len(averageData['PHCs'][2])),averageData['PHCs'][2], "Average Cadence")

axs[0,1].hist(allData['heartRateZones'],bins=[1,2,3,4,5,6])

fig.suptitle(name)

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

## Show in terminal for user USER INTERFACE
print('Overall data'.center(ui_width))
print('-'*ui_width)
print('Max Pulse'.ljust(17),'|',maxPulse)
print('Time'.ljust(17),'|',overallData['time'][0]+'h '+overallData['time'][2]+overallData['time'][3]+'m '+overallData['time'][4]+overallData['time'][5]+'s')
print('Average HR Zone'.ljust(17),'|',overallData['aveHRZone'])
print('Average Intensity'.ljust(17),'|',heartRateZones[round(overallData['aveHRZone'])]['Intensity'])
print('-'*ui_width)
print(heartRateZones[int(overallData['aveHRZone'])]["Comment"])
print('-'*ui_width)
input('Press enter to view graphs...')
plt.show()