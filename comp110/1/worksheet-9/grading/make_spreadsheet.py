import os
import glob
import sys

#ROOT_DIR = r"C:\Users\edpow\Desktop\COMP110 FT S1 (2021)-COMP110 COMPUTER BASED (80%) Worksheet Tasks-98228"
#ROOT_DIR = r"C:\Users\edpow\Dropbox\Work Falmouth\_Marking 2122\110"
ROOT_DIR = r"C:\Users\edpow\Downloads\comp110_refer"

def make_row(username, path):
    sys.stdout.write("%s," % username)

    dat = {}

    with open(path, "rt") as datfile:
        for line in datfile:
            if '=' in line:
                key, value = [x.strip() for x in line.split("=")]
                dat[key] = value
    
    levels = [
        ("00150", "Self-Test Diagnostic"),
        ("10981", "Signal Amplifier"),
        ("20176", "Differential Converter"),
        ("21340", "Signal Comparator"),
        ("22280", "Signal Multiplexer"),
        ("30647", "Sequence Generator"),
        ("31904", "Sequence Counter"),
        ("32050", "Signal Edge Detector"),
        ("33762", "Interrupt Handler"),
        ("40196", "Signal Pattern Detector"),
        ("41427", "Sequence Peak Detector"),
        ("42656", "Sequence Reverser"),
        ("43786", "Signal Multiplier")
    ]
    
    def test_level_completed(level_id):
        return ("Best.%s.Cycles" % level_id) in dat
    
    levels_completed = sum(1 for (id, name) in levels if test_level_completed(id))
    sys.stdout.write("%i," % levels_completed)
    
    def test_diffconv_250():
        key = "Best.20176.Cycles"
        return key in dat and int(dat[key]) <= 250

    def test_seqcount_4():
        key = "Best.31904.Nodes"
        return key in dat and int(dat[key]) <= 4

    def test_seqsort():
        return "Best.63534.Cycles" in dat

    sys.stdout.write("1," if test_diffconv_250() else "0,")
    sys.stdout.write("1," if test_seqcount_4() else "0,")
    sys.stdout.write("1," if test_seqsort() else "0,")
    
    sys.stdout.write("\n")


def find_file(dir, filename):
    result = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            if f.lower() == filename.lower():
                result.append(os.path.join(dir, dirpath, f))
    return result

for d in os.listdir(ROOT_DIR):
    student_name = d.split('_')[0]
    dpath = os.path.join(ROOT_DIR, d)
    if os.path.isdir(dpath):
        save_dat_path = find_file(dpath, "save.dat")
        if len(save_dat_path) == 1:
            make_row(student_name, save_dat_path[0])
        else:
            sys.stdout.write(f"{student_name},0,0,0,0,{save_dat_path}\n")

