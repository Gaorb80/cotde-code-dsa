// Cốt Đê – 5 thuật toán sắp xếp bằng C++
// Video: <link YouTube>
//
// Một dãy mẫu chạy qua cả năm chiêu: 9 1 2 10 8 5 7 4 6 (xếp tăng dần).
//   Chiêu 1  Sắp xếp Chọn (Selection Sort)  : mỗi lượt tìm số nhỏ nhất, đưa lên đầu phần chưa xếp
//   Chiêu 2  Sắp xếp Chèn (Insertion Sort)  : bốc từng số, chèn vào đúng kẽ trong phần đã xếp
//   Chiêu 3  Sắp xếp Nổi bọt (Bubble Sort)  : hai số sát nhau so kè, số to lùi về sau
//   Chiêu 4  Sắp xếp Trộn (Merge Sort)      : chia đôi tới khi còn 1 số, rồi gộp lại theo đầu hàng
//   Chiêu 5  Sắp xếp Nhanh (Quick Sort)     : chọn một số làm trọng tài, chia hai phe nhỏ hơn / lớn hơn
//
// Biên dịch: g++ -std=c++17 -Wall -Wextra sap_xep.cpp -o sap_xep
// Chạy xong sẽ in từng bước của mỗi chiêu, kèm số lần so sánh để đối chiếu với video.

#include <iostream>
using namespace std;

const int N = 9;                 // dãy có 9 số
int demSoSanh = 0;               // đếm số lần so sánh hai số, để so các chiêu với nhau

// in dãy ra màn hình, ví dụ: 9 1 2 10 8 5 7 4 6
void inDay(int a[], int n) {
    for (int i = 0; i < n; i++) cout << a[i] << " ";
    cout << "\n";
}

// đổi chỗ hai số
void doiCho(int& x, int& y) {
    int tam = x;
    x = y;
    y = tam;
}

// ============================================================
// Chiêu 1 · Sắp xếp Chọn
// Lượt i: tìm số nhỏ nhất trong phần chưa xếp (từ i đến cuối), đổi chỗ nó với số ở vị trí i.
// ============================================================
void sapXepChon(int a[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int nhoNhat = i;                         // tạm coi số ở vị trí i là nhỏ nhất
        for (int j = i + 1; j < n; j++) {
            demSoSanh++;
            if (a[j] < a[nhoNhat]) nhoNhat = j;  // gặp số nhỏ hơn thì nhớ vị trí của nó
        }
        if (nhoNhat != i) doiCho(a[i], a[nhoNhat]);
        cout << "Luot " << i + 1 << ": ";
        inDay(a, n);
    }
}

// ============================================================
// Chiêu 2 · Sắp xếp Chèn
// Phần a[0..i-1] đã xếp. Bốc số a[i], dời các số lớn hơn nó sang phải một ô, rồi đặt nó vào chỗ trống.
// ============================================================
void sapXepChen(int a[], int n) {
    for (int i = 1; i < n; i++) {
        int dangCam = a[i];                      // lá bài vừa bốc
        int j = i - 1;
        while (j >= 0) {
            demSoSanh++;
            if (a[j] <= dangCam) break;          // gặp số bé hơn hoặc bằng: đã tới đúng kẽ
            a[j + 1] = a[j];                     // số lớn hơn thì lùi sang phải một ô
            j--;
        }
        a[j + 1] = dangCam;                      // chèn vào kẽ vừa mở
        cout << "Boc " << dangCam << ": ";
        inDay(a, n);
    }
}

// ============================================================
// Chiêu 3 · Sắp xếp Nổi bọt
// Mỗi lượt đi từ đầu dãy, so hai số sát nhau, số to hơn thì đổi chỗ ra sau.
// Cuối lượt, số to nhất của phần chưa xếp nổi lên đuôi. Lượt nào không đổi chỗ lần nào thì dừng sớm.
// ============================================================
void sapXepNoiBot(int a[], int n) {
    for (int luot = 1; luot < n; luot++) {
        bool daDoiCho = false;                   // cờ: lượt này có đổi chỗ không?
        for (int j = 0; j < n - luot; j++) {     // n - luot: các số cuối đã đúng chỗ, khỏi so nữa
            demSoSanh++;
            if (a[j] > a[j + 1]) {
                doiCho(a[j], a[j + 1]);
                daDoiCho = true;
            }
        }
        cout << "Luot " << luot << ": ";
        inDay(a, n);
        if (!daDoiCho) break;                    // không đổi chỗ lần nào: dãy đã xếp xong
    }
}

