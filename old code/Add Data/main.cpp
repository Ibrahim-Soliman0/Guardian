#include <bits/stdc++.h>

#define ll long long
#define FastIO (ios_base:: sync_with_stdio(false), cin.tie(NULL), cout.tie(NULL));

using namespace std;

int main()
{
    FastIO
    unordered_map<string, ll> normal_data_lines, malicious_data_lines;
    unordered_set<string> normal_process_name, malicious_process_name;

    ifstream testFile(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\test.txt)");

    ll n, m, n_count, m_count;
    testFile >> n >> m;
    string line;
    ll count;
    for (int i = 0; i < n; ++i)
    {
        testFile >> line >> count;
        normal_data_lines[line] += count;
    }

    for (int i = 0; i < m; ++i)
    {
        testFile >> line >> count;
        malicious_data_lines[line] += count;
    }

    testFile >> n_count >> m_count;

    for (int i = 0; i < n_count; ++i)
    {
        testFile >> line;
        normal_process_name.insert(line);
    }

    for (int i = 0; i < m_count; ++i)
    {
        testFile >> line;
        malicious_process_name.insert(line);
    }

    testFile.close();

    ifstream dataFile(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\Data.txt)");

    dataFile >> n >> m;
    for (int i = 0; i < n; ++i)
    {
        dataFile >> line >> count;
        normal_data_lines[line] += count;
    }

    for (int i = 0; i < m; ++i)
    {
        dataFile >> line >> count;
        malicious_data_lines[line] += count;
    }

    dataFile >> n_count >> m_count;

    for (int i = 0; i < n_count; ++i)
    {
        dataFile >> line;
        normal_process_name.insert(line);
    }

    for (int i = 0; i < m_count; ++i)
    {
        dataFile >> line;
        malicious_process_name.insert(line);
    }

    dataFile.close();

    ofstream dataFile_output(R"(D:\Personal\Graduation Project\Source Code\Info Stealer Algorithm (Naive Bayes)\Data.txt)");

    dataFile_output << normal_data_lines.size() << " " << malicious_data_lines.size() << endl;

    for (auto& p : normal_data_lines)
        dataFile_output << p.first << " " << p.second << endl;

    for (auto& p : malicious_data_lines)
        dataFile_output << p.first << " " << p.second << endl;

    dataFile_output << normal_process_name.size() << " " << malicious_process_name.size() << endl;

    for (auto& name : normal_process_name)
        dataFile_output << name << endl;

    for (auto& name : malicious_process_name)
        dataFile_output << name << endl;

    dataFile_output.close();

    return 0;
}
