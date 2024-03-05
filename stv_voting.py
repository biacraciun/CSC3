class STV_voting:
    def __init__(self, candidate_labels, ballots):
        self.candidate_labels = candidate_labels
        self.ballots = ballots
        self.quota = self.calculate_quota()
        self.active_candidates = set(candidate_labels.keys()) 

    def calculate_quota(self):
        total_votes = sum(ballot.numVoters for ballot in self.ballots)
        quota = 1 + (total_votes // (1 + 1))
        print(f"The quota is {quota}")
        return quota

    def count_first_preferences(self):
        first_pref_counts = {candidate: 0 for candidate in self.active_candidates}
        for ballot in self.ballots:
            for rank in ballot.candidateRankings:
                if rank in self.active_candidates:
                    first_pref_counts[rank] += ballot.numVoters
                    break  
        return first_pref_counts

    def redistribute_votes(self, eliminated_candidate):
        for ballot in self.ballots:
            if eliminated_candidate in ballot.candidateRankings:
                ballot.candidateRankings.remove(eliminated_candidate)

    def find_lowest_candidate(self, vote_counts):
        return min(vote_counts, key=vote_counts.get)

    def run_election(self):
        while True:
            vote_counts = self.count_first_preferences()
            print("Vote counts:", vote_counts)

            winners = [candidate for candidate, votes in vote_counts.items() if votes >= self.quota]
            if winners:
                winner = winners[0]
                print(f"The winner is {self.candidate_labels[winner]} with {vote_counts[winner]} votes.")
                return self.candidate_labels[winner]

            if len(self.active_candidates) > 1:
                lowest_candidate = self.find_lowest_candidate(vote_counts)
                self.active_candidates.remove(lowest_candidate)
                self.redistribute_votes(lowest_candidate)
                print(f"Number {lowest_candidate} is the lowest")
                print(f"Eliminating {self.candidate_labels[lowest_candidate]} and redistributing votes.")
            else:
                remaining_candidate = next(iter(self.active_candidates))
                print(f"The winner by default is {self.candidate_labels[remaining_candidate]}.")
                return self.candidate_labels[remaining_candidate]