// ============================================================
// Chiêu 4 · Sắp xếp Trộn
// Chia đôi dãy cho tới khi mỗi nhóm còn 1 số, rồi gộp từng cặp nhóm lại theo đầu hàng.
// Gộp cần một mảng phụ để đặt tạm kết quả (tốn thêm bộ nhớ).
// ============================================================
void gop(int a[], int dau, int giua, int cuoi) {
    int phu[N];                                  // mảng phụ
    int i = dau;                                 // đầu hàng của nhóm trái
    int j = giua + 1;                            // đầu hàng của nhóm phải
    int k = 0;
    while (i <= giua && j <= cuoi) {
        demSoSanh++;
        if (a[i] <= a[j]) phu[k++] = a[i++];     // nhặt đứa bé hơn ra trước (bằng nhau thì nhặt nhóm trái: giữ thứ tự)
        else              phu[k++] = a[j++];
    }
    while (i <= giua) phu[k++] = a[i++];         // nhóm nào còn dư thì nhặt nốt
    while (j <= cuoi) phu[k++] = a[j++];
    for (k = 0; k < cuoi - dau + 1; k++) a[dau + k] = phu[k];   // chép kết quả về chỗ cũ
    cout << "Gop [" << dau << ".." << cuoi << "]: ";
    for (int t = dau; t <= cuoi; t++) cout << a[t] << " ";
    cout << "\n";
}

void sapXepTron(int a[], int dau, int cuoi) {
    if (dau >= cuoi) return;                     // nhóm chỉ còn 1 số: khỏi xếp
    int giua = (dau + cuoi) / 2;
    sapXepTron(a, dau, giua);                    // xếp nửa trái
    sapXepTron(a, giua + 1, cuoi);               // xếp nửa phải
    gop(a, dau, giua, cuoi);                     // gộp hai nửa đã xếp
}

// ============================================================
// Chiêu 5 · Sắp xếp Nhanh
// Lấy số cuối đoạn làm trọng tài. Số nhỏ hơn trọng tài dồn sang trái, số lớn hơn sang phải,
// rồi đặt trọng tài vào giữa: nó đứng đúng chỗ vĩnh viễn. Sau đó làm tiếp với hai phe.
// ============================================================
int chiaPhe(int a[], int dau, int cuoi) {
    int trongTai = a[cuoi];
    int bien = dau;                              // a[dau..bien-1] là phe nhỏ hơn trọng tài
    for (int j = dau; j < cuoi; j++) {
        demSoSanh++;
        if (a[j] < trongTai) {
            doiCho(a[bien], a[j]);
            bien++;
        }
    }
    doiCho(a[bien], a[cuoi]);                    // đặt trọng tài vào giữa hai phe
    cout << "Trong tai " << trongTai << " dung o vi tri " << bien << ": ";
    inDay(a, N);
    return bien;
}

void sapXepNhanh(int a[], int dau, int cuoi) {
    if (dau >= cuoi) return;
    int viTri = chiaPhe(a, dau, cuoi);
    sapXepNhanh(a, dau, viTri - 1);              // phe nhỏ hơn
    sapXepNhanh(a, viTri + 1, cuoi);             // phe lớn hơn
}

// ============================================================
// Chạy thử cả năm chiêu trên cùng một dãy
// ============================================================
void chepDay(int nguon[], int dich[], int n) {
    for (int i = 0; i < n; i++) dich[i] = nguon[i];
}

int main() {
    int goc[N] = {9, 1, 2, 10, 8, 5, 7, 4, 6};
    int a[N];

    cout << "=== Chieu 1: Chon ===\n";
    chepDay(goc, a, N); demSoSanh = 0;
    sapXepChon(a, N);
    cout << "So lan so sanh: " << demSoSanh << "\n\n";

    cout << "=== Chieu 2: Chen ===\n";
    chepDay(goc, a, N); demSoSanh = 0;
    sapXepChen(a, N);
    cout << "So lan so sanh: " << demSoSanh << "\n\n";

    cout << "=== Chieu 3: Noi bot ===\n";
    chepDay(goc, a, N); demSoSanh = 0;
    sapXepNoiBot(a, N);
    cout << "So lan so sanh: " << demSoSanh << "\n\n";

    cout << "=== Chieu 4: Tron ===\n";
    chepDay(goc, a, N); demSoSanh = 0;
    sapXepTron(a, 0, N - 1);
    cout << "So lan so sanh: " << demSoSanh << "\n\n";

    cout << "=== Chieu 5: Nhanh ===\n";
    chepDay(goc, a, N); demSoSanh = 0;
    sapXepNhanh(a, 0, N - 1);
    cout << "So lan so sanh: " << demSoSanh << "\n";

    return 0;
}

// Thử tự làm: dãy 5 1 4 2 3, xếp bằng Nổi bọt, sau lượt 1 dãy trông thế nào? (câu hỏi cuối video)
