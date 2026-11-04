// Ôn tập · Câu 8 (đề mẫu): cây nhị phân 8 / 3 10 / 1 6 _ 14 / -2 _ 4 7
//
//                 8
//          3            10
//       1     6            14
//     -2     4  7
//
// a) Thứ tự duyệt:
//      trước : 8 3 1 -2 6 4 7 10 14
//      giữa  : -2 1 3 4 6 7 8 10 14
//      sau   : -2 1 4 7 6 3 14 10 8
// b) Khai báo lưu trữ móc nối, mỗi nút một số nguyên: struct nutCay (bên dưới).
// c) Hàm tongDuong: tổng các nút có giá trị dương (khung 3 bước: dừng, phần của nút, gộp).
//
// Biên dịch: g++ -std=c++17 -Wall -Wextra cau8_mau.cpp -o cau8

#include <iostream>
using namespace std;

// b) Khai báo
struct nutCay
{
    int duLieu;
    nutCay *trai;
    nutCay *phai;
};

nutCay *taoNut(int x)
{
    nutCay *p = new nutCay;
    p->duLieu = x;
    p->trai = p->phai = NULL;
    return p;
}

// c) Tổng các nút dương
int tongDuong(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu > 0)
        return t->duLieu + tongDuong(t->trai) + tongDuong(t->phai);
    return tongDuong(t->trai) + tongDuong(t->phai);
}

// a) Ba kiểu duyệt: chỉ khác vị trí dòng in
void duyetTruoc(nutCay *t) // gốc, trái, phải
{
    if (t != NULL)
    {
        cout << t->duLieu << " ";
        duyetTruoc(t->trai);
        duyetTruoc(t->phai);
    }
}

void duyetGiua(nutCay *t) // trái, gốc, phải
{
    if (t != NULL)
    {
        duyetGiua(t->trai);
        cout << t->duLieu << " ";
        duyetGiua(t->phai);
    }
}

void duyetSau(nutCay *t) // trái, phải, gốc
{
    if (t != NULL)
    {
        duyetSau(t->trai);
        duyetSau(t->phai);
        cout << t->duLieu << " ";
    }
}

void huyCay(nutCay *&t)
{
    if (t != NULL)
    {
        huyCay(t->trai);
        huyCay(t->phai);
        delete t;
        t = NULL;
    }
}

int main()
{
    nutCay *t = taoNut(8);
    t->trai = taoNut(3);
    t->phai = taoNut(10);
    t->trai->trai = taoNut(1);
    t->trai->phai = taoNut(6);
    t->phai->phai = taoNut(14);
    t->trai->trai->trai = taoNut(-2);
    t->trai->phai->trai = taoNut(4);
    t->trai->phai->phai = taoNut(7);

    cout << "truoc: ";
    duyetTruoc(t);
    cout << "\ngiua : ";
    duyetGiua(t);
    cout << "\nsau  : ";
    duyetSau(t);
    cout << "\ntong cac nut duong: " << tongDuong(t) << endl; // 8+3+1+6+4+7+10+14 = 53

    huyCay(t);
    return 0;
}
