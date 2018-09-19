import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import time
import matplotlib.animation as animation
import socket
import state
import signal
import sys


fig = plt.figure('Live Plotting')
ax = fig.add_subplot(111)

##figHumid = plt.figure()
##axHumid = figHumid.add_subplot(111)

heatMap = [[-1 for x in range(100)] for y in range(100)]
humidityHeatMap = [[-1 for x in range(100)] for y in range(100)]

print('<< press CTRL+C to terminity >>')

plt.show(block=False)

def plotHumid(newHumidityHeatMap):

##    print(str(len(newHumidityHeatMap[0])))
##    for rowIterator in range(len(newHumidityHeatMap)):
##        for columnIterator in range(len(newHumidityHeatMap[0])):
##            print(newHumidityHeatMap[rowIterator][columnIterator], end="")
##            print(" ", end="")
##        print("")

    figHumid = plt.figure('humidity Figure')
    axHumid = figHumid.add_subplot(111)

    
    dfHumid = pd.DataFrame(newHumidityHeatMap)
    axHumid = sns.heatmap(dfHumid)
    axHumid.invert_yaxis()
    
    plt.title('** HeatMap (Humidity)** ')
    plt.xlabel('X Coordinate (Deci-Meter per unit)')
    plt.ylabel('y Coordinate (Deci-Meter per unit)')


    print('showed')
    plt.show()
    #figHumid.canvas.draw()
    print('here')
    return

