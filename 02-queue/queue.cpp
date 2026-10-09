// Cốt Đê – Queue (hàng đợi) bằng C++
// Video: <link YouTube>

#include <iostream>
#include <string>
using namespace std;

const int SUC_CHUA = 5;          // máy in nhận tối đa 5 lệnh chờ

struct HangDoi {
    string phanTu[SUC_CHUA];     // các lệnh in, xếp theo thứ tự gửi
    int dau = 0;                 // ô của lệnh sắp được in
    int cuoi = 0;                // ô trống tiếp theo để nhận lệnh mới
};

bool rong(HangDoi &q) { return q.dau == q.cuoi; }
bool day(HangDoi &q)  { return q.cuoi == SUC_CHUA; }

// enqueue: xếp thêm một lệnh vào cuối hàng
void enqueue(HangDoi &q, string x) {
    if (day(q)) {
        cout << "Hang doi day, khong nhan lenh " << x << "\n";
        return;
    }
    q.phanTu[q.cuoi] = x;
    q.cuoi++;
}

// dequeue: lấy lệnh ở đầu hàng ra để in
string dequeue(HangDoi &q) {
    if (rong(q)) {
        cout << "Hang doi rong\n";
        return "";
    }
    string x = q.phanTu[q.dau];
    q.dau++;
    return x;
}

int main() {
    HangDoi mayIn;
    enqueue(mayIn, "An");
    enqueue(mayIn, "Binh");
    enqueue(mayIn, "Chi");

    cout << "In bai cua: " << dequeue(mayIn) << "\n";   // An, gửi trước nên in trước
    cout << "In bai cua: " << dequeue(mayIn) << "\n";   // Binh
    cout << "In bai cua: " << dequeue(mayIn) << "\n";   // Chi

    // Chỗ hở: dau và cuoi chỉ tăng, ba ô đầu đã trống mà không dùng lại được
    enqueue(mayIn, "Dung");
    enqueue(mayIn, "Em");
    enqueue(mayIn, "Giang");                            // báo đầy dù còn ô trống

    return 0;
}
