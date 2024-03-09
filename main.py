from voting_data_reader import VotingDataReader
from stv_voting import STV_voting
from manipulator import Manipulator

if __name__ == "__main__":
    votingDataReader = VotingDataReader('voting_data.txt')
    #votingDataReaderTest = VotingDataReader('voting_data_test.txt')
    #stv_voting = STV_voting(votingDataReader.getLabels(), votingDataReader.getBallots())
    #winner = stv_voting.run_election()
    manipulator = Manipulator(votingDataReader.getLabels(), votingDataReader.getBallots())