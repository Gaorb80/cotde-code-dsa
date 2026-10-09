// Cốt Đê – Stack (ngăn xếp) bằng C++
// Video: <link YouTube>

#include <iostream>
using namespace std;

const int SUC_CHUA = 5;          // bàn cô giáo để được tối đa 5 cuốn vở

struct NganXep {
    char phanTu[SUC_CHUA];       // các cuốn vở, xếp từ dưới lên
    int dinh = -1;               // vị trí cuốn trên cùng, -1 nghĩa là chồng rỗng
};

bool rong(NganXep &s) { return s.dinh == -1; }
bool day(NganXep &s)  { return s.dinh == SUC_CHUA - 1; }

// push: đặt thêm một cuốn lên trên cùng
void push(NganXep &s, char x) {
    if (day(s)) {
        cout << "Chong vo day roi, khong push duoc\n";
        return;
    }
    s.dinh++;
    s.phanTu[s.dinh] = x;
}

// pop: lấy cuốn trên cùng ra
char pop(NganXep &s) {
    if (rong(s)) {
        cout << "Chong vo rong, khong pop duoc\n";
        return '?';
    }
    char x = s.phanTu[s.dinh];
    s.dinh--;                    // chỉ hạ dinh xuống một ô, không xoá gì cả
    return x;
}

// in văn bản đang có, đọc từ dưới lên
void inVanBan(NganXep &s) {
    cout << "Van ban: ";
    for (int i = 0; i <= s.dinh; i++) {
        cout << s.phanTu[i];
    }
    cout << "\n";
}

int main() {
    // Phần 1: chồng vở trên bàn cô giáo
    NganXep chongVo;
    push(chongVo, 'C');
    push(chongVo, 'O');
    push(chongVo, 'T');

    cout << "Lay ra: " << pop(chongVo) << "\n";   // T, nộp sau nên được chấm trước
    cout << "Lay ra: " << pop(chongVo) << "\n";   // O
    cout << "Lay ra: " << pop(chongVo) << "\n";   // C

    // Phần 2: Ctrl+Z mini
    // Mỗi lần gõ một chữ là một lần push. Ctrl+Z là một lần pop.
    NganXep lichSu;
    push(lichSu, 'C');
    push(lichSu, 'O');
    push(lichSu, 'T');
    inVanBan(lichSu);                              // COT

    cout << "Bam Ctrl+Z\n";
    pop(lichSu);
    inVanBan(lichSu);                              // CO

    return 0;
}
