import tkinter as tk
from tkinter import *
import pyttsx3

def story1():
    global choice
    choice=0
    mainWin()

def story2():
    global choice
    choice=1
    mainWin()

def story3():
    global choice
    choice=2
    mainWin()

def mainWin():
    global choice, stories, story, storyEntry, newStory, label2, Btn3, wn
    wn = Tk()
    wn.title("DataFlair Spin Yarn")
    wn.configure(bg='mint cream')
    wn.minsize(width=500,height=500)
    wn.geometry("300x300")
    headingLabel = Label(wn, text="DataFlair Spin Yarn", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(x=120, y=10)
    newStory = stories[choice]
    label1 = Label(wn, text="Here is the starting line of the story", fg='black', bg="mint cream", font=('Calibre', 12))
    label1.place(x=30, y=50)
    storyline = StringVar()
    storyline.set(newStory)
    label2 = Label(wn, textvariable=storyline, bg="mint cream", fg='black', font=('Calibre', 10))
    label2.place(x=30, y=80)
    storyEntry = tk.Text(wn, width=50, height=10)
    storyEntry.place(x=50, y=120)
    Btn3 = tk.Button(wn, text="Done", bg='gray', fg='white', font=('Calibre', 12), command=show_read_story)
    Btn3.place(x=200, y=300)
    wn.mainloop()

def read():
    global modifiedStory
    voiceEngine = pyttsx3.init('sapi5')
    voices = voiceEngine.getProperty('voices')
    voiceEngine.setProperty('voice', voices[1].id)
    voiceEngine.say("Here is your story")
    voiceEngine.say(modifiedStory)

def show_read_story():
    global modifiedStory
    modifiedStory = storyEntry.get("1.0", "end-1c")
    modifiedStory = newStory[:-3] + modifiedStory

    wn = Tk()
    wn.title("DataFlair Spin Yarn")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("300x300")
    headingLabel = Label(wn, text="DataFlair Spin Yarn", fg='black', font=('Courier', 15, 'bold'), wraplength=300)
    headingLabel.place(x=100, y=10)

    story = StringVar(wn)
    label = Label(wn, textvariable=story, bg="mint cream", fg='black', font=('Calibre', 12))
    label.place(x=50, y=70)
    l = len(modifiedStory)
    i = 0
    while i < (l // 50 + 1):
        start = i * 50
        end = (i + 1) * 50
        if (i + 1) * 50 > l:
            end = l
        i += 1
        print(modifiedStory[start:end], file=story)
    Btn = tk.Button(wn, text="Read the Story", bg='gray', fg='white', font=('Calibre', 12), command=read)
    Btn.place(x=200, y=300)
    wn.mainloop()

wn = Tk()
wn.title("DataFlair Spin Yarn")
wn.configure(bg='mint cream')
wn.minsize(width=500, height=500)
wn.geometry("300x300")

choice = 0
newStory = ''
modifiedStory = ''
stories = [
    "Ben is very good at yarning a good story. But the story he wrote yesterday ...",
    "One day at night I was bored and started watching a horror movie. After an hour or so ...",
    "Me and my friends planned to go on a trip last week. We started with a very ..."
]
story = StringVar()

headingLabel = Label(wn, text="DataFlair Spin Yarn", fg='black', font=('Courier', 15, 'bold'))
headingLabel.place(x=100, y=10)

label = Label(wn, text="Please select one of the stores by clicking one of the buttons", fg='black', bg="mint cream",
              font=('Calibre', 12))
label.place(x=30, y=80)

storyEntry = Entry(wn, font=('Calibre', 10))
label2 = Label(wn, textvariable=story, bg="mint cream", fg='black', font=('Calibre', 10))

Btn1 = tk.Button(wn, text="Story 1", bg='#d1ccc0', fg='black', font=('Calibre', 12), command=story1)
Btn1.place(x=200, y=130)

Btn2 = tk.Button(wn, text="Story 2", bg='#d1ccc0', fg='black', font=('Calibre', 12), command=story2)
Btn2.place(x=200, y=180)

Btn3 = tk.Button(wn, text="Story 3", bg='#d1ccc0', fg='black', font=('Calibre', 12), command=story3)
Btn3.place(x=200, y=230)

wn.mainloop()