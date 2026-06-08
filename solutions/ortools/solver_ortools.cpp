/*
 * =================================================================
 * Bài toán TSP với Cửa sổ Thời gian (TSPTW)
 * Giải bằng Google OR-Tools Routing Solver (C++)
 * =================================================================
 *
 * Phương pháp: Guided Local Search (GLS) với Disjunctions (Ràng buộc mềm)
 * - Bước 1: Cho phép bỏ qua khách hàng thông qua disjunction với penalty cực lớn (10^12)
 *             Kỹ thuật này giúp giải thuật khởi tạo luôn tìm thấy lời giải khả thi ban đầu
 *             và tránh crash/bế tắc khi có cửa sổ thời gian chặt chẽ.
 * - Bước 2: Xây dựng lời giải ban đầu bằng heuristic PATH_CHEAPEST_ARC.
 * - Bước 3: Cải thiện lời giải bằng Guided Local Search (GLS) để ép solver thăm
 *             đầy đủ toàn bộ khách hàng (nhằm loại bỏ penalty khổng lồ) và tối ưu hóa
 *             tổng thời gian di chuyển (travel time).
 *
 * Biên dịch: Sử dụng CMake (trong thư mục build) hoặc qua Makefile.
 * Chạy:      ./solver_ortools < test1.txt
 * =================================================================
 */

#include <iostream>
#include <vector>
#include <limits>
#include "ortools/constraint_solver/routing.h"
#include "ortools/constraint_solver/routing_enums.pb.h"
#include "ortools/constraint_solver/routing_index_manager.h"
#include "ortools/constraint_solver/routing_parameters.h"

using namespace std;
using namespace operations_research;

