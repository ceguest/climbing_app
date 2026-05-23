import random, tkinter as tk
from tkinter import ttk, filedialog as fd 

def introMessage(a):
    window = tk.Toplevel()
    window.title('Codenames - Intro')
    txt = tk.Label(window,
                   text = ('Sorry, the word list could not be located.\n\n'
                           'Press OK to open the file manager and navigate '
                           'to the location of the Word_List.txt file that '
                           'you downloaded with this application.'),
                   wraplength = 200,
                   justify = 'left')
    txt.pack()
    btn = tk.Button(window,
                    text = 'OK',
                    command = window.destroy)
    btn.pack()
    a.wait_window(window)

def getWords():
    try:
        full_list = open('Word_List.txt','r').read()
    except:
        a = tk.Tk()
        a.withdraw()
        a.update()
        introMessage(a)
        full_list = fd.askopenfile().read()
        a.destroy()
    word_list = full_list.split('\n')
    return word_list

def gameWords(word_list):
    game_words = []
    random.shuffle(word_list)
    for i in range(25):
        game_words.append(word_list[i])
    return game_words

def chooseP1():
    p1 = random.randint(1,2)
    return p1

def colourList(p1):
    if p1 == 1:
        a , b = 9 , 8
    else:
        a , b = 8 , 9
    colour_list = ['Blue']*a + ['Red']*b + ['Bystander']*7 + ['Assassin']
    random.shuffle(colour_list)
    return colour_list
    
def setupGame(game_words,colour_list):
    game_matrix = {}
    for i in range(len(game_words)):
        game_matrix[game_words[i]] = colour_list[i]
    return game_matrix

def btnPress(event,game_matrix,lbl_blue,lbl_red):
    button = event.widget
    word = button.cget('text')
    colour = game_matrix[word]
    button.configure(state = 'disabled')
    button.unbind('<Button-1>')
    if colour == 'Assassin':
        button.configure(style = 'Assassin.TButton')
        if lbl_blue['text'] != '0' and lbl_red['text'] != '0':
            youLose()
    elif colour == 'Bystander':
        button.configure(style = 'Bystander.TButton')
    elif colour == 'Blue':
        button.configure(style = 'Blue.TButton')
        score = updateScore(lbl_blue)
        if score == 0 and lbl_red['text'] != '0':
            youWin('Blue')
    elif colour == 'Red':
        button.configure(style = 'Red.TButton')
        score = updateScore(lbl_red)
        if score == 0 and lbl_blue['text'] != '0':
            youWin('Red')

def youLose():
    popup = tk.Toplevel(background = '#FFFAFA')
    popup.title('Codenames - Game Over')
    title = ttk.Label(popup,
                      background = '#FFFAFA',
                      text = '\nGame Over!\n',
                      font = ('Helvetica',15,'bold'),
                      anchor = 'center')
    message = ('Unfortunately you found the assassin.\n\n'
               'This means the game is over, but you can still click on the '
               'remaining words to reveal the full board if you want to.\n\n'
               'Alternatively return to the main screen and click "Restart" '
               'to play again, or "Quit Game" to exit the application.\n')
    title.pack()
    txt_lose = ttk.Label(popup,
                         background = '#FFFAFA',
                         text = message,
                         wraplength = 500,
                         font = ('Helvetica',12))
    txt_lose.pack()
    popup.focus_force()

def youWin(colour):
    popup = tk.Toplevel(background = '#FFFAFA')
    popup.title('Codenames - Game Over')
    title = ttk.Label(popup,
                      background = '#FFFAFA',
                      foreground = colour,
                      text = colour + ' Wins!\n',
                      font = ('Helvetica',15,'bold'),
                      anchor = 'center')
    message = ('Congratulations to the ' + colour + ' team.\n\n'
               'This means the game is over, but you can still click on the '
               'remaining words to reveal the full board if you want to.\n\n'
               'Alternatively return to the main screen and click "Restart" '
               'to play again, or "Quit Game" to exit the application.\n')
    title.pack()
    txt_lose = ttk.Label(popup,
                         background = '#FFFAFA',
                         text = message,
                         wraplength = 500,
                         font = ('Helvetica',12))
    txt_lose.pack()
    popup.focus_force()

