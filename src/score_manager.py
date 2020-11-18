##!/usr/bin/env python3

import time
import pickle
import os
import random

import constants as c

class ScoreManager:

    class ScoreEntry:
        def __init__(self, name, score, tags=None, score_time=None):
            self.name = name
            self.score = score
            self.tags = tags if tags is not None else []
            self.score_time = score_time if score_time is not None else time.time()

        def __str__(self):
            return f"{self.name} - {round(self.score, 2)} - " + \
                   f"{time_to_string(self.score_time)} - " + \
                   f"{self.tags if self.tags else 'no tags'}"

        def __repr__(self):
            return self.__str__()

        def copy(self):
            return ScoreManager.ScoreEntry(self.name,
                self.score,
                tags=self.tags,
                score_time = self.score_time)

        def __add__(self, other):
            copy = self.copy()
            copy.score += other.score
            copy.tags += other.tags
            return copy

    def __init__(self, filename=None):
        self.scores = []
        self.path = os.path.join(c.SCORE_SAVE_PATH, filename)
        self.has_unsaved_changes = False

    def __str__(self):
        return "\n".join([str(score) for score in self.scores])

    def add_score(self, name, score, tags=None, score_time=None):
        new_score = self.ScoreEntry(name, score, tags=tags, score_time=score_time)
        self.scores.append(new_score)
        self.scores.sort(reverse=True, key=lambda x:x.score_time)
        self.has_unsaved_changes = True

    def get_last_hours(self, num_hours):
        """ Return a list of only the scores created in the last specified
            number of hours.
        """
        now = time.time()
        cutoff = now - num_hours*3600
        return [item for item in self.scores if item.score_time > cutoff]

    def get_total_by_player(self, num_hours=None):
        source = self.scores if num_hours is None else self.get_last_hours(num_hours)
        score_dict = {}
        for score_entry in source:
            name = score_entry.name
            if name not in score_dict:
                score_dict[name] = score_entry.copy()
            else:
                score_dict[name] += score_entry
        return score_dict

    def save_if_changes(self):
        if self.has_unsaved_changes:
            self.save_to_file()

    def save_to_file(self):
        with open(self.path, "wb") as pickle_file:
            pickle.dump(self, pickle_file)

    @staticmethod
    def from_file(filename):
        path = os.path.join(c.SCORE_SAVE_PATH, filename)
        if not os.path.isfile(path):
            return ScoreManager(filename=filename)
        else:
            with open(path, "rb") as pfile:
                return pickle.load(pfile)

def ago_format(number, unit):
    number = int(number)
    s = "s" if number != 1 else ""
    return f"{number} {unit}{s} ago"

def time_to_string(t):
    now = time.time()
    ago = now - t
    if ago < 60:
        return ago_format(ago, "second")
    elif ago < 60*60:
        return ago_format(ago/60, "minute")
    elif ago < 60*60*24*2:
        return ago_format(ago/3600, "hour")
    else:
        return ago_format(ago/3600*24, "day")

if __name__ == '__main__':
    scoreboard = ScoreManager.from_file("test_scores.pkl")
    # print(f"\n{'-'*10} Last hour {'-'*10}")
    # for score in scoreboard.get_last_hours(1):
    #     print(score)
    print(f"\n{'-'*10} Totals {'-'*10}")
    totals = scoreboard.get_total_by_player(1)
    totals_list = [(key, totals[key]) for key in totals]
    totals_list.sort(key=lambda x:x[1].score, reverse=True)
    for item in totals_list:
        print(f"{item[1]}")
    scoreboard.save_to_file()
