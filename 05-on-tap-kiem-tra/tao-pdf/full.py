# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import *

parts = []
add = parts.append


def fig(*items):
    return '<div class="fig">' + ''.join(items) + '</div>'


def f3(seq, name, hg=34):
    return (f'<figure>{svg_tree(CAU8, badges={v: i + 1 for i, v in enumerate(seq)}, hg=hg, vg=40, r=13)}'
            f'<figcaption><b>{name}</b>: {fmt(seq)}</figcaption></figure>')


def path_of(t, x):
    out, cur = [], t
    while cur is not None:
        out.append(cur.v)
        if x < cur.v:
            cur = cur.l
        elif x > cur.v:
            cur = cur.r
        else:
            break
    return out


def insertion_table(seq):
    rows, t = [], None
    for k in seq:
        if t is None:
            rows.append(f'<tr><td class="c"><b>{k}</b></td><td>Cây rỗng, nên {k} là <b>gốc</b></td></tr>')
            t = N(k)
            continue
        steps, cur = [], t
        while True:
            if k < cur.v:
                steps.append(f'{k} &lt; {cur.v}, sang trái')
                if cur.l is None:
                    cur.l = N(k)
                    last = f'đặt làm con <b>trái</b> của {cur.v}'
                    break
                cur = cur.l
            else:
                steps.append(f'{k} &gt; {cur.v}, sang phải')
                if cur.r is None:
                    cur.r = N(k)
                    last = f'đặt làm con <b>phải</b> của {cur.v}'
                    break
                cur = cur.r
        rows.append(f'<tr><td class="c"><b>{k}</b></td><td>{"; ".join(steps)} → {last}</td></tr>')
    return '<table><tr><th style="width:14mm">Khóa</th><th>Đường đi từ gốc</th></tr>' + ''.join(rows) + '</table>'


def bs_rows(A, x):
    """Tim nhi phan theo kieu co (vi tri dem tu 1)."""
    n = len(A)
    lo, hi, k = 1, n, 1
    rows = []
    while lo <= hi:
        mid = (lo + hi) // 2
        out = []
        for i in range(1, n + 1):
            cls = 'c'
            if i < lo or i > hi:
                cls += ' d'
            if i == mid:
                cls += ' h'
            out.append(f'<span class="{cls}" style="min-width:9mm">{A[i - 1]}</span>')
        if A[mid - 1] == x:
            note = f'A[{mid}] = {A[mid - 1]} = x → <b>tìm thấy</b>'
        elif A[mid - 1] < x:
            note = f'A[{mid}] = {A[mid - 1]} &lt; {x} → bỏ nửa trái, [{mid + 1}..{hi}]'
        else:
            note = f'A[{mid}] = {A[mid - 1]} &gt; {x} → bỏ nửa phải, [{lo}..{mid - 1}]'
        rows.append(f'<div class="tr"><span class="lb">Lượt {k}<br>[{lo}..{hi}]</span><span class="arr">{"".join(out)}</span> <span class="note">{note}</span></div>')
        if A[mid - 1] == x:
            break
        if A[mid - 1] < x:
            lo = mid + 1
        else:
            hi = mid - 1
        k += 1
    return ''.join(rows)


# ================================================================ TRANG BIA + HUONG DAN
add('''<h1>Ôn tập DSA: Sắp xếp · Tìm kiếm · Cây<small>Bản đầy đủ có giải thích, theo cách làm của cô Hồng. Dành cho bài kiểm tra: mỗi câu gồm 3 ý: a) duyệt cây, b) khai báo, c) viết hàm.</small></h1>''')
add('<div class="box"><b class="t">Cách dùng:</b> đọc phần A (cây) trước vì đề mẫu Câu 8 nằm ở đó, rồi B (cây tìm kiếm), C (sắp xếp), D (tìm kiếm). '
    'Mỗi phần có <b>code</b>, <b>hình</b> và <b>ví dụ có đáp án</b>. Cuối tài liệu là phụ lục các bước sắp xếp cho 3 dãy số trong đề của cô. '
    'Khung <span style="background:#eaf5ec;border:.3mm solid #86b58f;padding:0 1mm">xanh</span> là đáp án; khung <span style="background:#fbeed0;border:.3mm solid #d8b25a;padding:0 1mm">vàng</span> là lỗi hay mất điểm.</div>')
