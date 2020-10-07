"""
Exam PDF Generator
A Python program that generates an exam with its respective answer sheet and answer key and outputs it as PDF documents based on a .xlsx file
Programmed by Uziel Humberto López Meneses
First stable version programmed on March 10 2020
Last changes made on September 30 2020
Tested on Windows 10. Works as expected.
"""

from exam import Exam #Class with which all operations needed to make the output files are done
import pandas as pd  #To read information from the Excel sheet 

name_of_file_with_questions = str(input("Please insert the name of the file where the questions are located at (include .xlsx extention): "))
header = str(input("Please insert the header for the exam: "))
subheader = str(input("Please insert the subheader: "))

file = pd.read_excel(name_of_file_with_questions, index_col=None, header=0)
file = file.fillna({'Pregunta':''}) #If there is empty cells in the questions row, we fill them with an empty string.
how_many_questions = file.count()['Pregunta'] 

exam = Exam(header, subheader, how_many_questions) #We instance an exam object with the basic information given

#Initial values used for adding questions and sections to the exam inside the following loop
topic = file.at[0,'Tema']
question_num = 0
section_num = 1
exam.add_section(topic, section_num)
current_question_num = None
current_topic = None

#We iterate through every row in the .xlsx (each containing a question with its respective information)
"""
row[0] contains the topic to which the question belongs to
row[1] contains the question number (which teachers will use to keep control of the questions numbering in the Excel file)
row[2] contains the string with the question to be printed in the file
row[3] contains the name of the file of the figure that is used in the current question (if any)
row[4] contains the type of question of the current question
row[5:] contains the list of possible answer options that will appear in the exam sheet (if the question type requires them)
"""
for row in file.itertuples(index=False): 
    
    if row[0] == topic: #If the topic hasn't changed, we add 1 to the section's question count
        if question_num != row[1]:
            question_num += 1
    else:
        section_num += 1  #If it has chaged, we update the section number and reset the question count
        question_num = 1
        topic = row[0]
        exam.add_section(topic, section_num)
    
    question = row[2]
    figure = row[3]
    
    type_of_question = row[4]
    answer_options = list(row[5:])

    #If the question extends throught several "subquestions", the question will use several question slots both the answer sheet and answerkey
    #but all of the subquestions don't need to have their own question number since they belong to a question.
    if type_of_question == "Enunciado": 

        if (int(row[1]) != current_question_num) or (current_topic != topic):
            current_question_num = int(row[1])
            question_num = current_question_num
            current_topic = topic

        else:
            aux_question_num = question_num
            question_num = ''
            exam.add_question(str(question), answer_options, str(question_num), type_of_question, str(figure))
            question_num = aux_question_num
            continue
        
    exam.add_question(question, answer_options, str(question_num), type_of_question, str(figure))
    
exam.output_exam_files() #We output the PDF files to the same folder in which this .py file is contained in