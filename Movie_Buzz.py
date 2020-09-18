from time import *
import random
import pandas as pd

clear = lambda : print("\n"*40)
p = lambda x : sleep(x)

#input
def gameMode():
    mode = input("Enter the type of game mode: \n"
                 "PVP - 2 Players against each other \n"
                 "PVE - Play against the computer\n")
    mode = mode.lower()
    p(0.5)
    if mode != 'pvp' and mode != 'pve':
        print("Invalid Input! Please try again")
        p(0.5)
        return gameMode()
    return mode

def numOfRounds():
    rounds = input("Enter the number of Rounds to Play \n")
    p(0.5)
    if rounds.isnumeric():
        pass
    else:
        print("Invalid Input! Please try again")
        p(0.5)
        return numOfRounds()
    return int(rounds)

def getDiff():
    diff = input("Enter the difficulty level of the game: \n"
                 "Easy - 10 Guesses \n"
                 "Medium - 8 Guesses \n"
                 "Hard - 6 Guesses \n"
                 "Expert - 4 Guesses \n")
    diff = diff.lower()
    p(0.5)
    if diff not in ['easy','medium','hard','expert']:
        print("Invalid Input! Please try again")
        p(0.5)
        return getDiff()
    return diff

def getGuess(diff):
    global guess
    if diff == 'easy':
        guess = 10
    elif diff == 'medium':
        guess = 8
    elif diff == 'hard':
        guess = 6
    elif diff == 'expert':
        guess = 4
    return guess

def roundfn(guess,rounds, diff, mode, p1, p2):
    global movie
    p(0.5)
    if mode == 'pvp':
        movie_inp = input("Enter the name of the Movie {}: \n".format(p1))
        movie = movie_inp.upper()
    elif mode == 'pve':
        movie_inp = movie_list[random.randint(0, len(movie_list))]
        movie = movie_inp.upper()
    mlist = [i for i in movie]
    scorelist = [j for j in movie if j.isalnum()]
    queslist = []
    for i in mlist:
        if i in 'AEIOU:,.+-&$#@!*\/\'':
            queslist.append(i)
        elif i == ' ':
            queslist.append(' ')
        else:
            queslist.append('_')
    clear()
    p(0.25)
    print(" ".join(queslist))
    gcount = 1
    glist = []
    while guess:
        p(0.25)
        x = input("Enter guess {} ({} guesses left): \n".format(gcount, guess)).upper()
        p(0.25)

        if x in 'AEIOU:,.+-&$#@!*\/\'':
            print("Try Again. Only guess a consonant or a number.")
            print("\n")
            print(" ".join(queslist))
            continue
        elif x in glist:
            print("Already Guessed. Try Again!")
            print("\n")
            print(" ".join(queslist))
            continue
        glist.append(x)

        if x == movie:
            p(0.25)
            print("{} Wins!!! \n".format(p2))
            print("\n")
            print(" ".join(queslist))
            break

        ind = []
        if x in mlist:
            for i in range(len(mlist)):
                if mlist[i] == x:
                    ind.append(i)

        if ind == []:
            print("Wrong guess!")
            guess = guess - 1
        else:
            for i in ind:
                queslist.pop(i)
                queslist.insert(i, x)

        if queslist == mlist:
            p(0.25)
            print("{} Wins!!! \n".format(p2))
            print("\n")
            print(" ".join(queslist))
            break

        if guess > 0:
            print("\n")
            print(" ".join(queslist))
            p(0.25)
            print("Already Guessed: {}".format(", ".join(glist)))

        gcount = gcount + 1
    else:
        print(" ")
        print("Correct Answer: {} \n".format(movie))

    scr = len(scorelist)
    for x in queslist:
        if x == '_':
            scr = scr - 1
    score = scr/len(scorelist)
    return score

def gamepvp(guess, rounds, diff, mode):
    global movie,mlist
    p1 = input("Enter player 1 name(Press Enter for default) \n")
    p2 = input("Enter player 2 name(Press Enter for default) \n")
    if p1 == '':
        p1 = 'Player 1'
    if p2 == '':
        p2 = 'Player 2'

    p1_scores = []
    p2_scores = []
    rcount = 1

    while(rounds):
        p2s = roundfn(guess, rounds, diff, mode, p1, p2)
        p1s = roundfn(guess, rounds, diff, mode, p2, p1)
        p1_scores.append(p1s)
        p2_scores.append(p2s)

        print("Round {} Score:".format(rcount))
        print("{} Score: {}".format(p1,p1s))
        print("{} Score: {}".format(p2,p2s))

        input("Press Enter to continue")

        rcount = rcount + 1
        rounds = rounds - 1
    p1final = sum(p1_scores)/len(p1_scores)
    p2final = sum(p2_scores)/len(p2_scores)

    print("{} Final Score: {}".format(p1,p1final))
    print("{} Final Score: {}".format(p2,p2final))

    if p1final > p2final:
        print("{} WINS THE GAME!!!!".format(p1))
    elif p2final > p1final:
        print("{} WINS THE GAME!!!!".format(p2))
    else:
        print("Its a Draw")


def gamepve(guess, rounds, diff, mode):
    p2 = input("Enter players name(Press Enter for default) \n")
    if p2 == '':
        p2 = 'Player'

    p2_scores = []
    rcount = 1

    while (rounds):
        p2s = roundfn(guess, rounds, diff, mode, None, p2)
        p2_scores.append(p2s)

        print("Round {} Score:".format(rcount))
        print("{}'s Score: {}".format(p2, p2s))

        rcount = rcount + 1
        rounds = rounds - 1
    p2final = sum(p2_scores) / len(p2_scores)

    print("{}'s Final Score: {}".format(p2,p2final))

if __name__ == '__main__':
    print("---------------- Movie Buzz ----------------")
    print(" ")
    mode = gameMode()
    print(" ")
    diff = getDiff()
    print(" ")
    rounds = numOfRounds()
    print(" ")
    guess = getGuess(diff)
    print(" ")
    if mode == 'pvp':
        gamepvp(guess, rounds, diff, mode)
    elif mode == 'pve':
        df = pd.read_csv('movie.csv', encoding='unicode_escape')
        movie_list = list(df['title'])
        gamepve(guess, rounds, diff, mode)