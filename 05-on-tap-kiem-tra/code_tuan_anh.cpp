// Ôn tập: sắp xếp, tìm kiếm, cây, stack, queue
// Nguồn: code của Tuấn Anh (học với cô Hồng), gom 9 file thành 1 file, chạy bằng menu.
// Biên dịch: g++ -std=c++17 -Wall -Wextra code_tuan_anh.cpp -o on_tap
//
// ĐÃ KIỂM TRA LOGIC (so với bản gốc):
//   [SỬA]  tongduong: bản gốc viết (khoa > 0) + ..., chỉ ĐẾM nút dương chứ không CỘNG giá trị.
//          Sửa thành (khoa > 0 ? khoa : 0). Đúng loại câu c) của đề: "tổng các nút có giá trị dương".
//   [SỬA]  Merge: a[i] < a[j] đổi thành a[i] <= a[j] để sắp xếp ổn định (bằng nhau thì giữ thứ tự cũ).
//   [SỬA]  Tên file bản gốc "sx_chon(Quick_Sort)": chọn là Selection, Quick là sắp xếp nhanh.
//   [ĐÚNG] Selection, Bubble, Quick (Hoare, lấy phần tử giữa), Merge, tìm tuần tự, tìm nhị phân,
//          chen/duyệt/dem/demle/tongnut trên cây, stack, queue: logic đúng.
//   [LƯU Ý] Tìm nhị phân chỉ đúng khi mảng đã sắp xếp tăng dần.
//   [LƯU Ý] top/front/back trả -1 khi rỗng: lẫn với khóa thật là -1, đủ dùng khi ôn thi.
//   [LƯU Ý] Queue::push đi hết danh sách để nối cuối (O(n)); chạy đúng, chậm hơn khi giữ thêm con trỏ cuối.
//   [LƯU Ý] Chương trình gốc không delete cây/stack/queue; ở đây giữ nguyên cho gọn.
//
// PHONG CÁCH CODE CỦA TUẤN ANH:
//   - #include<bits/stdc++.h> + using namespace std;
//   - tên tiếng Việt không dấu, viết thường liền nhau: taonut, khoitao, tongnut, demle, chen, duyet
//   - cây: struct Nut { khoa, trai, phai }; typedef Nut* cay;  (stack/queue: Nut { khoa, tiep })
//   - dấu ngoặc nhọn xuống dòng (Allman), thụt lề 4 ô, if một dòng không cần {}
//   - hàm dùng con trỏ tham chiếu Stack &s, cay &t để sửa thẳng vào cấu trúc
//   - mỗi bài: nhập n rồi nhập từng phần tử, in kết quả bằng cout << ... << " "
//   - tên sắp xếp/tìm kiếm viết hoa chữ đầu: SelectionSort, BubbleSort, QuickSort, MergeSort

#include<bits/stdc++.h>
using namespace std;

// ============================================================
// SẮP XẾP
// ============================================================

namespace sapxep
{
    void SelectionSort(int a[], int n)
    {
        for(int i = 0; i < n - 1; i++)
        {
            int min = i;

            for(int j = i + 1; j < n; j++)
                if(a[j] < a[min])
                    min = j;

            swap(a[i], a[min]);
        }
    }

    void BubbleSort(int a[], int n)
    {
        for(int i = 0; i < n - 1; i++)
            for(int j = 0; j < n - 1 - i; j++)
                if(a[j] > a[j + 1])
                    swap(a[j], a[j + 1]);
    }

    void QuickSort(int a[], int l, int r)
    {
        int i = l, j = r;
        int x = a[(l + r) / 2];

        while(i <= j)
        {
            while(a[i] < x) i++;
            while(a[j] > x) j--;

            if(i <= j)
            {
                swap(a[i], a[j]);
                i++;
                j--;
            }
        }

        if(l < j)
            QuickSort(a, l, j);

        if(i < r)
            QuickSort(a, i, r);
    }

    void Merge(int a[], int l, int m, int r)
    {
        int b[1000];
        int i = l, j = m + 1, k = 0;

        while(i <= m && j <= r)
        {
            if(a[i] <= a[j])
                b[k++] = a[i++];
            else
                b[k++] = a[j++];
        }

        while(i <= m)
            b[k++] = a[i++];

        while(j <= r)
            b[k++] = a[j++];

        for(i = l, k = 0; i <= r; i++)
            a[i] = b[k++];
    }

