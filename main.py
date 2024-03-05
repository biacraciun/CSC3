from voting_data_reader import VotingDataReader
from ballots import Ballot
from stv_voting import STV_voting


if __name__ == "__main__":
    file = 'voting_data.txt'
    candidateLabels = dict()
    ballots = []
    extractLabels = 0

    with open(file, 'r') as f:
        data = f.read()
        for line in data.split('\n'):
            if "ALTERNATIVE NAME" in line:
                relevant_text = line.split("ALTERNATIVE NAME")[1].strip()
                candidate_number, candidate_name = relevant_text.split(":")
                candidateLabels[candidate_number] = candidate_name
                extractLabels = 1
            elif extractLabels == 1:
                if line.strip() == "":
                    continue
                numVoters, candidateRankings = line.split(":")
                candidateRankings = candidateRankings.split(",")
                candidateRankings = [ranking.strip() for ranking in candidateRankings]
                ballots.append(Ballot(int(numVoters), list(candidateRankings)))

    votingDataReader = VotingDataReader(candidateLabels, ballots)
    stv_voting = STV_voting(candidateLabels, ballots)
    winner = stv_voting.run_election()