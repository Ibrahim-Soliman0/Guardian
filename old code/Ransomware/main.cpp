#include <iostream>
#include <filesystem>

using namespace std;
int main()
{
    string test_path = "C:\\Users\\moham\\AppData\\Local\\Packages\\Microsoft.Windows.Search_cw5n1h2txyewy\\AC\\INetCache\\NQZM54VD\\BB18qTPD[1].gif.WNCRYT";

    filesystem::path filePath = test_path;

    // Print the file extension using the extension() method
    // of the path object.
    cout << "File extension is: " << filePath.extension()
         << endl;

    return 0;
}
