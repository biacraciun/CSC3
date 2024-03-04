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