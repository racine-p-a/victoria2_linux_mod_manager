# victoria2_linux_mod_manager

Current version `0.1`.

Works only for the steam version (using steam PROTON). It is only a simple file that I would like to keep
as light and simple as possible.

Issues/bug reports are welcome.

## Installation

Just download/clone the python file and place it on your computer wherever you want and then launch it.

```bash
python3 VMM.py
```

Now, just follow the steps explained in the upper half of the (ugly) interface.
- launch steam.
- add a launch option to the game (`PROTON_DUMP_DEBUG_COMMANDS=1 %command%`).
- force the use of a specific Steam Play compatibility : `Proton 4.11-13`.
- in some cases, you might have to rename the executable `v2game.exe` to `victoria2.exe`.
- launch victoria 2.
- one you are on the game main menu, quit the game.
- click on ___Save your data___ in the mod manager interface, this should detect all the mods you already have
installed.
 


## Usage

Select the mod you want in the mod list and click the button ___Launch selected mod___.

### Install more mods

Download the mod you want on your preferred website ([list on wiki](https://vic2.paradoxwikis.com/List_of_mods),
[Paradox forum](https://forum.paradoxplaza.com/forum/forums/victoria-2-user-modifications.543/),
[moddb](https://www.moddb.com/games/victoria-2-heart-of-darkness/mods), etc...).

Extract and place the files in the mod directory of your game (should look like something like
`/.../SteamLibrary/steamapps/common/Victoria 2/mod`). 

## TODOs

Make the interface less ugly.
Make it more error resilient.

Make it configurable.
- where to store the run file

Place logs in interface
- failure to find the proton run file and/or directory