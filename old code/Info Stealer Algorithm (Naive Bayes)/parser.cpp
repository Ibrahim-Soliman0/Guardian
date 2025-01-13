#include <bits/stdc++.h>
#include "csv.hpp"
#define ll long long
#define FastIO (ios_base:: sync_with_stdio(false),cin.tie(NULL), cout.tie(NULL));

using namespace std;

string removeWS(string path)
{
    string token;
    size_t pos = 0;
    while ((pos = path.find(' ')) != string::npos)
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
    while ((pos = path.find('\\')) != string::npos)
    {
        token = path.substr(0, pos);
        tokens.push_back(token);
        path.erase(0, pos + 1);
    }
    tokens.push_back(path);

    return tokens;
}

int main(int argc, char *argv[])
{
    FastIO

    string to_read = (std::string(argv[1]) == "1") ? "one.csv": "two.csv";
    csv::CSVReader reader("C:/Windows/System32/AntiMalware/" + to_read);

    unordered_map<string, vector<string>> process;
    unordered_map<string, unordered_set<string>> process_unique;

    for (auto& line : reader)
    {
        string process_name = line["Process Name"].get(), path = line["Path"].get();
        auto tokens = stringParser(path);
        for(auto& token : tokens)
        {
            token = removeWS(token);
            if (token.empty())
                continue;
            process[process_name].emplace_back(token);
            process_unique[process_name].insert(token);
        }
    }

    string to_output = (std::string(argv[1]) == "1") ? "first.txt": "second.txt";
    ofstream parsedFile("C:/Windows/System32/AntiMalware/" + to_output);

    parsedFile << process.size() << endl;
    for (auto& p : process)
    {
        parsedFile << p.first << " " << p.second.size() << endl;
        for (auto& path : p.second)
            parsedFile << path << endl;
    }

    parsedFile << process_unique.size() << endl;
    for (auto& p : process_unique)
    {
        parsedFile << p.first << " " << p.second.size() << endl;
        for (auto& path : p.second)
            parsedFile << path << endl;
    }

    parsedFile.close();

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
//    freopen(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\test.txt)", "w", stdout);
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
