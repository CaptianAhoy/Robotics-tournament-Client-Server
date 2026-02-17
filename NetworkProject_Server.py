from socket import *
from _thread import *
import pickle
import time

def ScoreThread(connectSocket):
    connectSocket.close()

def serverMain():
    serverPort = 15555
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print('Server is ready')
    
    temp = 0

    while True:

        connectSocket,addr = serverSocket.accept()
        # start_new_thread(ScoreThread, (connectSocket,))

        # print("From", addr)
        try:
            sentence = int(connectSocket.recv(1024))
        except:
            print('Client Disconected')
            break

        print("What we received: ", sentence)

        if sentence == 1:
            connectSocket.send(b"Starting Game")
            time.sleep(1)

            # Prints the current Rankings ====================================

            try:
                f = open('rank.txt', 'r')
            except:
                print('File cannot be found')

            connectSocket.send(b'1')

            rankFile = []
            rankFileRaw = []
            
            for line in f:
                x = line.split(',')
                if len(x) > 2:
                    rankFileRaw.append(line)
                    rankFile.append(f'{x[0]}. {x[1]}   Points: {x[2]}')
                else:
                    rankFile.append(f'{x[0]}')

            sendingRankFile = pickle.dumps(rankFile)
            connectSocket.send(sendingRankFile)
            f.close()

            # ================================================================

            time.sleep(1)
            
            # Prints the current Schedule ====================================

            try:
                f = open('schedule.txt', 'r')
            except:
                print('File not found')

            scheduleFile = []
            scheduleFileRaw = []

            for line in f:
                scheduleFileRaw.append(line)
                x = line.split(',')
                #print(f'x = {x}\nlength = {len(x)}')
                if len(x) > 1 and x[1] != '':
                    scheduleFile.append(f'{x[0]} vs {x[1]}')
                else:
                    scheduleFile.append(f'{x[0]} vs undesided')

            sendingScheduleFile = pickle.dumps(scheduleFile)
            connectSocket.send(sendingScheduleFile)
            
            time.sleep(1)
            
            connectSocket.send(scheduleFile[temp].encode())
            f.close()
            # ===============================================================

            time.sleep(1)

            # Change rank ===================================================
            
            setupOne = {}

            for i in rankFileRaw:
                x = i.split(',')
                setupOne[x[1]] = int(x[2])

            rankup = (connectSocket.recv(1024).decode("ascii")).title()
            print(rankup)
            if rankup == 'Linthechat':
                continue
                
            setupOne[rankup] = setupOne[rankup] + 1

            numberOrder = []
            
            for i in setupOne:
                numberOrder.append(setupOne[i])
            
            fixedNumberOrder = sorted(numberOrder, reverse=True)
            
            fi = open('rank.txt', 'w')

            theRankNumber = 1

            #print(setupOne)  

            used = []

            for i in fixedNumberOrder:
                #print(i)
                for s in setupOne:
                    #print(s)
                    if setupOne[s] == i and s not in used:
                        fi.write(f'{theRankNumber},{s},{i}\n')
                        used.append(s)
                        theRankNumber += 1
                       
            connectSocket.send(b"Ranking Updated")
            fi.close()
            # ==============================================================

            time.sleep(1)

            # Set next Schedule ============================================

            #print(rankup) # Moving on to the next round
            #print(scheduleFileRaw) # raw text file

            fi = open('schedule.txt', 'w')
            
            newLineOrNo = 1

            for i in scheduleFileRaw:
                x = i.split(',')
                if len(x) > 1 and x[1] != '':
                    fi.write(i)
                else:
                    fi.write(i + f'{rankup}\n')
                    newLineOrNo = 0
            if newLineOrNo == 1:
                fi.write(f'{rankup},')
            fi.close()
            temp += 1

            
                
        # ==============================================================

        if sentence == 2:
            connectSocket.send(b"Checking Team Rank")

            time.sleep(1)

            try:
                f = open('rank.txt', 'r')
            except:
                print('File cannot be found')

            connectSocket.send(b"2")
            
            textFile = []

            team = connectSocket.recv(1024).decode("ascii")

            print(f'Team from client = {team}')

            if (team == 'all'):
                for line in f:
                    x = line.split(',')
                    if len(x) > 2:
                        textFile.append(f'{x[0]}. {x[1]} | Points:{x[2]}')
                    else:
                        textFile.append(f'{x[0]}')
                
            else: 
                for line in f:
                    if team in line.lower():
                        x = line.split(',')
                        textFile.append(f'{x[0]}. {x[1]} | Points: {x[2]}')

            if len(textFile) == 0:
                textFile.append(f'{team} not found \n')

            sendingTextFile = pickle.dumps(textFile) # converts list to bytes that can be sent
            connectSocket.send(sendingTextFile)
            

        if sentence == 3:
            connectSocket.send(b"Checking Game Schedule")
            time.sleep(1)

            try:
                f = open('schedule.txt', 'r')
            except:
                print('File cannot be found')

            connectSocket.send(b"3")
            
            textFile = []

            team = connectSocket.recv(1024).decode("ascii")

            print(f'Team from client = {team}')

            for line in f:
                if team in line.lower():
                    x = line.split(',')
                    textFile.append(f'{x[0]} vs {x[1]}')

            if len(textFile) == 0:
                textFile.append(f'{team} not found \n')

            sendingTextFile = pickle.dumps(textFile) # converts list to bytes that can be sent
            connectSocket.send(sendingTextFile)

        connectSocket.close()

serverMain()

