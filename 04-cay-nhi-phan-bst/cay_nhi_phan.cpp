// Cốt Đê · Cấu trúc cây · code mẫu dùng xuyên suốt 3 phần
//
//   Phần 1: cây nhị phân, lưu trữ, duyệt cây
//   Phần 2: cây tìm kiếm nhị phân (BST): tìm, thêm, hủy
//   Phần 3: viết hàm đệ quy trên cây
//
// Một cây mẫu chạy qua cả ba phần: 44 18 88 13 37 59 108 15 23 40 55 71
//
//                 44
//          18            88
//       13    37      59    108
//         15 23 40  55  71
//
// Tên theo cách đặt của cô: nutCay, duLieu, trai, phai.
// Biên dịch: g++ -std=c++17 -Wall -Wextra cay_nhi_phan.cpp -o cay

#include <iostream>
using namespace std;

// ============================================================
// PHẦN 1 · Cây nhị phân, lưu trữ, duyệt cây
// ============================================================

// Lưu trữ móc nối: mỗi nút gồm dữ liệu và hai con trỏ.
// Cây được biểu diễn bằng con trỏ tới nút gốc; t == NULL là cây rỗng.
struct nutCay
{
    int duLieu;
    nutCay *trai;
    nutCay *phai;
};

// Tạo một nút mới: điền dữ liệu, hai con trỏ về NULL, trả về địa chỉ nút.
nutCay *taoNut(int x)
{
    nutCay *p = new nutCay;
    p->duLieu = x;
    p->trai = p->phai = NULL;
    return p;
}

// Dựng tay cây mẫu, gắn từng con trỏ trai/phai (chưa cần biết BST).
nutCay *dungCayMau()
{
    nutCay *t = taoNut(44);
    t->trai = taoNut(18);
    t->phai = taoNut(88);
    t->trai->trai = taoNut(13);
    t->trai->phai = taoNut(37);
    t->phai->trai = taoNut(59);
    t->phai->phai = taoNut(108);
    t->trai->trai->phai = taoNut(15);
    t->trai->phai->trai = taoNut(23);
    t->trai->phai->phai = taoNut(40);
    t->phai->trai->trai = taoNut(55);
    t->phai->trai->phai = taoNut(71);
    return t;
}

// Lưu trữ bằng mảng (cây đầy đủ, đánh số từ 0).
int conTrai(int i) { return 2 * i + 1; }
int conPhai(int i) { return 2 * i + 2; }
int cha(int j) { return (j - 1) / 2; }

// Ba kiểu duyệt: chỉ khác vị trí dòng in.
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

// ============================================================
// PHẦN 2 · Cây tìm kiếm nhị phân (BST)
// ============================================================

// Tìm khóa x: NULL nếu không có.
nutCay *timKiem(nutCay *t, int x)
{
    if (t == NULL) return NULL;
    if (x == t->duLieu) return t;
    if (x < t->duLieu)
        return timKiem(t->trai, x);
    return timKiem(t->phai, x);
}

// Cùng việc đó bằng vòng lặp.
nutCay *timKiemLap(nutCay *t, int x)
{
    while (t != NULL)
    {
        if (x == t->duLieu) return t;
        if (x < t->duLieu)
            t = t->trai;
        else
            t = t->phai;
    }
    return NULL;
}

// Thêm x vào BST. Tham số nutCay *&t là tên khác của chính ô con trỏ
// được truyền vào, nên t = taoNut(x) ghi thẳng vào cây thật.
void boSung(nutCay *&t, int x)
{
    if (t == NULL)
        t = taoNut(x);
    else if (x < t->duLieu)
        boSung(t->trai, x);
    else if (x > t->duLieu)
        boSung(t->phai, x);
    // x == t->duLieu: đã có, không làm gì
}

// Tạo cây từ mảng: bắt đầu từ cây rỗng, thêm lần lượt từng phần tử.
void taoCay(nutCay *&t, int a[], int n)
{
    t = NULL;
    for (int i = 0; i < n; i++)
        boSung(t, a[i]);
}

// Hủy nút có hai con: chọn nút thế mạng, chép khóa của nó lên nút cần hủy,
// rồi hủy nút thế mạng cũ (có tối đa một con).
//
// Cách hai (theo hình và code trong sách): trái nhất của cây con phải.
void timTheMang(nutCay *&p, nutCay *&q)
{
    if (q->trai != NULL)
        timTheMang(p, q->trai);
    else
    {
        p->duLieu = q->duLieu; // chép khóa của q lên nút cần hủy
        p = q;                 // p trỏ tới nút sẽ bị hủy thật sự
        q = q->phai;           // nối cha của q với con phải của q
    }
}

