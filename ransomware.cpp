#include <bits/stdc++.h>

#define npos string::npos
#define FastIO (ios_base:: sync_with_stdio(false),cin.tie(NULL), cout.tie(NULL));

using namespace std;

unordered_map<string, bool> normalextensions;

bool check_extension(string path)
{
    if (path.empty() || path.find('.') == npos)
        return false;

    size_t front = path.find('.'), back = path.rfind('.');
    if (front == back)
        return false;

    string extension = path.substr(back+1);
    transform(extension.begin(), extension.end(), extension.begin(), ::tolower);
    if (!normalextensions[extension])
        return true;

    return false;
}

int main()
{
    FastIO

    ifstream normalextensionsfile(R"(C:\Windows\System32\AntiMalware\normalextensions.txt)");
//    ifstream normalextensionsfile("D:/Personal/Graduation Project/Source Code/Ransomware/normalextensions.txt");

    string extension;
    while (normalextensionsfile >> extension)
        normalextensions[extension] = true;

    normalextensionsfile.close();

    ifstream fullpaths(R"(C:\Windows\System32\AntiMalware\fullpaths.txt)");
//    ifstream fullpaths("D:/Personal/Graduation Project/Source Code/Ransomware/fullpaths.txt");

    unordered_map<string, int> process;
    vector<string> ransom;

    int process_count, path_count;
    string process_name;

    fullpaths >> process_count;
    for (int i = 0; i < process_count; ++i)
    {
        fullpaths >> process_name >> path_count;
        string path;
        getline(fullpaths, path);
        bool skip = false;
        for (int j = 0; j < path_count; ++j)
        {
            getline(fullpaths, path);
            if (skip)
                continue;
            size_t pos = path.find_last_of('\\') + 1;
            process[process_name] += check_extension(path.substr(pos));
            if (process[process_name] >= 10)
            {
                ransom.emplace_back(process_name);
                skip = true;
            }
        }
    }

        ofstream outputFile(R"(C:\Windows\System32\AntiMalware\ransom.txt)");
//    ofstream outputFile("D:/Personal/Graduation Project/Source Code/Ransomware/output.txt");

    outputFile << ransom.size() << endl;

    for (auto& p : ransom)
        outputFile << p << endl;

    outputFile.close();

    return 0;
}
