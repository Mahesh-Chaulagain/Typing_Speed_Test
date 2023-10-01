import curses
from curses import wrapper
import time
import random

DEFAULT_WORD_LENGTH = 5
RANDOM_TEXT = "text.txt"

#start screen
def start_screen(stdscr):
    stdscr.clear()  #clear screen
    stdscr.addstr("Welcome to speed typing test!")
    stdscr.addstr("\n Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey() #wait for user to type something so that program does not close immediately


#display screen 
def display_text(stdscr,target,current,wpm=0,acc=0):
    stdscr.addstr(target)
    stdscr.addstr(2,0,f"WPM:{wpm}")
    # stdscr.addstr(3,0,f"Accuracy:{acc:.2f}%")

    for i,char in enumerate(current):   #provides index and element as tuple
        correct_char = target[i]
        color = curses.color_pair(1)
        if(char != correct_char):
            color = curses.color_pair(2)
        stdscr.addstr(0,i,char,color)


#load text from another file
def load_text():
    with open(RANDOM_TEXT,"r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() #"strip()" gets rid of any leading or trailing whitespace


# def typing_accuracy(current_text,target_text):
    total_characters = min(len(current_text),len(target_text))    #calculate errors in text

    if total_characters == 0:
        return 0    #no error then accuracy 100%
    
    matching_characters=0

    for current,target in zip(current_text,target_text):
        if current == target:
            matching_characters +=1
    matching_percentage = (matching_characters/total_characters) * 100
    return matching_percentage


#calculate wpm
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)    #do not delay waiting for the user to press a key
    # accuracy = typing_accuracy(current_text,target_text)

    while True:
        time_elapsed = max(time.time() - start_time, 1)  #results in not getting divide by zero error. if anything less than one it gives us one
        wpm = round((len(current_text) / (time_elapsed / 60)) / DEFAULT_WORD_LENGTH)  #gives words per minute assuming one word is 5 character long

        # if 30 chars typed in 15 seconds
        #     wpm=30/(15/60) = 120

        stdscr.clear()
        display_text(stdscr,target_text,current_text,wpm,0)
        stdscr.refresh()

        # "".join(current_text) -> #takes list as an argument and combines every single character in the list
        # " ".join(current_text) ->#if "hello" typed output will be h e l l o
        # "-".join(current_text) ->#if "hello" input then output is h-e-l-l-e

        if len("".join(current_text)) == len(target_text):
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if current_text == []:
            start_time = time.time()

        if ord(key) == 27:  #ord(key) is ASCII representation of escape key
            break 

        if key in ("KEY_BACKSPACE",'\b','\x7f'):    #all are representation of backspace key on different os
            if len(current_text) > 0:
                current_text.pop()  #removes last character from the list
        elif len(current_text) < len(target_text):
            current_text.append(key)
       
            
def main(stdscr):   #stdscr is sandard output screen
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)   #green foreground black bg
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        wpm_test(stdscr)
        stdscr.addstr(3,0,"you completed the text! press any key to continue.. and [esc] to end")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)   #calls main function while initializing all of the stuffs related to curses module

