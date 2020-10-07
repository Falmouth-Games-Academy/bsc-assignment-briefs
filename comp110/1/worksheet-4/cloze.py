import itertools
import inspect
import sys
import re

import quizgen

def draw_truth_table(*expression_strs):
    expressions = [eval(s) for s in expression_strs]

    text = ""

    text += "<table><thead><tr>"
    
    td_style = 'style="border: 1px solid black; padding: 5px;"'
    th_style = 'style="border: 1px solid black; padding: 5px;"'

    for param in inspect.signature(expressions[0]).parameters:
        text += f'<th {th_style} scope="col">{param}</th>\n'
    
    for expr_str in expression_strs:
        text += f'<th {th_style} scope="col">{expr_str.split(":")[1].strip()}</th>\n'

    text += "</tr></thead><tbody>\n"

    num_args = len(inspect.signature(expressions[0]).parameters)
    for args in itertools.product([False, True], repeat=num_args):
        text += "<tr>"
        for arg in args:
            text += f'<td {td_style}>{arg}</td>'

        for expression in expressions:
            answer = expression(*args)
            choices = "".join([
                "=" if answer == False else "",
                "False",
                "~",
                "=" if answer == True else "",
                "True"
            ])
        
            text += f'<td {td_style}>{{1:MULTICHOICE:{choices}}}</td>'
        text += "</tr>\n"

    text += "</tbody></table>\n"

    return text


quiz = quizgen.Quiz()

tt = draw_truth_table("lambda A,B,C: A and B and not C")
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_1a", 
    f"<p>Complete the following truth table:</p>{tt}"
))

tt = draw_truth_table("lambda A,B,C: A and not (B and not C)")
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_1b", 
    f"<p>Complete the following truth table:</p>{tt}"
))

tt = draw_truth_table("lambda A,B,C: (A or not B) and (A or C)")
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_1c", 
    f"<p>Complete the following truth table:</p>{tt}"
))

tt = draw_truth_table("lambda A,B,C,D: A and not (B or not C) and (not A and D)")
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_1d", 
    f"<p>Complete the following truth table:</p>{tt}"
))

id1 = "not (A or B)"
id2 = "not A and not B"
tt = draw_truth_table("lambda A,B: "+id1, "lambda A,B: "+id2)
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_3a", 
    f"<p>Show that <b>{id1} = {id2}</b> by completing the following truth table:</p>{tt}"
))

id1 = "not (A and B)"
id2 = "not A or not B"
tt = draw_truth_table("lambda A,B: "+id1, "lambda A,B: "+id2)
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_3b", 
    f"<p>Show that <b>{id1} = {id2}</b> by completing the following truth table:</p>{tt}"
))

id1 = "(A and B) or (A and C)"
id2 = "A and (B or C)"
tt = draw_truth_table("lambda A,B,C: "+id1, "lambda A,B,C: "+id2)
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_3c", 
    f"<p>Show that <b>{id1} = {id2}</b> by completing the following truth table:</p>{tt}"
))

id1 = "(A or B) and (A or C)"
id2 = "A or (B and C)"
tt = draw_truth_table("lambda A,B,C: "+id1, "lambda A,B,C: "+id2)
quiz.addQuestion(quizgen.Question("cloze", "ws_logic_3d", 
    f"<p>Show that <b>{id1} = {id2}</b> by completing the following truth table:</p>{tt}"
))


# print("-"*40)
# print("3a")
# draw_truth_table(lambda A,B: not (A or B))

# print("-"*40)
# print("3b")
# draw_truth_table(lambda A,B: not (A and B))

# print("-"*40)
# print("3c")
# draw_truth_table(lambda A,B,C: (A and B) or (A and C))

# print("-"*40)
# print("3d")
# draw_truth_table(lambda A,B,C: (A or B) and (A or C))

quiz.writeXmlTree("quiz.xml")
