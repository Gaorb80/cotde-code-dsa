# -*- coding: utf-8 -*-
"""Cac doan code C++ dung chung (« » danh dau toan tu phai doi khi sap giam dan)."""

DECL = """
struct nutCay
{
    int duLieu;
    nutCay *trai;
    nutCay *phai;
};
"""

TAONUT = """
nutCay *taoNut(int x)
{
    nutCay *p = new nutCay;
    p->duLieu = x;
    p->trai = p->phai = NULL;
    return p;
}
"""

BOSUNG = """
void boSung(nutCay *&t, int x)      // t là tham chiếu: sửa thẳng vào cây thật
{
    if (t == NULL)
        t = taoNut(x);
    else if (x < t->duLieu)
        boSung(t->trai, x);
    else if (x > t->duLieu)
        boSung(t->phai, x);
    // x == t->duLieu: đã có, không làm gì
}
"""

DUYET = """
void duyetTruoc(nutCay *t)      // gốc, trái, phải
{
    if (t != NULL)
    {
        cout << t->duLieu << " ";
        duyetTruoc(t->trai);
        duyetTruoc(t->phai);
    }
}
void duyetGiua(nutCay *t)       // trái, gốc, phải   (BST: tăng dần)
{
    if (t != NULL)
    {
        duyetGiua(t->trai);
        cout << t->duLieu << " ";
        duyetGiua(t->phai);
    }
}
void duyetSau(nutCay *t)        // trái, phải, gốc
{
    if (t != NULL)
    {
        duyetSau(t->trai);
        duyetSau(t->phai);
        cout << t->duLieu << " ";
    }
}
"""

HAM_CAY = """
int demNut(nutCay *t)
{
    if (t == NULL) return 0;
    return 1 + demNut(t->trai) + demNut(t->phai);
}
int demLe(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu % 2 != 0)         // không viết == 1: -15 % 2 bằng -1
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
"""

HAM_CAY_THEM = """
int demLa(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->trai == NULL && t->phai == NULL) return 1;
    return demLa(t->trai) + demLa(t->phai);
}
int chieuCao(nutCay *t)             // cây rỗng cao 0, chỉ có gốc cao 1
{
    if (t == NULL) return 0;
    int hTrai = chieuCao(t->trai);
    int hPhai = chieuCao(t->phai);
    return 1 + (hTrai > hPhai ? hTrai : hPhai);
}
nutCay *timKiem(nutCay *t, int x)   // BST: NULL nếu không có
{
    if (t == NULL) return NULL;
    if (x == t->duLieu) return t;
    if (x < t->duLieu) return timKiem(t->trai, x);
    return timKiem(t->phai, x);
}
nutCay *nhoNhat(nutCay *t)          // đi mãi sang trái
{
    if (t == NULL) return NULL;
    while (t->trai != NULL) t = t->trai;
    return t;
}
"""

XOA = """
void timTheMang(nutCay *&p, nutCay *&q)   // cách hai: trái nhất của cây con phải
{
    if (q->trai != NULL)
        timTheMang(p, q->trai);
    else
    {
        p->duLieu = q->duLieu;   // chép khóa của q lên nút cần hủy
        p = q;                   // p trỏ tới nút sẽ bị hủy thật sự
        q = q->phai;             // nối cha của q với con phải của q
    }
}
int xoaNut(nutCay *&t, int x)             // 1: hủy được, 0: không có x
{
    if (t == NULL) return 0;
    if (x < t->duLieu) return xoaNut(t->trai, x);
    if (x > t->duLieu) return xoaNut(t->phai, x);
    nutCay *p = t;               // t->duLieu == x
    if (t->trai == NULL)
        t = t->phai;             // lá, hoặc chỉ có con phải
    else if (t->phai == NULL)
        t = t->trai;             // chỉ có con trái
    else
        timTheMang(p, t->phai);  // đủ hai con
    delete p;
    return 1;
}
"""

SELECTION = """
void SelectionSort(int a[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        int vt = i;                         // vị trí phần tử «nhỏ nhất»
        for (int j = i + 1; j < n; j++)
            if (a[j] «<» a[vt])
                vt = j;
        swap(a[i], a[vt]);
    }
}
"""

INSERTION = """
void InsertionSort(int a[], int n)
{
    for (int i = 1; i < n; i++)
    {
        int x = a[i], j = i - 1;
        while (j >= 0 && a[j] «>» x)        // dồn các phần tử lớn hơn x sang phải
        {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = x;                       // chèn x vào chỗ trống
    }
}
"""

BUBBLE = """
void BubbleSort(int a[], int n)
{
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - 1 - i; j++)
            if (a[j] «>» a[j + 1])
                swap(a[j], a[j + 1]);
}
"""

MERGE = """
void Merge(int a[], int dau, int giua, int cuoi)
{
    int b[1000], i = dau, j = giua + 1, k = 0;
    while (i <= giua && j <= cuoi)
        if (a[i] «<=» a[j]) b[k++] = a[i++];
        else b[k++] = a[j++];
    while (i <= giua) b[k++] = a[i++];
    while (j <= cuoi) b[k++] = a[j++];
    for (i = dau, k = 0; i <= cuoi; i++) a[i] = b[k++];
}
void MergeSort(int a[], int dau, int cuoi)
{
    if (dau < cuoi)
    {
        int giua = (dau + cuoi) / 2;
        MergeSort(a, dau, giua);
        MergeSort(a, giua + 1, cuoi);
        Merge(a, dau, giua, cuoi);
    }
}
"""

QUICK = """
void QuickSort(int a[], int dau, int cuoi)
{
    int i = dau, j = cuoi, x = a[(dau + cuoi) / 2];   // pivot = phần tử giữa
    while (i <= j)
    {
        while (a[i] «<» x) i++;
        while (a[j] «>» x) j--;
        if (i <= j)
        {
            swap(a[i], a[j]);
            i++;
            j--;
        }
    }
    if (dau < j) QuickSort(a, dau, j);
    if (i < cuoi) QuickSort(a, i, cuoi);
}
"""

TIM = """
int timTuanTu(int a[], int n, int x)
{
    for (int i = 0; i < n; i++)
        if (a[i] == x) return i;
    return -1;
}
int timNhiPhan(int a[], int n, int x)       // a đã tăng dần
{
    int dau = 0, cuoi = n - 1;
    while (dau <= cuoi)
    {
        int giua = (dau + cuoi) / 2;
        if (a[giua] == x) return giua;
        if (a[giua] < x) dau = giua + 1;
        else cuoi = giua - 1;
    }
    return -1;
}
"""

CAU8_MAIN = """
int main()
{
    nutCay *t = taoNut(8);
    t->trai = taoNut(3);                   t->phai = taoNut(10);
    t->trai->trai = taoNut(1);             t->trai->phai = taoNut(6);
    t->phai->phai = taoNut(14);
    t->trai->trai->trai = taoNut(-2);
    t->trai->phai->trai = taoNut(4);       t->trai->phai->phai = taoNut(7);
    cout << tongDuong(t);                  // 53
}
"""
