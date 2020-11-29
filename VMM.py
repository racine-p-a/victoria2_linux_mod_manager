# -*- coding:Utf-8 -*-

import subprocess
from tkinter import *
from tkinter.ttk import *
import os.path
import stat
from shutil import copyfile


def launch_steam():
    subprocess.run('steam &', shell=True, check=True, executable='/bin/sh')


def launch_victoria2():
    subprocess.run('steam steam://rungameid/42960 &', shell=True, check=True, executable='/bin/sh')


class InterfaceV2MM(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Victoria 2 Mod Manager (linux)')

        # STEAM FRAME
        steam_frame = LabelFrame(self.root, text="INSTALLATION")
        steam_frame.grid(column=0, row=0)

        #       STEAM LAUNCHER
        self.steam_launch_label = Label(steam_frame, text="First, launch steam.").grid(column=0, row=0, sticky='W')
        self.steam_launcher_button = Button(steam_frame, text="Launch Steam", command=launch_steam, width=15) \
            .grid(column=0, row=1, pady=(0, 0), sticky='W')
        #       ADD LAUNCH OPTION
        self.file_label = Label(
            steam_frame,
            text="Now add the text below as a launch option (you can remove it later).") \
            .grid(column=0, row=4, sticky='W')
        self.launch_option = Entry(steam_frame, width=10)
        self.launch_option.grid(row=5, sticky='ew')
        self.launch_option.insert(0, 'PROTON_DUMP_DEBUG_COMMANDS=1 %command%')
        #       CHECK PROTON VERSION
        self.proton_version_label = Label(
            steam_frame,
            text="At the same place, check that you force the SteamPlay Compatibility and choose the version « PROTON "
                 "4.11-13 ».").grid(column=0, row=6, sticky='W')
        #       LAUNCH VICTORIA 2 ONCE
        self.launch_victoria = Label(steam_frame, text="Launch Victoria 2.").grid(column=0, row=14, sticky='W')
        self.steam_launcher_button = Button(steam_frame, text="Launch Victoria 2", command=launch_victoria2) \
            .grid(column=0, row=15, pady=(0, 0), sticky='W')
        #       COLLECT YOUR DATA
        self.grab_data = Label(steam_frame, text="Collect your game data").grid(column=0, row=16, sticky='W')
        self.grab_data_button = Button(steam_frame, text="Save your data", command=self.grab_game_data) \
            .grid(column=0, row=17, pady=(0, 0), sticky='W')
        #       SWAP YOUR EXECUTABLES
        self.steam_launch_label = Label(steam_frame, text="Then, modify the executable we want to use.").grid(column=0,
                                                                                                              row=18,
                                                                                                              sticky='W')
        self.steam_launcher_button = Button(steam_frame, text="Swap the game executable", command=self.swap_executable).grid(column=0, row=19, pady=(0, 0), sticky='W')

        # GAME FRAME
        mod_list_frame = LabelFrame(self.root, text="MOD LIST")
        mod_list_frame.grid(column=0, row=1)
        #       LIST OF MODS FOUNT
        self.mod_list_label = Label(mod_list_frame, text="Mods fount in your steam files.").grid(column=0, row=1,
                                                                                                 sticky='W')
        self.mod_list = Listbox(mod_list_frame)
        self.mod_list.grid(column=0, row=2, sticky='W')
        for mod in self.get_list_of_mods(os.path.expanduser("~") + '/.v2mm/run'):
            self.mod_list.insert(END, mod)
        #       LAUNCH MOD BUTTON
        Button(mod_list_frame, text='Launch selected mod', command=self.launch_game_with_selected_mod).grid(column=1,
                                                                                                            row=2)

        # LOGS OF THE MOD MANAGER
        # TODO

        # END BUTTONS FRAME
        end_button_frame = LabelFrame(self.root)
        end_button_frame.grid(column=0, row=2)
        Button(end_button_frame, text='Leave', command=self.root.quit).grid(row=0, column=0)

    def swap_executable(self):
        """
        We game usually uses victoria2.exe while we want it to use v2game.exe.
        The solution is to :
        - rename victoria2.exe to _victoria2.exe
        - copy v2game.exe to victoria2.exe
        :return:
        """
        game_folder = self.extract_game_directory_from_proton_runfile(os.path.expanduser("~") + '/.v2mm/run')
        os.rename(game_folder + '/victoria2.exe', game_folder + '/_victoria2.exe')
        copyfile(game_folder + '/v2game.exe', game_folder + '/victoria2.exe')

    def launch_game_with_selected_mod(self):
        """
        Launches the game with the appropriate mod. Made with the following steps :
        1° create a temporary file (erase any existing file with the same name)
        2° copy the content of our run file in the new one with a modification
        3° execute this new file within a sub-shell
        :return:
        """
        # Getting the original content.
        source_file_opener = open(os.path.expanduser("~") + '/.v2mm/run', 'r')
        executable_content = source_file_opener.readlines()
        # Modifying the executable to inject our mod.
        new_content = ''
        for line in executable_content:
            if line.startswith('DEF_CMD'):
                new_content += line[0:-2] + ' "-mod=mod/' + self.mod_list.get(ANCHOR) + '")' + "\n"
            else:
                new_content += line
        source_file_opener.close()
        # 1° Creating the new file.
        destination_file = os.path.expanduser("~") + '/.v2mm/mod_launcher'
        destination_file_opener = open(destination_file, 'w')
        # 2° Copy the modified content.
        destination_file_opener.write(new_content)
        destination_file_opener.close()
        # Remember to make the file executable
        st = os.stat(destination_file)
        os.chmod(destination_file, st.st_mode | stat.S_IEXEC)
        # 3° Execute in a sub-shell
        subprocess.run(destination_file + ' &', shell=True, check=True, executable='/bin/sh')

    def get_list_of_mods(self, runfile_location):
        mod_list = ['---']
        # We need to extract the game directory which is within the file. It is the line starting by « cd " ».
        game_directory = self.extract_game_directory_from_proton_runfile(runfile_location)
        if not game_directory:  # If failure to load mods, send back empty list.
            return mod_list

        for item in os.listdir(game_directory + "/mod/"):
            if os.path.isfile(game_directory + "/mod/" + item):  # Is it a file ?
                # And is its extension « .mod » ?
                if item.endswith('.mod'):
                    mod_list.append(item)
        return mod_list

    @staticmethod
    def extract_game_directory_from_proton_runfile(runfile_location):
        """
        Extracts the game main directory using the data from the run file generated by PROTON.
        :param runfile_location: The location of the run file generated by PROTON.
        :return:
        """
        try:
            file_opener = open(runfile_location, 'r')
            executable_content = file_opener.readlines()
            for line in executable_content:
                if line.startswith('cd "'):
                    return line[4:-2]
        except FileNotFoundError:
            return False
        return False

    def grab_game_data(self):
        """
        Collects Proton's debug log and saves them somewhere. Then, updates the mod list.
        :return:
        """

        # The files are - most of the time - stored in a temporary folder.
        # The common location is /tmp/proton_UNIX-USERNAME .
        # One log file is enough for the mod manager : /tmp/proton_UNIX-USERNAME/run

        # Get the file location
        home_directory = os.path.expanduser("~")
        username = os.path.basename(home_directory)
        # So, the file we want is...
        path_to_run_exe = '/tmp/proton_' + username + '/run'
        # We want to copy it somewhere. ~/v2mm/run might be a good place.
        file_source = open(path_to_run_exe, 'r')
        if not os.path.exists(home_directory + '/.v2mm/'):  # Creates the directory if it does not exist.
            os.mkdir(home_directory + '/.v2mm/')
        file_destination = open(home_directory + '/.v2mm/run', 'w')
        file_destination.write(file_source.read())
        file_source.close()
        file_destination.close()

        # Update the mod listbox once the data are loaded.
        self.mod_list.delete(0, END)
        for mod in self.get_list_of_mods(os.path.expanduser("~") + '/.v2mm/run'):
            self.mod_list.insert(END, mod)


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
