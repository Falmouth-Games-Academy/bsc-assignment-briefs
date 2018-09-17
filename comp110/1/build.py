import pygit2
repo = pygit2.Repository('../..')
repo.lookup_reference("HEAD").resolve()
head = repo.head
head_name = head.shorthand

try:
    from pathlib import Path   # Python 3
except ImportError:
    from pathlib2 import Path  # Python 2

import os
import subprocess

for i in range(2):
    subprocess.Popen(['pdflatex', "-jobname=" + str(head_name) + '-comp110-assignment-1-brief', 'build.tex']).wait()

directory_list = [ d for d in Path('.').glob("[-A-Za-z0-9]*") if d.is_dir() ]

for d in directory_list:
    working_directory = str(d)

    old_files = [ f for f in Path(working_directory).glob("*.pdf") if f.is_file() ]
    for f in old_files:
        os.remove(str(f))

    for i in range(2):
        subprocess.Popen(['lualatex', "-jobname=" + str(head_name) + '-comp110-assignment-1-' + working_directory, 'build.tex'],
                         cwd = working_directory).wait()

    old_files = []
    for e in ['*.aux','*.out','*.nav','*.log','*.snm','*.toc']:
        temp = [ f for f in Path(working_directory).glob(e) if f.is_file() ]
        old_files.extend(temp)
    for f in old_files:
        os.remove(str(f))
        