def regrate(newHeatMap,newHumidityHeatMap):

    startTime = time.time()

    arrayRowCount, arrayColumnCount = len(newHeatMap), len(newHeatMap[0])
    #print(len(HeatMap))
    
    figTemp = plt.figure('Temparature Figure')
    axTemp = figTemp.add_subplot(111)


    
    plt.show(block=False)
   
    sentinel = True
    sentinel2 = True
    boundaryDistanceThreshold = 2

    topNeighbor = -1
    rightNeighbor = -1
    bottomNeighbor = -1
    leftNeighbor = -1

    count = 0
    while (sentinel and sentinel2):
        sentinel = False  # Assume that there are no more blind spots
        sentinel2 = False # Detect interpolation in whole matrix
        
        for rowIterator in range(len(newHeatMap)):
            for columnIterator in range(len(newHeatMap[0])):
                sentinel3 = False # Detect interpolation in a single index
               
                if newHeatMap[rowIterator][columnIterator] == -1:
                    sentinel = True  # Keep looping until we find that there are no more blind spots

                    ''' Search for the nearest neighbors '''
                    # Top neighbor
                    topNeighbor = rowIterator - 1
                    while topNeighbor >= 0:
                        if newHeatMap[topNeighbor][columnIterator] != -1:
                            break
                        topNeighbor -= 1
                    # At this point topNeighbor contains either -
                    #    Y co-ordinate of the nearest top neighbor IF one exists
                    #    -1                                        IF no neighbor exist

                    # Right neighbor
                    rightNeighbor = columnIterator + 1
                    while rightNeighbor < len(newHeatMap[0]):
                        if newHeatMap[rowIterator][rightNeighbor] != -1:
                            break
                        rightNeighbor += 1
                    if rightNeighbor == len(newHeatMap[0]):
                        rightNeighbor = -1
                    # At this point rightNeighbor contains either -
                    #    X co-ordinate of the nearest right neighbor IF one exists
                    #    -1                                          IF no neighbor exist

                    # Bottom neighbor
                    bottomNeighbor = rowIterator + 1
                    while bottomNeighbor < len(newHeatMap):
                        if newHeatMap[bottomNeighbor][columnIterator] != -1:
                            break
                        bottomNeighbor += 1
                    if bottomNeighbor == len(newHeatMap):
                        bottomNeighbor = -1
                    # At this point rightNeighbor contains either -
                    #    Y co-ordinate of the nearest bottom neighbor IF one exists
                    #    -1                                           IF no neighbor exist

                    # Left neighbor
                    leftNeighbor = columnIterator - 1
                    while leftNeighbor >= 0:
                        if newHeatMap[rowIterator][leftNeighbor] != -1:
                            break
                        leftNeighbor -= 1
                        #print (leftNeighbor)
                    # At this point topNeighbor contains either -
                    #    X co-ordinate of the nearest left neighbor IF one exists
                    #    -1                                         IF no neighbor exist

                    if leftNeighbor != -1 and rightNeighbor != -1:

                        sentinel2 = True
                        sentinel3 = True

                        offSetTemp = (newHeatMap[rowIterator][rightNeighbor] - newHeatMap[rowIterator][leftNeighbor]) / (rightNeighbor - leftNeighbor)
                        offSetTemp = float(offSetTemp)

                        offSetHumid = (newHumidityHeatMap[rowIterator][rightNeighbor] - newHumidityHeatMap[rowIterator][leftNeighbor]) / (rightNeighbor - leftNeighbor)
                        offSetHumid = float(offSetHumid)

                        #print(str(leftNeighbor) + '--' + str(rightNeighbor))
                        
                        if(newHeatMap[rowIterator][rightNeighbor] >= newHeatMap[rowIterator][leftNeighbor]):

                            #print(str(heatMap[rowIterator][rightNeighbor]) + '--++' + str(heatMap[rowIterator][leftNeighbor]))
                            
                            x = leftNeighbor + 1
                            y = leftNeighbor

                            while rightNeighbor > x:
                                newHeatMap[rowIterator][x] = float(newHeatMap[rowIterator][y]) + offSetTemp
                                newHeatMap[rowIterator][y+1] = float(newHeatMap[rowIterator][x])
                                x = x + 1
                                y = y + 1
                                
                        elif(newHeatMap[rowIterator][rightNeighbor] <= newHeatMap[rowIterator][leftNeighbor]):

                            x = leftNeighbor + 1
                            y = leftNeighbor
                            
                            while rightNeighbor > x:
                                newHeatMap[rowIterator][x] = float(newHeatMap[rowIterator][y]) + offSetTemp
                                newHeatMap[rowIterator][y+1] = float(newHeatMap[rowIterator][x])
                                #print(str(newHeatMap[rowIterator][y+1]))
                                x = x + 1
                                y = y + 1
                                
                        if(newHumidityHeatMap[rowIterator][rightNeighbor] >= newHumidityHeatMap[rowIterator][leftNeighbor]):

                            x = leftNeighbor + 1
                            y = leftNeighbor

                            while rightNeighbor > x:
                                newHumidityHeatMap[rowIterator][x] = float(newHumidityHeatMap[rowIterator][y]) + offSetHumid
                                newHumidityHeatMap[rowIterator][y+1] = float(newHumidityHeatMap[rowIterator][x])
                                #print(str(newHumidityHeatMap[rowIterator][y+1]))
                                x = x + 1
                                y = y + 1
                                
                        elif(newHumidityHeatMap[rowIterator][rightNeighbor] <= newHumidityHeatMap[rowIterator][leftNeighbor]):

                            x = leftNeighbor + 1
                            y = leftNeighbor
                            
                            while rightNeighbor > x:
                                newHumidityHeatMap[rowIterator][x] = float(newHumidityHeatMap[rowIterator][y]) + offSetHumid
                                newHumidityHeatMap[rowIterator][y+1] = float(newHumidityHeatMap[rowIterator][x])
                                #print(str(newHumidityHeatMap[rowIterator][y+1]))
                                x = x + 1
                                y = y + 1  
                            
                                       
                    if topNeighbor != -1 and bottomNeighbor != -1:

                        sentinel2 = True
                        sentinel3 = True

                        offSetTemp = (newHeatMap[bottomNeighbor][columnIterator] - newHeatMap[topNeighbor][columnIterator]) / (bottomNeighbor - topNeighbor)
                        offSetTemp = float(offSetTemp)

                        offSetHumid = (newHumidityHeatMap[bottomNeighbor][columnIterator] - newHumidityHeatMap[topNeighbor][columnIterator]) / (bottomNeighbor - topNeighbor)
                        offSetHumid = float(offSetHumid)
                        
                        if(newHeatMap[bottomNeighbor][columnIterator] >= newHeatMap[topNeighbor][columnIterator]):

                            x = topNeighbor + 1
                            y = topNeighbor

                            while bottomNeighbor > x:
                                newHeatMap[x][columnIterator] = float(newHeatMap[y][columnIterator]) + offSetTemp
                                newHeatMap[y+1][columnIterator] = float(newHeatMap[x][columnIterator])
                                x = x + 1
                                y = y + 1

                        elif (newHeatMap[bottomNeighbor][columnIterator] <= newHeatMap[topNeighbor][columnIterator]): 
                            x = topNeighbor + 1
                            y = topNeighbor

                            while bottomNeighbor > x:
                                newHeatMap[x][columnIterator] = float(newHeatMap[y][columnIterator]) + offSetTemp
                                newHeatMap[y+1][columnIterator] = float(newHeatMap[x][columnIterator])
                                x = x + 1
                                y = y + 1

                        if(newHumidityHeatMap[bottomNeighbor][columnIterator] >= newHumidityHeatMap[topNeighbor][columnIterator]):

                            x = topNeighbor + 1
                            y = topNeighbor

                            while bottomNeighbor > x:
                                newHumidityHeatMap[x][columnIterator] = float(newHumidityHeatMap[y][columnIterator]) + offSetHumid
                                newHumidityHeatMap[y+1][columnIterator] = float(newHumidityHeatMap[x][columnIterator])
                                x = x + 1
                                y = y + 1

                        elif (newHumidityHeatMap[bottomNeighbor][columnIterator] <= newHumidityHeatMap[topNeighbor][columnIterator]): 
                            x = topNeighbor + 1
                            y = topNeighbor

                            while bottomNeighbor > x:
                                newHumidityHeatMap[x][columnIterator] = float(newHumidityHeatMap[y][columnIterator]) + offSetHumid
                                newHumidityHeatMap[y+1][columnIterator] = float(newHumidityHeatMap[x][columnIterator])
                                x = x + 1
                                y = y + 1
                    
                if sentinel3:
                    print("", end="")
                    # Animation code starts here

                    dfTemp = pd.DataFrame(newHeatMap)
                    axTemp = sns.heatmap(dfTemp,cbar=False)
                    axTemp.invert_yaxis()
                    plt.title('** HeatMap (Temparature) ** ')
                    plt.xlabel('X Coordinate (Deci-Meter per unit)')
                    plt.ylabel('y Coordinate (Deci-Meter per unit)')

                    fig.canvas.draw()

    dfTemp = pd.DataFrame(newHeatMap)
    axTemp = sns.heatmap(dfTemp)
    axTemp.invert_yaxis()
    plt.title('** HeatMap (Temparature)** ')
    plt.xlabel('X Coordinate (Deci-Meter per unit)')
    plt.ylabel('y Coordinate (Deci-Meter per unit)')

