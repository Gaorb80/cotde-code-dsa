# Tài liệu cô Hồng: Sắp xếp, Tìm kiếm, Cây

Tổng hợp từ nhóm Zalo (5 ảnh + `de_quy.txt`). Phần "Lời giải" do mình tự làm, có chạy kiểm tra, không phải của cô. Hai ảnh 1 và 2 đã được đối chiếu lại với ảnh gốc.

Mục lục: [1. Cây nhị phân tìm kiếm](#1-cây-nhị-phân-tìm-kiếm-bst-dựng-cây-và-hủy-nút) · [2. Sắp xếp](#2-các-thuật-toán-sắp-xếp) · [3. Merge sort](#3-minh-họa-merge-sort) · [4. Tìm nhị phân](#4-tìm-kiếm-nhị-phân) · [5. Cây và đệ quy](#5-cây-nhị-phân-và-đệ-quy-de_quytxt) · [6. Mẹo thi](#6-mẹo-thi)

---

## 1. Cây nhị phân tìm kiếm (BST): dựng cây và hủy nút

*(Ảnh 1)*

**Bài 1**

a) Minh họa giải thuật dựng cây nhị phân tìm kiếm với dãy khóa nhập vào theo thứ tự: `18 13 15 12 20 11 30 19 28 14`

b) Sau đó, lần lượt thực hiện các thao tác trên cây dựng được ở câu a):
- Hủy nút có giá trị 30
- Hủy nút có giá trị 20

thì cây thay đổi như thế nào trong từng bước? Vẽ cây minh họa và giải thích.

**Bài 2**

a) Dựng cây nhị phân tìm kiếm với dãy khóa: `51 31 43 29 65 10 20 36 78 59 15 45 55`

b) Sau đó lần lượt:
- Hủy nút có giá trị 36
- Hủy nút có giá trị 43

thì cây thay đổi như thế nào trong từng bước? Vẽ cây minh họa và giải thích.

### Lời giải (tự làm)

Quy tắc dựng: bắt đầu từ cây rỗng, thêm lần lượt từng khóa; nhỏ hơn nút đang xét thì sang trái, lớn hơn thì sang phải, gặp chỗ trống thì đặt nút mới.

**Bài 1a: cây sau khi dựng**

```
            18
        13      20
      12  15   19  30
     11  14       28
```

**Bài 1b**
- Hủy 30: nút 30 chỉ có một con (28 bên trái), nên nối cha của 30 (là 20) thẳng tới 28 rồi delete 30.
- Hủy 20: nút 20 có hai con (19 và 28). Hai cách thế mạng:
  - Cách hai (theo sách và code của cô): trái nhất của cây con phải. Cây con phải của 20 lúc này chỉ có 28, nên chép 28 lên nút 20, rồi hủy nút 28 cũ. Kết quả: nút 28 có con trái là 19.
  - Cách một: phải nhất của cây con trái là 19. Chép 19 lên nút 20, rồi hủy nút 19 cũ. Kết quả: nút 19 có con phải là 28.

```
Cách hai:        18               Cách một:        18
             13      28                        13      19
           12  15   19                        12  15      28
          11  14                             11  14
```

**Bài 2a: cây sau khi dựng**

```
                 51
          31              65
       29     43        59    78
     10      36 45        55
       20
      15
```

**Bài 2b**
- Hủy 36: là nút lá, chỉ cần cho con trái của 43 bằng `NULL` rồi delete.
- Hủy 43: lúc này 43 chỉ còn con phải là 45, nên nối con phải của 31 thẳng tới 45 rồi delete 43.

```
Sau khi hủy cả hai:     51
                  31          65
               29    45     59    78
             10               55
               20
              15
```

---

## 2. Các thuật toán sắp xếp

*(Ảnh 2)*

**a) Mô tả và viết hàm** thực hiện các thuật toán sắp xếp:

