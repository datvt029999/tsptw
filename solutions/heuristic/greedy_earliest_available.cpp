#include <climits>
#include <iostream>
#include <vector>

using namespace std;

int main(void)
{
    int n, previous_point = 0, previous_time = 0;
    cin >> n;
    vector<int> e(n + 1), l(n + 1), d(n + 1);

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
    cout << n << endl;
    vector<bool> visited(n + 1, false);

    for (int i = 1; i <= n; i++)
    {
        int best_point;

        for (int j = 1, best_deadline = INT_MAX, best_distance = INT_MAX; j <= n; j++)
        {
            if (!visited[j] && previous_time + t[previous_point][j] <= l[j] && (l[j] < best_deadline || (l[j] == best_deadline && t[previous_point][j] < best_distance)))
            {
                best_point = j;
                best_deadline = l[j];
                best_distance = t[previous_point][j];
            }
        }
        cout << best_point << " ";
        visited[best_point] = true;
        previous_time = max(previous_time + t[previous_point][best_point], e[best_point]) + d[best_point];
        previous_point = best_point;
    }
    cout << endl;
    return 0;
}