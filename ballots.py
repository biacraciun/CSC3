class Ballot():
    def __init__(self, numVoters, candidateRankings):
        self.numVoters = numVoters
        self.candidateRankings = candidateRankings

    def vote(self):
        pass

    def getNumVoters(self):
        return self.numVoters
    
    def getCandidateRankings(self):
        return self.candidateRankings

    def getPos(self, candidate):
        if candidate in self.candidateRankings:
            return self.candidateRankings.index(candidate)
        else:
            idx = 0 
            for currentCandidate in self.candidateRankings:
                if type(currentCandidate) == list and candidate in currentCandidate:
                    return [idx, currentCandidate.index(candidate)]
                idx += 1
        return None

    def _setCandidate(self, pos, candidate):
        if type(pos) == list:
            self.candidateRankings[pos[0]][pos[1]] = candidate
        else:
            self.candidateRankings[pos] = candidate

    def switchCandidates(self, candidate1, candidate2):
        pos1 = self.getPos(candidate1)
        pos2 = self.getPos(candidate2)
        if pos1 is None or pos2 is None:
            return
        self._setCandidate(pos1, candidate2)
        self._setCandidate(pos2, candidate1)

    def pushCandidateToLastRank(self, candidate):
        lastCandidate = self.candidateRankings[max(len(self.candidateRankings) - 1, 0)]
        if type(lastCandidate) == list:
            lastCandidate = lastCandidate[0]
        self.switchCandidates(lastCandidate, candidate)

    def pushCandidateToFirstRank(self, candidate):
        firstCandidate = self.candidateRankings[0]
        if type(firstCandidate) == list:
            firstCandidate = firstCandidate[0]
        self.switchCandidates(firstCandidate, candidate)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.candidateRankings == other.candidateRankings and self.numVoters == self.numVoters
        return False