# Maze to the Super Bowl

By Abhinav Penaganti

This is a command line maze about NFL teams and stadiums. You will
move through four divisions, find one hidden folder, and finish in
the locker room where the last password is waiting.

## How to solve it

1. Unzip the maze folder if you have not already.
2. `cd` into the maze folder.
3. Read the first file to start:
   - Mac/Linux/WSL: `cat kickoff.md`
   - PowerShell: `Get-Content kickoff.md`
4. Each file tells you what stadium you are at and which folder to
   `cd` into next. Keep reading and moving until you reach the end.
5. One stop is hidden. If a file tells you to look for something
   hidden, use `ls -a` (Mac/Linux/WSL) or `Get-ChildItem -Force`
   (PowerShell) to find it.
6. Windows users: hidden folders do not stay hidden on Windows like
   they do on Mac and Linux. Run `.\hide-dotfiles.ps1` from this
   folder first if you want the hidden folder to act hidden.
7. You are done when you reach `overtime/super-bowl-locker.md` and
   find the password.

## Commands you will need

- `cd <folder>` — move into a folder
- `cd ..` — move up one folder
- `ls` / `Get-Content` — list files
- `ls -a` / `Get-ChildItem -Force` — list files, including hidden ones
- `cat <file>` / `Get-Content <file>` — read a file