    void MergeSort(int a[], int l, int r)
    {
        if(l < r)
        {
            int m = (l + r) / 2;

            MergeSort(a, l, m);
            MergeSort(a, m + 1, r);

            Merge(a, l, m, r);
        }
    }
}

// ============================================================
// TÌM KIẾM
// ============================================================

namespace timkiem
{
    int tuantu(int a[], int n, int x)
    {
        for(int i = 0; i < n; i++)
            if(a[i] == x)
                return i;

        return -1;
    }

    int nhiphan(int a[], int n, int x) // a đã sắp tăng dần
    {
        int l = 0, r = n - 1;

        while(l <= r)
        {
            int mid = (l + r) / 2;

            if(a[mid] == x)
                return mid;
            else if(a[mid] < x)
                l = mid + 1;
            else
                r = mid - 1;
        }

        return -1;
    }
}

// ============================================================
// CÂY NHỊ PHÂN TÌM KIẾM
// ============================================================

namespace caynp
{
    struct Nut
    {
        int khoa;
        Nut *trai, *phai;
    };
    typedef Nut* cay;

    cay taonut(int x)
    {
        cay p = new Nut;
        p->khoa = x;
        p->trai = p->phai = NULL;
        return p;
    }

    void chen(cay &t, int x)
    {
        if(t == NULL)
            t = taonut(x);
        else if(t->khoa < x)
            chen(t->phai, x);
        else if(t->khoa > x)
            chen(t->trai, x);
        // bằng nhau: đã có, bỏ qua
    }

    void duyet(cay t) // thứ tự trước: gốc, trái, phải
    {
        if(t != NULL)
        {
            cout << t->khoa << " ";
            duyet(t->trai);
            duyet(t->phai);
        }
    }

    int dem(cay t)
    {
        if(t == NULL) return 0;
        return 1 + dem(t->trai) + dem(t->phai);
    }

    int demle(cay t)
    {
        if(t == NULL) return 0;
        return (t->khoa % 2 != 0) + demle(t->trai) + demle(t->phai);
    }

    int tongnut(cay t)
    {
        if(t == NULL) return 0;
        return t->khoa + tongnut(t->trai) + tongnut(t->phai);
    }

    int tongduong(cay t)
    {
        if(t == NULL) return 0;
        return (t->khoa > 0 ? t->khoa : 0) + tongduong(t->trai) + tongduong(t->phai);
    }
}

// ============================================================
// STACK (danh sách liên kết)
// ============================================================

namespace ngxep
{
    struct Nut
    {
        int khoa;
        Nut *tiep;
    };
    typedef Nut* Stack;

    Stack taonut(int x)
    {
        Stack p = new Nut;
        p->khoa = x;
        p->tiep = NULL;
        return p;
    }

    void khoitao(Stack &s)
    {
        s = NULL;
    }

    bool rong(Stack s)
    {
        return s == NULL;
    }

    void push(Stack &s, int x)
    {
        Stack p = taonut(x);
        p->tiep = s;
        s = p;
    }

    void pop(Stack &s)
    {
        if(s == NULL)
            return;

        Stack p = s;
        s = s->tiep;
        delete p;
    }

    int top(Stack s)
    {
        if(s == NULL)
            return -1;

        return s->khoa;
    }

    int dem(Stack s)
    {
        if(s == NULL)
            return 0;

        return 1 + dem(s->tiep);
    }

    void xuat(Stack s)
    {
        while(s != NULL)
        {
            cout << s->khoa << " ";
            s = s->tiep;
        }
    }
}

// ============================================================
// QUEUE (danh sách liên kết)
// ============================================================

namespace hangdoi
{
    struct Nut
    {
        int khoa;
        Nut *tiep;
    };
    typedef Nut* Queue;

    Queue taonut(int x)
    {
        Queue p = new Nut;
        p->khoa = x;
        p->tiep = NULL;
        return p;
    }

    void khoitao(Queue &q)
    {
        q = NULL;
    }

    bool rong(Queue q)
    {
        return q == NULL;
    }

    void push(Queue &q, int x)
    {
        Queue p = taonut(x);

        if(q == NULL)
            q = p;
        else
        {
            Queue tam = q;
            while(tam->tiep != NULL)
                tam = tam->tiep;

            tam->tiep = p;
        }
    }

    void pop(Queue &q)
    {
        if(q == NULL)
            return;

        Queue p = q;
        q = q->tiep;
        delete p;
    }

    int front(Queue q)
    {
        if(q == NULL)
            return -1;

        return q->khoa;
    }

    int back(Queue q)
    {
        if(q == NULL)
            return -1;

        while(q->tiep != NULL)
            q = q->tiep;

        return q->khoa;
    }