// Cách một: phải nhất của cây con trái.
void timTheMang1(nutCay *&p, nutCay *&q)
{
    if (q->phai != NULL)
        timTheMang1(p, q->phai);
    else
    {
        p->duLieu = q->duLieu;
        p = q;
        q = q->trai;
    }
}

// Hủy nút có khóa x (thế mạng cách hai): 1 nếu hủy được, 0 nếu không có x.
int xoaNut(nutCay *&t, int x)
{
    if (t == NULL)
        return 0;
    if (x < t->duLieu)
        return xoaNut(t->trai, x);
    if (x > t->duLieu)
        return xoaNut(t->phai, x);
    nutCay *p = t; // t->duLieu == x
    if (t->trai == NULL)
        t = t->phai; // lá, hoặc chỉ có con phải
    else if (t->phai == NULL)
        t = t->trai; // chỉ có con trái
    else
        timTheMang(p, t->phai); // đủ hai con
    delete p;
    return 1;
}

// Như trên, thế mạng cách một.
int xoaNut1(nutCay *&t, int x)
{
    if (t == NULL)
        return 0;
    if (x < t->duLieu)
        return xoaNut1(t->trai, x);
    if (x > t->duLieu)
        return xoaNut1(t->phai, x);
    nutCay *p = t;
    if (t->trai == NULL)
        t = t->phai;
    else if (t->phai == NULL)
        t = t->trai;
    else
        timTheMang1(p, t->trai);
    delete p;
    return 1;
}

// Hủy toàn bộ cây theo thứ tự sau: con trước, gốc sau.
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

// ============================================================
// PHẦN 3 · Hàm đệ quy trên cây (khung 3 bước)
//   1. cây rỗng: trả về 0 (điều kiện dừng)
//   2. phần đóng góp của riêng nút t
//   3. gộp: phần của nút + kết quả cây trái + kết quả cây phải
// Các hàm dưới đây đúng cho mọi cây nhị phân, không dựa vào tính chất BST,
// trừ nhoNhat, lonNhat, mucCuaNut.
// ============================================================

int demNut(nutCay *t)
{
    if (t == NULL) return 0;
    return 1 + demNut(t->trai) + demNut(t->phai);
}

int demLa(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->trai == NULL && t->phai == NULL) return 1;
    return demLa(t->trai) + demLa(t->phai);
}

int chieuCao(nutCay *t) // cây rỗng cao 0, cây chỉ có gốc cao 1
{
    if (t == NULL) return 0;
    int hTrai = chieuCao(t->trai);
    int hPhai = chieuCao(t->phai);
    return 1 + (hTrai > hPhai ? hTrai : hPhai);
}

int demChia3(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu % 3 == 0)
        return 1 + demChia3(t->trai) + demChia3(t->phai);
    return demChia3(t->trai) + demChia3(t->phai);
}

int demLe(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu % 2 != 0) // không viết == 1: -15 % 2 bằng -1
        return 1 + demLe(t->trai) + demLe(t->phai);
    return demLe(t->trai) + demLe(t->phai);
}

long long tongNut(nutCay *t)
{
    if (t == NULL) return 0;
    return t->duLieu + tongNut(t->trai) + tongNut(t->phai);
}

long long tongDuong(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu > 0)
        return t->duLieu + tongDuong(t->trai) + tongDuong(t->phai);
    return tongDuong(t->trai) + tongDuong(t->phai);
}

long long tongChan(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu % 2 == 0)
        return t->duLieu + tongChan(t->trai) + tongChan(t->phai);
    return tongChan(t->trai) + tongChan(t->phai);
}

int demHaiCon(nutCay *t)
{
    if (t == NULL) return 0;
    int d = 0;
    if (t->trai != NULL && t->phai != NULL) d = 1;
    return d + demHaiCon(t->trai) + demHaiCon(t->phai);
}

int doDaiDuongDi(nutCay *t, int muc) // PT: gọi lần đầu với muc = 0
{
    if (t == NULL) return 0;
    return muc + doDaiDuongDi(t->trai, muc + 1) + doDaiDuongDi(t->phai, muc + 1);
}

void inMuc(nutCay *t, int k) // in các nút ở mức k, trái sang phải
{
    if (t == NULL) return;
    if (k == 0)
        cout << t->duLieu << " ";
    else
    {
        inMuc(t->trai, k - 1);
        inMuc(t->phai, k - 1);
    }
}

void inGiam(nutCay *t) // đảo duyệt giữa: phải, gốc, trái
{
    if (t != NULL)
    {
        inGiam(t->phai);
        cout << t->duLieu << " ";
        inGiam(t->trai);
    }
}

