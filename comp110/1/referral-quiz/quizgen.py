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
    
    def appendMultiChoice(self, answers, weight=1):
        self.questiontext += "{%r:MULTICHOICE:" % weight
        self.questiontext += "~".join(f"%{percent}%{answer}" for (answer, percent) in answers)
        self.questiontext += "}"
    

if __name__ == '__main__':
    quiz = Quiz()

    # Question 1
    quiz.addQuestion(Description("refer_q1_title", "<h3>SpaceChem</h3>"))
    # No question

    # Question 2
    quiz.addQuestion(Description("refer_q2_title", "<h3>Binary notation</h3>"))
    # Reuse existing questions

    # Question 3
    quiz.addQuestion(Description("refer_q3_title", "<h3>Flowcharts and pseudocode</h3>"))
    

    # Question 4
    quiz.addQuestion(Description("refer_q4_title", "<h3>Logic gates</h3>"))

    question = ClozeQuestion("refer_q4")
    question.appendText("<p>Complete the following truth table:</p>")
    question.appendText("<table><tr>")
    for header in ["A", "B", "C", "A or not B", "A or C", "(A or not B) and (A or C)"]:
        question.appendText("<th>" + header + "</th>")
    question.appendText("</tr></table>")
    for A in [False, True]:
        for B in [False, True]:
            for C in [False, True]:
                question.appendText(f"<tr><td>{A}</td><td>{B}</td><td>{C}</td>")
                for Q in [A or not B, A or C, (A or not B) and (A or C)]:
                    question.appendText("<td>")
                    question.appendMultiChoice([(str(X), 100 if Q == X else 0) for X in [False, True]])
                    question.appendText("</td>")
                question.appendText("</tr>")
    question.appendText("</table>")
    quiz.addQuestion(question)

    # Question 5
    quiz.addQuestion(Description("refer_q5_title", "<h3>Computational complexity</h3>"))
    quiz.addQuestion(Description("refer_q5_code", """<p>Consider the following C# function:
<pre>static bool hasDuplicate(List<int> list)
{
    for (int i = 0; i < list.Count; i++)
    {
        for (int j = 0; j < list.Count; j++)
        {
            Console.WriteLine("Comparing {0} and {1}", i, j);
            if (i != j && list[i] == list[j])
            {
                return true;
            }
        }
    }

    return false;
}"""))

    question = ShortAnswerQuestion("refer_q5_1", "If the list has 3 elements, how many times will the Console.WriteLine function be called in the worst case?")
    question.addAnswer("9")
    quiz.addQuestion(question)

    question = ShortAnswerQuestion("refer_q5_2", "If the list has 5 elements, how many times will the Console.WriteLine function be called in the worst case?")
    question.addAnswer("25")
    quiz.addQuestion(question)

    question = MultiChoice("refer_q5_3", "If the list has n elements, how many times will the Console.WriteLine function be called in the worst case?")
    question.addAnswer("n", 0)
    question.addAnswer("2n", 0)
    question.addAnswer("n<sup>2</sup>", 100)
    question.addAnswer("2<sup>n</sup>", 0)
    quiz.addQuestion(question)

    question = MultiChoice("refer_q5_4", "What word could we use to describe the computational complexity of this function?")
    question.addAnswer("Constant", 0)
    question.addAnswer("Linear", 0)
    question.addAnswer("Quadratic", 100)
    question.addAnswer("Logarithmic", 0)
    question.addAnswer("Exponential", 0)
    quiz.addQuestion(question)

    # Question 6
    quiz.addQuestion(Description("refer_q6_title", "<h3>Data structures</h3>"))

    # Question 7
    quiz.addQuestion(Description("refer_q7_title", "<h3>Traversal</h3>"))

    # Question 8
    quiz.addQuestion(Description("refer_q8_title", "<h3>Floating point numbers</h3>"))
    quiz.addQuestion(Description("refer_q8a_title", "<h3>Vectors</h3>"))

    # Question 9
    quiz.addQuestion(Description("refer_q9_title", "<h3>Assembly code</h3>"))

    quiz.writeXmlTree("quiz.xml")
    