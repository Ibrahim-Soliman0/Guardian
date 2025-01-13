#include <bits/stdc++.h>
#define ll long long
#define FastIO (ios_base:: sync_with_stdio(false),cin.tie(NULL), cout.tie(NULL));

using namespace std;

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

int main()
{
    FastIO

    unordered_map<string, vector<string>> process;
    unordered_map<string, unordered_set<string>> process_unique;

    ifstream firstFile(R"(C:\Windows\System32\AntiMalware\first.txt)");

    int p_size;
    firstFile >> p_size;

    for (int i = 0; i < p_size; ++i)
    {
        int path_count;
        string process_name;
        firstFile >> process_name >> path_count;
        for (int j = 0; j < path_count; ++j)
        {
            string path;
            firstFile >> path;
            process[process_name].emplace_back(path);
            process_unique[process_name].insert(path);
        }
    }

    ifstream secondFile(R"(C:\Windows\System32\AntiMalware\second.txt)");

    secondFile >> p_size;

    for (int i = 0; i < p_size; ++i)
    {
        int path_count;
        string process_name;
        secondFile >> process_name >> path_count;
        for (int j = 0; j < path_count; ++j)
        {
            string path;
            secondFile >> path;
            process[process_name].emplace_back(path);
            process_unique[process_name].insert(path);
        }
    }

    //******************************************* importing data *******************************************************
    ifstream dataFile(R"(C:\Windows\System32\AntiMalware\Data.txt)");

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

    ofstream outputFile(R"(C:\Windows\System32\AntiMalware\output.txt)");

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

    return 0;
}
