#include <bits/stdc++.h>
#define ll long long
#define FastIO (ios_base:: sync_with_stdio(false),cin.tie(NULL), cout.tie(NULL));

using namespace std;

unordered_map<string, ll> normal, malicious;
unordered_map<string, bool> weights;

bool classifyProcess(unordered_set<string>& process_paths, long double& normal_chance, long double& malicious_chance, ll& total_normal, ll& total_malicious)
{
    // n is the probability that the process is normal while m is that its malicious
    long double n = normal_chance, m = malicious_chance;
    for (const string& path : process_paths)
    {
        if (!normal.count(path) || !malicious.count(path))
            continue;
        string pth = path;
        transform(pth.begin(), pth.end(), pth.begin(), ::tolower);
        if (weights[pth])
            m *= 1000;
        m *= (long double) malicious[path] / total_malicious;
        n *= (long double) normal[path] / total_normal;
    }

    return n < m;
}

int main()
{
    FastIO

    unordered_map<string, unordered_set<string>> process_unique;
    unordered_map<string, vector<string>> process_read_copy, process_fullpaths;
    unordered_map<string, bool> do_process;

    ifstream parsedfile(R"(C:\Windows\System32\AntiMalware\parsedfile.txt)");
//    ifstream parsedfile("D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/parsedfile.txt");

    int path_size, path_count;
    string process_name;
    parsedfile >> path_size;

    for (int i = 0; i < path_size; ++i)
    {
        parsedfile >> process_name >> path_count;
        string path;
        for (int j = 0; j < path_count; ++j)
        {
            parsedfile >> path;
            process_unique[process_name].insert(path);
        }
    }

    parsedfile >> path_size;

    for (int i = 0; i < path_size; ++i)
    {
        parsedfile >> process_name >> path_count;
        do_process[process_name] = path_count >= 5;
        string path;
        getline(parsedfile, path);
        for (int j = 0; j < path_count; ++j)
        {
            getline(parsedfile, path);
            process_read_copy[process_name].emplace_back(path);
        }

    }

    parsedfile.close();

    //******************************************* importing data *******************************************************
    ifstream dataFile(R"(C:\Windows\System32\AntiMalware\Data.txt)");
//    ifstream dataFile(R"(D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/Data.txt)");

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

    ifstream weightsFile(R"(C:\Windows\System32\AntiMalware\weights.txt)");
//    ifstream weightsFile(R"(D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/weights.txt)");

    string weight;
    while (weightsFile >> weight)
        weights[weight] = true;

    weightsFile.close();

    //******************************************************************************************************************

    ofstream outputFile(R"(C:\Windows\System32\AntiMalware\output.txt)");
//    ofstream outputFile(R"(D:/Personal/Graduation Project/Source Code/Info Stealer Algorithm (Naive Bayes)/output.txt)");

    long double normal_chance = n_count / total_count, malicious_chance = m_count / total_count;

    vector<string> classified_malicious;

    for (auto& p : process_unique)
    {
        if (do_process[p.first])
        {
            if (classifyProcess(p.second, normal_chance, malicious_chance, total_normal, total_malicious))
                classified_malicious.push_back(p.first);
        }
    }

    outputFile << classified_malicious.size() << endl;
    for (string& m : classified_malicious)
    {
        outputFile << m << " " << process_read_copy[m].size() << endl;
        for (string& path : process_read_copy[m])
            outputFile << path << endl;
    }

    outputFile.close();

    return 0;
}
