import random

class Team:
    def __init__(self, name : str, tier : int, rank : int):
        self.name = name
        self.tier = tier
        self.rank = rank
        self.__pts = 0
    
    def get_points(self):
        return self.__pts

    def add_points(self, n : int):
        self.__pts += n

class Match:
    def __init__(self, home : Team, away : Team):
        self.__home = home
        self.__away = away
        self.__score = (0,0)
        self.__poss = random.choice([i+8 for i in range(3 * (1 + abs(home.tier - away.tier)))])
        self.__succ = 58
        self.__kick = 78

    def __simulate_team(self, poss : int, succ1 : int, succ2 : int, kick : int):
        pts = tries = 0
        for _ in range(poss):
            num = random.randint(0, 100)
            if num <= succ1:
                tries += 1
                pts += 5
                if random.randint(0, 100) <= kick:
                    pts += 2
            elif num <= 100 - succ2 and random.randint(0, 100) <= kick:
                pts += 3
        return pts, tries
    
    def __calc_points(self, pts1 : int, pts2 : int, tries : int) -> int:
        p = 1 if tries >= 4 else 0
        if pts1 == pts2:
            return p + 2
        if pts1 > pts2:
            return p + 4
        if pts2 - pts1 <= 7:
            return p + 1
        return p

    def simulate(self, groupStageGame=True):
        poss1 = self.__poss - (self.__home.tier * random.choice([1,2]))
        poss2 = self.__poss - (self.__away.tier * random.choice([1,2]))

        succ1 = self.__succ - (self.__home.rank * 2)
        succ2 = self.__succ - (self.__away.rank * 2)

        kick1 = self.__kick - (self.__home.rank // 2)
        kick2 = self.__kick - (self.__away.rank // 2) 

        pts1, tries1 = self.__simulate_team(poss1, succ1, succ2, kick1)
        pts2, tries2 = self.__simulate_team(poss2, succ2, succ1, kick2)

        if groupStageGame:
            self.__home.add_points(n=self.__calc_points(pts1, pts2, tries1))
            self.__away.add_points(n=self.__calc_points(pts2, pts1, tries2))
        else:
            while pts1 == pts2:
                pts1, tries1 = self.__simulate_team(poss1, succ1, succ2, kick1)
                pts2, tries2 = self.__simulate_team(poss2, succ2, succ1, kick2)

        self.__score = (pts1, pts2)

    def print_match(self):
        print(self.__home.name + " " + str(self.__score[0]) + " " + self.__away.name + " " + str(self.__score[1]))

    def get_winner(self) -> Team:
        if self.__score[0] >= self.__score[1]:
            return self.__home
        return self.__away

class Tournament:
    def __init__(self, group_a, group_b, group_c, group_d):
        self.__group_a = group_a
        self.__group_b = group_b
        self.__group_c = group_c
        self.__group_d = group_d

    def run_tournament(self):
        self.__run_group_stage(groups=[self.__group_a, self.__group_b, self.__group_c, self.__group_d])
        self.__run_ko_stage(ko=[self.__group_c[0], self.__group_d[1], self.__group_b[0], self.__group_a[1], 
              self.__group_d[0], self.__group_c[1], self.__group_a[0], self.__group_b[1]])

    def __run_group_stage(self, groups : list[list[Team]]):
        for i, group in enumerate(groups):
            matches = self.__get_matches(group=group)
            print("Group " + str(i + 1) + " Matches:")
            for match in matches:
                match.simulate()
                match.print_match()
            group.sort(reverse=True, key=lambda t: t.get_points())
            print("\nGroup " + str(i + 1) + " Table:")
            for team in group:
                print(team.name + " " + str(team.get_points()))
            print("\n")


    def __run_ko_stage(self, ko : list[Team]):
        level = len(ko) / 2
        i = 1
        while len(ko) > 1:
            match = Match(ko.pop(0), ko.pop(0))
            match.simulate(groupStageGame=False)
            match.print_match()
            ko.append(match.get_winner())
            if i == level:
                level /= 2
                i = 1
                print("\n")
            else:
                i += 1

        print("WINNER: " + ko.pop().name)

    def __get_matches(self, group : list[Team]) -> list[Match]:
        matches = []
        for i in range(len(group) - 1):
            for j in range(i + 1, len(group)):
                matches.append(Match(group[i], group[j]))
        return matches

def main():
    rwc2023 = Tournament([Team("France", 1, 3), Team("New Zealand", 1, 4), Team("Italy", 1, 12), Team("Uruguay", 2, 17), Team("Namibia", 3, 21)],
                        [Team("Ireland", 1, 1), Team("South Africa", 1, 2), Team("Scotland", 1, 5), Team("Tonga", 2, 15), Team("Romania", 3, 19)],
                        [Team("Wales", 1, 7), Team("Fiji", 2, 8), Team("Australia", 1, 9), Team("Georgia", 2, 13), Team("Portugal", 3, 16)],
                        [Team("England", 1, 6), Team("Samoa", 2, 11), Team("Japan", 1, 14), Team("Chile", 3, 22), Team("Argentina", 1, 10)])
    rwc2023.run_tournament()

if __name__ == "__main__":
    main()
