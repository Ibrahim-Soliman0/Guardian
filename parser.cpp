#include <bits/stdc++.h>

#define ll long long
#define npos string::npos
#define FastIO (ios_base:: sync_with_stdio(false),cin.tie(NULL), cout.tie(NULL));

using namespace std;

string removeWS(string path)
{
    string token;
    size_t pos = 0;
    while ((pos = path.find(' ')) != npos)
    {
        token += path.substr(0, pos);
        path.erase(0, pos + 1);
    }
    if (!path.empty())
        token += path;
    if (token.empty())
        token = path;

    return token;
}

vector<string> stringParser(string path)
{
    vector<string> tokens;
    size_t pos = 0;
    string token;
    while ((pos = path.find('\\')) != npos)
    {
        token = path.substr(0, pos);
        tokens.push_back(token);
        path.erase(0, pos + 1);
    }
    tokens.push_back(path);

    return tokens;
}

string cleanPath(string path)
{
    if (path.find(':') == npos)
        return  "";

    size_t find = path.find(':');
    path.replace(0, find-1, "");
    return path;
}

int main()
{
    FastIO

    ifstream input("C:/Windows/System32/AntiMalware/input.txt");
//    ifstream input("D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/input.txt");

    unordered_map<string, unordered_set<string>> process, process_read_copy, process_fullpaths;
    
    string line;
    while (getline(input, line))
    {
        string process_name, path;

        size_t find = line.find(">>");
        path = line.substr(find + 3);
        process_name = line.substr(0, find - 1);

        size_t is_read = path.find(' ');
        if (is_read != npos)
        {
            string before_space = path.substr(0, is_read), after_space = path.substr(is_read);
            string clean_path = cleanPath(after_space);
            if (clean_path.empty())
                continue;
            if (before_space == "(ReadFile)" || before_space == "(CopyFile)" || before_space == "(MakeFile)")
                process_read_copy[process_name].insert(clean_path);

            if (!clean_path.empty())
                process_fullpaths[process_name].insert(clean_path);
            clean_path.erase(0, 2);

            auto tokens= stringParser(clean_path);
            for(string& token : tokens)
            {
                token = removeWS(token);
                if (token.empty())
                    continue;
                process[process_name].insert(token);
            }
        }
        else
        {
            string clean_path = cleanPath(path);
            if (!clean_path.empty())
                process_fullpaths[process_name].insert(clean_path);
            clean_path.erase(0, 2);
            if (clean_path.empty())
                continue;

            auto tokens= stringParser(clean_path);
            for(string& token : tokens)
            {
                token = removeWS(token);
                if (token.empty())
                    continue;
                process[process_name].insert(token);
            }
        }
    }

    input.close();

    ofstream parsedFile("C:/Windows/System32/AntiMalware/parsedfile.txt");
//    ofstream parsedFile("D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/parsedfile.txt");

    parsedFile << process.size() << endl;
    for (auto& p : process)
    {
        parsedFile << p.first << " " << p.second.size() << endl;
        for (const string& path : p.second)
            parsedFile << path << endl;
    }

    parsedFile << process_read_copy.size() << endl;
    for (auto& p : process_read_copy)
    {
        parsedFile << p.first << " " << p.second.size() << endl;
        for (const string& path : p.second)
            parsedFile << path << endl;
    }

    parsedFile.close();

    ofstream fullpaths("C:/Windows/System32/AntiMalware/fullpaths.txt");
//    ofstream fullpaths("D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/fullpaths.txt");

    fullpaths << process_fullpaths.size() << endl;
    for (auto& p : process_fullpaths)
    {
        fullpaths << p.first << " " << p.second.size() << endl;
        for (const string& path : p.second)
            fullpaths << path << endl;
    }

    fullpaths.close();

    //******************************************* making the data file *************************************************

//    vector<string> malicious_process_name, normal_process_name;
//    for (auto& p : process)
//    {
//        if (p.first == "RegSvcs.exe")
//        {
//            malicious_process_name.push_back(p.first);
//            for (auto& item : p.second)
//                    malicious[item]++;
//        }
//        else
//        {
//            normal_process_name.push_back(p.first);
//            for (auto& item : p.second)
//                normal[item]++;
//        }
//    }
//
//    freopen(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\line.txt)", "w", stdout);
//
//    cout << normal.size() << " " << malicious.size() << endl;
//
//    for (auto& item : normal)
//        cout << item.first << ' ' << item.second << endl;
//
//    for (auto& item : malicious)
//        cout << item.first << ' ' << item.second << endl;
//
//    cout << normal_process_name.size() << " " << malicious_process_name.size() << endl;
//
//    for (auto& name : normal_process_name)
//        cout << name << endl;
//
//    for (auto& name : malicious_process_name)
//        cout << name << endl;

    //******************************************************************************************************************

    return 0;
}
