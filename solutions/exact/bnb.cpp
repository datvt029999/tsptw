#include <climits>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int n, current_time = 0, best_time = INT_MAX, min_time = INT_MAX;
vector<int> e(1001), l(1001), d(1001), s(1001), best_s(1001), arrivals(1001), best_arrivals(1001);
vector<vector<int>> t(1001, vector<int>(1001));
vector<bool> visited(1001, false);

void generate_routes(int k);

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // Set to true to add additional text explaining the output, false otherwise
    bool print = true;

    // Comment out the following line to read from the standard input instead of the input file
    freopen(("../../input/" + string(argv[1]) + ".txt").c_str(), "r", stdin);

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
    s[0] = arrivals[0] = 0;
    generate_routes(1);

    if (print)
    {
        cout << "Problem size   : ";
    }
    cout << n << endl;

    if (print)
    {
        cout << "Best solution  : ";
    }

    for (int i = 1; i <= n; i++)
    {
        cout << best_s[i] << " ";
    }

    if (print)
    {
        cout << "\nBest total time: " << best_time << "\nArrivals       :";

        for (int i = 1; i <= n; i++)
        {
            cout << " " << best_arrivals[i];
        }
    }
    cout << endl;
    return 0;
}

void generate_routes(int k)
{
    for (int i = 1, time_finishing_delivering = arrivals[k - 1] + d[s[k - 1]]; i <= n; i++)
    {
        if (!visited[i])
        {
            arrivals[k] = max(time_finishing_delivering + t[s[k - 1]][i], e[i]);

            if (arrivals[k] > l[i])
            {
                continue;
            }
            s[k] = i;
            visited[i] = true;
            current_time += t[s[k - 1]][i];

            if (k == n)
            {
                int total_time = current_time + t[s[k]][0];

                if (total_time < best_time)
                {
                    best_time = total_time;

                    for (int j = 1; j <= n; j++)
                    {
                        best_s[j] = s[j];
                        best_arrivals[j] = arrivals[j];
                    }
                }
            }
            else if (current_time + (n - k + 1) * min_time < best_time)
            {
                generate_routes(k + 1);
            }
            visited[i] = false;
            current_time -= t[s[k - 1]][i];
        }
    }
    return;
}