add(fig(f3(P8, 'Đề mẫu Câu 8, thứ tự trước'), ))
add('<div class="box">'
    '<table><tr><th>Phần</th><th>Nội dung</th><th>Dạng đề</th></tr>'
    '<tr><td class="c">A</td><td>Cây nhị phân: khai báo, duyệt, hàm đệ quy</td><td>Câu 8 a, b, c; 6 bài đệ quy</td></tr>'
    '<tr><td class="c">B</td><td>Cây nhị phân tìm kiếm: dựng, bổ sung, hủy nút</td><td>Bài 1, Bài 2 (dựng và hủy)</td></tr>'
    '<tr><td class="c">C</td><td>Sắp xếp: chọn, chèn, nổi bọt, trộn, nhanh</td><td>Viết hàm tăng/giảm dần</td></tr>'
    '<tr><td class="c">D</td><td>Tìm kiếm: tuần tự, nhị phân</td><td>Ví dụ 5 (x = 20)</td></tr>'
    '<tr><td class="c">E</td><td>Phụ lục: các bước 5 thuật toán trên 3 dãy số</td><td>Trình bày các bước</td></tr></table></div>')

# ================================================================ PHAN A
add('<h2>A. Cây nhị phân</h2>')
add('<h3>A1. Khái niệm và khai báo</h3>')
add('<p>Cây nhị phân: mỗi nút có <b>tối đa hai con</b>, phân biệt <b>con trái</b> và <b>con phải</b>. '
    '<b>Gốc</b> là nút trên cùng; <b>lá</b> là nút không có con; <b>mức</b> của gốc là 0; <b>chiều cao</b> là số nút trên đường dài nhất từ gốc xuống lá (cây rỗng cao 0, cây chỉ có gốc cao 1).</p>')
add('<p>Với cây Câu 8: gốc 8; lá là −2, 4, 7, 14; nút 3 có hai con (1 và 6), nút 1 chỉ có con trái (−2), nút 10 chỉ có con phải (14); chiều cao 4.</p>')
add('<h4>Lưu trữ móc nối</h4><p>Mỗi nút gồm dữ liệu và hai con trỏ. Cây được biểu diễn bằng <b>con trỏ tới nút gốc</b>; con trỏ bằng <code>NULL</code> là cây rỗng.</p>')
add('<div class="two"><div>' + code(S.DECL) + '</div><div>' + code(S.TAONUT) + '</div></div>')
add('<div class="box warn"><b>Chú ý khi viết b):</b> khai báo <b>đủ ba trường</b> (<code>duLieu</code>, <code>trai</code>, <code>phai</code>), con trỏ kiểu <code>nutCay *</code>, và <b>dấu <code>;</code> sau dấu <code>}</code></b>. Đề nói "mỗi nút lưu một số nguyên" nên <code>duLieu</code> kiểu <code>int</code>.</div>')
add('<h4>Lưu trữ bằng mảng (cây đầy đủ, đánh số từ 0)</h4>'
    '<p>Nút i có con trái ở <code>2*i + 1</code>, con phải ở <code>2*i + 2</code>; cha của nút j ở <code>(j - 1) / 2</code>. Ví dụ nút 4 có con 9 và 10; nút 9 có cha là 4.</p>')