| # | Thuật toán | Thứ tự |
|---|---|---|
| 1 | Chọn (Selection Sort) | tăng dần |
| 2 | Chọn (Selection Sort) | giảm dần |
| 3 | Chèn (Insertion Sort) | tăng dần |
| 4 | Chèn (Insertion Sort) | giảm dần |
| 5 | Nổi bọt (Bubble Sort) | tăng dần |
| 6 | Nổi bọt (Bubble Sort) | giảm dần |
| 7 | Trộn (Merge Sort) | tăng dần |
| 8 | Trộn (Merge Sort) | giảm dần |
| 9 | Nhanh (Quick Sort) | tăng dần |
| 10 | Nhanh (Quick Sort) | giảm dần |

**b) Trình bày các bước** của mỗi thuật toán với dãy số sau:

1. `9, 1, 2, 10, 8, 5, 7, 4, 6`
2. `5, 15, 12, 2, 10, 12, 9, 1, 9, 3, 2, 3`
3. `51, 61, 21, 12, 101, 121, 91, 101, 91, 31`

Code tăng dần của Selection, Bubble, Quick, Merge: xem `code_tuan_anh.cpp`. Muốn **giảm dần** chỉ đổi dấu so sánh (`<` thành `>` và ngược lại). Insertion Sort chưa có trong code của Tuấn Anh, nên tự viết:

```cpp
void InsertionSort(int a[], int n) // tăng dần
{
    for(int i = 1; i < n; i++)
    {
        int x = a[i], j = i - 1;
        while(j >= 0 && a[j] > x)
        {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = x;
    }
}
```

---

## 3. Minh họa Merge sort

*(Ảnh 3: ảnh không có tiêu đề, chỉ có sơ đồ chia đôi dãy rồi trộn lại.)*

Dãy ban đầu: `[5, 15, 12, 2, 10, 12, 9, 1, 9, 3, 2, 3]`

Chia đôi:

```
[5, 15, 12, 2, 10, 12, 9, 1, 9, 3, 2, 3]
├── [5, 15, 12, 2, 10, 12]
│   ├── [5, 15, 12]
│   │   ├── [5, 15]
│   │   │   ├── [5]
│   │   │   └── [15]
│   │   └── [12]
│   └── [2, 10, 12]
│       ├── [2, 10]
│       │   ├── [2]
│       │   └── [10]
│       └── [12]
└── [9, 1, 9, 3, 2, 3]
    ├── [9, 1, 9]
    │   ├── [9, 1]
    │   │   ├── [9]
    │   │   └── [1]
    │   └── [9]
    └── [3, 2, 3]
        ├── [3, 2]
        │   ├── [3]
        │   └── [2]
        └── [3]
```

Trộn lại:

```
[5, 15] + [12]          -> [5, 12, 15]
[2, 10] + [12]          -> [2, 10, 12]
[9, 1]  + [9]           -> [1, 9, 9]
[3, 2]  + [3]           -> [2, 3, 3]

[5, 12, 15] + [2, 10, 12]   -> [2, 5, 10, 12, 12, 15]
[1, 9, 9]   + [2, 3, 3]     -> [1, 2, 3, 3, 9, 9]

[2, 5, 10, 12, 12, 15] + [1, 2, 3, 3, 9, 9]
                            -> [1, 2, 2, 3, 3, 5, 9, 9, 10, 12, 12, 15]
```

Ảnh đóng khung các phần tử 12, 12, 9, 3; ảnh không giải thích ý nghĩa khung.

---

## 4. Tìm kiếm nhị phân

*(Ảnh 4 và 5, hai ảnh nối tiếp nhau của cùng một ví dụ)*

**Ví dụ 5.** Cho `A = {-8, -5, 0, 4, 15, 20, 50, 63, 75, 98}` và `x = 20`. Dùng tìm kiếm nhị phân để xác định x có trong dãy hay không?

Vị trí tính từ 1:

| Vị trí | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Giá trị | -8 | -5 | 0 | 4 | 15 | 20 | 50 | 63 | 75 | 98 |

Mỗi lượt lấy phần tử ở giữa ("trung vị") của không gian tìm kiếm rồi thu hẹp một nửa:

