#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std;

int main(void)
{
    // Size of the problem (N)
    int size = 5;

    // Version of the input data (1 - 6)
    int version = 1;

    // Set to true to add additional text explaining the output, false otherwise
    bool print = true;

    set<int> sizes = {5, 10, 100, 200, 300, 500, 600, 700, 900, 1000};

    if (sizes.find(size) == sizes.end())
    {
        cout << "Invalid problem size. Please choose from the following:";

        for (int customers : sizes)
        {
            cout << " " << customers;
        }
        cout << endl;
        return 1;
    }
    else if (version < 1 || version > 6)
    {
        cout << "Invalid input version. Please choose a version from 1 to 6." << endl;
        return 1;
    }
    freopen(("../../input/" + to_string(size) + "/" + to_string(version) + ".txt").c_str(), "r", stdin);
    int n, previous_point = 0, total_time = 0;
    cin >> n;
    vector<int> e(n + 1), l(n + 1), d(n + 1), previous_times(n + 1);

    for (int i = 1; i <= n; i++)
    {
        cin >> e[i] >> l[i] >> d[i];
    }
    vector<vector<int>> t(n + 1, vector<int>(n + 1));

    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= n; j++)
        {
            cin >> t[i][j];
        }
    }

    if (print)
    {
        cout << "Size   : " << size << "\nVersion: " << version << "\n    Number of customers      : ";
    }
    cout << n << endl;

    if (print)
    {
        cout << "    Solution                 : ";
    }
    vector<bool> visited(n + 1, false);
    previous_times[0] = 0;

    for (int i = 1; i <= n; i++)
    {
        int best_point;

        for (int j = 1, best_deadline = INT_MAX, best_distance = INT_MAX; j <= n; j++)
        {
            if (!visited[j] && previous_times[i - 1] + t[previous_point][j] <= l[j] && (l[j] < best_deadline || (l[j] == best_deadline && t[previous_point][j] < best_distance)))
            {
                best_point = j;
                best_deadline = l[j];
                best_distance = t[previous_point][j];
            }
        }
        cout << best_point << " ";
        visited[best_point] = true;
        total_time += t[previous_point][best_point];
        previous_times[i] = max(previous_times[i - 1] + t[previous_point][best_point], e[best_point]) + d[best_point];
        previous_point = best_point;
    }

    if (print)
    {
        cout << "\n    Time                     : " << total_time << "\n    Time finishing delivering:";

        for (int i = 1; i <= n; i++)
        {
            cout << " " << previous_times[i];
        }
    }
    cout << endl;
    return 0;
}