add('<h3>A2. Ba kiểu duyệt cây</h3>')
add('<p>Ba hàm giống hệt nhau, <b>chỉ khác vị trí dòng <code>cout</code></b>: in gốc <i>trước</i> hai cây con (trước), <i>giữa</i> hai cây con (giữa), hay <i>sau</i> hai cây con (sau). Cách nhớ: "trước/giữa/sau" là vị trí của <b>gốc</b> so với trái và phải.</p>')
add(code(S.DUYET))
add(fig(f3(P8, 'Trước (gốc, trái, phải)', 31), f3(I8, 'Giữa (trái, gốc, phải)', 31), f3(Q8, 'Sau (trái, phải, gốc)', 31)))
add('<div class="box ans"><b>Đọc nhanh:</b> trước = <code>' + fmt(P8) + '</code> · giữa = <code>' + fmt(I8) + '</code> · sau = <code>' + fmt(Q8) + '</code>.<br>'
    '<span class="sm">Số trong chấm xanh là thứ tự nút được thăm. Cây tìm kiếm nhị phân thì duyệt giữa cho dãy tăng dần (đúng với Câu 8: −2 1 3 4 6 7 8 10 14).</span></div>')

add('<h3>A3. Đề mẫu Câu 8 làm trọn</h3>')
add(fig(f'<figure>{svg_tree(CAU8, hg=44, vg=50, r=15)}<figcaption>Hình minh họa cây nhị phân cho câu a</figcaption></figure>'))
add('<p><b>a) Thứ tự duyệt.</b> Cách làm từng bước (duyệt trước): thăm 8; sang trái thăm 3; sang trái thăm 1; sang trái thăm −2 (hết nhánh), lùi lại; 1 không có con phải, lùi về 3; sang phải thăm 6, rồi 4, rồi 7; lùi về 8; sang phải thăm 10; 10 không có con trái; sang phải thăm 14. Kết quả:</p>')
add('<div class="box ans">Trước: <code>' + fmt(P8) + '</code><br>Giữa: <code>' + fmt(I8) + '</code><br>Sau: <code>' + fmt(Q8) + '</code></div>')
add('<p><b>b) Khai báo</b> (lưu trữ móc nối, mỗi nút một số nguyên):</p>' + code(S.DECL))
add('<p><b>c) Hàm tính tổng các nút có giá trị dương.</b> Nút dương thì lấy <code>duLieu</code> cộng với kết quả hai cây con; nút không dương thì chỉ gộp hai cây con.</p>' + code('''
long long tongDuong(nutCay *t)
{
    if (t == NULL) return 0;               // cây rỗng: dừng
    if (t->duLieu > 0)                     // nút dương: cộng giá trị của nó
        return t->duLieu + tongDuong(t->trai) + tongDuong(t->phai);
    return tongDuong(t->trai) + tongDuong(t->phai);   // nút âm hoặc 0: bỏ qua
}'''))
add('<table><tr><th>Nút</th>' + ''.join(f'<th>{v}</th>' for v in P8) + '<th>Tổng</th></tr>'
    '<tr><td>Đóng góp</td>' + ''.join(f'<td class="c">{v if v > 0 else 0}</td>' for v in P8) + f'<td class="c"><b>{tong_duong}</b></td></tr></table>')
add('<div class="box warn"><b>Lỗi hay gặp:</b> viết <code>return (t->duLieu &gt; 0) + ...</code> chỉ <i>đếm</i> số nút dương (được 8), không <i>cộng giá trị</i> (phải được 53). Nút −2 phải bị bỏ qua, không trừ.</div>')