def updateScore(label):
    score = int(label['text'])
    score -= 1
    label.configure(text = str(score))
    return score

def setStyles():
    style = ttk.Style()
    style.theme_use('alt')
    style.configure('Standard.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'),
                    focuscolor = 'None')
    style.configure('Assassin.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'))
    style.map('Assassin.TButton',
              background = [('disabled','#696969')],
              foreground = [('disabled','white')],
              embossed = [('disabled',False)])
    style.configure('Bystander.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'))
    style.map('Bystander.TButton',
              background = [('disabled','#F4A460')],
              foreground = [('disabled','black')],
              embossed = [('disabled',False)])
    style.configure('Blue.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'))
    style.map('Blue.TButton',
              background = [('disabled','#ADD8E6')],
              foreground = [('disabled','black')],
              embossed = [('disabled',False)])
    style.configure('Red.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'))
    style.map('Red.TButton',
              background = [('disabled','#F08080')],
              foreground = [('disabled','black')],
              embossed = [('disabled',False)])
    style.configure('Alert.TButton',
                    relief = 'groove',
                    font = ('Helvetica',15,'bold'),
                    foreground = 'red')    

def helpGUI(p1,screen_width,screen_height):
    help_width = screen_width / 2
    help_height = screen_height / 2
    popup = tk.Toplevel(width = help_width,
                        height = help_height,
                        background = '#FFFAFA')
    popup.title('Codenames - Help')
    title = ttk.Label(popup,
                      background = '#FFFAFA',
                      text = '\nWelcome to Codenames.\n',
                      font = ('Helvetica',15,'bold'),
                      anchor = 'center')
    title.pack()
    if p1 == 1:
        first = 'Blue'
    else:
        first = 'Red'
    msg_start = first + ' has been chosen to play first this time.\n'
    txt_first = ttk.Label(popup,
                          background = '#FFFAFA',
                          foreground = first,
                          text = msg_start,
                          wraplength = 500,
                          font = ('Helvetica',12))
    txt_first.pack()
    message = ('The game is automatically set up and ready to play.\n\n'
               'To get started please ensure you are not sharing your screen '
               'then click the "Show Key" button, take a photo of the key, '
               'and then close the key popup. At this point you are ready to '
               'share your screen with the other players.\n\n'
               'To check a word please click on its button - the background '
               'will change colour to indicate whether it is a point for one '
               'of the teams, a bystander, or the assassin.\n\n'
               'The blue and red boxes at the bottom of the screen are for '
               'making any notes required throughout the game, for example '
               'previous clues and the number of words indicated.\n\n'
               'To close the main window please click the "Quit Game" button.\n'
               'You can also navigate away using the usual method for your OS '
               'eg Alt-Tab or swiping the trackpad.\n\n'
               'Click the help button at any time to see this message again.\n')
    txt_help = ttk.Label(popup,
                         background = '#FFFAFA',
                         text = message,
                         wraplength = 500,
                         font = ('Helvetica',12))
    txt_help.pack()
    popup.focus_force()
    
def keyGUI(game_matrix,word_list,screen_width,screen_height):
    key_width = screen_width / 2
    key_height = screen_height / 2
    popup = tk.Toplevel(width = key_width,
                        height = key_height)
    popup.title('Codenames - Key')
    for i in range(5):
        for j in range(5):
            num = j*5 + i
            col = game_matrix[word_list[num]]
            if col == "Assassin":
                col = 'Black'
            elif col == "Bystander":
                col = '#F4A460'
            frame = tk.Frame(popup, bg = col,
                             height = key_height / 5,
                             width = key_width / 5,
                             highlightbackground = 'black',
                             highlightthickness = 1)
            frame.propagate(0)
            frame.grid(row = i,
                       column = j)
    popup.focus_force()

def restartGame(window,all_words):
    for widget in window.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    p1, matrix, words = initialise(all_words)
    gameGUI(window,matrix,words,p1,all_words)

