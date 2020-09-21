#!/usr/bin/env python3

import random
random.seed(1920)

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


class ClozeQuestion(Question):
    def __init__(self, name):
        Question.__init__(self, "cloze", name)
    
    def appendText(self, text):
        self.questiontext += text
    
    def appendShortAnswer(self, answer, weight=1):
        self.questiontext += "{%r:SHORTANSWER:=%s}" % (weight, answer)
    

if __name__ == '__main__':
    quiz = Quiz()
    
    # Question 1
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
    
    quiz.writeXmlTree("quiz.xml")
    