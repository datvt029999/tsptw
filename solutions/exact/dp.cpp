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
    freopen(("../../input/" + string(argv[1]) + ".txt").c_str(), "r", stdin);

    int n;
    cin >> n;
    int nodes = n + 1, masks = 1 << n;
    vector<int> e(nodes), l(nodes), d(nodes), s;
    vector<vector<int>> t(nodes, vector<int>(nodes)), best_total_times(masks, vector<int>(nodes, INT_MAX)), best_arrivals(masks, vector<int>(nodes)), previous_points(masks, vector<int>(nodes));

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
        int arrival = max(t[0][i], e[i]);

        if (arrival <= l[i])
        {
            int mask = 1 << (i - 1);
            best_total_times[mask][i] = t[0][i];
            best_arrivals[mask][i] = arrival;
            previous_points[mask][i] = 0;
        }
    }

    for (int mask = 0; mask < masks; mask++)
    {
        for (int current_point = 1; current_point <= n; current_point++)
        {
            if (best_total_times[mask][current_point] < INT_MAX)
            {
                for (int point = 1, time_finishing_delivering = best_arrivals[mask][current_point] + d[current_point]; point <= n; point++)
                {
                    if (mask & (1 << (point - 1)))
                    {
                        continue;
                    }
                    int arrival = max(time_finishing_delivering + t[current_point][point], e[point]);

                    if (arrival > l[point])
                    {
                        continue;
                    }
                    int new_mask = mask | (1 << (point - 1)), time = best_total_times[mask][current_point] + t[current_point][point];

                    if (time < best_total_times[new_mask][point])
                    {
                        best_total_times[new_mask][point] = time;
                        best_arrivals[new_mask][point] = arrival;
                        previous_points[new_mask][point] = current_point;
                    }
                    else if (time == best_total_times[new_mask][point] && arrival < best_arrivals[new_mask][point])
                    {
                        best_arrivals[new_mask][point] = arrival;
                        previous_points[new_mask][point] = current_point;
                    }
                }
            }
        }
    }
    int best_time = INT_MAX, mask = --masks, last_point;

    for (int current_point = 1; current_point <= n; current_point++)
    {
        if (best_total_times[mask][current_point] < INT_MAX)
        {
            int total = best_total_times[mask][current_point] + t[current_point][0];

            if (total < best_time)
            {
                best_time = total;
                last_point = current_point;
            }
        }
    }

    while (last_point > 0)
    {
        s.push_back(last_point);
        int previous_point = previous_points[mask][last_point];
        mask ^= 1 << (last_point - 1);
        last_point = previous_point;
    }
    reverse(s.begin(), s.end());

    if (print)
    {
        cout << "Problem size   : ";
    }
    cout << n << endl;

    if (print)
    {
        cout << "Best solution  : ";
    }

    for (int point : s)
    {
        cout << point << " ";
    }

    if (print)
    {
        vector<int> arrivals;
        int arrival = 0, previous_point = 0;

        for (int point : s)
        {
            arrival = max(arrival + d[previous_point] + t[previous_point][point], e[point]);
            arrivals.push_back(arrival);
            previous_point = point;
        }
        cout << "\nBest total time: " << best_time << "\nArrivals       :";

        for (int arrival : arrivals)
        {
            cout << " " << arrival;
        }
    }
    cout << endl;
    return 0;
}