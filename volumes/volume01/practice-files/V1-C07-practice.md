# Practice Guide: Chapter 7

## Objective
To build the critical muscle memory required to survive in `vim` and confidently navigate its three modes.

## Assignment 1: The Nano Warm-up
1. Open your terminal.
2. Type `nano my_first_file.txt`.
3. Type the following sentence: "Nano is easy, but Vim is inevitable."
4. Press `Ctrl + O`, then `Enter` to save.
5. Press `Ctrl + X` to exit.
6. Verify the file was saved by running `cat my_first_file.txt`.

## Assignment 2: Surviving Vim (The Save)
1. Type `vim my_second_file.txt`. You are now in **Normal Mode**.
2. Try typing "Hello". *Notice how it doesn't work correctly or does weird things?*
3. Press `Esc` just to be safe.
4. Press the letter `i`. Look at the bottom of the screen to verify you see `-- INSERT --`.
5. Now, type: "I am officially a Vim user."
6. Press the `Esc` key to return to **Normal Mode**. (The `-- INSERT --` text will disappear).
7. Type `:wq` and press `Enter` to write the file and quit.
8. Verify it worked by running `cat my_second_file.txt`.

## Assignment 3: Surviving Vim (The Panic Quit)
Sometimes you open a critical configuration file and accidentally delete a line. The safest thing to do is force-quit without saving, so you don't break the server.

1. Type `vim my_second_file.txt`.
2. Press `i` to enter Insert Mode.
3. Mash your keyboard to create a bunch of garbage text (e.g., `asdfkjasdf;laskdjf`).
4. **DO NOT SAVE.**
5. Press `Esc` to return to Normal Mode.
6. Type `:q!` and press `Enter`.
7. Run `cat my_second_file.txt`. 

*Notice how your garbage text is gone? The file remains perfectly intact because you forced a quit without writing.*

## Success Criteria
You have successfully completed this practice if you can effortlessly transition between Normal Mode (`Esc`), Insert Mode (`i`), and Command Mode (`:`), and if you understand the critical difference between `:wq` and `:q!`.
