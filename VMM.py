# -*- coding:Utf-8 -*-

import subprocess
from tkinter import *
from tkinter.ttk import *
import os.path
import stat
from shutil import copyfile


def launch_victoria2():
    subprocess.run('steam steam://rungameid/42960 &', shell=True, check=True, executable='/bin/sh')


class InterfaceV2MM(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('Victoria 2 Mod Manager (linux)')
        self.manager_data_directory = os.path.expanduser("~") + '/.v2mm/'

        # The interface is made up of three main frames. One containing two sub-frames, one for logs and one for the
        # leave button.

        # MAIN FRAME
        main_frame = Frame(self.root)
        main_frame.grid(row=0, column=0)
        # The main frame is composed ow two sub-frames. The left one for actions and buttons dans the right one for
        # data shown in a table.

        #   LEFT SUB-FRAME
        left_sub_frame = Notebook(main_frame)
        # The left sub_frame is made up of two tabs. One for installation and one for usage.
        tab_installation = Frame(left_sub_frame)
        left_sub_frame.add(tab_installation, text='Installation')

        #       STEAM LAUNCHER
        steam_launch_label = Label(tab_installation, text="1° First, launch steam.")
        steam_launch_label.grid(column=0, row=2, sticky='W')
        steam_launcher_button = Button(
            tab_installation,
            text="Launch Steam",
            command=self.launch_steam,
            width=15
        )
        steam_launcher_button.grid(column=0, row=3, pady=(0, 0), sticky='W')
        #       ADD LAUNCH OPTION
        file_label = Label(
            tab_installation,
            text="2° Now add the text below as a launch option (you can remove it later).")
        file_label.grid(column=0, row=4, sticky='W')
        launch_option = Entry(tab_installation, width=10)
        launch_option.grid(row=5, sticky='ew')
        launch_option.insert(0, 'PROTON_DUMP_DEBUG_COMMANDS=1 %command%')
        #       CHECK PROTON VERSION
        proton_version_label = Label(
            tab_installation,
            text="3° At the same place, check that you force\nthe SteamPlay Compatibility and choose the version"
                 " « PROTON 4.11-13 ».")
        proton_version_label.grid(column=0, row=6, sticky='W')
        #       LAUNCH VICTORIA 2 ONCE
        launch_victoria = Label(tab_installation, text="4° Launch the game once.")
        launch_victoria.grid(column=0, row=7, sticky='W')
        steam_launcher_button = Button(tab_installation, text="Launch Victoria 2", command=launch_victoria2)
        steam_launcher_button.grid(column=0, row=8, pady=(0, 0), sticky='W')
        #       COLLECT YOUR DATA
        grab_data = Label(tab_installation, text="5° Collect your game data")
        grab_data.grid(column=0, row=9, sticky='W')
        grab_data_button = Button(tab_installation, text="Save your data", command=self.grab_game_data)
        grab_data_button.grid(column=0, row=10, pady=(0, 0), sticky='W')
        #       SWAP YOUR EXECUTABLES
        steam_launch_label = Label(
            tab_installation,
            text="6° Then, modify the executable we want to use."
        )
        steam_launch_label.grid(column=0, row=11, sticky='W')
        steam_launcher_button = Button(
            tab_installation,
            text="Swap the game executable",
            command=self.swap_executable)
        steam_launcher_button.grid(column=0, row=12, pady=(0, 0), sticky='W')

        tab_usage = Frame(left_sub_frame)
        left_sub_frame.add(tab_usage, text='Usage')

        # GAME FRAME
        #       LIST OF MODS FOUNT
        mod_list_label = Label(tab_usage, text="Mods fount in your steam files.")
        mod_list_label.grid(column=0, row=1, sticky='W')
        self.mod_list = Listbox(tab_usage)
        self.mod_list.grid(column=0, row=2, sticky='W')
        for mod in self.get_list_of_mods(self.manager_data_directory + 'run'):
            self.mod_list.insert(END, mod)
        #       LAUNCH MOD BUTTON
        Button(tab_usage, text='Launch selected mod', command=self.launch_game_with_selected_mod).grid(column=1, row=2)

        left_sub_frame.grid(row=1, column=0)

        #   RIGHT SUB-FRAME
        right_sub_frame = Frame(main_frame)
        right_sub_frame.grid(row=1, column=1)
        data = Treeview(right_sub_frame, columns=2, show=["headings"])
        data['columns'] = ('Data', 'Value')
        data.heading('#1', text='Data')
        data.heading('#2', text='Value')
        data.column("Data", minwidth=150)
        data.column("Value", minwidth=800)
        data.insert('', '1', values=('V2MM directory', self.manager_data_directory))
        data.insert('', '1', values=('Game directory', self.extract_game_directory_from_proton_runfile(self.manager_data_directory + 'run')))
        data.grid(column=1, row=4)



        # LOGS FRAME
        self.log_frame = Text(self.root, height=10, width=100)
        self.log_frame.grid(row=2, column=0)
        self.log_frame.insert(END, "Logs :")


        # END BUTTON FRAME
        end_button_frame = Frame(self.root)
        end_button_frame.grid(row=3, column=0)
        Button(end_button_frame, text='Leave', command=self.root.quit).grid(row=0, column=0)

        if self.is_game_already_installed():
            left_sub_frame.select(tab_usage)

    def get_game_directory(self):
        return ''


    def is_game_already_installed(self):
        """
        How do we check if the mod manager has already been installed ? Well, we just check if some files are already
        present in the manager directory.
        :return:
        """
        if os.path.exists(self.manager_data_directory):
            if os.path.exists(self.manager_data_directory + 'mod_launcher'):
                return True
        return False

    def launch_steam(self):
        """
        Just launches steam in a sub process.
        TODO : Find a way to get the command output and display it in the logs.
        :return:
        """
        subprocess.run('steam &',
                       shell=True,
                       check=True,
                       executable='/bin/sh'
                       )

    def swap_executable(self):
        """
        Te game usually uses victoria2.exe while we want it to use v2game.exe.
        The solution is to :
        - rename victoria2.exe to _victoria2.exe
        - copy v2game.exe to victoria2.exe
        :return:
        """
        game_folder = self.extract_game_directory_from_proton_runfile(self.manager_data_directory + 'run')
        os.rename(game_folder + '/victoria2.exe', game_folder + '/_victoria2.exe')  # todo try and logs
        copyfile(game_folder + '/v2game.exe', game_folder + '/victoria2.exe')  # todo try and logs

    def launch_game_with_selected_mod(self):
        """
        Launches the game with the appropriate mod. Made with the following steps :
        1° create a temporary file (erase any existing file with the same name)
        2° copy the content of our run file in the new one with a modification
        3° execute this new file within a sub-shell
        :return:
        """
        # Getting the original content.
        source_file_opener = open(self.manager_data_directory + 'run', 'r')
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
        destination_file = self.manager_data_directory + 'mod_launcher'
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
        game_directory = self.extract_game_directory_from_proton_runfile(runfile_location) # todo check
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
            # todo logs
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
        # todo check if path_to_run_exe exists -> logs
        file_source = open(path_to_run_exe, 'r')
        if not os.path.exists(self.manager_data_directory):  # Creates the directory if it does not exist. todo -> logs
            os.mkdir(home_directory + '/.v2mm/')
        file_destination = open(home_directory + '/.v2mm/run', 'w') # todo try and logs
        file_destination.write(file_source.read()) # todo try and logs
        file_source.close()
        file_destination.close()

        # Update the mod listbox once the data are loaded.
        self.mod_list.delete(0, END)
        for mod in self.get_list_of_mods(self.manager_data_directory + 'run'):
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
