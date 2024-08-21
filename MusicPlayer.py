import os
import pygame
from tkinter import *
from mutagen.id3 import ID3, error

root = Tk()
root.minsize(300, 300)

# Songs and real names arrays
listofsongs = []
realnames = []
index = 0
v = StringVar()
songlabel = Label(root, textvariable=v, width=35)


def nextsong(event):
    global index
    index += 1
    if index >= len(listofsongs):
        index = 0  # Loop back to the first song
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def previoussong(event):
    global index
    index -= 1
    if index < 0:
        index = len(listofsongs) - 1  # Loop back to the last song
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")
    return songname


def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    return songname


def directorychooser():
    # Directly set the directory path to the desired folder containing the mp3 files
    directory = r"E:\ALL FILES\mini projects\music player\music for project"
    os.chdir(directory)

    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            realdir = os.path.realpath(file)
            listofsongs.append(realdir)

            try:
                audio = ID3(realdir)
                realnames.append(audio["TIT2"].text[0])
            except (error, KeyError):  # Handle missing or corrupt ID3 tags
                realnames.append(os.path.basename(realdir))  # Use file name as fallback

    if listofsongs:
        pygame.mixer.init()
        pygame.mixer.music.load(listofsongs[0])
        pygame.mixer.music.play()
        updatelabel()


label = Label(root, text="Music Player")
label.pack()

listbox = Listbox(root)
listbox.pack()

nextbutton = Button(root, text="NEXT SONG")
nextbutton.pack()

previousbutton = Button(root, text="PREVIOUS SONG")
previousbutton.pack()

stopbutton = Button(root, text="STOP SONG")
stopbutton.pack()

nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", previoussong)
stopbutton.bind("<Button-1>", stopsong)

songlabel.pack()

# Automatically call directorychooser to load songs from the specified folder
directorychooser()

for item in realnames:
    listbox.insert(END, item)

root.mainloop()
