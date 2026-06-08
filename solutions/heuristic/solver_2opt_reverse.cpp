#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <climits>
using namespace std;
struct khachHang{
    int e, l, d;
};
int n;
vector<khachHang> kh;
vector<vector<int>> t;

// Giá trị lớn nhất của t[i][j] — dùng để chuẩn hoá t về [0, 1]
int t_max = 1; // khởi tạo bằng 1 để tránh chia cho 0

chrono::steady_clock::time_point thoiDiemBatDau;
const double gioihan_thoigian = 9.0;

inline double thoiGianDaTroi(){
    return chrono::duration<double>(chrono::steady_clock::now() - thoiDiemBatDau).count();
    //.count để lấy ra con số double thuần tuý để so sánh với giới hạn thời gian
}
// -----------------------------------------------------------------------
// Hàm tham lam với hàm chi phí kết hợp (đã chuẩn hoá đúng cách)
// -----------------------------------------------------------------------
// Công thức:
//   cost = w * t_norm + (1 - w) * slack_norm
//
// Trong đó:
//   t_norm    = t[cur][id] / t_max
//              → chuẩn hoá thời gian di chuyển về [0, 1]
//              → nhỏ = đường gần → tốt hơn
//
//   slack     = kh[id].l - tgThuc - t[cur][id]
//              → thời gian còn lại trong cửa sổ sau khi đến nơi
//              → ĐÂY MỚI LÀ thước đo đúng của ‘khẩn cấp’, không phải l[id] tuyệt đối
//   slack_norm = slack / t_max
//              → chuẩn hoá về cùng thang với t_norm
//              → nhỏ = sắp hết giờ = khẩn cấp hơn → ưu tiên chọn
//
// TẠI SAO DÙNG SLACK THAY VÌ l[id]?
//   l[id] tuyệt đối không phản ánh được mức độ khẩn cấp so với vị trí hiện tại.
//   Ví dụ: khách A (l=100) và khách B (l=200), hiện ở xa A hơn B rất nhiều.
//   → Dùng l[id] thì chọn A trước, nhưng thực ra có thể không kịp đến A!
//   w = 0.7 → ưu tiên 70% cho gần, 30% cho khẩn cấp
//   (w được truyền vào từ ngoài để có thể thử nhiều giá trị khác nhau)
// -----------------------------------------------------------------------
vector<int> thamLam(double w){
    vector<bool> visited(n + 1, false);
    vector<int> route;
    int cur = 0;
    long long tgThuc = 0; // thời gian thực tế trên đồng hồ của người giao hàng
    for(int i = 0 ; i < n ; i++){
        int next = -1;
        double costMin = 1e18;
        for(int id = 1 ; id <= n ; id++){
            if(visited[id]) continue;
            long long tgDen = tgThuc + t[cur][id];
            long long start = max(tgDen, (long long) kh[id].e);
            // Chỉ xét khách hàng còn kịp phục vụ trong cửa sổ thời gian
            if(start <= kh[id].l){
                // Chuẩn hoá thời gian di chuyển về [0, 1]
                double t_norm = (double)t[cur][id] / t_max;
                // Slack = thời gian còn lại trong cửa sổ thời gian sau khi đến nơi
                // Slack nhỏ → sắp hết giờ → khẩn cấp hơn
                // Khác với l[id]: l[id] là deadline cố định, còn slack thay đổi theo tgThuc và t[cur][id]
                double slack = kh[id].l - (tgThuc + t[cur][id]);
                // Chuẩn hoá slack về [0, 1] bằng cách chia cho t_max
                // (cả slack và t đều đo bằng đơn vị thời gian → cùng thang đo với t_max)
                double slack_norm = slack / t_max;
                // Hàm chi phí kết hợp:
                //   - t_norm nhỏ → đường gần → chọn trước
                //   - slack_norm nhỏ → sắp hết giờ → chọn trước
                double cost = w * t_norm + (1 - w) * slack_norm;
                if(cost < costMin){
                    costMin = cost;
                    next = id;
                }
            }
        }
        if(next == -1) break; // không còn khách nào kịp → dừng tham lam
        // Cập nhật trạng thái: di chuyển đến khách next
        visited[next] = true;
        route.push_back(next);
        long long tgDen = tgThuc + t[cur][next];
        tgThuc = max(tgDen, (long long) kh[next].e) + kh[next].d; // chờ nếu đến sớm, rồi phục vụ
        cur = next;
    }
    return route;
}
// Hàm kiểm tra tính khả thi và tính thời gian di chuyển
bool check(const vector<int> &route, long long &tgDiChuyen){
    tgDiChuyen = 0;
    long long tgThuc = 0;
    int cur = 0;
    for(int id : route){
        tgThuc += t[cur][id];
        tgDiChuyen += t[cur][id];
        if(tgThuc < kh[id].e) tgThuc = kh[id].e; // nếu đến sớm phải chờ
        if(tgThuc > kh[id].l) return false; // nếu đến muộn thì không khả thi
        tgThuc += kh[id].d; // thêm thời gian phục vụ tại khách hàng id
        cur = id;
    }
    tgDiChuyen += t[cur][0]; // sau khi hoàn thành qauy về kho
    return true;
}
// sau khi tham lam có lộ trình, thực hiện 2opt để cải thiện lộ trình trên
void caiThien2opt(vector<int> &route){
    if(route.size() < 3) return; // nếu lộ trình ít hơn 3 điểm thì không đảo
    bool totHon = true;
    long long tgTotNhat;
    // kiểm tra lộ trình ban đầu có khả thi không, tính tổng thời gian di chuyển gán vào thời gian tốt nhất
    check(route, tgTotNhat);
    while(totHon && thoiGianDaTroi() < gioihan_thoigian){
        totHon = false;
        int m = route.size();
        for(int i = 0 ; i < m - 1 ; i++){
            for(int j = i + 1 ; j < m ; j++){
                // tạo lộ trình mới bằng cách đảo đoạn từ i đến j
                reverse(route.begin() + i, route.begin() + j + 1);
                long long tgMoi;
                bool khaThi = check(route, tgMoi); // tính tgMoi
                if(khaThi && tgMoi < tgTotNhat){
                    tgTotNhat = tgMoi;
                    totHon = true;
                    break; // nếu tốt hơn, quét lại từ đầu
                }
                else{
                    reverse(route.begin() + i, route.begin() + j + 1); // nếu không tốt hơn thì đảo lại như cũ
                }
            }
            if(totHon) break;
        }
    }
}
void printSolution(const vector<int> &route, long long tgDiChuyen){
    cout << "Lộ trình: 0 -> ";
    for(int id : route){
        cout << id << " -> ";
    }
    cout << "0\n";
    cout << "Tổng thời gian di chuyển: " << tgDiChuyen << endl;
}
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    thoiDiemBatDau = chrono::steady_clock::now();
    kh.resize(n + 1);
    for(int i = 1 ; i <= n ; i++){
        cin >> kh[i].e >> kh[i].l >> kh[i].d;
    }
    t.assign(n + 1, vector<int>(n + 1));
    for(int i = 0 ; i <= n ; i++){
        for(int j = 0 ; j <= n ; j++){
            cin >> t[i][j];
        }
    }

    // Tính t_max = giá trị lớn nhất trong ma trận thời gian di chuyển
    // Dùng để chuẩn hoá cả t[i][j] và slack về cùng thang đo trong hàm tham lam
    for(int i = 0 ; i <= n ; i++)
        for(int j = 0 ; j <= n ; j++)
            t_max = max(t_max, t[i][j]);

    vector<int> bestRoute;
    long long bestTg = LLONG_MAX;
    for(int wi = 0 ; wi <= 10 ; wi++){
        double w = wi / 10.0; // w lần lượt = 0.0, 0.1, 0.2, ..., 1.0
        vector<int> route = thamLam(w);
        long long tg;
        // Chỉ giữ lại nếu lộ trình ĐẦY ĐỦ (đủ n khách) và KHẢ THI
        if((int)route.size() == n && check(route, tg)){
            if(tg < bestTg){
                bestTg = tg;
                bestRoute = route;
            }
        }
    }
    if(bestRoute.empty()){
        cout << "Không tìm thấy lời giải" << endl;
        return 0;
    }
    // In lộ trình tham lam tốt nhất
    printSolution(bestRoute, bestTg);
    // Cải thiện bằng 2-opt
    caiThien2opt(bestRoute);
    long long tgDiChuyen;
    bool khaThi2opt = check(bestRoute, tgDiChuyen);
    if(khaThi2opt){
        printSolution(bestRoute, tgDiChuyen);
    } else {
        cout << "Lộ trình sau 2-opt không khả thi" << endl;
    }
    return 0;
}
