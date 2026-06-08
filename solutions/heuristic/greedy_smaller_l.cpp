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

    int n, previous_point = 0, total_time = 0;
    cin >> n;
    vector<int> e(n + 1), l(n + 1), d(n + 1), s, arrivals(n + 1);

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
    vector<bool> visited(n + 1, false);
    bool feasible = true;
    arrivals[0] = 0;

    for (int i = 1; i <= n; i++)
    {
        int best_point = 0, time_finishing_delivering = arrivals[i - 1] + d[previous_point];

        for (int j = 1, best_deadline = INT_MAX, best_distance = INT_MAX; j <= n; j++)
        {
            if (!visited[j] && time_finishing_delivering + t[previous_point][j] <= l[j] && time_finishing_delivering + t[previous_point][j] <= l[j] && (l[j] < best_deadline || (l[j] == best_deadline && t[previous_point][j] < best_distance)))
            {
                best_point = j;
                best_deadline = l[j];
                best_distance = t[previous_point][j];
            }
        }

        if (best_point < 1)
        {
            feasible = false;
            cout << "The greedy heuristic based on smaller l[i] gives infeasible solution." << endl;
            break;
        }
        s.push_back(best_point);
        visited[best_point] = true;
        total_time += t[previous_point][best_point];
        arrivals[i] = max(time_finishing_delivering + t[previous_point][best_point], e[best_point]);
        previous_point = best_point;
    }

    if (feasible)
    {
        if (print)
        {
            cout << "Problem size: ";
        }
        cout << n << endl;

        if (print)
        {
            cout << "Solution    : ";
        }

        for (int point : s)
        {
            cout << point << " ";
        }

        if (print)
        {
            cout << "\nTotal time  : " << total_time + t[previous_point][0] << "\nArrivals    :";

            for (int i = 1; i <= n; i++)
            {
                cout << " " << arrivals[i];
            }
        }
        cout << endl;
    }
    return 0;
}