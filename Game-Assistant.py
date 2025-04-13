import subprocess
import os
def exeGame():
    source_path = __file__[0:__file__.find("Game-Assistant")]
    subprocess.run(["powershell", "Start-Process", "python.exe", "-Verb", "RunAs","-ArgumentList", f"'{source_path+"Game-Assistant\\zzzGui.py"}'"])
if __name__ == "__main__":
    exeGame()