add('<h3>A4. Khung đệ quy trên cây (3 bước)</h3>')
add('<p>Mọi hàm "đếm / tính tổng trên cây" đều theo một khung:</p><ol><li><b>Cây rỗng</b> (<code>t == NULL</code>): trả về 0, đây là điều kiện dừng.</li><li><b>Phần đóng góp của riêng nút t</b>.</li><li><b>Gộp:</b> phần của nút + kết quả cây trái + kết quả cây phải.</li></ol>')
add(code(S.HAM_CAY))
add(code(S.HAM_CAY_THEM))
add('<h4>Kết quả trên cây Câu 8</h4><table><tr><th>Hàm</th><th>Kết quả</th><th>Giải thích</th></tr>'
    '<tr><td><code>demNut</code></td><td class="c">9</td><td>8, 3, 1, −2, 6, 4, 7, 10, 14</td></tr>'
    '<tr><td><code>demLa</code></td><td class="c">4</td><td>−2, 4, 7, 14</td></tr>'
    '<tr><td><code>chieuCao</code></td><td class="c">4</td><td>đường 8 → 3 → 1 → −2 có 4 nút</td></tr>'
    '<tr><td><code>demLe</code></td><td class="c">3</td><td>3, 1, 7 (−2 là chẵn)</td></tr>'
    '<tr><td><code>tongNut</code></td><td class="c">51</td><td>8+3+1−2+6+4+7+10+14</td></tr>'
    '<tr><td><code>tongDuong</code></td><td class="c">53</td><td>bỏ −2: 51 + 2</td></tr></table>')
add('<div class="box warn"><b>Số lẻ âm:</b> <code>-15 % 2</code> bằng <code>-1</code> trong C++, nên viết <code>% 2 != 0</code>, không viết <code>== 1</code>.</div>')

add('<h3>A5. Sáu bài tập đệ quy của cô (de_quy.txt), có lời giải</h3>')
add('<ol class="sm"><li>Khai báo cây nhị phân lưu trữ móc nối, mỗi nút một số nguyên → <code>struct nutCay</code> (A1).</li>'
    '<li>Thủ tục bổ sung x vào BST có gốc trỏ bởi T → <code>boSung</code> (B3).</li>'
    '<li>Đếm số nút → <code>demNut</code>.</li><li>Đếm số nút lẻ → <code>demLe</code>.</li>'
    '<li>Tổng giá trị các nút → <code>tongNut</code>.</li><li>Tổng giá trị các nút dương → <code>tongDuong</code> (A3, A4).</li></ol>')
add('<div class="box">Chỉ khác nhau ở <b>phần đóng góp của nút</b>: đếm nút là <code>1</code>; đếm lẻ là <code>(t->duLieu % 2 != 0)</code>; tổng là <code>t->duLieu</code>; tổng dương là <code>(t->duLieu &gt; 0 ? t->duLieu : 0)</code>. Học khung một lần, thay phần này là xong.</div>')

L1 = [20, -8, 35, -15, 3, 28, 50, -3, 9, 0]
L2 = [14, 9, 21, 6, 12, 18, 30, 11, 25]
t1, t2 = build(L1), build(L2)
lo1 = lambda t: sum(1 for v in ino(t) if v % 2 != 0)
add('<h3>A6. Hai đề luyện (tự làm rồi đối chiếu)</h3>')
add('<p><b>Đề 1.</b> Dựng BST từ dãy <code>' + fmt(L1) + '</code>. a) Duyệt trước, giữa, sau. b) Đếm nút lẻ. c) Tổng nút dương.</p>')
add(fig(f'<figure>{svg_tree(t1, hg=36, vg=44, r=14)}<figcaption>BST dựng từ dãy của Đề 1</figcaption></figure>'))
add('<div class="box ans">Trước: <code>' + fmt(pre(t1)) + '</code><br>Giữa: <code>' + fmt(ino(t1)) + '</code> (tăng dần)<br>Sau: <code>' + fmt(post(t1)) +
    f'</code><br>Nút lẻ: <b>{lo1(t1)}</b> ({", ".join(str(v) for v in ino(t1) if v % 2 != 0)}) · Tổng nút dương: <b>{sum(v for v in ino(t1) if v > 0)}</b> · Tổng tất cả: {sum(ino(t1))}</div>')
add('<p><b>Đề 2.</b> Dựng BST từ dãy <code>' + fmt(L2) + '</code>. a) Duyệt trước, giữa, sau. b) Đếm nút chia hết cho 3. c) Chiều cao cây.</p>')
add(fig(f'<figure>{svg_tree(t2, hg=38, vg=44, r=14)}<figcaption>BST dựng từ dãy của Đề 2</figcaption></figure>'))


