'''
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Farkle: a dice game.

    Farkle is an uncommon folk betting game where players rotate throwing rounds of six (6) six-sided dice (d6s), with each participant seeking to
    be the first to reach a given score threshhold, by default set to 2000.
    
    Each player's turn is divided into a number of throws. Throws are scored as follows: ones (1) are worth 100 points, and fives (5) are worth 50
    points. Also, in the event of a triple, where three dice rolls present the same number - which may be any of the possible values 1-6 - the value
    is 100x the face value of the number on the die, except if the number is a 5 or a 1, in which case the value of the triple becomes 500 and 1000,
    respectively. Groups of 4 dice with the same face-value are worth twice the equivalent triple, eg. four (4) 2s are valued at 2(100)(2) = 400.
    Values for groups of five and six dice are likewise double that of the next smallest group.

    A throw is called 'successful' if it can score any points.
    
    A turn will end either by scoring points and passing, or by rolling an unsuccessful throw.    
        After rolling a successful throw and scoring points, a player may pass and add the points from the round tally to the player's total score.
        If a throw cannot score any points the player forfeits all points earned that round and the next player's turn begins.
    In either case, play proceeds with the next player, who intially rolls all 6 dice regardless of the last player's results.

    To clarify, an unsuccessful intitial throw might look like 2 2 4 3 4 3, since there are no 1s or 5s and no groups of three or more.

    At the end of each successful throw, a player must choose which dice to score and whether or not to reroll. Unscored dice may be re-rolled in a
    subsequent throw, but beware of overextending after a lucky roll or two and losing all the round's points should the next one be unsuccessful.
    
    For example, an initial throw might be 1 2 3 3 2 6 - successful because the 1 is scoreable. The player may then choose to either take 100 points
    for the round and pass, or add 100 to their running round tally and reroll the remaining five dice. Suppose they do the latter, coming up with
    5 5 3 4 2. The player must now choose between four options, although one is ill-advised:
        a) taking both of the 5s, adding 100 to their running tally (now 200) and re-rolling the remaining three dice.
        b) taking both 5s and passing the turn to the next player, scoring a total of 200 points.
        c) taking only one 5, adding 50 to their running tally and re-rolling the remaining 4 dice.
        d) (strategically deficient) taking one 5 and passing, scoring a total of 150 points for the round.

    Finally, should all six of the dice be scored during the course of a player's turn, that player may then re-roll all six dice as though they
    were unscored. This incentivizes taking risks when only a few unscored dice remain.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''
import random
import re

class Die:
    def __init__(self, name):
        self.name = name
        self.faceValue = None
        self.scored = False
    
    def roll_die(self):
        self.faceValue = random.randint(1,6)

class Throw:
    def __init__(self, dice):
        self.dice = dice
        for d in self.dice:
            d.scored = False
        self.score = 0
        self.goAgain = True
        self.remaining_dice = None
        self.roll()
        self.scoreThrow()

    def roll(self):
        for die in self.dice:
            die.roll_die()
        self.diceVals = [str(x.faceValue) for x in self.dice]
   
    def scoreThrow(self):
        vals = ''.join(self.diceVals)
        groups = re.search(r'^.*(\d).*\1.*\1', vals)

        def isSuccessful():
            if groups:
                return True      
            elif '1' in vals or '5' in vals:
                return True
            else:
                return False
        
        notGood = isSuccessful()

        if notGood == False:
            # delete tally and skip to next player
            print('Rolling dice....\n')
            for d in self.dice:
                print(f"Die {d.name}: {d.faceValue}\n")
            print("\nYou busted! Better luck next time. ")
            self.score = 0
        else:
            for d in self.dice:
                print(f"Die {d.name}: {d.faceValue}\n")
            if groups:
                group_scored = input("Do you want to score any groups? Y/N ")
                if group_scored.lower() == 'y':
                    grouped_dice = []
                    group_vals = []
                    
                    dice_in_group = input("Please select the names of the dice you wish to score as a group: \n")
                    grouped_dice = [d for name in dice_in_group.split() for d in self.dice if name == d.name]
                    group_vals = [d.faceValue for d in grouped_dice]
                    
                    for d in grouped_dice:
                        d.scored = True
                    
                    self.score = recursiveGroupScorer(group_vals)
                    print(self.score)
                    ungrouped_dice = [d for d in self.dice if d.scored == False]
                    # if all dice are scored, the player gets an extra round
                    if ungrouped_dice:
                        for d in ungrouped_dice: print(f"Die {d.name}: {d.faceValue}\n")
                        newquestion = input("Select the remaining dice to score. If none, write 'N'. \n").lower()
                        if newquestion == 'n':
                            # query to pass or roll again
                            query = input("Press 'S' to score this round's points. Press any other key to keep trying your luck. \n").lower()
                            if query == 's':
                                self.goAgain = False
                            else:
                                self.remaining_dice = ungrouped_dice

                        else:
                            for d in ungrouped_dice:
                                if d.name in newquestion.split():
                                    if d.faceValue == 1:
                                        self.score += 100
                                        d.scored = True
                                    elif d.faceValue == 5:
                                        self.score += 50
                                        d.scored = True
                            # query to pass or roll again
                            query = input("Press 'S' to score this round's points. Press any other key to keep trying your luck. \n").lower()
                            if query == 's':
                                self.goAgain = False
                            else:
                                self.remaining_dice = [d for d in self.dice if d.scored == False]
            else:
                question = input("Select the names of the dice you wish to score. \n")
                for f in self.dice:
                    if f.name in question.split():
                        if f.faceValue == 1:
                            self.score += 100
                            f.scored = True
                        elif f.faceValue == 5:
                            self.score += 50
                            f.scored = True
                # query to pass or roll again
                query = input("Press 'S' to score this round's points. Press any other key to keep trying your luck. \n").lower()
                if query == 's':
                    self.goAgain = False
                else:
                    self.remaining_dice = [d for d in self.dice if d.scored == False]                




class Scoreboard:
    def __init__(self, players):
        die_a = Die('a')
        die_b = Die('b')
        die_c = Die('c')
        die_d = Die('d')
        die_e = Die('e')
        die_f = Die('f')
        self.dice = [die_a, die_b, die_c, die_d, die_e, die_f]
        if len(players) > 10: raise Exception("Too many players!")
        self.players = [[name, 0] for name in players]
        # print(f"Players and their scores: {self.players}")
        self.threshhold = 2000
        self.topScore = 0
        self.topScorer = None
        self.turnOrder = random.sample(self.players,len(players))
        print(f"The order of play will be: {[a[0] for a in self.players]}")
        while self.topScore < self.threshhold:
            for i in self.turnOrder:
                running = True
                while running:
                    print(f"It's your turn {i[0]} go ahead!")
                    running = self.turn(i)
                print(f"Here's where the score curently stands: \n")
                for player in self.players:
                    print(f"{player[0]}:   {player[1]} points\n")
        else:
            print(f"Congratulations {self.topScorer}! You are victorious, having scored {self.topScore} total points!")



    def turn(self, player):
        roundTally = 0
        x = Throw(self.dice)
        
        while x.goAgain == True:
            if x.score == 0: return False
            else: roundTally += x.score
            
            if not x.remaining_dice:
                for d in self.dice:
                    d.scored = False
                x.remaining_dice = self.dice
            dice_to_throw = x.remaining_dice
            for d in dice_to_throw: d.scored = False
            x = Throw(dice_to_throw)
        else:
            roundTally += x.score
            player[1] += roundTally
            if player[1] > self.topScore:
                self.topScore = player[1]
                self.topScorer = player
                print(f'New highest score! {player[0]} has taken the lead with {player[1]} points!')
            print(f'{player[0]}, you scored {roundTally} points this round.')
            return False





                    


def recursiveGroupScorer(dice_val_list):
    if len(dice_val_list) == 3:
        if dice_val_list[0] == 1:
            return 1000
        else:
            return dice_val_list[0] * 100
    else: return 2 * recursiveGroupScorer(dice_val_list[:-1])


if __name__ == "__main__":
    peoplePlaying = input("Please enter the players' names: \n\n\n").split()
    game = Scoreboard(peoplePlaying)