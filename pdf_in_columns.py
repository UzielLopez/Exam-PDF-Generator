from fpdf import FPDF #PDF_In_Columns inherites from this class

"""
This class is used to create PDF files formated into two columns
In the context of Exam PDF Generator, it's only used in for the Exam sheet
"""

class PDF_In_Columns(FPDF):

    def __init__(self):
        super().__init__()
        self.col = 0 #Variable that tracks the current column that needs to be filled (0 indexed)
        self.y0= None  #y coordinate within the document where the column should start
    
    """
    Sets the document variables to take into account the current column
    Returns: nothing
    """
    def set_col(self, col):
        self.col = col #We change the variable to refer to the current column being filled
        x = 10+(col*100) #The multiplier indicates how many dots will be allowed in the column width. 10 is the margin between columns
        self.set_left_margin(x) #We need to redefine the left margin that will be used as reference for the given column
        self.set_x(x) #We update the x coordinate of the cursor to point to where the current column begins so it can start writting there
    
    """
    Adds a footer to each page
    Returns: nothing
    """
    def footer(self): 
        self.set_left_margin(10) #We reset the margin so it doesn't depend on the current column margin
        where_foot_is=-10 #This indicatates that the foot should be 10 mm up the bottom of the page
        self.set_y(where_foot_is) 
        self.set_font('Arial','I',8)
        self.cell(0,10,'Pág. '+ str(self.page) ,0,0,'C')
    
    """
    Defines the logic to be followed when checking if a page break is needed. In this case, we only need a page break
    when the there is two columns and the content that will be inserted won't feet in the space that is left on the second column
    Returns: bool, indicating if a page break will be performed or not
    """
    def accept_page_break(self): #note: Cell and multicell call this method every time they are called
        
        #If there is no big image that takes up space in the two columnsm we use this logic first
        if self.img_trg==False: #Si no hay una imagen grande que tome dos columnas, se usan estos valores
            if self.page==1:
                self.y0=50 #note: this should be changed as the header size in the exam sheet changes, based on what get_y() returns after the header
            else:
                self.y0=10 #note: this value depends on the margin b or t

        #If there is space for another column, just add another column, don't accept a page break
        if(self.col<1): 
            self.set_col((self.col+1))
            self.set_y(self.y0)
            return False
        #If there is no space for another column, accept the page break and reset the column tracker
        else:
            self.set_col(0)
            return True
    
    """
    Inserts an image in the current column
    This method is necessary because when inserting an image with .image() (as it is inherited from FPDF)
    the FPDF accept_page_break method would be called instead of the one that has been overriden in this class definition.
    It also helps to differentiate when you need no insert a big image vs just a helping figure for a question
    @param name (str): path to the file containing the image
    @param x (int): x coordinate within the document where the image will be inserted at
    @param y (int): y coordinate within the document where the image will be inserted at
    @param w (int): width of the image to be inserted
    @param h (int): height of the image to be inserted
    @param type (str): format of the image. If not specified, it is obtained from the image file extension
    @param link (int): if the image will be use as a hyperlink, link is the address where the user will be redirected to
    Returns: nothing
    """

    def image_mod(self, name, x=None, y=None, w=0,h=0,type='',link=''):
        super().image(name, x=None, y=None, w=w, h=h, type='',link='')