# import subprocess
# import os
# def exeGame():
#     source_path = __file__[0:__file__.find("Game-Assistant")]
    
#     subprocess.run(["powershell", "Start-Process", "python.exe", "-Verb", "RunAs","-ArgumentList", f"'{source_path+"Game-Assistant\\zzzGui.py"}'"])
# if __name__ == "__main__":
#     exeGame()
import subprocess
import os
import sys

def exeGame():
    try:
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 找到 Game-Assistant 目录
        game_assistant_dir = os.path.join(current_dir.split("Game-Assistant")[0], "Game-Assistant")
        # 目标脚本路径
        target_script = os.path.join(game_assistant_dir, "zzzGui.py")

        # 使用当前 Python 解释器
        python_exe = sys.executable

        # 静默启动（无窗口）
        subprocess.Popen(
            [python_exe, target_script],
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=False
        )

    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    exeGame()