def h(t):
    return 0 if t is None else 1 + max(h(t.l), h(t.r))


add('<div class="box ans">Trước: <code>' + fmt(pre(t2)) + '</code><br>Giữa: <code>' + fmt(ino(t2)) + '</code><br>Sau: <code>' + fmt(post(t2)) +
    f'</code><br>Chia hết cho 3: <b>{sum(1 for v in ino(t2) if v % 3 == 0)}</b> ({", ".join(str(v) for v in ino(t2) if v % 3 == 0)}) · Chiều cao: <b>{h(t2)}</b></div>')

# ================================================================ PHAN B
add('<div class="pagebreak"></div><h2>B. Cây nhị phân tìm kiếm (BST)</h2>')
add('<h3>B1. Định nghĩa và dựng cây</h3>')
add('<p>BST là cây nhị phân trong đó <b>mọi nút</b> có khóa lớn hơn tất cả khóa ở cây con trái và nhỏ hơn tất cả khóa ở cây con phải; các khóa khác nhau. '
    'Dựng cây: bắt đầu từ cây rỗng, thêm lần lượt từng khóa. Mỗi khóa đi từ gốc: <b>nhỏ hơn thì sang trái, lớn hơn thì sang phải</b>, gặp chỗ trống thì đặt nút mới ở đó. Khóa đã có thì bỏ qua.</p>')
add('<h4>Bài 1a: dãy ' + fmt(SEQ_B1) + '</h4>')
b1 = build(SEQ_B1)
add(insertion_table(SEQ_B1))
add(fig(f'<figure>{svg_tree(b1, hg=40, vg=46, r=14)}<figcaption>Cây BST của Bài 1a</figcaption></figure>'))
add('<h4>Bài 2a: dãy ' + fmt(SEQ_B2) + '</h4>')
b2 = build(SEQ_B2)
add(insertion_table(SEQ_B2))
add(fig(f'<figure>{svg_tree(b2, hg=40, vg=46, r=14)}<figcaption>Cây BST của Bài 2a</figcaption></figure>'))
add('<div class="box ans">Kiểm tra bằng duyệt giữa phải tăng dần. Bài 1a: <code>' + fmt(ino(b1)) + '</code>. Bài 2a: <code>' + fmt(ino(b2)) + '</code>.</div>')

add('<h3>B2. Bổ sung, tìm kiếm, nhỏ nhất</h3>')
add('<p>Tham số <code>nutCay *&amp;t</code> là <b>tên khác của chính ô con trỏ</b> được truyền vào, nên <code>t = taoNut(x)</code> ghi thẳng vào cây thật. Nếu quên dấu <code>&amp;</code>, cây không thay đổi.</p>')
add(code(S.BOSUNG))
add(code('''
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
}'''))

add('<h3>B3. Hủy nút</h3>')
add('<p>Tìm nút x như khi tìm kiếm, rồi xét số con:</p>'
    '<ol><li><b>Lá:</b> bỏ nút, cha của nó trỏ <code>NULL</code>.</li>'
    '<li><b>Một con:</b> cha của nút trỏ thẳng tới con duy nhất của nó.</li>'
    '<li><b>Hai con:</b> chọn <b>nút thế mạng</b>, chép khóa của nó lên nút cần hủy, rồi hủy nút thế mạng cũ (nút này có tối đa một con).<br>'
    '· <b>Cách hai (theo sách):</b> nút thế mạng là <b>trái nhất của cây con phải</b>.<br>· <b>Cách một:</b> nút thế mạng là <b>phải nhất của cây con trái</b>.</li></ol>')