    int dem(Queue q)
    {
        if(q == NULL)
            return 0;

        return 1 + dem(q->tiep);
    }

    void xuat(Queue q)
    {
        while(q != NULL)
        {
            cout << q->khoa << " ";
            q = q->tiep;
        }
    }
}

// ============================================================
// CHƯƠNG TRÌNH CHẠY THỬ (menu)
// ============================================================

void nhapmang(int a[], int &n)
{
    cout << "Nhap n: ";
    cin >> n;

    for(int i = 0; i < n; i++)
    {
        cout << "a[" << i << "] = ";
        cin >> a[i];
    }
}

void xuatmang(int a[], int n)
{
    cout << "Mang: ";
    for(int i = 0; i < n; i++)
        cout << a[i] << " ";
    cout << "\n";
}

void chaysapxep(int chon)
{
    int a[100], n;
    nhapmang(a, n);

    if(chon == 1) sapxep::SelectionSort(a, n);
    if(chon == 2) sapxep::BubbleSort(a, n);
    if(chon == 3) sapxep::QuickSort(a, 0, n - 1);
    if(chon == 4) sapxep::MergeSort(a, 0, n - 1);

    cout << "Sau khi sap xep. ";
    xuatmang(a, n);
}

void chaytimkiem(int chon)
{
    int a[100], n, x;
    nhapmang(a, n);

    cout << "Nhap x can tim: ";
    cin >> x;

    int k = (chon == 5) ? timkiem::tuantu(a, n, x) : timkiem::nhiphan(a, n, x);

    if(k == -1)
        cout << "Khong tim thay x\n";
    else
        cout << "Tim thay x tai vi tri: " << k << "\n";
}

void chaycay()
{
    caynp::cay t = NULL;
    int n, x;

    cout << "Nhap so nut: ";
    cin >> n;

    for(int i = 0; i < n; i++)
    {
        cout << "Nhap gia tri: ";
        cin >> x;
        caynp::chen(t, x);
    }

    cout << "duyet cay: ";
    caynp::duyet(t);
    cout << "\nso nut cua cay: " << caynp::dem(t);
    cout << "\nso nut le: " << caynp::demle(t);
    cout << "\ntong nut: " << caynp::tongnut(t);
    cout << "\ntong cac nut duong: " << caynp::tongduong(t) << "\n";
}

void chaystack()
{
    ngxep::Stack s;
    ngxep::khoitao(s);

    int n, x;
    cout << "Nhap so phan tu: ";
    cin >> n;

    for(int i = 0; i < n; i++)
    {
        cout << "Nhap gia tri: ";
        cin >> x;
        ngxep::push(s, x);
    }

    cout << "Stack: ";
    ngxep::xuat(s);
    cout << "\nPhan tu dau Stack: " << ngxep::top(s);
    cout << "\nSo phan tu Stack: " << ngxep::dem(s);

    ngxep::pop(s);
    cout << "\nStack sau khi Pop: ";
    ngxep::xuat(s);
    cout << "\n";
}

void chayqueue()
{
    hangdoi::Queue q;
    hangdoi::khoitao(q);

    int n, x;
    cout << "Nhap so phan tu: ";
    cin >> n;

    for(int i = 0; i < n; i++)
    {
        cout << "Nhap gia tri: ";
        cin >> x;
        hangdoi::push(q, x);
    }

    cout << "Queue: ";
    hangdoi::xuat(q);
    cout << "\nPhan tu dau Queue: " << hangdoi::front(q);
    cout << "\nPhan tu cuoi Queue: " << hangdoi::back(q);
    cout << "\nSo phan tu Queue: " << hangdoi::dem(q);

    hangdoi::pop(q);
    cout << "\nQueue sau khi Pop: ";
    hangdoi::xuat(q);
    cout << "\n";
}

int main()
{
    cout << "1 Selection  2 Bubble  3 Quick  4 Merge\n";
    cout << "5 Tim tuan tu  6 Tim nhi phan (mang tang dan)\n";
    cout << "7 Cay nhi phan tim kiem  8 Stack  9 Queue\n";
    cout << "Chon: ";

    int chon;
    cin >> chon;

    if(chon >= 1 && chon <= 4) chaysapxep(chon);
    else if(chon == 5 || chon == 6) chaytimkiem(chon);
    else if(chon == 7) chaycay();
    else if(chon == 8) chaystack();
    else if(chon == 9) chayqueue();

    return 0;
}
