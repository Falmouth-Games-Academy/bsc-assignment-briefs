#!/usr/bin/env python3

import random
random.seed(1920)

import re
from decimal import Decimal
import math

import xml.etree.ElementTree as ET

class Quiz:
    def __init__(self):
        self.questions = []
    
    def addQuestion(self, question):
        self.questions.append(question)
    
    def getXmlTree(self):
        root = ET.Element("quiz")
        for question in self.questions:
            el = question.getXmlElement()
            root.append(el)
        return root
    
    def writeXmlTree(self, filename):
        tree = ET.ElementTree(self.getXmlTree())
        tree.write(filename, "UTF-8", True)


class Question:
    def __init__(self, questiontype, name, text=""):
        self.questiontype = questiontype
        self.name = name
        self.questiontext = text
    
    def setText(self, text):
        self.questiontext = text
    
    def getXmlElement(self):
        el = ET.XML("""
            <question type="description">
                <name>
                    <text></text>
                </name>
                <questiontext format="html">
                    <text></text>
                </questiontext>
                <generalfeedback format="html">
                    <text></text>
                </generalfeedback>
                <defaultgrade>1.0000000</defaultgrade>
                <penalty>0.3333333</penalty>
                <hidden>0</hidden>
                <idnumber></idnumber>
            </question>
        """)
        
        el.set("type", self.questiontype)
        el.find("./name/text").text = self.name
        el.find("./questiontext/text").text = self.questiontext
        
        return el
        
        
class Description(Question):
    def __init__(self, name, text=""):
        Question.__init__(self, "description", name, text)

    def getXmlElement(self):
        el = Question.getXmlElement(self)
        el.find('./defaultgrade').text = "0.0000000"
        el.find('./penalty').text = "0.0000000"
        return el


class ShortAnswerQuestion(Question):
    def __init__(self, name, text=""):
        Question.__init__(self, "shortanswer", name, text)
        self.answers = []
    
    def addAnswer(self, text, fraction=100, feedback=""):
        self.answers.append((text, fraction, feedback))
    
    def getXmlElement(self):
        el = Question.getXmlElement(self)
        for text, fraction, feedback in self.answers:
            ael = ET.XML("""
                <answer fraction="100" format="moodle_auto_format">
                    <text></text>
                    <feedback format="html">
                        <text></text>
                    </feedback>
                </answer>
            """)
            ael.set("fraction", str(fraction))
            ael.find("./text").text = text
            ael.find("./feedback/text").text = feedback
            el.append(ael)
        
        return el


class MultiChoice(ShortAnswerQuestion):
    def __init__(self, name, text=""):
        ShortAnswerQuestion.__init__(self, name, text)
        self.questiontype = "multichoice"


class MatchingQuestion(Question):
    def __init__(self, name, text=""):
        Question.__init__(self, "matching", name, text)
        self.subquestions = []

    def addQuestionAndAnswer(self, questionText, answerText):
        self.subquestions.append((questionText, answerText))

    def getXmlElement(self):
        el = Question.getXmlElement(self)
        for question, answer in self.subquestions:
            qel = ET.XML("""
                <subquestion format="html">
                    <text></text>
                    <answer><text></text></answer>
                </subquestion>
            """)
            qel.find("./text").text = question
            qel.find("./answer/text").text = answer
            el.append(qel)

        return el


class NumericalQuestion(ShortAnswerQuestion):
    def __init__(self, name, text=""):
        ShortAnswerQuestion.__init__(self, name, text)
        self.questiontype = "numerical"


class ClozeQuestion(Question):
    def __init__(self, name):
        Question.__init__(self, "cloze", name)
    
    def appendText(self, text):
        self.questiontext += text
    
    def appendShortAnswer(self, answer, weight=1):
        self.questiontext += "{%r:SHORTANSWER:=%s}" % (weight, answer)
    

