from stv_voting import STV_voting
from ballots import Ballot
import copy

class Manipulator:

    def __init__(self, labels, ballots):
        self.originalBallots = ballots
        self.originalLabels = labels
        stv_voting = STV_voting(self.originalLabels, self.deepCopyBallots(self.originalBallots))
        self.originalVoteDistribution = stv_voting.count_first_preferences()
        self.originalVoteDistribution = dict(sorted(self.originalVoteDistribution.items(), key=lambda item: item[1]))
        self.originalWinner = stv_voting.run_election(False)[0] 
        print(self.originalLabels)
        print(self.originalWinner)
        print(len(self.originalBallots))
        self.findPossibleManipulators(self.originalWinner)
        print("Possible Manipulators")
        for alternative in self.possibleManipulators.keys():
            print(alternative, len(self.possibleManipulators[alternative]), sum(ballot.numVoters for ballot in self.possibleManipulators[alternative]))
        


        manipulatedWinners = []
        minManipulatorsCount = 10000000000000
        minManipulators = []

        for candidate in self.originalLabels.keys():
            if candidate == self.originalWinner:
                continue
            numManipulations = self.find_lowest_manipulators(candidate)
            manipulatedWinners.append((candidate, numManipulations))
            if minManipulatorsCount == numManipulations:
                minManipulatorsCount = numManipulations
                minManipulators.append((candidate, numManipulations))
            elif minManipulatorsCount > numManipulations:
                minManipulatorsCount = numManipulations
                minManipulators = [(candidate, numManipulations)]
            #manipulatedBallots = self.deepCopyBallots(self.originalBallots)
            #self.putAllLosersFirst(manipulatedBallots, self.possibleManipulators[candidate])
            #stv_voting = STV_voting(self.originalLabels, manipulatedBallots)
            #winners = stv_voting.run_election(True)
            #winner = winners[0]
            #print(winners)
            #if winner != self.originalWinner:
            #    manipulatedWinners.append([candidate, winner])
        print(manipulatedWinners)
        print(minManipulatorsCount, minManipulators)
        for minManipulator in minManipulators:
            self._run_specific_manipulated_election(self.originalBallots, minManipulator[1] + 1, self.possibleManipulators[minManipulator[0]], minManipulator[0], False)
        #manipulators = self.possibleManipulators['3']
        #preferredManipulators = [manipulator for manipulator in manipulators if (type(manipulator.candidateRankings[0]) == list and not '3' in manipulator.candidateRankings[0]) or (type(manipulator.candidateRankings[0]) != list and not '3' == manipulator.candidateRankings[0]) ]
        #possibleManipulators = [manipulator for manipulator in manipulators if not (type(manipulator.candidateRankings[0]) == list and not '3' in manipulator.candidateRankings[0]) or (type(manipulator.candidateRankings[0]) != list and not '3' == manipulator.candidateRankings[0])]

        #self._run_specific_manipulated_election(self.originalBallots, 121, preferredManipulators, possibleManipulators, False)
        

    def find_lowest_manipulators(self, alternateWinner):
        manipulators = self.possibleManipulators[alternateWinner]
        #preferredManipulators = [manipulator for manipulator in manipulators if (type(manipulator.candidateRankings[0]) == list and not alternateWinner in manipulator.candidateRankings[0]) or (type(manipulator.candidateRankings[0]) != list and not alternateWinner == manipulator.candidateRankings[0]) ]
        #possibleManipulators = [manipulator for manipulator in manipulators if not ((type(manipulator.candidateRankings[0]) == list and not alternateWinner in manipulator.candidateRankings[0]) or (type(manipulator.candidateRankings[0]) != list and not alternateWinner == manipulator.candidateRankings[0]))]
        totalNumManipulators = sum(ballot.numVoters for ballot in manipulators)
        
        #manipulationCount = totalNumManipulators + 1

        #for manCount in range(totalNumManipulators + 1):
        #    winners = self._run_specific_manipulated_election(self.originalBallots, manCount, preferredManipulators, possibleManipulators)
        #    if alternateWinner in winners:
        #        manipulationCount = manCount
        #        break
        manipulationCount = self._rec_find_lowest_manipulators(alternateWinner, 0, totalNumManipulators + 2, self.originalBallots, manipulators)
        if manipulationCount > totalNumManipulators:
            return 10000000
        return manipulationCount

    def _rec_find_lowest_manipulators(self, alternateWinner, start, end, ballots, possibleManipulators):
        if start + 1 >= end:
            return start
        mid = int((start + end) / 2)

        winners = self._run_specific_manipulated_election(ballots, mid, possibleManipulators, alternateWinner)
        
        if alternateWinner in winners:
            return self._rec_find_lowest_manipulators(alternateWinner, start, mid, ballots,  possibleManipulators)
        return self._rec_find_lowest_manipulators(alternateWinner, mid, end, ballots,  possibleManipulators)

    def _run_specific_manipulated_election(self, ballots, mid, possibleManipulators, alternateWinner, silent=True):
        manipulatedBallots = self.deepCopyBallots(ballots)

        manipulators = []
        currentManipulators = 0
        #self._add_manipulators(ballots, mid, preferredManipulators, manipulators, currentManipulators, manipulatedBallots)
        self._add_manipulators(ballots, mid, possibleManipulators, manipulators, currentManipulators, manipulatedBallots, alternateWinner)

        self.putAllLosersFirst(manipulatedBallots, manipulators)
        stv_voting = STV_voting(self.originalLabels, manipulatedBallots)
        return stv_voting.run_election(silent)


    def _add_manipulators(self, ballots, mid, possibleManipulators, manipulators, currentManipulators, manipulatedBallots, manWinner):
        for candidate in self.originalVoteDistribution.keys():
            if candidate == manWinner:
                continue
            for ballot in self.firstPreference[candidate]:
                if not ballot in possibleManipulators:
                    continue
                if currentManipulators + ballot.numVoters <= mid:
                    currentManipulators += ballot.numVoters
                    manipulators.append(ballot)
                else:
                    diff = (currentManipulators + ballot.numVoters) - mid
                    if diff == 0:
                        break
                    manipulatorBallot = Ballot(mid - currentManipulators, copy.deepcopy(ballot.candidateRankings))
                    manipulators.append(manipulatorBallot)
                    manipulatedBallots.append(manipulatorBallot)
                    manipulatedBallots.append(Ballot(diff, copy.deepcopy(ballot.candidateRankings)))
                    manipulatedBallots.remove(ballot)
                    break
        if currentManipulators < mid:
            for ballot in self.firstPreference[manWinner]:
                if not ballot in possibleManipulators:
                    continue
                if currentManipulators + ballot.numVoters <= mid:
                    currentManipulators += ballot.numVoters
                    manipulators.append(ballot)
                else:
                    diff = (currentManipulators + ballot.numVoters) - mid
                    if diff == 0:
                        break
                    manipulatorBallot = Ballot(mid - currentManipulators, copy.deepcopy(ballot.candidateRankings))
                    manipulators.append(manipulatorBallot)
                    manipulatedBallots.append(manipulatorBallot)
                    manipulatedBallots.append(Ballot(diff, copy.deepcopy(ballot.candidateRankings)))
                    manipulatedBallots.remove(ballot)
                    break

    def deepCopySingleBallot(self, ballot):
        return Ballot(ballot.numVoters, copy.deepcopy(ballot.candidateRankings))

    def deepCopyBallots(self, ballots):
        return [ self.deepCopySingleBallot(ballot) for ballot in ballots ]

    def findPossibleManipulators(self, winner):
        self.possibleManipulators = dict()
        self.firstPreference = dict()
        for candidate in self.originalLabels.keys():
            self.firstPreference[candidate] = []
            if candidate != winner:
                self.possibleManipulators[candidate] = []
        for ballot in self.originalBallots:
            self.firstPreference[ballot.candidateRankings[0]].append(ballot)
            for rank in ballot.candidateRankings:
                if (type(rank) == list and winner in rank) or (type(rank) != list and winner == rank):
                    break
                if type(rank) != list:
                    self.possibleManipulators[rank].append(ballot)
                else:
                    for candidate in rank:
                        self.possibleManipulators[candidate].append(ballot)
    
    def putCandidateFirst(self, ballots, candidate, changeBallots, winner):
        for changeBallot in changeBallots:
            newBallot = self.deepCopySingleBallot(changeBallot)
            newBallot.pushCandidateToFirstRank(candidate)
            newBallot.pushCandidateToLastRank(winner)
            self.manipulateBallot(ballots, changeBallot, newBallot)

    def putAllLosersFirst(self, ballots, changeBallots):
        losers = [candidate for candidate in self.originalLabels.keys() if candidate != self.originalWinner]
        candidateRanking = [losers]
        self.manipulateMultipleBallots(ballots, changeBallots, candidateRanking)

    def manipulateMultipleBallots(self, ballots, oldBallots, candidateRanking):
        totalVoters = 0
        for ballot in oldBallots:
            if ballot in ballots:
                totalVoters += ballot.numVoters
                ballots.remove(ballot)
        ballots.append(Ballot(totalVoters, candidateRanking))


    def manipulateBallot(self, ballots, oldBallot, newBallot):
        if oldBallot in ballots:
            ballots.remove(oldBallot)
            ballots.append(newBallot)
        else:
            print("Ballot can not be manipulated, it does not exist.")