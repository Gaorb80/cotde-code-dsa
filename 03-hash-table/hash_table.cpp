// Cốt Đê – Hash table (bảng băm) bằng C++
// Video: <link YouTube>
// Ý tưởng: tủ hồ sơ 13 ngăn. Hàm băm tính ra ngăn từ mã (mã chia lấy dư cho 13).
// Hồ sơ cùng ngăn móc vào nhau như một đoàn tàu (xâu chuỗi, danh sách liên kết).

#include <iostream>
#include <string>
using namespace std;

const int SO_O = 13;             // tủ có 13 ngăn, đánh số 0 đến 12

struct HoSo {
    int ma;                      // mã sinh viên (key)
    string ten;                  // dữ liệu cần tra (value)
    HoSo* tiep;                  // cái móc: trỏ tới hồ sơ kế tiếp nằm chung ngăn (toa sau)
};

HoSo* bang[SO_O];                // 13 đầu tàu, mỗi ngăn một con trỏ; mảng toàn cục nên ban đầu đều là nullptr

// hàm băm: tính ra ngăn từ mã. Ví dụ 50 % 13 = 11 (50 chia 13 được 3, dư 11)
int viTri(int ma) { return ma % SO_O; }

// thêm hồ sơ: tính ra ngăn, gắn hồ sơ mới vào đầu đoàn tàu của ngăn đó
void them(int ma, string ten) {
    int o = viTri(ma);
    bang[o] = new HoSo{ma, ten, bang[o]};
}

// tìm hồ sơ: tính ra ngăn, đi dọc đoàn tàu theo con trỏ tiep, so mã từng hồ sơ
HoSo* tim(int ma) {
    HoSo* p = bang[viTri(ma)];
    while (p != nullptr) {
        if (p->ma == ma) return p;
        p = p->tiep;             // sang toa kế tiếp trong cùng ngăn
    }
    return nullptr;              // đi hết đoàn tàu mà chưa gặp: không có hồ sơ này
}

// trả lại bộ nhớ đã cấp bằng new
void xoaHet() {
    for (int o = 0; o < SO_O; o++) {
        while (bang[o] != nullptr) {
            HoSo* p = bang[o];
            bang[o] = p->tiep;
            delete p;
        }
    }
}

int main() {
    them(50, "An");              // 50 % 13 = 11
    them(24, "Binh");            // 24 % 13 = 11: va chạm, cùng ngăn với mã 50 nhưng không ghi đè
    them(40, "Chi");             // 40 % 13 = 1

    cout << "Ma 50 nam o o " << viTri(50) << "\n";
    cout << "Ma 24 nam o o " << viTri(24) << "\n";

    HoSo* h = tim(50);
    if (h != nullptr) cout << "Tim ma 50: " << h->ten << "\n";   // An vẫn còn
    h = tim(24);
    if (h != nullptr) cout << "Tim ma 24: " << h->ten << "\n";
    if (tim(99) == nullptr) cout << "Khong co ma 99\n";

    xoaHet();
    return 0;
}

// Thử tự làm: tủ 13 ngăn, mã 37 nằm ngăn nào? (câu hỏi cuối video)
