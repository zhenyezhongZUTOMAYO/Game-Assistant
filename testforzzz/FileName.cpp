#include <windows.h>
#include <shellapi.h>
#include <iostream>

int main() {
    // ��·���滻Ϊ���������
    LPCSTR pythonCommand = "python D:\\Git\\Game-Assistant\\openzzz\\main.py";

    // ʹ�� ShellExecute �Թ���ԱȨ����������
    HINSTANCE result = ShellExecuteA(
        NULL,                   // �����ھ�����޴��ڣ�
        "runas",                // �������ԱȨ��
        "cmd.exe",              // Ҫִ�еĳ���
        ("/c " + std::string(pythonCommand)).c_str(), // ����
        NULL,                   // ����Ŀ¼��Ĭ�ϣ�
        SW_HIDE                 // ����״̬�����أ�
    );

    // ���ִ�н��
    if ((int)result <= 32) {
        std::cerr << "Failed to run command as administrator! Error code: " << (int)result << std::endl;
        return 1;
    }

    std::cout << "Command executed successfully!" << std::endl;
    return 0;
}