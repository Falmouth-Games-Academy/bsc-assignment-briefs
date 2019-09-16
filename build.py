import pygit2
repo = pygit2.Repository('.')
repo.lookup_reference("HEAD").resolve()
head = repo.head
head_name = head.shorthand

from pathlib2 import Path
import os
import subprocess

directory_list = [ d for d in Path('.').glob("[a-z]*[0-9]*") if d.is_dir() ]

for d in directory_list:
    sub_directory_list = [ s for s in Path(str(d)).glob("[0-9]*") if d.is_dir() ]

    for s in sub_directory_list:
        working_directory = str(s)
        assignment_number = working_directory.split('\\')[-1]

        old_files = [ f for f in Path(working_directory).glob("*.pdf") if f.is_file() ]
        for f in old_files:
            os.remove(str(f))

        for i in range(2):
            subprocess.Popen('pdflatex build.tex -jobname=' + str(head_name) + '-' + str(d) + '-assignment-' +
                             assignment_number + '-' + 'brief', cwd = working_directory).wait()

        old_files = []
        for e in ['*.aux','*.out','*.nav','*.log','*.snm','*.toc','*.tcp']:
            temp = [ f for f in Path(working_directory).glob(e) if f.is_file() ]
            old_files.extend(temp)
        for f in old_files:
            os.remove(str(f))