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

unordered_map<string, ll> normal, malicious;

bool classifyProcess(unordered_set<string>& process_paths, long double& normal_chance, long double& malicious_chance, ll& total_normal, ll& total_malicious)
{
    // n is the probability that the process is normal while m is that its malicious
    long double n = normal_chance, m = malicious_chance;
    for (auto& path : process_paths)
    {
        if (!normal.count(path) || !malicious.count(path))
            continue;
        n *= (long double) normal[path] / total_normal;
        m *= (long double) malicious[path] / total_malicious;
    }

    return n < m;
}

// number of arguments sent, the arguments themselves
// notice that the first argument is always the run command (argv[0]) start from 1
int main(int argc, char *argv[])
{
    auto start = chrono::high_resolution_clock::now();
    FastIO
//    string to_read = (argv[1] == "1") ? "1.csv": "2.csv";
//    csv::CSVReader reader(to_read);
    csv::CSVReader reader("D:/Personal/Graduation Project/Data/one.csv");

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

    string to_output = (argv[1] == "1") ? "first.txt": "second.txt";
    ofstream parsedFile(to_output);

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

    //******************************************* importing data *******************************************************
    ifstream dataFile(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\Data.txt)");

    int n, m;
    dataFile >> n >> m;

    ll total_normal = 0, total_malicious = 0;

    string line;
    ll count;
    for (int i = 0; i < n; ++i)
    {
        dataFile >> line >> count;
        count++;
        normal[line] = count;
        total_normal += count;
        // to make sure there is no data found in the normal and not in the malicious
        // thus it will make the probability of identifying it for either of them ZERO
        malicious[line]++;
        total_malicious++;
//        cout << line << " " << count << endl;
    }

    for (int i = 0; i < m; ++i)
    {
        dataFile >> line >> count;
        count++;
        malicious[line] = count;
        total_malicious += count;
        // to make sure there is no data found in the malicious and not in the normal
        // thus it will make the probability of identifying it for either of them ZERO
        normal[line]++;
        total_normal++;
//        cout << line << " " << count << endl;
    }

    long double n_count, m_count, total_count;
    dataFile >> n_count >> m_count;
    total_count = n_count + m_count;

    dataFile.close();
    //******************************************************************************************************************

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

    ofstream outputFile(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\Output.txt)");

    long double normal_chance = n_count / total_count, malicious_chance = m_count / total_count;

    vector<string> classified_malicious;

    for (auto& p : process_unique)
    {
        if (classifyProcess(p.second, normal_chance, malicious_chance, total_normal, total_malicious))
            classified_malicious.push_back(p.first);
    }

    outputFile << classified_malicious.size() << endl;
    for (auto& i : classified_malicious)
    {
        outputFile << i << " " << process_unique[i].size() << endl;
        for (auto& path : process_unique[i])
        {
            outputFile << path << endl;
        }
    }

    outputFile.close();

//    auto end = chrono::high_resolution_clock::now();
//
//    chrono::duration<double> elapsed = end - start;
//
//    cout << "Time taken: " << elapsed.count() << " seconds\n";

    return 0;
}