def wordButtons(screen,std_h,std_w,word_list,game_matrix,lbl_blue,lbl_red):
    for i in range(5):
        for j in range(5):
            num = j*5 + i
            frame = tk.Frame(screen,
                             height = std_h,
                             width = std_w)
            frame.propagate(0)
            frame.grid(row = i,
                       column = j)
            word = ttk.Button(frame,
                              text = word_list[num],
                              style = 'Standard.TButton')
            word.bind('<Button-1>',
                      lambda event,gm = game_matrix, lb = lbl_blue, lr = lbl_red:
                      btnPress(event, gm, lbl_blue, lbl_red))
            word.pack(expand = True,
                      fill = 'both')

def padding(screen):
    frm_pad_col = tk.Frame(screen, width = 10)
    frm_pad_col.propagate(0)
    frm_pad_col.grid(column = 5)
    frm_pad_row = tk.Frame(screen, height = 10)
    frm_pad_row.propagate(0)
    frm_pad_row.grid(row = 5, columnspan = 6)

def helpButton(screen,std_h,std_w,screen_width,screen_height,p1):
    frm_help = tk.Frame(screen,
                        height = std_h,
                        width = std_w)
    frm_help.propagate(0)
    frm_help.grid(column = 7, row = 0)
    btn_help = ttk.Button(frm_help,
                          text = 'Help',
                          style = 'Standard.TButton',
                          command = lambda p = p1, sw = screen_width,
                          sh = screen_height: helpGUI(p,sw,sh))
    btn_help.pack(expand = True, fill = 'both')

def keyButton(screen,std_h,std_w,game_matrix,word_list,
              screen_width,screen_height):
    frm_key = tk.Frame(screen,
                       height = std_h,
                       width = std_w)
    frm_key.propagate(0)
    frm_key.grid(column = 7, row = 1)
    btn_key = ttk.Button(frm_key,
                         text = 'Show Key',
                         style = 'Alert.TButton',
                         command = lambda gm = game_matrix, wl = word_list,
                         sw = screen_width, sh = screen_height:
                         keyGUI(gm, wl, sw, sh))
    btn_key.pack(expand = True, fill = 'both')

def restartButton(screen,std_h,std_w,window,all_words):
    frm_restart = tk.Frame(screen,
                           height = std_h,
                           width = std_w)
    frm_restart.propagate(0)
    frm_restart.grid(column = 7, row = 3)
    btn_restart = ttk.Button(frm_restart,
                             text = 'Restart',
                             style = 'Alert.TButton',
                             command = lambda w = window, aw = all_words:
                             restartGame(w,aw))
    btn_restart.pack(expand = True, fill = 'both')

def quitButton(screen,std_h,std_w):
    frm_quit = tk.Frame(screen,
                        height = std_h,
                        width = std_w)
    frm_quit.propagate(0)
    frm_quit.grid(column = 7,row = 4)
    btn_quit = ttk.Button(frm_quit,
                          text = 'Quit Game',
                          style = 'Alert.TButton',
                          command = window.destroy)
    btn_quit.pack(expand = True, fill = 'both')

def noteBoxes(screen,std_h,std_w):
    frm_txt_blue = tk.Frame(screen,
                            height = std_h,
                            width = std_w * 3)
    frm_txt_blue.propagate(0)
    frm_txt_blue.grid(column = 0, row = 6,
                      columnspan = 3,
                      padx = 3)
    txt_blue = tk.Text(frm_txt_blue,bg = '#ADD8E6')
    txt_blue.pack(expand = True,
                  fill = 'both')
    txt_blue.insert(tk.END,'Blue team can make notes here:\n')
    frm_txt_red = tk.Frame(screen,
                           height = std_h,
                           width = std_w * 3)
    frm_txt_red.propagate(0)
    frm_txt_red.grid(column = 3, row = 6,
                     columnspan = 5)
    txt_red = tk.Text(frm_txt_red,bg = '#F08080')
    txt_red.pack(expand = True,
                  fill = 'both')
    txt_red.insert(tk.END,'Red team can make notes here:\n')