int main() {
    int N;
    if (!(cin >> N)) return 0;
    // Cửa sổ thời gian: e[i]..l[i], thời gian phục vụ: d[i]
    vector<int64_t> e(N + 1, 0);
    vector<int64_t> l(N + 1, 0);
    vector<int64_t> d(N + 1, 0);
    // Depot (nút 0) có thời gian bắt đầu = 0, kết thúc vô hạn, phục vụ = 0
    e[0] = 0;
    l[0] = 2000000000LL;
    d[0] = 0;
    for (int i = 1; i <= N; ++i) {
        cin >> e[i] >> l[i] >> d[i];
    }
    // Ma trận thời gian di chuyển t[i][j]
    vector<vector<int64_t>> t(N + 1, vector<int64_t>(N + 1, 0));
    for (int i = 0; i <= N; ++i) {
        for (int j = 0; j <= N; ++j) {
            cin >> t[i][j];
        }
    }
    //Khởi tạo mô hình Routing
    // N + 1 nút (kho + khách hàng), 1 xe, xuất phát và kết thúc tại kho (0)
    RoutingIndexManager manager(N + 1, 1, RoutingIndexManager::NodeIndex(0));
    RoutingModel routing(manager); // Đối tượng chứa toàn bộ mô hình
    
    /* Đăng ký callback thời gian di chuyển giữa hai điểm bất kì, nhận vào hai tham số index from và to
     chuyển đổi chúng sang node thực tế và trả về thời gian dựa vào ma trận t*/
    auto compute_travel_time = [manager, &t, N] (int64_t from_index, int64_t to_index) -> int64_t{
        int from_node = manager.IndexToNode(from_index).value();
        int to_node = manager.IndexToNode(to_index).value();
        if(from_node < 0 || from_node > N || to_node < 0 || to_node > N) return 0;
        return t[from_node][to_node];
    };
    const int transit_callback_index = routing.RegisterTransitCallback(compute_travel_time);
    // Thiết lập hàm mục tiêu chính của bài toán là tối thiểu hoá tổng chi phí di chuyển (travel_time) trên các cung đường được 
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index);
    // Đăng ký callback thời gian (gồm thời gian phục vụ tại nút xuất phát + di chuyển)
    auto compute_total_time = [manager, &d, &t, N] (int64_t from_index, int64_t to_index) -> int64_t{
        int from_node = manager.IndexToNode(from_index).value();
        int to_node = manager.IndexToNode(to_index).value();
        if(from_node < 0 || from_node > N || to_node < 0 || to_node > N) return 0;
        return t[from_node][to_node] + d[from_node];
    };
    const int time_callback_index = routing.RegisterTransitCallback(compute_total_time);
    // Thêm ràng buộc thời gian (Time Dimension)
    int64_t horizon = 2000000000LL;
    routing.AddDimension(
        time_callback_index,
        horizon,  // cho phép chờ vô hạn tại các khách hàng (slack max)
        horizon,  // tổng thời gian tối đa của cả hành trình (capacity max)
        true,     // fix_start_cumul_to_zero: bắt đầu từ thời điểm 0 tại kho
        "Time");
    /*AddDimension tạo ra một biến cộng dồn dọc theo lộ trình để theo dõi thời điểm xe đến từng nút
    Khi xe từ nút i sang nút j. thời điểm đến nút j(u[j]) được tính tự động:
    u[j] >= u[i] + d[i] + t[i][j] (thời điểm đến nút i + phục vụ tại i + thời gian đi từ i sang j)
    slack_max = horizon: cho phép xe đến sớm và chờ tại các nút thoải mái mà không bị phạt*/
    const RoutingDimension& time_dimension = routing.GetDimensionOrDie("Time");

    // Đặt cửa sổ thời gian cho các khách hàng và thêm ràng buộc mềm (disjunctions)
    for (int i = 1; i <= N; ++i) {
        int64_t index = manager.NodeToIndex(RoutingIndexManager::NodeIndex(i));

        // ràng buộc cứng, biến thời gian tích luỹ tại i phải nằm trong khoảng e[i] và l[i]
        time_dimension.CumulVar(index)->SetRange(e[i], l[i]);

        // khai báo nút index này có thể bị bỏ qua, nếu bị bỏ qua, hàm mục tiêu cộng thêm 10^12 -> giữ mô hình luôn khả thi khi khởi tạo
        routing.AddDisjunction({index}, 1000000000000LL); // 10^12 penalty
    }

    // Đặt cửa sổ thời gian cho depot xuất phát và kết thúc
    int64_t depot_start_index = routing.Start(0);
    time_dimension.CumulVar(depot_start_index)->SetRange(0, horizon);
    
    int64_t depot_end_index = routing.End(0);
    time_dimension.CumulVar(depot_end_index)->SetRange(0, horizon);

    //Thiết lập thông số tìm kiếm 
    RoutingSearchParameters search_parameters = DefaultRoutingSearchParameters();
    
    /*Heuristic lời giải ban đầu: Path Cheapest Arc: Chiến lược sinh lời giải ban đầu, bắt đầu từ 
    kho, liên tục chèn các cung có thời gian di chuyển ngắn nhất mà không vi phạm ràng buộc thời gian các điểm đã chèn*/
    search_parameters.set_first_solution_strategy(FirstSolutionStrategy::PATH_CHEAPEST_ARC);
    
    // Metaheuristic cải thiện: Guided Local Search (GLS)
    search_parameters.set_local_search_metaheuristic(LocalSearchMetaheuristic::GUIDED_LOCAL_SEARCH);
    
    // Giới hạn thời gian chạy tối đa (20 giây để tìm kiếm sâu hơn trên các bài toán lớn)
    search_parameters.mutable_time_limit()->set_seconds(20);

    //Giải bài toán
    const Assignment* solution = routing.SolveWithParameters(search_parameters);

    //Xuất kết quả
    if (solution) {
        vector<int> route;
        int visited_count = 0;
        int64_t index = routing.Start(0);
        // Bỏ qua điểm depot bắt đầu
        index = solution->Value(routing.NextVar(index));
        
        while (!routing.IsEnd(index)) {
            auto node = manager.IndexToNode(index).value();
            route.push_back(node);
            visited_count++;
            index = solution->Value(routing.NextVar(index));
        }

        // Chỉ chấp nhận lời giải nếu viếng thăm ĐẦY ĐỦ toàn bộ N khách hàng
        if (visited_count == N) {
            cout << N << "\n";
            for (int i = 0; i < N; ++i) {
                cout << route[i] << (i == N - 1 ? "" : " ");
            }
            cout << "\n";
        } else cout << "Không tìm thấy lời giải hợp lệ! (Chỉ thăm được " << visited_count << "/" << N << " nút)\n";
    } else cout << "Không tìm thấy lời giải hợp lệ!\n";
    return 0;
}
