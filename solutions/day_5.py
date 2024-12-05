import numpy as np
import csv
import re



def part_1():
    with open("data/day_5_input.txt", 'r') as file:
        reader = csv.reader(file)
        rules = []
        updates = []
        rules_done = False
        for row in reader:
            if len(row) == 0:
                rules_done = True
                continue
            if not rules_done:
                rules.extend(row)
            else:
                updates.append(row)

        rule_dict = {}
        for rule in rules:
            r = rule.split("|")
            k = r[0]
            v = r[1]
            if k in rule_dict:
                rule_dict[k].append(v)
            else:
                rule_dict[k] = [v]

        good_updates = []

        for update in updates:
            good_update = True
            rupdate = list(reversed(update))
            for idx, p in enumerate(rupdate[:-1]):
                be_before = rule_dict[p]
                next_pages = rupdate[idx+1:]
                for r in be_before:
                    if r in next_pages:
                        good_update = False
            if good_update:
                good_updates.append(update)
        
        middle_sum = 0

        for gu in good_updates:
            middle_idx = int((len(gu) - 1) / 2)
            middle_sum += int(gu[middle_idx])

        print(middle_sum)
           
        

def part_2():
    with open("data/day_5_input.txt", 'r') as file:
        reader = csv.reader(file)
        rules = []
        updates = []
        rules_done = False
        for row in reader:
            if len(row) == 0:
                rules_done = True
                continue
            if not rules_done:
                rules.extend(row)
            else:
                updates.append(row)

        rule_dict = {}
        for rule in rules:
            r = rule.split("|")
            k = r[0]
            v = r[1]
            if k in rule_dict:
                rule_dict[k].append(v)
            else:
                rule_dict[k] = [v]

        bad_updates = []

        for update in updates:
            good_update = True
            rupdate = list(reversed(update))
            for idx, p in enumerate(rupdate[:-1]):
                be_before = rule_dict[p]
                next_pages = rupdate[idx+1:]
                for r in be_before:
                    if r in next_pages:
                        good_update = False
            if not good_update:
                bad_updates.append(update)
        
        good_now_updates = []

        for bu in bad_updates:
            rbu = list(reversed(bu))
            for i in range(len(rbu) - 1):
                for j in range(i+1, len(rbu)):
                    be_before = rule_dict[rbu[i]]
                    if rbu[j] in be_before:
                        temp = rbu[j]
                        rbu[j] = rbu[i]
                        rbu[i] = temp
            good_now_updates.append(list(reversed(rbu)))

        middle_sum = 0

        for u in good_now_updates:
            middle_idx = int((len(u) - 1) / 2)
            middle_sum += int(u[middle_idx])

        print(middle_sum)

part_1()
part_2()