def gameGUI(window,game_matrix,word_list,p1,all_words):
    window.update()
    window.deiconify()
    screen = tk.Toplevel()
    screen.title('Codenames')
    screen.attributes('-fullscreen',True)
    screen.resizable(width=False, height=False)
    screen.update_idletasks()
    screen.deiconify()
    screen_width = screen.winfo_width()
    screen_height = screen.winfo_height()
    std_w = (screen_width - 10) / 6
    std_h = (screen_height - 10) / 6
    ''' Create ttk formatting styles'''
    setStyles()
    ''' Padding between word buttons and other GUI elements'''
    padding(screen)
    ''' Create help button'''
    helpButton(screen,std_h,std_w,screen_width,screen_height,p1)
    ''' Show key button'''
    keyButton(screen,std_h,std_w,game_matrix,word_list,screen_width,screen_height)
    ''' Initialise scores display'''
    frm_scores = tk.Frame(screen,
                          height = std_h,
                          width = std_w,
                          relief = 'groove',
                          borderwidth = 1)
    frm_scores.grid_propagate(0)
    frm_scores.grid(column = 7, row = 2)
    frm_text = tk.Frame(frm_scores,
                        width = std_w,
                        height = std_h / 4)
    frm_text.grid_propagate(0)
    frm_text.grid(row = 0,
                  column = 0,
                  columnspan = 2)
    txt_scores = ttk.Label(frm_text,
                           text = 'Words left to guess:',
                           font = ('Helvetica',10,'bold'),
                           anchor = 'center',
                           background = frm_text['bg'])
    txt_scores.pack_propagate(0)
    txt_scores.pack(expand = True,
                    fill = 'both')
    frm_blue = tk.Frame(frm_scores,
                        height = 6 * std_h / 4,
                        width = std_w / 2,
                        bg = '#ADD8E6')
    frm_blue.propagate(0)
    frm_blue.grid(row = 1,
                  column = 0)
    frm_red = tk.Frame(frm_scores,
                        height = 6 * std_h / 4,
                        width = std_w / 2,
                        bg = '#F08080')
    frm_red.propagate(0)
    frm_red.grid(row = 1,
                  column = 1)
    for i in range(3):
        frm_blue.rowconfigure(i, minsize = frm_blue['height']/3)
        frm_blue.columnconfigure(i, minsize = frm_blue['width']/3)
        frm_red.rowconfigure(i, minsize = frm_red['height']/3)
        frm_red.columnconfigure(i, minsize = frm_red['width']/3)
    if p1 == 1:
        msg_blue = '9'
        msg_red = '8'
    else:
        msg_blue = '8'
        msg_red = '9'
    lbl_blue = ttk.Label(frm_blue,
                         text = msg_blue,
                         font = ('Helvetica',15,'bold'),
                         background = '#ADD8E6',
                         anchor = 'center')
    lbl_blue.grid(column = 1,
                  row = 0,
                  sticky = 'ESW')
    lbl_red = ttk.Label(frm_red,
                        text = msg_red,
                        font = ('Helvetica',15,'bold'),
                        background = '#F08080',
                        anchor = 'center')
    lbl_red.grid(column = 1,
                 row = 0,
                 sticky = 'ESW')
    ''' Restart button'''
    restartButton(screen,std_h,std_w,window,all_words)
    ''' Quit button'''
    quitButton(screen,std_h,std_w)
    ''' Create word buttons'''
    wordButtons(screen,std_h,std_w,word_list,game_matrix,lbl_blue,lbl_red)
    ''' Initialise note entry areas'''
    noteBoxes(screen,std_h,std_w)
    screen.focus_force()
    ''' Call intro/help popup'''
    helpGUI(p1,screen_width,screen_height)    

    screen.mainloop()

def ctrlBox():
    window = tk.Tk()
    window.iconify()
##    window.withdraw()
    return window

def initialise(all_words):
    p1 = chooseP1()
    game_words = gameWords(all_words)
    colours = colourList(p1)
    matrix = setupGame(game_words,colours)
    return p1, matrix, game_words

if __name__ == '__main__':
    all_words = getWords()
    p1, matrix, words = initialise(all_words)
    window = ctrlBox()
    gameGUI(window,matrix,words,p1,all_words)