- **Lượt 1:** không gian tìm kiếm S = [1, 10]. Trung vị là A[5] = 15 < 20 = x. Mảng tăng dần nên các phần tử từ vị trí 1 đến 5 đều nhỏ hơn x, chắc chắn không phải kết quả. Giảm một nửa: S = [6, 10].
- **Lượt 2:** trung vị là A[8] = 63 > 20 = x. Các phần tử từ vị trí 9 đến 10 đều lớn hơn x. Giảm một nửa: S = [6, 7].
- **Lượt 3:** S = [6, 7] có số phần tử chẵn nên có hai trung vị, chọn trung vị đầu tiên là vị trí 6. A[6] = 20 = x, **kết luận x có trong mảng A**.

Code: `nhiphan(a, n, x)` trong `code_tuan_anh.cpp`. Nhớ điều kiện: mảng phải được sắp tăng dần.

---

## 5. Cây nhị phân và đệ quy (`de_quy.txt`)

6 bài tập, file gốc không có đáp án:

1. Viết khai báo biểu diễn một cây nhị phân bằng phương pháp lưu trữ móc nối, trong đó mỗi nút lưu trữ một số nguyên.
2. Viết thủ tục bổ sung giá trị x vào cây nhị phân tìm kiếm có gốc được trỏ bởi con trỏ T.
3. Viết hàm đệ quy đếm số nút của một cây nhị phân.
4. Viết hàm đệ quy đếm số nút có giá trị lẻ của một cây nhị phân.
5. Viết hàm đệ quy tính tổng giá trị của các nút có trên cây.
6. Viết hàm đệ quy tính tổng giá trị của các nút có giá trị dương trên cây nhị phân.

### Lời giải (tự làm, chạy được: xem `cau8_mau.cpp` và `../04-cay-nhi-phan-bst/cay_nhi_phan.cpp`)

```cpp
struct nutCay
{
    int duLieu;
    nutCay *trai;
    nutCay *phai;
};

void boSung(nutCay *&t, int x)          // bài 2
{
    if (t == NULL)
    {
        t = new nutCay;
        t->duLieu = x;
        t->trai = t->phai = NULL;
    }
    else if (x < t->duLieu)
        boSung(t->trai, x);
    else if (x > t->duLieu)
        boSung(t->phai, x);
}

int demNut(nutCay *t)                    // bài 3
{
    if (t == NULL) return 0;
    return 1 + demNut(t->trai) + demNut(t->phai);
}

int demLe(nutCay *t)                     // bài 4
{
    if (t == NULL) return 0;
    if (t->duLieu % 2 != 0)              // không viết == 1: -15 % 2 bằng -1
        return 1 + demLe(t->trai) + demLe(t->phai);
    return demLe(t->trai) + demLe(t->phai);
}

long long tongNut(nutCay *t)             // bài 5
{
    if (t == NULL) return 0;
    return t->duLieu + tongNut(t->trai) + tongNut(t->phai);
}

long long tongDuong(nutCay *t)           // bài 6
{
    if (t == NULL) return 0;
    if (t->duLieu > 0)
        return t->duLieu + tongDuong(t->trai) + tongDuong(t->phai);
    return tongDuong(t->trai) + tongDuong(t->phai);
}
```

---

## 6. Mẹo thi

- **Khung đệ quy trên cây 3 bước:** (1) cây rỗng trả 0, (2) phần đóng góp của nút t, (3) gộp: phần của nút + kết quả trái + kết quả phải.
- **Ba kiểu duyệt chỉ khác vị trí dòng in:** trước = gốc, trái, phải; giữa = trái, gốc, phải; sau = trái, phải, gốc.
- **Duyệt giữa của BST luôn tăng dần.** Dùng để tự kiểm tra cây đã dựng đúng chưa.
- **Hủy nút hai con:** chép khóa của nút thế mạng lên nút cần hủy, rồi hủy nút thế mạng cũ (nút này có tối đa một con). Nói rõ dùng cách một hay cách hai.
- **Tổng nút dương:** phải cộng giá trị `t->duLieu`, đừng chỉ đếm (`t->duLieu > 0`). Đây là lỗi có trong code gốc của Tuấn Anh.
- **Tìm nhị phân:** mảng phải tăng dần, mỗi lượt loại một nửa không gian tìm kiếm.
