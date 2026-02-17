from socket import *
import pickle

def ClientMain():
    serverIP = 'localhost'
    serverPort = 15555
    while True:
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverIP,serverPort))

        print("1. Start a game")
        print("2. Check Team Rank")
        print("3. Check Game Schedule")
        print("4. Exit")
        try:
            sentence = int(input("Please Pick by Entering a Number: "))
        except:
            print("Please Enter one of the following Numbers")

        if sentence > 4 or sentence < 1:
            print("Please Enter one of the following Numbers")
            continue
        elif sentence == 4:
            break

        betterSentence = str(sentence)

        clientSocket.send(betterSentence.encode())
        
        choiceMessage = clientSocket.recv(1024).decode("ascii")

        print('\n' + choiceMessage + '\n')

        choice2Message = clientSocket.recv(1024).decode("ascii")

        if choice2Message == "1":
            gameRanksData = b""
            while True:
                chunk = clientSocket.recv(4096)
                if not chunk:
                    break
                gameRanksData += chunk
                if len(chunk) < 4096:
                    break

            try:
                gamesRanks = pickle.loads(gameRanksData)
                print("\n Current Ranks \n")
                for line in gamesRanks:
                    print(line)
            except Exception as e:
                print("Error loading game ranks info:", e)

            gameMatchData = b""
            while True:
                chunk = clientSocket.recv(4096)
                if not chunk:
                    break
                gameMatchData += chunk
                if len(chunk) < 4096:
                    break

            try:
                gameMatch = pickle.loads(gameMatchData)
                print("\n Current Matches \n")
                for line in gameMatch:
                    print(line)
            except Exception as e:
                print("Error loading game match info:", e)
            
            print("\n Next Match: \n")

            nextMatch = clientSocket.recv(1024).decode("ascii")
            matchSplit = nextMatch[:-1].split(" vs ")
            #print(matchSplit)
            if matchSplit[1] == 'undeside':
                print('All matches have been played')
                doneFor = 'LInTheChat'
                clientSocket.send(doneFor.encode())
                continue
            else:
                print(nextMatch)
            # Decide on match winner
            winner = input("Please enter the name of the winner: ")

            #print(matchSplit)
            if winner.lower() == matchSplit[0].lower():
                clientSocket.send(winner.encode())
            elif winner.lower() == matchSplit[1].lower():
                clientSocket.send(winner.encode())
            else:
                print(f'{winner} is not the expected name')
            
            # Finish updating rank
            confirm = clientSocket.recv(1024).decode("ascii")
            print(confirm)
        
        if choice2Message == "2":
            lookup = input('Please enter a team name("ALL" for all ranks): ').lower()
            
            clientSocket.send(lookup.encode())

            # Decodes List from server 

            receivedTextFile = b""
            while True:
                chunk = clientSocket.recv(4096)
                if not chunk:
                    break
                receivedTextFile += chunk

            textFile = pickle.loads(receivedTextFile) # Schedule List

            for line in textFile:
                print(line)
            

        if choice2Message == "3":
           
            lookup = input('Please enter a team name: ').lower()
            
            clientSocket.send(lookup.encode())

            # Decodes List from server 

            receivedTextFile = b""
            while True:
                chunk = clientSocket.recv(4096)
                if not chunk:
                    break
                receivedTextFile += chunk

            textFile = pickle.loads(receivedTextFile) # Schedule List

            for line in textFile:
                print(line)

        clientSocket.close()

ClientMain()

