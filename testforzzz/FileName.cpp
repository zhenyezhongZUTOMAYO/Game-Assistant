#include <windows.h>
#include <shellapi.h>
#include <iostream>

int main() {
    // 将路径替换为程序主入口
    LPCSTR pythonCommand = "python D:\\Git\\Game-Assistant\\openzzz\\main.py";

    // 使用 ShellExecute 以管理员权限运行命令
    HINSTANCE result = ShellExecuteA(
        NULL,                   // 父窗口句柄（无窗口）
        "runas",                // 请求管理员权限
        "cmd.exe",              // 要执行的程序
        ("/c " + std::string(pythonCommand)).c_str(), // 参数
        NULL,                   // 工作目录（默认）
        SW_HIDE                 // 窗口状态（隐藏）
    );

    // 检查执行结果
    if ((int)result <= 32) {
        std::cerr << "Failed to run command as administrator! Error code: " << (int)result << std::endl;
        return 1;
    }

    std::cout << "Command executed successfully!" << std::endl;
    return 0;
}