add(code(S.XOA))
add('<h4>Bài 1b: hủy 30, rồi 20</h4>')
b1a = delete(dup(b1), 30, 2)
b1b2 = delete(dup(b1a), 20, 2)
b1b1 = delete(dup(b1a), 20, 1)
add(fig(tree_fig(b1, 'Trước: nút 30 (đỏ)', mark={30: 'del'}, hg=30, vg=42, r=13),
        tree_fig(b1a, 'Sau hủy 30 (một con): 28 nối lên', mark={28: 'new'}, hg=30, vg=42, r=13)))
add('<p><b>Hủy 30:</b> nút 30 chỉ có <b>một con</b> (con trái là 28). Cha của 30 là 20, nên cho con phải của 20 trỏ thẳng tới 28 rồi giải phóng 30.</p>')
add(fig(tree_fig(b1a, 'Trước khi hủy 20 (đỏ), 20 có hai con 19 và 28', mark={20: 'del'}, hg=30, vg=42, r=13),
        tree_fig(b1b2, 'Cách hai: 28 thế mạng', mark={28: 'rep'}, hg=30, vg=42, r=13),
        tree_fig(b1b1, 'Cách một: 19 thế mạng', mark={19: 'rep'}, hg=30, vg=42, r=13)))
add('<p><b>Hủy 20 (hai con):</b> cách hai, cây con phải của 20 chỉ có 28 (không có con trái), nên 28 là nút trái nhất: chép 28 lên nút 20, hủy nút 28 cũ. Cách một, nút phải nhất của cây con trái (19) là 19: chép 19 lên nút 20, hủy nút 19 cũ. Cả hai đều cho BST hợp lệ.</p>')
add('<h4>Bài 2b: hủy 36, rồi 43</h4>')
b2a = delete(dup(b2), 36, 2)
b2b = delete(dup(b2a), 43, 2)
add(fig(tree_fig(b2, 'Trước: hủy 36 (đỏ)', mark={36: 'del'}, hg=26, vg=40, r=12),
        tree_fig(b2a, 'Sau hủy 36 (lá). Tiếp: hủy 43 (đỏ)', mark={43: 'del'}, hg=26, vg=40, r=12),
        tree_fig(b2b, 'Sau hủy 43 (một con): 45 nối lên', mark={45: 'rep'}, hg=26, vg=40, r=12)))
add('<p><b>Hủy 36:</b> nút lá (con trái của 43), cho con trái của 43 bằng <code>NULL</code> rồi giải phóng. <b>Hủy 43:</b> lúc này chỉ còn con phải 45, cho con phải của 31 trỏ thẳng tới 45 rồi giải phóng 43.</p>')

# ================================================================ PHAN C
add('<div class="pagebreak"></div><h2>C. Sắp xếp</h2>')
add('<p>Đề yêu cầu: (a) mô tả và viết hàm cho 5 thuật toán, mỗi cái <b>tăng dần</b> và <b>giảm dần</b>; (b) trình bày các bước trên 3 dãy số. Code dưới đây là sắp <b>tăng dần</b>; '
    'phần tô <span style="background:#ffe08a;outline:.2mm solid #b88a00;padding:0 1mm;font-family:Consolas">vàng</span> là chỗ <b>đảo dấu</b> để được bản giảm dần. Tất cả mảng đánh số từ 0.</p>')
add('<table><tr><th>Thuật toán</th><th>Ý tưởng</th><th>Tốt nhất</th><th>Xấu nhất</th><th>Ổn định</th><th>Mảng phụ</th></tr>'
    '<tr><td>Chọn</td><td>Chọn phần tử nhỏ nhất của phần chưa sắp, đổi về đầu</td><td class="c">n²</td><td class="c">n²</td><td class="c">không</td><td class="c">không</td></tr>'
    '<tr><td>Chèn</td><td>Chèn từng phần tử vào đúng chỗ trong phần đầu đã sắp</td><td class="c">n</td><td class="c">n²</td><td class="c">có</td><td class="c">không</td></tr>'
    '<tr><td>Nổi bọt</td><td>So cặp kề, sai thứ tự thì đổi; phần tử lớn nhất nổi dần về cuối</td><td class="c">n² (có cờ: n)</td><td class="c">n²</td><td class="c">có</td><td class="c">không</td></tr>'
    '<tr><td>Trộn</td><td>Chia đôi, sắp từng nửa, trộn hai nửa đã sắp</td><td class="c">n log n</td><td class="c">n log n</td><td class="c">có</td><td class="c">O(n)</td></tr>'
    '<tr><td>Nhanh</td><td>Chọn pivot, đưa nhỏ hơn sang trái, lớn hơn sang phải, sắp hai phía</td><td class="c">n log n</td><td class="c">n²</td><td class="c">không</td><td class="c">không</td></tr></table>')

