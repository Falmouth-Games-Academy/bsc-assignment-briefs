#!/usr/bin/env python3

import sys
import os
import sqlite3
import glob


core_levels = [
    ("research-example-1", "Of Pancakes and Spaceships"),
    ("research-tutorial-1", "Slightly Different"),
    ("research-tutorial-1point5", "Crossover"),
    ("research-example-2", "An Introduction to Bonding"),
    ("research-tutorial-2", "A Brief History of SpaceChem"),
    ("research-tutorial-3", "Removing Bonds"),

    ("research-tutorial-4", "Double Bonds"),
    ("research-tutorial-5", "Best Left Unanswered"),
    ("research-tutorial-6", "Multiple Outputs"),
    ("production-tutorial-1", "An Introduction to Pipelines"),
    ("production-tutorial-2", "There's Something in the Fishcake"),
    ("production-tutorial-3", "Sleepless on Sernimir IV"),

    ("bonding-2", "Every Day is the First Day"),
    ("bonding-3", "It Takes Three"),
    ("bonding-4", "Split Before Bonding"),
    ("bonding-6", "Settling into the Routine"),
    ("bonding-7", "Nothing Works"),
    # ("bonding-boss", "A Most Unfortunate Malfunction"),
    # ("bonding-5", "Challenge: In-Place Swap")
]

stretch_c_levels = [
    ("bonding-5", "Challenge: In-Place Swap"),
    ("sensing-1", "An Introduction to Sensing"),
    ("sensing-2", "Prelude to a Migraine"),
    ("sensing-3", "Random Oxides"),
]


class SaveFile:
    def __init__(self, filepath):
        self.connection = sqlite3.connect(filepath)
        self.connection.row_factory = sqlite3.Row

    def get_level_row(self, level_id):
        c = self.connection.cursor()
        c.execute('''SELECT * FROM Level WHERE id=?''', (level_id,))
        return c.fetchone()

    def is_level_completed(self, level_id):
        row = self.get_level_row(level_id)
        return row is not None and row['passed'] != 0

    def check_level_completion(self, level_set):
        return [
            (level_id, level_name, self.is_level_completed(level_id))
            for level_id, level_name in level_set
        ]
    
    def get_feedback_and_grades(self):
        feedback_core = "CORE:\n"
        completion = self.check_level_completion(core_levels)
        core_completion_count = sum(1 for (_, _, complete) in completion if complete)
        feedback_core += f"✅ You completed {core_completion_count} out of {len(core_levels)} levels\n"
        for level_id, level_name, complete in completion:
            if not complete:
                feedback_core += f"❌ You did not complete '{level_name}'\n"

        feedback_sa = "STRETCH GOAL A:\n"
        row = self.get_level_row('bonding-2')
        if row is None or row['passed'] == 0:
            feedback_sa += "❌ You did not complete 'Every Day is the First Day'"
            done_sa = False
        elif row['cycles'] > 300:
            feedback_sa += f"❌ You completed 'Every Day is the First Day' in {row['cycles']} cycles, which is more than 300"
            done_sa = False
        else:
            feedback_sa += f"✅ You completed 'Every Day is the First Day' in {row['cycles']} cycles"
            done_sa = True
        feedback_sa += "\n"

        feedback_sb = "STRETCH GOAL B:\n"
        row = self.get_level_row('bonding-3')
        if row is None or row['passed'] == 0:
            feedback_sb += "❌ You did not complete 'It Takes Three'"
            done_sb = False
        elif row['symbols'] > 20:
            feedback_sb += f"❌ You completed 'It Takes Three' in {row['symbols']} symbols, which is more than 20"
            done_sb = False
        else:
            feedback_sb += f"✅ You completed 'It Takes Three' in {row['symbols']} symbols"
            done_sb = True
        feedback_sb += "\n"
        
        feedback_sc = "STRETCH GOAL C:\n"
        completion = self.check_level_completion(stretch_c_levels)
        count_sc = sum(1 for (_, _, complete) in completion if complete)
        for level_id, level_name, complete in completion:
            if complete:
                feedback_sc += f"✅ You completed '{level_name}'\n"
            else:
                feedback_sc += f"❌ You did not complete '{level_name}'\n"

        done_stretches = 0
        if done_sa:
            done_stretches += 1
        if done_sb:
            done_stretches += 1
        if count_sc == len(stretch_c_levels):
            done_stretches += 1

        if core_completion_count == len(core_levels):
            if done_stretches == 3:
                feedback_general = "You completed all core levels and all stretch goals. Excellent work!"
            elif done_stretches == 2:
                feedback_general = "You completed all core levels and two of the stretch goals. Great work!"
            elif done_stretches == 1:
                feedback_general = "You completed all core levels and one of the stretch goals. Good work!"
            else:
                feedback_general = "You completed all core levels -- good work! However you didn't manage to complete any of the stretch goals."
        else:
            feedback_general = "You didn't quite manage to finish all the core levels. Well done for what you did complete, but be sure to seek out help if you get stuck on future tasks!"
        
        feedback = f"{feedback_general}\n\n{feedback_core}\n{feedback_sa}\n{feedback_sb}\n{feedback_sc}"
        grades = [core_completion_count, 1 if done_sa else 0, 1 if done_sb else 0, count_sc]
        return feedback, grades

class OgvDirectory(SaveFile):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get_level_row(self, level_id):
        level_name = [n for i, n in core_levels + stretch_c_levels if i == level_id][0]
        g = glob.glob(os.path.join(self.dir_path, f"SpaceChem - {level_name} *.ogv"))
        if len(g) > 0:
            filename = os.path.basename(g[0])
            stats = filename.split('(')[1].split(')')[0]
            stats = [int(s) for s in stats.split(',')]
            return {
                'passed': 1,
                'cycles': stats[0],
                'symbols': stats[2]
            }
        else:
            return None


if __name__ == '__main__':
    base_path = sys.argv[1]

    feedback_file = open("feedback.txt", "wt")
    grade_file = open("grades.csv", "wt")

    def print_fb(text):
        feedback_file.write(text)
        feedback_file.write("\n")

    for dir_name in sorted(os.listdir(base_path)):
        dir_path = os.path.join(base_path, dir_name)
        if os.path.isdir(dir_path) and dir_name.endswith("assignsubmission_file_"):
            student_name = dir_name.split('_')[0].title()

            print_fb("=" * 60)
            print_fb(student_name)
            print_fb("=" * 60)
            save_file_path = os.path.join(dir_path, "000.user")
            save_file = None
            if os.path.exists(save_file_path):
                save_file = SaveFile(save_file_path)
            elif any(glob.glob(os.path.join(dir_path, "*.ogv"))):
                save_file = OgvDirectory(dir_path)
                print_fb("NB: you provided videos but did not provide a save file. Please be sure to read submission instructions carefully!\n")
            else:
                print_fb("🚷 Save file not found\n")

            if save_file is not None:
                feedback, grades = save_file.get_feedback_and_grades()
                print_fb(feedback)
                grade_file.write(f"{student_name},{','.join(str(g) for g in grades)}\n")

