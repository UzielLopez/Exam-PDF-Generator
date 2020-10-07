from pdf_in_columns import PDF_In_Columns #Contains a modified class to output PDF's formated in columns (for the exam itself)
from fpdf import FPDF #To create PDF files that are not restricted to columns (for the answer key and answer sheet)
from random import shuffle #To randomize the order in which the answers are presented and what the correct
from PIL import Image, ImageFont, ImageDraw #To create the images that will contain the options for each question as well as their answers
import os #To find the folders that contain the resources used to create the exam as well as the figures for each question

class Exam(): 
    
    """
    Initializer function
    @param header (str): the header that will be written in the exam sheet
    @param subheader (str): the subheader that will be written in the exam sheet
    @param how_many_questions (int): how many questions will the exam have
    Returns: nothing 
    """
    def __init__(self, header, subheader, how_many_questions):
        
        #Exam sheet file creation and set up
        self.main_exam_file = PDF_In_Columns()
        #Set up the first page: add the header and subheader and space for the student's information
        self.main_exam_file.add_page()
        self.main_exam_file.set_font('Arial', 'B', 16) 
        self.main_exam_file.cell(0, 10, header, 0, 2, 'C') 
        self.main_exam_file.cell(0, 10, subheader, 0, 2, 'C')
        self.main_exam_file.set_font('Arial', 'B', 13)
        self.main_exam_file.cell(0, 10, "STUDENT NUMBER: " + '_'*16 + "   "*4 + "NAME:"+ "_"*27)
        #Place the 'cursor' where the exam contents will be added in
        self.main_exam_file.set_x(10)
        self.main_exam_file.multi_cell(90, 5,  '\n' * 2)
        
        #Answer sheet file creation and set up
        self.answer_sheet = FPDF()
        self.answer_sheet.add_page()
        self.answer_sheet.set_font('Arial', 'B', 16)
        self.answer_sheet.cell(0, 10,'ANSWER SHEET', 0, 2, 'C')
        self.answer_sheet.set_font('Arial', 'B', 13)
        self.answer_sheet.cell(0, 10, "STUDENT NUMBER: "+ '_'*16+ "   "*4 + "NAME:" + "_"*27)

        #Answer key file creation and set up
        self.answer_key = FPDF()
        self.answer_key.add_page()
        self.answer_key.set_font('Arial', 'B', 16)
        self.answer_key.cell(0, 10, header, 0, 2, 'C') 
        self.answer_key.cell(0, 10, subheader, 0, 2, 'C')
        self.answer_key.cell(0, 10,'ANSWER KEY', 0, 2, 'C')
        
        self.option_letters = ["a", "b", "c", "d"] #Used to map the answers to a letter to display them as options for a question
        self.roman_numerals = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'] #Used to format section numbers
        
        self.main_exam_file.pg_aux = None #Auxiliary varibale to store the page number where a image was inserted
        self.font = ImageFont.truetype("arial.ttf", 50) #Font for the question numbers in the exam sheet
        
        self.dir_name = os.path.dirname(os.path.abspath(__file__)) #Folder where this .py files is stored in (should match with the figures and resources folder)
        empty_opt = "Opcion_nula.png" #Name of the file which contains empty circles for the students to fill
        empty_opt_img_file = os.path.join(self.dir_name, "Resources", empty_opt)
        self.empty_opt_image = Image.open(empty_opt_img_file)

        self.how_many_questions_left = how_many_questions
        self.questions_per_column_in_AS = 25 #How many question slots will be allowed in each column (section headers count as a question slot)
        how_many_columns_in_AS = 0
        self.width_opt_img, self.height_opt_img = self.empty_opt_image.size 
        
        #We calculate the dimentions of the images that will contain the options in both the answer key and answer sheet
        if how_many_questions > self.questions_per_column_in_AS: 

            how_many_columns_in_AS = how_many_questions // self.questions_per_column_in_AS #Full columns
            questions_in_extra_column = how_many_questions % self.questions_per_column_in_AS #How many questions will have the non full column (if it is needed)
            max_height = self.height_opt_img * self.questions_per_column_in_AS #Calculate the height of the resulting image
            
            if questions_in_extra_column != 0: #If there is an non full column, we need to take it into acount
                how_many_columns_in_AS += 1
        
        else:
            how_many_columns_in_AS = 1 #If not even one column is filled, we just need one take into acount one column
            max_height = (self.height_opt_img * how_many_questions) #Calculate the height of the resulting imag
        
        
        self.margin = 60 #Space between the question number and the options for the question (in pixels)
        self.total_image_width = (self.width_opt_img + self.margin*2) * how_many_columns_in_AS #Calculate the width of the image
        
        #We create the "empty canvas" for each image. 
        #In this canvas, the options and headers of section will be pasted in, resulting in one image containing all the questions and sections
        self.column_img = Image.new('RGB', (self.total_image_width, max_height), (255, 255, 255))
        self.empty_col_img = Image.new('RGB', (self.total_image_width, max_height), (255, 255, 255))
        
        self.how_many_q_in_col = 1 #Count of how many questions there are in the current column of the answer sheet

        #Offsets in column_img and empty_col_img. Used to track where the next image containing the options will be inserted at.
        self.x_offset = 0
        self.y_offset = 0
        
    """
    Adds a section to all the exam files
    @param topic (str): the topic that the section will be about
    @param section_number (int): the section number for the current section. 
    Used as index for the list containing the sections in roman numerals (self.roman_numerals)
    Returns: nothing 
    """
    def add_section(self, topic, section_number):

        self.main_exam_file.set_font('Arial', 'B', 12)
        self.main_exam_file.multi_cell(90, 5,  '\n' + self.roman_numerals[section_number] + '. '+topic.upper() + '\n'*2) #Escribir la sección en el examen
        
        font_sec = ImageFont.truetype("arialbd.ttf", 85) 
        empty_space = ((self.width_opt_img + self.margin) -
                       (font_sec.getsize('SECT. '+ self.roman_numerals[section_number])[0]))
        margin_sec_x = (empty_space / 2) #Margenes para centrar el texto de sección en la hoja de answers y en la answer_key.
        margin_sec_y = (self.height_opt_img -
                          font_sec.getsize('SECT. ' + self.roman_numerals[section_number])[1]) / 2
        frame = Image.new('RGB', (self.width_opt_img + self.margin, self.height_opt_img),
                         (210, 210, 210)) #Lienzo para el texto de sección
        draw = ImageDraw.Draw(frame)
        draw.text((margin_sec_x, margin_sec_y - 8), 'SECT. ' + self.roman_numerals[section_number] ,
                  (0,0,0), font_sec) #Escribimos la sección (el -8 es arbitrario. Se añade para que se vea mejor centrado)
        
        self.column_img.paste(frame, (self.x_offset, self.y_offset) ) #Y la pegamos en las imágenes creadas previamente
        self.empty_col_img.paste(frame, (self.x_offset, self.y_offset) )
        
        self.update_answers_column()
     
    """
    Adds a question to the three files associated with the exam
    @param question (str): the question itself.
    @param answers (list of str): the possible answers for that question. The correct one should be at index 0 and there should be a total of 4 elements in the list.
    @param num (str): the question associated to the to-be-added question
                      It's a string beacause there could be no question number for a given question and trying to convert nothing to a int is not possible
    @param type_of_question (str): Indicates what type of question will be added to the exam. For more information, please consult the GitHub repository.
    @param image (str): the name of the file that contains the figure associated with the current answer (if any).
    Returns: nothing 
    """
    def add_question(self, question, answers, num, type_of_question, image):
        
        #We verify if the current mage has a image that takes two column spaces so we format the rest of the pages accordingly.
        if self.main_exam_file.pg_aux == self.main_exam_file.page:
            self.main_exam_file.img_trg = True 
        else:
            self.main_exam_file.img_trg = False
        
        #This self. variables are used in other functions and are updated each time a new question is added
        self.type = type_of_question
        self.question_num = num
        question_num_str = ''
        if num != '': #We won't add a question number if it's notneeded 
            question_num_str = (num + ". ")
        self.main_exam_file.set_font('Arial', '', 10)
        self.main_exam_file.multi_cell(90, 2, '\n') #Blank space between question
        
        self.main_exam_file.multi_cell(90, 4, question_num_str + question) #We write down the question and its question number
        self.how_many_questions_left -= 1 #We update the count of how many questions are left to be added
        
        if image != "nan":

            #We open the image file asscociated to the image, calculate its dimensions, adapt its size to the scale used by FPDF and paste it to the exam
            figure_file_path = os.path.join(self.dir_name, "Figures for exam", image)
            figure_img = Image.open(figure_file_path) 
            fig_img_width, fig_img_height = figure_img.size
            #FPDF uses a 96 dpi resolution, so we most resize the image accordingly
            margin_x = (self.main_exam_file.w - ( (fig_img_width)/(96/25.4) )) / 2  #Margin used to center the image in the current page (if necessary)
            fig_normalized_height =  ((fig_img_height)/(96/25.4))

            if type_of_question != "Imagen": #If we don't need the image to be big (that is, for it to be centered in the page), we paste it in the current column
                self.main_exam_file.image_mod(figure_file_path, h = fig_normalized_height)            
                self.main_exam_file.multi_cell(90, 2, '\n') #Space between the image and the following question
                if type_of_question == "Enunciado":
                    self.type = "Enunciado"
                
        #If the question is a multiple choice question, we shuffle the possible answers and keep track of the correct one so we can add it to the answer key
        #Then, we add the question and its options to the exam sheet
        if type_of_question == "Opcion":
            correct_ans = answers[0] 
            shuffle(answers) 
            correct_ans_index = answers.index(correct_ans)
            self.main_exam_file.multi_cell(90, 5, "a) "+ str(answers[0]) +  "\nb) "+str(answers[1]) +"\nc) "+ str(answers[2])+
                             "\nd) "+ str(answers[3]))
            self.add_option(self.option_letters[correct_ans_index]) 
        
        #If the question is an open-ended question, we just leave some space for the student to write their answer
        elif type_of_question =="Abierta":
            self.main_exam_file.multi_cell(90, 5, '\n' + ("_"*237)) #Se agrega un espacio para escribir
            self.add_option(self.type)

        #If the question revolves around an image, we paste the image in the middle and make it big so the student can write on it (if required)
        #and see it clearly
        elif type_of_question == "Imagen":
            self.main_exam_file.img_trg = True #We indicate that a big image has been inserted so it is taking into account for the following questions

            #We need to check each time an image of this kind is inserted if it will fit in the current page. If it doesn't, we add one
            #FPDF didn't handle this by itself correctly so this had to be added
            if  (self.main_exam_file.get_y() + fig_normalized_height) > (self.main_exam_file.fh - self.main_exam_file.b_margin) or self.main_exam_file.col > 0:
                self.main_exam_file.add_page()
                
                self.main_exam_file.set_x(10) #This margin can be modified as needed!
                self.main_exam_file.set_y(10)
                
                self.main_exam_file.y0 = 10
                self.main_exam_file.set_col(0) #We restart the column count
                
            self.main_exam_file.pg_aux = self.main_exam_file.page #We keep track of the page where the big image was inserted
            self.main_exam_file.image(figure_file_path, margin_x, self.main_exam_file.get_y(), h = fig_normalized_height) #We paste the image, ignoring the columns
            self.main_exam_file.set_y(self.main_exam_file.get_y() + fig_normalized_height + 2) #We leave some empty space between the image and what is next
            self.main_exam_file.y0 = self.main_exam_file.get_y() #Now the reference for the columns to be added is the place where the image ends
            
            self.add_option(self.type)
        
        #If the questions is open-ended and involves an image, nothing else needs to be done
        elif type_of_question == "Enunciado":
            self.add_option(self.type)
        
        
        self.update_answers_column()
 
    """
    Updates the columns on both the answer sheet and answer key and checks if its necessary to add another column to the image
    Returns: nothing
    """
    def update_answers_column(self):
        self.y_offset += self.height_opt_img 
        if(self.how_many_questions_left!=0 and self.how_many_q_in_col%self.questions_per_column_in_AS==0):
            self.y_offset = 0
            self.x_offset += (self.margin*2 + self.width_opt_img)
        self.how_many_q_in_col += 1
        
    """
    Adds a the image containing the possible options for the cucrrent question to both the answer sheet and answer key
    @param letter_for_option (str): indicates what letter is associated with the correct answer so the function can load the appropriate image from the Resources folder
    This parameter can also contain the type of question that was inserted. If that's the case, it indicates that the question that was inserted wasn't a open-ended question
    Returns: nothing 
    """
    def add_option(self, letter_for_option):
        
        #We create a canvas where the options for a question will be and then we paste that canvas to the image that will be pasted in the answer sheet and answer key
        frame = Image.new('RGB', (self.width_opt_img + self.margin, self.height_opt_img), (255, 255, 255))
        draw = ImageDraw.Draw(frame)
        draw.text((0, 60), self.question_num , (0,0,0), font = self.font)
        
        if letter_for_option != self.type:

            #We open and paste the corresponding image for the given question, which will have marked in black the correct answer
            #This image will be pasted in the answer key and will help the teacher (s) with grading
            option_file = "Opcion_" + letter_for_option + ".png"
            option_img_file = os.path.join(self.dir_name, "Resources", option_file)

            img_opt = Image.open(option_img_file)
            frame.paste(img_opt, (self.margin, 0))

        else:
            #If the question is not open-ended, the answer should be written in the exam sheet
            draw.text((70, 68), "Answer in exam sheet" , (0,0,0), self.font)

        self.column_img.paste(frame, (self.x_offset, self.y_offset))
        
        #We need to redefine the canvas for the emtpy_col_img because if we don't, it will keep the previous contents
        frame = Image.new('RGB', (self.width_opt_img + self.margin, self.height_opt_img), (255, 255, 255))
        draw = ImageDraw.Draw(frame)
        draw.text((0, 60), self.question_num, (0,0,0), self.font)
        
        if (self.type=='Abierta' or self.type=='Imagen' or self.type == 'Enunciado'):
            draw.text((70, 68), "Answer in exam sheet" , (0,0,0), self.font)
        else:
            frame.paste(self.empty_opt_image, (self.margin, 0))
        
        self.empty_col_img.paste(frame, (self.x_offset, self.y_offset))
        
    """
    Outputs the three files associated with the exam to the current folder
    Returns: nothing 
    """
    def output_exam_files(self):

        #We save the images that contain all the options for the questions of the exam
        self.column_img.save('columna_llena.png') 
        self.empty_col_img.save('columna_vacia.png')
        
        #The exam sheet needs no more change, so we output it right away!
        self.main_exam_file.output('Exam.pdf','F')

        #We insert the images to their respective files and output them
        self.answer_sheet.image('columna_vacia.png', x = 10, y = self.answer_sheet.get_y() + 15,
                            w = self.total_image_width/18)
        self.answer_sheet.output('Answer Sheet.pdf','F')
        
        self.answer_key.image('columna_llena.png', x = 10, y = self.answer_sheet.get_y() + 25,  
                            w = self.total_image_width/18)
        self.answer_key.output('Answer key.pdf','F')

        #Delete temporary images created to contain the answer options and correct answers
        temp_files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in temp_files:
            if f.endswith(".png"):
                path_to_remove = os.path.join(self.dir_name, f)
                os.remove(path_to_remove)