##    for rowIterator in range(len(newHumidityHeatMap)):
##        for columnIterator in range(len(newHumidityHeatMap[0])):
##            print(newHumidityHeatMap[rowIterator][columnIterator], end="")
##            print(" ", end="")
##        print("")
##    print('----------------------')

    plotHumid(newHumidityHeatMap)

    print('finished ploting')

    return


def crop():
    rowCount = len(heatMap)
    columnCount = len(heatMap[0])

    while rowCount > 0:
        sentinel = False
        for columnIterator in range(len(heatMap[0])):
            if heatMap[rowCount-1][columnIterator] != -1:
                sentinel = True
                break
        if sentinel:
            break
        rowCount -= 1

    while columnCount > 0:
        sentinel = False
        for rowIterator in range(len(heatMap)):
            if heatMap[rowIterator][columnCount-1] != -1:
                sentinel = True
                break
        if sentinel:
            break
        columnCount -= 1


    #print(str(rowCount) + "---" + str(columnCount))
    
    newHeatMap = [[-1 for columnIterator in range(columnCount)] for rowIterator in range(rowCount)]
    newHumidityHeatMap = [[-1 for columnIterator in range(columnCount)] for rowIterator in range(rowCount)]
    
    for rowIterator in range(rowCount):
        for columnIterator in range(columnCount):
            newHeatMap[rowIterator][columnIterator] = heatMap[rowIterator][columnIterator]
            newHumidityHeatMap[rowIterator][columnIterator] = humidityHeatMap[rowIterator][columnIterator]

            
    regrate(newHeatMap,newHumidityHeatMap)
    plt.xlabel('X Coordinate (Deci-Meter per unit)')
    plt.ylabel('y Coordinate (Deci-Meter per unit)')
    return newHeatMap

##def animate(i):
##    graph_data = open('rawData.txt','r').read()
##    lines = graph_data.split('\n')
##    print(i)
##
##    for line in lines:
##        if len(line) > 1:
##            x, y,humidity,temparature = line.split(',')
##            #print(str(x) + '-- ' + str(y) + "--" + str(v)) 
##            heatMap[int(x)][int(y)] = float(temparature)
##            humidityHeatMap[int(x)][int(y)] = float(humidity)
##               
##            df = pd.DataFrame(heatMap)
##            ax = sns.heatmap(df, cbar=False)
##            ax.invert_yaxis()
##            fig.canvas.draw()
##            #time.sleep(.2)
##


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host = socket.gethostname()
s.connect(('192.168.0.4',10009))

def animate(i):
    
    while state.listen:
        
        
        data = s.recv(2048).decode()
        
        #print(data)
        if not data:
            break

        try:
            x, y,humidity,temparature = data.split(",")
                                        
        except:
            continue
        
        #print(str(x) + '-- ' + str(y) + "--" + str(humidity))
        heatMap[int(x)][int(y)] = float(temparature)
        humidityHeatMap[int(x)][int(y)] = float(humidity)

        df = pd.DataFrame(heatMap)
        ax = sns.heatmap(df, cbar=False)
        ax.invert_yaxis()
        plt.title('** HeatMap ** ')
        plt.xlabel('X Coordinate (Deci-Meter per unit)')
        plt.ylabel('y Coordinate (Deci-Meter per unit)')
        
        fig.canvas.draw()

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        print ('ready to interpolate')
        s.close()
        newHeatMap = crop()
        
        sys.exit(0)
        
signal.signal(signal.SIGINT, signal_handler)

ani = animation.FuncAnimation(fig,animate,blit=True)
plt.show()


