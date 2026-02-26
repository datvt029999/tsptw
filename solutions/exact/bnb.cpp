#include <climits>
#include <iostream>
#include <set>
#include <string>
#include <vector>

using namespace std;

int n, current_time = 0, best_time = INT_MAX, min_time = INT_MAX;
vector<int> e(1001), l(1001), d(1001), s(1001), best_s(1001), times(1001), best_times(1001);
vector<vector<int>> t(1001, vector<int>(1001));
vector<bool> visited(1001, false);

void generate_routes(int k);

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
    cin >> n;

    for (int i = 1; i <= n; i++)
    {
        cin >> e[i] >> l[i] >> d[i];
    }

    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= n; j++)
        {
            cin >> t[i][j];

            if (i != j)
            {
                min_time = min(min_time, t[i][j]);
            }
        }
    }
    s[0] = times[0] = 0;
    generate_routes(1);

    if (print)
    {
        cout << "Size   : " << size << "\nVersion: " << version << "\n    Number of customers      : ";
    }
    cout << n << endl;

    if (print)
    {
        cout << "    Best solution            : ";
    }

    for (int i = 1; i <= n; i++)
    {
        cout << best_s[i] << " ";
    }

    if (print)
    {
        cout << "\n    Best time                : " << best_time << "\n    Time finishing delivering: ";

        for (int i = 1; i <= n; i++)
        {
            cout << best_times[i] << " ";
        }
    }
    cout << endl;
    return 0;
}

void generate_routes(int k)
{
    for (int i = 1; i <= n; i++)
    {
        if (!visited[i])
        {
            int arrival = max(times[k - 1] + t[s[k - 1]][i], e[i]);

            if (arrival > l[i])
            {
                continue;
            }
            s[k] = i;
            visited[i] = true;
            current_time += t[s[k - 1]][i];
            times[k] = arrival + d[i];

            if (k < n)
            {
                if (current_time + (n - k) * min_time < best_time)
                {
                    generate_routes(k + 1);
                }
            }
            else if (current_time < best_time)
            {
                best_time = current_time;

                for (int j = 1; j <= n; j++)
                {
                    best_s[j] = s[j];
                    best_times[j] = times[j];
                }
            }
            visited[i] = false;
            current_time -= t[s[k - 1]][i];
        }
    }
    return;
}