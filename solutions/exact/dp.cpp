#include <algorithm>
#include <climits>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    // Set to true to add additional text explaining the output, false otherwise
    bool print = true;

    // Comment out the following line to read from the standard input instead of the input file
    freopen(("../../input/" + to_string(atoi(argv[1])) + ".txt").c_str(), "r", stdin);

    int n;
    cin >> n;
    vector<int> e(n + 1), l(n + 1), d(n + 1), route, best_finishing_times;
    int masks = 1 << n, final_mask = masks - 1, best_time = INT_MAX, last_point, current_time = 0, previous_point = 0;
    vector<vector<int>> t(n + 1, vector<int>(n + 1)), best_times(masks, vector<int>(n + 1, INT_MAX)), best_starting_times(masks, vector<int>(n + 1, INT_MAX)), parents(masks, vector<int>(n + 1, -1));

    for (int i = 1; i <= n; i++)
    {
        cin >> e[i] >> l[i] >> d[i];
    }

    for (int i = 0; i <= n; i++)
    {
        for (int j = 0; j <= n; j++)
        {
            cin >> t[i][j];
        }
    }

    for (int i = 1; i <= n; i++)
    {
        int starting_delivery_time = max(t[0][i], e[i]);

        if (starting_delivery_time <= l[i])
        {
            int mask = 1 << (i - 1);
            best_times[mask][i] = t[0][i];
            best_starting_times[mask][i] = starting_delivery_time;
            parents[mask][i] = 0;
        }
    }

    for (int mask = 0; mask < masks; mask++)
    {
        for (int current_point = 1; current_point <= n; current_point++)
        {
            if (best_times[mask][current_point] == INT_MAX)
            {
                continue;
            }

            for (int point = 1; point <= n; point++)
            {
                if (mask & (1 << (point - 1)))
                {
                    continue;
                }
                int starting_delivery_time = max(best_starting_times[mask][current_point] + d[current_point] + t[current_point][point], e[point]);

                if (starting_delivery_time > l[point])
                {
                    continue;
                }
                int new_mask = mask | (1 << (point - 1)), time = best_times[mask][current_point] + t[current_point][point];

                if (time < best_times[new_mask][point])
                {
                    best_times[new_mask][point] = time;
                    best_starting_times[new_mask][point] = starting_delivery_time;
                    parents[new_mask][point] = current_point;
                }
                else if (time == best_times[new_mask][point] && starting_delivery_time < best_starting_times[new_mask][point])
                {
                    best_starting_times[new_mask][point] = starting_delivery_time;
                    parents[new_mask][point] = current_point;
                }
            }
        }
    }

    for (int current_point = 1; current_point <= n; current_point++)
    {
        if (best_times[final_mask][current_point] < INT_MAX)
        {
            int total = best_times[final_mask][current_point] + t[current_point][0];

            if (total < best_time)
            {
                best_time = total;
                last_point = current_point;
            }
        }
    }

    while (last_point > 0)
    {
        route.push_back(last_point);
        int previous_point = parents[final_mask][last_point];
        final_mask ^= 1 << (last_point - 1);
        last_point = previous_point;
    }
    reverse(route.begin(), route.end());

    for (int x : route)
    {
        int finishing_time = max(current_time + t[previous_point][x], e[x]) + d[x];
        best_finishing_times.push_back(finishing_time);
        current_time = finishing_time;
        previous_point = x;
    }

    if (print)
    {
        cout << "Problem size             : ";
    }
    cout << n << endl;

    if (print)
    {
        cout << "Best solution            : ";
    }

    for (int x : route)
    {
        cout << x << ' ';
    }

    if (print)
    {
        cout << "\nBest total time          : " << best_time << "\nTime finishing delivering: ";

        for (int time : best_finishing_times)
        {
            cout << time << " ";
        }
    }
    cout << endl;
    return 0;
}