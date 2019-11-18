import sys
import re

def main(filename):
    with open(filename, 'rt') as f:
        file_content = f.read()
    
    rubric_start = file_content.find(r'\begin{markingrubric}') + len(r'\begin{markingrubric}')
    rubric_end = file_content.find(r'\end{markingrubric}')
    rubric_content = file_content[rubric_start:rubric_end]
    
    criteria = []
    crit_re = re.compile(r'\\criterion{([^{}]*)}{[0-9]*\\%}')
    
    match = crit_re.search(rubric_content)
    while match is not None:
        criterion_title = match.group(1)
        rubric_content = rubric_content[match.end():]
        next_match = crit_re.search(rubric_content)
        next_match_start = next_match.start() if next_match is not None else -1
        criterion_body = rubric_content[:next_match_start].strip().split(r'\grade')
        criteria.append((criterion_title, criterion_body))
        match = next_match
    
    ctrl_a = 'keystroke "a" using command down\nkeystroke " "'
    tab2 = 'keystroke tab\nkeystroke tab'
    return2 = 'keystroke return\nkeystroke return'
    
    for title, descs in criteria:
        title = title.replace(r'\&', '&')
        print(ctrl_a)
        print(f'keystroke "{title}"')
        print(tab2)
        
        descs = [d.strip() for d in descs]
        descs = [d for d in descs if d != '']
        assert(len(descs) == 6)
        
        grades = ['REFER FOR RESUBMISSION', 'ADEQUATE', 'COMPETENT', 'VERY GOOD', 'EXCELLENT', 'OUTSTANDING']
        
        for i in range(6):
            grade = grades[i]
            desc = descs[i]
            print(ctrl_a)
            print(f'keystroke "{grade}"')
            
            paras = [p.strip() for p in desc.split(r'\par')]
            for para in paras:
                para = para.replace(r'\fail', '').replace('\n', ' ').replace('\t', ' ').strip()
                
                print(return2)
                print(f'keystroke "{para}"')
            
            print(tab2)
        
        print(tab2)
        print('keystroke tab')

if __name__ == '__main__':
    main(sys.argv[1])
