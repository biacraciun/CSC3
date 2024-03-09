from ballots import Ballot
import re

class VotingDataReader():
    def __init__(self, file):
        self.candidateLabels = dict()
        self.ballots = []
        extractLabels = 0

        with open(file, 'r') as f:
            data = f.read()
            for line in data.split('\n'):
                if "ALTERNATIVE NAME" in line:
                    relevant_text = line.split("ALTERNATIVE NAME")[1].strip()
                    candidate_number, candidate_name = relevant_text.split(":")
                    self.candidateLabels[candidate_number] = candidate_name
                    extractLabels = 1
                elif extractLabels == 1:
                    if line.strip() == "":
                        continue
                    numVoters, candidateRankings = line.split(":")
                    #candidateRankings = candidateRankings.split(",")
                    candidateRankings = re.findall(r'{.+?}|[^,{}]+', candidateRankings)
                    candidateRankings = [ranking.strip() if ranking.strip()[0] != '{' else ranking[1:-1].split(',') for ranking in candidateRankings if ranking.strip() != ""]
                    self.ballots.append(Ballot(int(numVoters), list(candidateRankings)))
        
    def getBallots(self):
        return self.ballots
    
    def getLabels(self):
        return self.candidateLabels


