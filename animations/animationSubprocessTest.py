import sys
import signal
import subprocess
# import os

if __name__ == '__main__':
    while True:
        print('\n\nCHOOSE ANIMATION')
        print('1. Rainbow Spin')
        print('2. Blink Colors')
        print('3. Blink Randon Colors')
        print('4. EXIT')

        choice = int(input())
        animation = "none.py"

        if choice == 1:
            animation = "rainbowSpin.py"
        elif choice == 2:
            animation = "blinkColors.py"
        elif choice == 3:
            animation = "blinkRandom.py"
        else:
            exit(0)

        animProcess = subprocess.Popen([
            "python3", 
            "./"+animation, 
            "127.0.0.1",
            "300"
            ], stdout=subprocess.PIPE)


        if animProcess.poll() is None:
            print("Process is running")

        input("Animation running...\nPress ENTER to stop!")

        if animProcess.poll() is None:
            print("Process is running")
            animProcess.kill()
        else:
            print("Process has finished running")
            animProcess.kill()