add('<h3>C1. Sắp xếp chọn (Selection Sort)</h3><p>Lượt i: tìm phần tử nhỏ nhất trong <code>a[i..n-1]</code>, đổi chỗ với <code>a[i]</code>. Sau lượt i, đầu mảng đã đúng vị trí. Giảm dần: tìm phần tử <b>lớn nhất</b>.</p>' + code(S.SELECTION))
add('<h3>C2. Sắp xếp chèn (Insertion Sort)</h3><p>Phần <code>a[0..i-1]</code> đã sắp. Lấy <code>x = a[i]</code>, dồn các phần tử lớn hơn <code>x</code> sang phải một ô, đặt <code>x</code> vào chỗ trống. Giống xếp bài trên tay.</p>' + code(S.INSERTION))
add('<h3>C3. Sắp xếp nổi bọt (Bubble Sort)</h3><p>Mỗi lượt duyệt cặp kề, đổi chỗ nếu sai thứ tự. Sau lượt i, i + 1 phần tử lớn nhất đã về cuối, nên vòng trong chỉ chạy tới <code>n - 1 - i</code>.</p>' + code(S.BUBBLE))
add('<h3>C4. Sắp xếp trộn (Merge Sort)</h3><p>Chia đôi tại <code>giua = (dau + cuoi) / 2</code>, sắp đệ quy từng nửa, rồi <code>Merge</code> hai nửa đã sắp bằng mảng phụ <code>b</code>. '
    'Dùng <code>&lt;=</code> khi so sánh để bằng nhau thì lấy phần tử bên trái trước (ổn định).</p>' + code(S.MERGE))
add('<h3>C5. Sắp xếp nhanh (Quick Sort)</h3><p>Chọn pivot <code>x</code> là phần tử giữa. Con trỏ <code>i</code> tiến từ trái tới khi gặp phần tử <b>không nhỏ hơn</b> x; <code>j</code> lùi từ phải tới khi gặp phần tử <b>không lớn hơn</b> x; '
    'nếu <code>i &lt;= j</code> thì đổi chỗ rồi cả hai tiến vào. Khi hai con trỏ vượt nhau, mảng chia thành <code>[dau..j]</code> và <code>[i..cuoi]</code>, sắp đệ quy từng phần.</p>' + code(S.QUICK))
add('<div class="box warn"><b>Giảm dần:</b> chỉ đảo dấu so sánh ở chỗ tô vàng: Chọn <code>a[j] &gt; a[vt]</code> (tìm max); Chèn <code>a[j] &lt; x</code>; Nổi bọt <code>a[j] &lt; a[j+1]</code>; Trộn <code>a[i] &gt;= a[j]</code>; Nhanh <code>a[i] &gt; x</code> và <code>a[j] &lt; x</code>. Không đảo cả vòng lặp.</div>')

# ================================================================ PHAN D
add('<div class="pagebreak"></div><h2>D. Tìm kiếm</h2>')
add('<h3>D1. Tìm tuần tự và tìm nhị phân</h3>' + code(S.TIM))
add('<ul><li><b>Tuần tự:</b> duyệt từ đầu, gặp x thì trả vị trí, hết mảng thì trả −1. Mảng bất kỳ, O(n).</li>'
    '<li><b>Nhị phân:</b> chỉ dùng khi mảng <b>đã sắp tăng dần</b>. Mỗi lượt so x với phần tử giữa rồi loại một nửa. O(log n).</li></ul>')