// Riêng ba hàm sau dựa vào tính chất BST.
nutCay *nhoNhat(nutCay *t) // đi mãi sang trái
{
    if (t == NULL) return NULL;
    while (t->trai != NULL) t = t->trai;
    return t;
}

nutCay *lonNhat(nutCay *t) // đi mãi sang phải
{
    if (t == NULL) return NULL;
    while (t->phai != NULL) t = t->phai;
    return t;
}

int mucCuaNut(nutCay *t, int x) // gốc ở mức 0; -1 nếu không có x
{
    int muc = 0;
    while (t != NULL)
    {
        if (t->duLieu == x) return muc;
        if (x < t->duLieu)
            t = t->trai;
        else
            t = t->phai;
        muc++;
    }
    return -1;
}

// Kiểm tra BST: mỗi nút phải nằm trong khoảng (min, max), khoảng thu hẹp dần.
int laBST(nutCay *t, long long min, long long max)
{
    if (t == NULL) return 1;
    if (t->duLieu <= min || t->duLieu >= max) return 0;
    return laBST(t->trai, min, t->duLieu) && laBST(t->phai, t->duLieu, max);
}

// ============================================================
// Chạy thử từng phần
// ============================================================

void in(const char *ten, void (*f)(nutCay *), nutCay *t)
{
    cout << ten << ": ";
    f(t);
    cout << endl;
}

void phan1()
{
    cout << "=== Phan 1 ===" << endl;
    nutCay *t = dungCayMau();
    in("truoc", duyetTruoc, t);
    in("giua ", duyetGiua, t);
    in("sau  ", duyetSau, t);
    cout << "mang: nut 4 co con " << conTrai(4) << " va " << conPhai(4)
         << "; nut 9 co cha " << cha(9) << endl;
    huyCay(t);
}

void phan2()
{
    cout << "=== Phan 2 ===" << endl;
    int a[] = {44, 18, 88, 13, 37, 59, 108, 15, 23, 40, 55, 71};
    nutCay *t;
    taoCay(t, a, 12);
    in("giua (tang dan)", duyetGiua, t);

    cout << "tim 55: " << (timKiem(t, 55) != NULL ? "thay" : "khong co")
         << ", tim 56: " << (timKiemLap(t, 56) != NULL ? "thay" : "khong co") << endl;

    boSung(t, 50);
    in("them 50 (truoc)", duyetTruoc, t);
    huyCay(t);

    // Ví dụ 1 của cô: dãy 8 3 10 1 6 14 4 7; hủy 1 (lá), 3 (một con), rồi 8 (hai con) bằng hai cách.
    int b[] = {8, 3, 10, 1, 6, 14, 4, 7};
    taoCay(t, b, 8);
    xoaNut(t, 1);
    xoaNut(t, 3);
    xoaNut(t, 8);
    in("huy 8, cach 2 (truoc)", duyetTruoc, t);
    huyCay(t);

    taoCay(t, b, 8);
    xoaNut1(t, 1);
    xoaNut1(t, 3);
    xoaNut1(t, 8);
    in("huy 8, cach 1 (truoc)", duyetTruoc, t);
    huyCay(t);
}

void phan3()
{
    cout << "=== Phan 3 ===" << endl;
    nutCay *t = dungCayMau();
    cout << "so nut " << demNut(t) << ", so la " << demLa(t)
         << ", chieu cao " << chieuCao(t) << ", nut hai con " << demHaiCon(t) << endl;
    cout << "tong chan " << tongChan(t) << ", PT " << doDaiDuongDi(t, 0) << endl;
    cout << "nho nhat " << nhoNhat(t)->duLieu << ", lon nhat " << lonNhat(t)->duLieu
         << ", muc cua 55 " << mucCuaNut(t, 55) << endl;
    in("giam dan", inGiam, t);
    cout << "muc 2: ";
    inMuc(t, 2);
    cout << endl;
    cout << "la BST: " << laBST(t, -9999999999LL, 9999999999LL) << endl;
    huyCay(t);

    // Cây thử của cô, có khóa âm.
    int a[] = {20, -8, 35, -15, 3, 28, 50, -3, 9, 0};
    taoCay(t, a, 10);
    cout << "cay thu cua co: so nut " << demNut(t) << ", so le " << demLe(t)
         << ", tong " << tongNut(t) << ", tong duong " << tongDuong(t) << endl;
    huyCay(t);

    int c[] = {14, 9, 21, 6, 12, 18, 30, 11, 25};
    taoCay(t, c, 9);
    cout << "chia het cho 3: " << demChia3(t) << endl;
    huyCay(t);
}

int main()
{
    phan1();
    phan2();
    phan3();
    return 0;
}
