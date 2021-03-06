# GUI.py
# FINAL PROJECT FOR NETWORK CLASS

# ----------------------------Necessary imports tkinter
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as box
import tkinter.font as tkFont


# ----------------------------Imports for communication
import socket
import time
import json

# setting the IP and ports
client_IP = socket.gethostname()
port = 7500

#Open a socket and connect the client to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_IP, port))
# Individual score
individual_score = 0


# ----------------------------Global constants
NAME_OF_THE_GAME = 'Friendly Feud'
WINDOW_SIZE = '500x800'
NUMBER_OF_QUESTIONS = 10 # 10 questions
# ----------------------------Main window---------------------------------------
root = Tk()
root.title(NAME_OF_THE_GAME)

# ----------------------------Geometry for frames inside the root
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

# Set window size

# ----- Store an integer as a picked choice identifier
v = IntVar()
a1 = StringVar()
# ----------------------------Global variables used by client.py
username = ''
# ----------------------------Usernames for the leaderboard from the server's json
leader_player_one=''
leader_player_two=''
leader_player_three=''

current_question = StringVar()
a2 = StringVar()
a3 = StringVar()
a4 = StringVar()
questions_left = NUMBER_OF_QUESTIONS
# This is where the player scores can be inserted from the server
scores = {'player1':0,'player2':0,'player3':0}
question_frame = Frame(root)

    
#receive the question/answer from server and update GUI variables
def get_question_from_server():
    """ Make a server request with the specified
        question number, num, and sets the client's global
        variables with the correct question content
    """
    global current_question, a1,a2,a3,a4

    #receive the question and choices in pieces
    
    current_question.set(str(client_socket.recv(1024).decode()))
    client_socket.send('STATUS: RECEIVED'.encode())

    a1.set(str(client_socket.recv(1024).decode()))
    client_socket.send('STATUS: RECEIVED'.encode())

    a2.set(str(client_socket.recv(1024).decode()))
    client_socket.send('STATUS: RECEIVED'.encode())

    a3.set(str(client_socket.recv(1024).decode()))
    client_socket.send('STATUS: RECEIVED'.encode())  

    a4.set(str(client_socket.recv(1024).decode()))
    client_socket.send('STATUS: RECEIVED'.encode())


#------------------------------Styles
# Font styles
questionFontSize = tkFont.Font(family="Lucida Grande", size=18)
submitButtonFontSize = tkFont.Font(family="Helvetica", size=12)


# ---------------------------Username frame-------------------------------------
usernameFrame = Frame(root)
usernameFrame.pack()
# Create an image
w = Canvas(usernameFrame,height=450,width=450)
w.pack(expand=True, fill='both')
# Create an image
w.image = PhotoImage(file="giphy.gif")
w.create_image(0,0, image=w.image,anchor='nw')
        

# create username
label_username = Label(usernameFrame,text='Username:',font=submitButtonFontSize).pack()
# Hold username
uString = StringVar()
# Entry to ask for a username
userNameEntry = Entry(usernameFrame,textvariable=uString,width=20,font=submitButtonFontSize).pack()

# ---------------------------Exit from the program
def exitTheProgram():
    '''Destroy the window'''
    var = box.askyesno('Exiting','Are you sure?')
    if var == 1:
        box.showinfo('Exiting','Come back soon!')
        root.destroy()
    
def set_username():
    '''Get text from the entry and send it to the server'''
    global username
    username = uString.get()
    client_socket.send(username.encode())
    #time.sleep(10)
    usernameFrame.pack_forget()
    usernameFrame.destroy()

# Button to set username
button_get_username = Button(usernameFrame, text="Submit",
                          bg='white',
                          padx=20,
                          bd=0,
                          font=submitButtonFontSize,
                          command=set_username).pack()

usernameFrame.pack()
# ------------------------------------------------------------------------------


def show_leaderboard():
    # -----------------------------------Leaderboard frame--------------------------
    
    leaderboard_frame = Frame(root)

    leaderboard_scores = Label(leaderboard_frame, text='SCORES',font=questionFontSize).pack()
    
    player_one_label = Label(leaderboard_frame,text=leader_player_one,font=questionFontSize).pack()
    player_one_score = Label(leaderboard_frame,text=scores['player1'],font=questionFontSize).pack()
    player_two_label = Label(leaderboard_frame,text=leader_player_two,font=questionFontSize).pack()
    player_two_score = Label(leaderboard_frame,text=scores['player2'],font=questionFontSize).pack()
    player_three_label = Label(leaderboard_frame,text=leader_player_three,font=questionFontSize).pack()
    player_three_score = Label(leaderboard_frame,text=scores['player3'],font=questionFontSize).pack()

    
    
    # Exit the program
    button_close_leaderboard = Button(leaderboard_frame, text="close",
                                  bg='white',
                                  padx=20,
                                  bd=0,
                                  font=submitButtonFontSize,
                                  command=exitTheProgram).pack()
    return leaderboard_frame


def final_screen():
    '''Final screen where the player exit the game or restart the game'''
    final_screen_frame = Frame(root)
    button_play_again = Button(final_screen_frame, text="PLAY AGAIN",
                                  bg='white',
                                  padx=20,
                                  bd=0,
                                  font=submitButtonFontSize,
                                  command=lambda : final_screen_frame.pack_forget())


    button_exit = Button(final_screen_frame, text="EXIT",
                                  bg='white',
                                  padx=20,
                                  bd=0,
                                  font=submitButtonFontSize,
                                  command=exitTheProgram).pack()

    return final_screen_frame
    