add('<div class="box warn"><b>Điều kiện bắt buộc:</b> viết rõ "mảng đã sắp tăng dần" khi dùng tìm nhị phân. Cô dùng vị trí đếm từ 1 trong ví dụ; code C++ đếm từ 0, nên kết quả vị trí 6 tương ứng chỉ số 5.</div>')
A5 = [-8, -5, 0, 4, 15, 20, 50, 63, 75, 98]
add('<h3>D2. Ví dụ 5 của cô: x = 20</h3><p>A = ' + fmt(A5) + ', vị trí đếm từ 1. Ô vàng là "trung vị" của lượt, ô xám nhạt đã bị loại.</p>')
add('<div class="trace">' + bs_rows(A5, 20) + '</div>')
add('<div class="box ans"><b>Lượt 1:</b> trung vị là vị trí 5, A[5] = 15 &lt; 20 nên mọi phần tử vị trí 1 đến 5 đều nhỏ hơn x, loại, còn [6..10].<br>'
    '<b>Lượt 2:</b> A[8] = 63 &gt; 20 nên vị trí 9, 10 lớn hơn x, loại, còn [6..7].<br>'
    '<b>Lượt 3:</b> [6..7] có hai phần tử (số chẵn) nên có hai trung vị, chọn trung vị đầu tiên, vị trí 6. A[6] = 20 = x. <b>Kết luận: x có trong mảng.</b></div>')

# ================================================================ PHU LUC
add('<div class="pagebreak"></div><h2>E. Phụ lục: các bước sắp tăng dần cho 3 dãy của cô</h2>')
add('<p>Mỗi dòng là mảng <b>sau</b> mỗi lượt. Ô xám là phần đã về đúng chỗ, ô vàng là vị trí vừa đổi/chèn (chọn, chèn), ô nhạt ở phần Nhanh là đoạn đang không xử lý. '
    'Sắp giảm dần thì các bước giống nhau nhưng đảo dấu so sánh (hộp vàng ở phần C); kết quả cuối ghi sẵn ở từng dãy.</p>')
names = {1: 'Dãy 1', 2: 'Dãy 2', 3: 'Dãy 3'}
for si, A in enumerate(SEQS, 1):
    add(f'<h3>{names[si]}: {fmt(A)}</h3>')
    add(f'<div class="box ans sm">Kết quả tăng dần: <code>{fmt(sorted(A))}</code> · giảm dần: <code>{fmt(sorted(A, reverse=True))}</code></div>')
    add('<h4>Chọn</h4><div class="trace">' + ''.join(selection_trace(A)) + '</div>')
    add('<h4>Chèn</h4><div class="trace">' + ''.join(insertion_trace(A)) + '</div>')
    add('<h4>Nổi bọt</h4><div class="trace">' + ''.join(bubble_trace(A)) + '</div>')
    sp, mg = merge_trace(A)
    add('<h4>Trộn</h4><div class="merge"><div><h5>Chia đôi (giua = (dau + cuoi) / 2)</h5><div class="mono">' + '<br>'.join(sp) + '</div></div>'
        '<div><h5>Trộn từ dưới lên (theo thứ tự thực hiện)</h5><div class="mono">' + '<br>'.join(mg) + '</div></div></div>')
    add('<h4>Nhanh (pivot = phần tử giữa)</h4><div class="trace">' + ''.join(quick_trace(A)) + '</div>')

body = ''.join(parts)
extra = '.trace,.merge{page-break-inside:avoid} body{font-size:9.8pt} h4{margin:2mm 0 .8mm;font-size:9.6pt} pre.code{font-size:8.2pt} .fig svg{max-width:100%}'
if __name__ == '__main__':
    print(write_pdf('co-hong_day-du', 'Ôn tập DSA – bản đầy đủ', body, extra))
