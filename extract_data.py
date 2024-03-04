class VotingDataReader():
    def __init__(self, candidateLabels, ballots):
        self.candidateLabels = candidateLabels
        self.ballots = ballots
        
    def getBallots(self):
        return self.ballots
    
    def getLabels(self):
        return self.candidateLabels