if __name__ == '__main__':
    quiz = Quiz()

    def get_nice_random_number():
        mantissa = random.randrange(8, 16) / 8
        exponent = random.randrange(-8, 8+1)
        return (mantissa, exponent)

    def get_nice_random_number_10():
        mantissa = Decimal(random.randrange(100, 1000)) / Decimal(100)
        exponent = random.randrange(-3, 2+1)
        return mantissa * Decimal(2) ** exponent

    def can_represent_as_float(n):
        return float(n) == Decimal(n)

    def format_standard(mantissa, exponent):
        return str(mantissa * 2 ** exponent)

    def format_scientific_base2(mantissa, exponent):
        return f"{mantissa} &times; 2<sup>{exponent}</sup>"

    def format_e(mantissa, exponent):
        s = "%e" % (mantissa * 2 ** exponent)
        return s

    def format_scientific(mantissa, exponent):
        s = format_e(mantissa, exponent)
        match = re.match(r'([0-9.]*)e([-+0-9]*)', s)
        m = float(match.group(1))
        e = int(match.group(2))
        return f"{m} &times; 10<sup>{e}</sup>"

    def format_blank(mantissa, exponent):
        return ""

    formats = [format_scientific_base2, format_e, format_scientific, format_blank]

    # Question 1
    question = MatchingQuestion("ws8_q1")
    question.setText("<p>For each number, select the number whose value is equal.</p>")

    used_numbers = set()
    for fmt in formats:
        for i in range(5):
            number = get_nice_random_number()
            while number in used_numbers:
                number = get_nice_random_number()
            used_numbers.add(number)
            mantissa, exponent = number

            q = fmt(mantissa, exponent)
            if q != "":
                q = f"<p>{q}</p>"

            question.addQuestionAndAnswer(q, format_standard(mantissa, exponent))

    quiz.addQuestion(question)

    # Question 2
    answer_pattern = [True] * 5 + [False] * 5
    random.shuffle(answer_pattern)
    for part in range(10):
        n = None
        while n is None or can_represent_as_float(n) != answer_pattern[part]:
            n = get_nice_random_number_10()

        question = MultiChoice(f"ws8_q2_{part}",
                               f"<p>Can the number {n} be represented exactly in IEEE floating point format?</p>")

        question.addAnswer("Yes", 100 if answer_pattern[part] else 0)
        question.addAnswer("No", 0 if answer_pattern[part] else 100)

        quiz.addQuestion(question)

    # Question 3
    for part in range(5):
        question = NumericalQuestion(f"ws8_q3_{part}")

        rmin = -20
        rmax = 20
        if part < 2:
            rmin = 0

        vx = random.randrange(rmin, rmax+1)
        vy = random.randrange(rmin, rmax+1)

        question.setText(f"<p>Calculate the length of the vector ({vx}, {vy}), giving your answer to 2 decimal places.")

        question.addAnswer("%.2f" % math.sqrt(vx*vx + vy*vy))

        quiz.addQuestion(question)

    # Question 4
    for part in range(5):
        rmin = -10
        rmax = 10
        if part < 2:
            rmin = 0

        vx1 = random.randrange(rmin, rmax+1)
        vy1 = random.randrange(rmin, rmax+1)
        vx2 = random.randrange(rmin, rmax+1)
        vy2 = random.randrange(rmin, rmax+1)

        question = ClozeQuestion(f"ws8_q3_{part}_a")
        question.appendText(f"<p>Let A = ({vx1}, {vy1}) and B = ({vx2}, {vy2}).</p>")
        question.appendText(f"<p>Subtract the vectors: A-B = (")
        question.appendShortAnswer(str(vx1 - vx2))
        question.appendText(", ")
        question.appendShortAnswer(str(vy1 - vy2))
        question.appendText(")</p>")

        quiz.addQuestion(question)

        question = NumericalQuestion(f"ws8_q3_{part}_b")

        question.setText(f"<p>Therefore calculate the distance between A = ({vx1}, {vy1}) and B = ({vx2}, {vy2}), giving your answer to 2 decimal places.")

        dx = vx1-vx2
        dy = vy1-vy2
        question.addAnswer("%.2f" % math.sqrt(dx*dx + dy*dy))

        quiz.addQuestion(question)


    """
    for part in range(5):
        question = ShortAnswerQuestion("ws2_q1_%i" % part)
        n = random.randrange(0, 255)
        question.setText(f"<p>Convert <b>{n}</b> from decimal to 8-bit binary.</p>")
        question.addAnswer(f"{n:08b}")
        quiz.addQuestion(question)
    
    # Question 2
    for part in range(5):
        question = ShortAnswerQuestion("ws2_q2_%i" % part)
        n = random.randrange(0, 255)
        question.setText(f"<p>Convert <b>{n:08b}</b> from 8-bit binary to decimal.</p>")
        question.addAnswer(str(n))
        quiz.addQuestion(question)
    
    # Question 3
    for part in range(5):
        question = ClozeQuestion("ws2_q3_%i" % part)
        a = random.randrange(0, 127)
        b = random.randrange(0, 127)
        question.appendText(f"<p><b>Calculating {a} + {b}</b></p>")
        question.appendText(f"<p>Convert {a} to 8-bit binary: ")
        question.appendShortAnswer(f"{a:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Convert {b} to 8-bit binary: ")
        question.appendShortAnswer(f"{b:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Add these two numbers together: ")
        question.appendShortAnswer(f"{a+b:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Convert your answer from binary to decimal: ")
        question.appendShortAnswer(f"{a+b}")
        question.appendText(f"</p>")
        quiz.addQuestion(question)
    
    # Question 4
    for part in range(5):
        question = ClozeQuestion("ws2_q4_%i" % part)
        a = random.randrange(0, 127)
        b = random.randrange(0, 127)
        a, b = max(a,b), min(a,b) # Force answer to come out positive
        if part in [2, 3]: # Force answer to come out negative
            a,b = b,a
        if part == 4:
            b = a # Force answer to come out zero
        
        question.appendText(f"<p><b>Calculating {a} - {b}</b></p>")
        if a != b:
            question.appendText(f"<p>Convert {a} to 8-bit binary: ")
            question.appendShortAnswer(f"{a:08b}")
            question.appendText(f"</p>")
        question.appendText(f"<p>Convert {b} to 8-bit binary: ")
        question.appendShortAnswer(f"{b:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Express -{b} in 2's complement 8-bit binary: ")
        question.appendShortAnswer(f"{256-b:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Add the binary representations of {a} and -{b} together: ")
        question.appendShortAnswer(f"{(a+256-b)%256:08b}")
        question.appendText(f"</p>")
        question.appendText(f"<p>Convert your answer from 2's complement binary to decimal: ")
        question.appendShortAnswer(f"{a-b}")
        question.appendText(f"</p>")
        quiz.addQuestion(question)
    """
    
    quiz.writeXmlTree("quiz.xml")
    