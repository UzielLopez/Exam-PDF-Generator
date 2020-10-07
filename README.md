# Exam-PDF-Generator
A Python program that generates PDF files for an exam and both its answer sheet and answer key, based on the contents of an .xlsx file.

## Motivation
A teacher of mine once showed me the process he and his colleagues go through in order to create an exam where multiple classes and topics are involved. It is pretty messy, so I decided to create a tool that could help the teachers just worry about making the questions for the exam and let them forget about formatting the whole thing by hand.

## Requirements
You will need the following python libraries:
* PIL
* pandas
* fpdf

## How is it meant to be used?
The worlkflow that is intended for the techaers to adopt in orther for this program to be as effective as possible is the following: 
1. Some teacher (who most know how to execute a python program) uploads the given .xlsx template to a collaborative editing platform (such as Google Sheets) and creates a shared folder called "Figures for exam" where the figures used in the exam will be stored.
2. All the teachers involved in the creation of the exam will fill in the .xlsx file as needed. Each row represents a question and the columns represent the following:
  * Column A: Topic
  * Column B: Number of the question relative to the topic it belongs to.
  * Column C: The question itself
  * Column D: A file name (with its respective extension) that refers to the figure that is needed for that particular question
  * Column E: Type of question, which can be:
    * "Opcion": Multiple choice question
    * "Imagen": An image-based question. It is meant to be used when the student needs to draw or write somethng on top of an image.
    * "Enunciado": Open-ended question that can extend through several "subquestions"
    * "Abierta": An open-ended question
  * Column F: The correct answer for the current question. For question types different from multiple choice, this column will be ignored, it's just for reference.
  * Columns G-I: Wrong answers for the current question to be added if the question type is multiple choice.
  
3. When the .xlsx is completed and all the images have been added to the Resources folder, the teacher who created the shared document needs to download it along with the resource folder. They will need to download all the .py files and "Resources" folder located in this repo too and put everything into the same folder.
4. The teacher will run the main.py file and will insert a header and a subheader for the exam.
5. When the program is done executing, the three corresponding PDFs will be outputed in the same folder where the .py files are located.

## What I learnt
* How to work with OOP in Python
* How to use .py files made by me as modules for other .py files
* How to use some basic features in pandas library
* How to use paths with the os module
* Basic image manipulation with PIL