# ------------------------------------------------------------------------------
    
def show_current_question():
    '''Returns question frame with button handlers'''
    # -----------------------------------Question frame-----------------------------
    global question_frame, current_question, a1, a2, a3, a4

    # image for the questions
    # Create an image
    w = Canvas(question_frame,height=250,width=250)
    w.grid(row=0,column=0)
    # Create an image
    w.image = PhotoImage(file="time.gif")
    w.create_image(0,0, image=w.image,anchor='nw')
    
    # Progressbar how many questions left
    progressBar = ttk.Progressbar(question_frame, orient = HORIZONTAL,
                          length=100, mode='indeterminate')
    
    progressBar['value'] += questions_left * 10 + 1
    question_frame.update_idletasks()
    progressBar.grid(row=1, column=0)
    
    question_label = Label(question_frame,textvariable=current_question,font=questionFontSize).grid(row=2,column=0)
    

    first = Radiobutton(question_frame,textvariable=a1,
                            variable=v,
                            indicatoron=0,
                            padx=20,
                            pady=2,
                            width=20,
                            bd=0,
                            height=4,
                            value=1).grid(row=3, column=0,sticky="nsew")

    second = Radiobutton(question_frame,textvariable=a2,
                             variable=v,
                             indicatoron=0,
                             padx=20,
                             width=20,
                             bd=0,
                             height=4,
                             value=2).grid(row=4, column=0,sticky="nsew")

    third = Radiobutton(question_frame,textvariable=a3,
                            variable=v,
                            indicatoron=0,
                            padx=20,
                            width=20,
                            bd=0,
                            height=4,
                            value=3).grid(row=5, column=0,sticky="nsew")

    fourth = Radiobutton(question_frame,textvariable=a4,
                             variable=v,
                             indicatoron=0,
                             padx=20,
                             width=20,
                             bd=0,
                             height=4,
                             value=4).grid(row=6, column=0,sticky="nsew")


    # Submit button handler
    # Send the value from the checkbox to the server
    def sendToServer():
        '''This function sends an answer to the server'''
        global questions_left,individual_score,v, scores, leader_player_one,leader_player_two,leader_player_three
        
        # Case when no answer given
        if v.get() == 0:
            box.showinfo('Oops...','Have to pick one of the provided answers')
            # Should not send any request for the next question

        questions_left -= 1
        # Decide when to show score
        if questions_left == 0:
            #global and variable game_counter for testing
            #global game_counter
            # Player need to restart the client to start new game
            #game_counter = 0
            question_frame.destroy()
          
            #sending to server
            client_socket.recv(1024).decode() 
            client_socket.send(str(v.get()).encode()) #send the answer to server
            client_socket.recv(1024).decode() 
            client_socket.send('REQUESTING CLIENT SCORE'.encode())
            group_score = client_socket.recv(1024).decode() #THIS IS WHERE THE END OF COMMUNICATION IS
            
            data = json.loads(group_score)

            # SET player scores from the leaderboard's server data
            
            scores['player1'] = data['user1']['score']
            scores['player2'] = data['user2']['score']
            scores['player3'] = data['user3']['score']

            # SET player's usernames
            leader_player_one = data['user1']['username']
            leader_player_two = data['user2']['username']
            leader_player_three = data['user3']['username']
            
            # Show leaderboard with updated values from the server
            show_leaderboard().grid(row=0,column=1)
            
            # reset questions left for the next game
            questions_left = NUMBER_OF_QUESTIONS
            
        # Answer is given
        else:
            question_frame.grid_forget()
            client_socket.recv(1024).decode() 
            client_socket.send(str(v.get()).encode()) #send the answer to server
            client_socket.recv(1024).decode() 
            
            # This would be where we can add the ability to update score in real time
            # AKA let client know if they got the question right/wrong

            # create a new frame with next question
            v.set(0) # reset the selection for the next question
            get_question_from_server()
        
            show_current_question() #This is what we were missing, we needed to update the display
                                   


        
    #-----------------------------Submit button
    submitButton = Button(question_frame, text="Submit",
                              bg='white',
                              padx=20,
                              width=20,
                              height=3,
                              bd=0,
                              command=sendToServer).grid(row=7, column=0)

    
    question_frame.pack()
    return question_frame


# ------------------------------------------------------------------------------


# ----------------------------Assign questions and anwers from the server ----
def startGame():
    get_question_from_server()
    # Show questions
    show_current_question()
    
    '''Start the game. This command will request a question from the server'''
    box.showinfo('New game','The game is about to start')  

def showInstruction():
    '''Show game instruction'''
    # Added game instruction
    box.showinfo('Instruction','1. Enter username.\n2. Click submit button.\n 3. Answer 10 questions. \n 4. See your score.')

def showCredits():
    '''Show credits. List people who created this game'''
    box.showinfo('Credits','This is created by Walid, Daniel, Alex. WDA team')



# ----------------------------Create a menu
menu = Menu(root)
root.config(menu=menu)

choice = Menu(menu)
menu.add_cascade(label=NAME_OF_THE_GAME,menu=choice)

choice.add_command(label='Start the game',command=startGame)
choice.add_command(label='Instruction', command=showInstruction)
choice.add_command(label='Credits', command=showCredits)
choice.add_separator()
choice.add_command(label='Exit', command=exitTheProgram)

# ----------------------------Show main window
root.mainloop()
