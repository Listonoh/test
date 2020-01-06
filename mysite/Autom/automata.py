import itertools
import json
import re
import os
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)


class configuration:
    def __init__(self, state: str, position: int, text_version: int, father=None):
        self.state, self.position, self.text_version = state, position, text_version
        self.father = father

    def __str__(self):
        return f"state: {self.state}, position: {self.position}, text_version: {self.text_version} "


class Automaton:

    def clear(self):
        print(
            f"Loading clear automaton, \n Init State is 'st0' and window size is set to 1 \n Accepting state is 'st0' ") if self.out % 2 == 0 else None
        self.definition = {"s0": ["st0", 0],
                           "alphabet": [],
                           "sAcc": ["st0"],
                           "size_of_window": 1,
                           "name": "Clear automaton",
                           "type": "None",
                           "doc_string": "This is clear automaton",
                           "tr_function": {}
                           }

    def __init__(self, file="", out_mode=3):
        self.out = out_mode  # output mode
        print("------------Loading--------------") if self.out % 2 == 0 else None
        if file == "":
            self.clear()
        else:
            with open(file, mode='r') as inp:  # load data from json file
                self.definition = json.load(inp)
        print(f"Automaton loaded") if self.out % 2 == 0 else None
        print("----------------------------------") if self.out % 2 == 0 else None

    def get_something(self, text):
        return text + "\nahoj ja ks e\n tak sno sd dsa \n dfad f"

    def is_in_alphabet(self, ch):
        if ch in self.definition["alphabet"]:
            return True
        return False

    def add_to_alphabet(self, *chars):  # going to be internal
        for ch in chars:
            if not ch in self.definition["alphabet"]:
                self.definition["alphabet"].append(ch)

    def add_accepting_state(self, *states):
        for st in states:
            if st not in self.definition["sAcc"]:
                self.definition["sAcc"].append(st)

    def is_accepting_state(self, state):
        if state in self.definition["sAcc"]:
            return True
        return False

    def get_words_of_len(self, length=5, count=20):
        return_arr = []
        for possibility in itertools.product(self.definition["alphabet"], length):
            if True:
                return_arr.append(possibility)
            if len(return_arr) >= count:
                return return_arr
        return return_arr

    def get_words_of_length(self, length=5, count=20):
        retarr = []
        for possibility in itertools.product(self.mess["alphabet"], length):
            if True:
                retarr.append(possibility)
            if len(retarr) >= count:
                return retarr
        return retarr

    def __make_instruction(self, instruction, new_state, stat):
        pos = stat.position
        end_of_pos = self.size_of_window + pos

        if instruction == "MVR":  # move right
            conf = configuration(new_state, pos + 1, stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "MVL":  # move right
            conf = configuration(new_state, pos - 1, stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "Restart":  # restart
            conf = configuration(new_state, 0, stat.text_version, stat)
            self.configs.append(conf)
        elif instruction == "Accept":  # restart
            conf = configuration(new_state, 0, stat.text_version, stat)
            self.configs.append(conf)
        # matching rewrites, for remove use "[]"
        elif re.match(r"^\[.*\]$", instruction):
            # new copy of current state
            new_list = self.texts[stat.text_version].copy()
            new_values = eval(instruction)  # making array from string
            new_list[pos: end_of_pos] = new_values  # rewriting

            self.texts.append(new_list)
            conf = configuration(new_state, stat.position, len(self.texts) - 1, stat)
            self.configs.append(conf)
        return

    def add_instr(self, from_state: str, value, to_state: str, instruction: str, value_as_list: bool = False) -> bool:
        """
        Does not rewrite if exist, see replace_instruction
        modify delta[from_state, value] -> [state, instruction]
        return False if instruction exists / True otherwise
        """
        if not value_as_list:
            value = str(list(value))
        if from_state not in self.definition["tr_function"]:
            self.definition["tr_function"][from_state] = {value: []}
        if value not in self.definition["tr_function"][from_state]:
            self.definition["tr_function"][from_state][value] = []
        if [to_state, instruction] in self.definition["tr_function"][from_state][value]:
            return False
        self.definition["tr_function"][from_state][value].append(
            [to_state, instruction])
        return True

    def replace_tr_function(self, from_state, value, to_state, instruction):
        self.definition["tr_function"][from_state][value] = [
            [to_state, instruction]]

    def __move(self, window, conf):
        possibilities = self.definition["tr_function"][conf.state]
        if "['*']" in possibilities:  # for all possibilities do this
            for possibility in possibilities["['*']"]:
                print(
                    f">instruction: * -> new_state: ***") if self.out % 2 == 0 else None
                self.__make_instruction(possibility[1], possibility[0], conf)
        for possibility in possibilities[window]:
            print(
                f">instruction: {window} -> new_state: {possibility[0]}, instruction: {possibility[1]}  ") if self.out % 2 == 0 else None
            self.__make_instruction(possibility[1], possibility[0], conf)
        print("----------------------------------",
              end="\n\n") if self.out % 2 == 0 else None

    def __get_window(self, text, position):
        end_of_pos = position + self.size_of_window
        return str(text[position:end_of_pos])

    def __concat_text(self, text):
        newtext = []
        ctr = 0
        working_string = ""
        for i in text:
            if i == "[":
                ctr += 1
            elif i == "]":
                ctr -= 1
            working_string += i
            if ctr == 0:
                newtext.append(working_string)
                working_string = ""
        if ctr != 0:
            raise Exception("[] are not in pairs")
        return newtext

    def pretty_printer(self, conf: configuration):
        if conf is None:
            return
        else:
            self.pretty_printer(conf.father)
            text = self.texts[conf.text_version]
            i = 0
            b, e = conf.position, conf.position + self.size_of_window
            print("[", end="") if self.out % 3 == 0 else None
            while i < len(text):
                if b <= i < e:
                    print(Fore.RED + str(text[i]),
                          end="") if self.out % 3 == 0 else None
                else:
                    print(str(text[i]), end="") if self.out % 3 == 0 else None
                i += 1
                if i < len(text):
                    print(", ", end="") if self.out % 3 == 0 else None
            print("]") if self.out % 3 == 0 else None

    def iterate_text(self, text):
        self.texts = [self.__concat_text(text)]
        self.paths_of_stats = [[0]]
        # implicitly set to 1
        self.size_of_window = self.definition["size_of_window"]
        # implicitly set to "st0" and 0
        starting_status = configuration(
            self.definition["s0"][0], self.definition["s0"][1], 0)
        self.configs = [starting_status]
        print(self.texts[0]) if self.out % 2 == 0 else None
        while True:
            try:
                conf = self.configs.pop()
                if conf.state == "Accept":
                    raise Exception("Accepting state")
                print(
                    f"     > taking status : {conf}") if self.out % 2 == 0 else None
                window = self.__get_window(
                    self.texts[conf.text_version], conf.position)
                print(
                    f" text: {self.texts[conf.text_version]}") if self.out % 2 == 0 else None
                print(f" window: {window}") if self.out % 2 == 0 else None
                self.__move(window, conf)
            except:
                if self.is_accepting_state(conf.state):
                    print(
                        f"remaining tuples = {self.stats}") if self.out % 2 == 0 else None
                    print(
                        f"number of copies of text = {len(self.texts)}") if self.out % 2 == 0 else None
                    self.pretty_printer(conf)
                    return True
                elif self.configs.__len__() == 0:
                    return False

    def print_tr_function(self):
        for state in self.definition["tr_function"]:
            print(f"states: {state}: <", end="")
            for value in self.definition["tr_function"][state]:
                print(f" \"{value}\" : [", end="")
                for instruct in self.definition["tr_function"][state][value]:
                    print(f"{instruct}", end="")
                print("]")
            print(">")

    def save_tr_function(self, to):
        with open(to, "w") as to_file:
            json.dump(self.definition, to_file)

    def is_deterministic(self):
        for state in self.definition["tr_function"]:
            for value in self.definition["tr_function"][state]:
                if len(self.definition["tr_function"][state][value]) > 1:
                    return False
        return True
