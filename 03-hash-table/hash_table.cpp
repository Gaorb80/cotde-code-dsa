// Cốt Đê – Hash table (bảng băm) bằng C++
// Video: <link YouTube>

#include <iostream>
#include <string>
using namespace std;

const int SO_O = 13;             // bảng có 13 ô

struct HoSo {
    int ma;                      // mã sinh viên (key)
    string ten;                  // dữ liệu cần tra (value)
    HoSo* tiep;                  // hồ sơ tiếp theo nằm chung ô
};

HoSo* bang[SO_O];                // mỗi ô là đầu một danh sách liên kết; mảng toàn cục nên ban đầu đều là nullptr

// hàm băm: tính ô từ mã
int viTri(int ma) { return ma % SO_O; }

// thêm hồ sơ: chèn vào đầu danh sách của ô đó
void them(int ma, string ten) {
    int o = viTri(ma);
    bang[o] = new HoSo{ma, ten, bang[o]};
}

// tìm hồ sơ: chỉ dò trong đúng một ô
HoSo* tim(int ma) {
    HoSo* p = bang[viTri(ma)];
    while (p != nullptr) {
        if (p->ma == ma) return p;
        p = p->tiep;             // sang hồ sơ kế tiếp trong cùng ô
    }
    return nullptr;              // hết danh sách mà chưa gặp
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
    them(50, "An");
    them(24, "Binh");            // 24 % 13 = 11, rơi đúng ô của mã 50
    them(40, "Chi");             // 40 % 13 = 1

    cout << "Ma 50 nam o o " << viTri(50) << "\n";
    cout << "Ma 24 nam o o " << viTri(24) << "\n";

    HoSo* h = tim(50);
    if (h != nullptr) cout << "Tim ma 50: " << h->ten << "\n";   // An vẫn còn, không bị ghi đè
    h = tim(24);
    if (h != nullptr) cout << "Tim ma 24: " << h->ten << "\n";
    if (tim(99) == nullptr) cout << "Khong co ma 99\n";

    xoaHet();
    return 0;
}
