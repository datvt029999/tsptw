/*
 * Bộ sinh test case cho TSPTW (TSP with Time Windows)
 * Phương pháp: Sinh lộ trình ngẫu nhiên trước, rồi gán cửa sổ thời gian
 * dựa trên thời điểm đến thực tế nên đảm bảoinstance có lời giải khả thi.
 * Cách dùng: ./gen <N> [seed]
 *   N    : số khách hàng (1 <= N <= 1000)
 *   seed : hạt giống ngẫu nhiên (mặc định 42)
 * Định dạng output:
 *   Dòng 1: N
 *   Dòng i+1 (i=1..N): e(i) l(i) d(i)
 *   Dòng i+N+2 (i=0..N): hàng i của ma trận thời gian di chuyển t
 */
#include <iostream>
#include <vector>
#include <random>
#include <cstdlib>
#include <algorithm>
#include <cmath>
using namespace std;

int main(int argc, char* argv[]) {
    int N = 10;
    int seed = 42;
    if (argc > 1) N = atoi(argv[1]);
    if (argc > 2) seed = atoi(argv[2]);
    mt19937 rng(seed);
    auto randi = [&](int low, int high) {
        return low + (int)(rng() % (high - low + 1));
    };
    // rng() là hàm sinh số ngẫu nhiên cực lớn, chia lấy dư cho (high - low + 1) để đưa về khoảng [0, high - low], rồi cộng thêm low để đưa về khoảng [low, high]
    // Sinh vị trí ngẫu nhiên
    // Tọa độ nguyên trên lưới 1000x1000
    vector<int> x(N + 1), y(N + 1);
    x[0] = 500; y[0] = 500; // kho ở trung tâm
    for (int i = 1; i <= N; i++) {
        x[i] = randi(0, 999);
        y[i] = randi(0, 999);
    }

    // Ma trận thời gian di chuyển t[i][j]
    // Dùng khoảng cách Euclid (làm tròn) + nhiễu nhỏ (tối đa 10% khoảng cách)
    vector<vector<int>> t(N + 1, vector<int>(N + 1, 0));
    for (int i = 0; i <= N; i++) {
        for (int j = 0; j <= N; j++) {
            if (i == j){
                t[i][j] = 0;
                continue;
            }
            int dx = x[i] - x[j], dy = y[i] - y[j];
            int d = (int)sqrt((double)(dx*dx + dy*dy));
            // Thêm nhiễu nhỏ để ma trận không đối xứng hoàn toàn
            d += randi(0, max(1, d / 10));
            t[i][j] = d;
        }
    }

    //Sinh thời gian phục vụ d[i]
    vector<int> d(N + 1, 0);
    for (int i = 1; i <= N; i++) {
        d[i] = randi(5, 25); // phục vụ 5..25 đơn vị thời gian
    }

    //Sinh lộ trình ngẫu nhiên khả thi để tạo time windows
    // Xáo trộn ngẫu nhiên thứ tự khách hàng
    vector<int> route(N);
    iota(route.begin(), route.end(), 1); // [1, 2, ..., N]
    shuffle(route.begin(), route.end(), rng); // hàm shuffle xáo trộn ngẫu nhiên phần tử trong vector route
    // Tính thời điểm đến thực tế theo lộ trình này
    vector<int> arrival(N + 1, 0); // arrival[i] là thời điểm thực tế người giao hàng đến khách hàng i theo lộ trình
    {
        int cur = 0, tg = 0;
        for (int i = 0; i < N; i++) {
            int next = route[i];
            tg += t[cur][next];
            arrival[next] = tg;
            tg += d[next]; // cộng thêm thời gian phục vụ
            cur = next;
        }
    }
    // Gán cửa sổ thời gian dựa trên arrival
    // e[i] = arrival[i] - slack_before  (có thể đến sớm hơn một chút)
    // l[i] = arrival[i] + slack_after   (cho phép đến muộn hơn một chút)
    // Đảm bảo e[i] >= 0 bằng max
    vector<int> e(N + 1, 0), l(N + 1, 0);
    for (int i = 1; i <= N; i++) {
        int slack_before = randi(100, 500);
        int slack_after  = randi(500, 2000);
        e[i] = max(0, arrival[i] - slack_before);
        l[i] = arrival[i] + slack_after;
    }

    // Xuất kết quả
    cout << N << "\n";
    for (int i = 1; i <= N; i++) {
        cout << e[i] << " " << l[i] << " " << d[i] << "\n";
    }
    for (int i = 0; i <= N; i++) {
        for (int j = 0; j <= N; j++) {
            cout << t[i][j] << (j == N ? "\n" : " ");
        }
    }
    return 0;
}
