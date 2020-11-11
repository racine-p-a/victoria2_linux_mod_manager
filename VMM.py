# -*- coding:Utf-8 -*-

# Steps to make this mod manager working :
# - launch the game once with this option « PROTON_DUMP_DEBUG_COMMANDS=1 %command% » --> can't add the command
#                                                                                               option : must be made by
#                                                                                               user
# - detect and save somewhere the .run file created
# - modify this log file by adding the mod option
# - run the modified
import subprocess
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *


class InterfaceV2MM(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Victoria 2 Mod Manager (linux)')

        # STEAM FRAME
        steam_frame = LabelFrame(self.root, text="INSTALLATION")
        steam_frame.grid(column=0, row=0)

        #       STEAM LAUNCHER
        self.steam_launch_label = Label(steam_frame, text="First, launch steam.").grid(column=0, row=0, sticky='W')
        self.steam_launcher_button = Button(steam_frame, text="Launch Steam", command=self.launch_steam, width=15) \
            .grid(column=0, row=1, pady=(0, 0), sticky='W')
        #       ADD LAUNCH OPTION
        self.file_label = Label(
            steam_frame,
            text="Now add the text below as a launch option (you can remove it later).")\
            .grid(column=0, row=2, sticky='W')
        self.launch_option = Entry(steam_frame, width=10)
        self.launch_option.grid(row=3, sticky='ew')
        self.launch_option.insert(0, 'PROTON_DUMP_DEBUG_COMMANDS=1 %command%')
        #       CHECK PROTON VERSION
        self.proton_version_label = Label(
            steam_frame,
            text="At the same place, check that you force the SteamPlay Compatibility and choose the version « PROTON 4.11-13 ».") \
            .grid(column=0, row=4, sticky='W')
        #       LAUNCH VICTORIA 2 ONCE
        self.launch_victoria = Label(steam_frame, text="Launch Victoria 2.").grid(column=0, row=14, sticky='W')
        self.steam_launcher_button = Button(steam_frame, text="Launch Victoria 2", command=self.launch_victoria2) \
            .grid(column=0, row=15, pady=(0, 0), sticky='W')


        # END BUTTONS FRAME
        end_button_frame = LabelFrame(self.root)
        end_button_frame.grid(column=0, row=1)
        Button(end_button_frame, text='Leave', command=self.root.quit).grid(row=0, column=0)

    def launch_steam(self):
        subprocess.run('steam &', shell=True, check=True, executable='/bin/sh')

    def launch_victoria2(self):
        subprocess.run('steam steam://rungameid/42960 &', shell=True, check=True, executable='/bin/sh')



if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Just launch the mainloop.
        myInterface = InterfaceV2MM()
        myInterface.root.mainloop()
        exit()
    else:
        print('Hello, you somehow mislaunched the mod manager. Use this command instead :')
        print('python3 VMM.py')
        exit()

