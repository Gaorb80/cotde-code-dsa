# -*- coding: utf-8 -*-
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import snippets as S

SP = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\Users\Duong_Bao\Downloads'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# ---------------------------------------------------------------- du lieu
CAU8 = manual((8, (3, (1, (-2, None, None), None), (6, (4, None, None), (7, None, None))), (10, None, (14, None, None))))
P8, I8, Q8 = pre(CAU8), ino(CAU8), post(CAU8)
assert P8 == [8, 3, 1, -2, 6, 4, 7, 10, 14] and I8 == [-2, 1, 3, 4, 6, 7, 8, 10, 14] and Q8 == [-2, 1, 4, 7, 6, 3, 14, 10, 8]
tong_duong = sum(v for v in ino(CAU8) if v > 0)
assert tong_duong == 53

fmt = lambda a: ' '.join(map(str, a))

SEQ_B1 = [18, 13, 15, 12, 20, 11, 30, 19, 28, 14]
SEQ_B2 = [51, 31, 43, 29, 65, 10, 20, 36, 78, 59, 15, 45, 55]
SEQS = [[9, 1, 2, 10, 8, 5, 7, 4, 6], [5, 15, 12, 2, 10, 12, 9, 1, 9, 3, 2, 3], [51, 61, 21, 12, 101, 121, 91, 101, 91, 31]]


def tree_fig(t, cap, **kw):
    return f'<figure>{svg_tree(t, **kw)}<figcaption>{cap}</figcaption></figure>'


def write_pdf(name, title, body, extra=''):
    htmlf = os.path.join(SP, name + '.html')
    open(htmlf, 'w', encoding='utf-8').write(PAGE.format(title=title, css=CSS, extra=extra, body=body))
    pdf = os.path.join(OUT, name + '.pdf')
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={pdf}', 'file:///' + htmlf.replace('\\', '/')],
                   check=True, capture_output=True)
    return pdf


# ================================================================ CHEATSHEET
def cheatsheet():
    tr = lambda seq: svg_tree(CAU8, badges=order_badges([v for v in seq]), hg=30, vg=40, r=13)
    # (cung mot cay, huy hieu = so thu tu duyet)
    figs = ''.join(
        f'<figure>{svg_tree(CAU8, badges={v: i + 1 for i, v in enumerate(seq)}, hg=33, vg=36, r=12.5)}'
        f'<figcaption><b>{name}</b>: {fmt(seq)}</figcaption></figure>'
        for name, seq in (('Trước', P8), ('Giữa', I8), ('Sau', Q8)))

    b2 = build(SEQ_B2)
    c2 = delete(delete(dup(b2), 36, 2), 43, 2)
    b1 = build(SEQ_B1)
    a1 = delete(delete(dup(b1), 30, 2), 20, 2)

    body = f"""
<h1>Cheatsheet DSA – tra nhanh<small>Sắp xếp · Tìm kiếm · Cây nhị phân · theo cách làm của cô Hồng. Đề: 3 ý a) duyệt cây, b) khai báo, c) viết hàm.</small></h1>

<h2>① Đề mẫu Câu 8: đáp án trọn bộ</h2>
<div class="fig">{figs}</div>
<div class="box ans"><b class="t">a)</b> Trước (gốc-trái-phải): <code>{fmt(P8)}</code> &nbsp;·&nbsp; Giữa (trái-gốc-phải): <code>{fmt(I8)}</code> &nbsp;·&nbsp; Sau (trái-phải-gốc): <code>{fmt(Q8)}</code><br>
<span class="sm">Số trong chấm xanh = thứ tự được thăm. Gốc 8 luôn đầu tiên ở duyệt trước, cuối cùng ở duyệt sau. Cây này là BST nên duyệt giữa tăng dần.</span></div>
<div class="two">
<div><b class="t">b) Khai báo</b>{code(S.DECL)}</div>
<div><b class="t">c) Tổng nút dương</b> (= {tong_duong})
{code('''
long long tongDuong(nutCay *t)
{
    if (t == NULL) return 0;
    if (t->duLieu > 0)
        return t->duLieu
             + tongDuong(t->trai)
             + tongDuong(t->phai);
    return tongDuong(t->trai)
         + tongDuong(t->phai);
}''')}</div></div>

<h2>② Hàm đệ quy trên cây: một khung cho mọi bài</h2>
{code('''
int f(nutCay *t)
{
    if (t == NULL) return 0;                // 1. cây rỗng: điều kiện dừng
    return «PHẦN_NÚT» + f(t->trai) + f(t->phai);   // 2. phần của nút  3. gộp trái + phải
}''')}
<table><tr><th>Đề bài</th><th>PHẦN_NÚT</th><th>Đề bài</th><th>PHẦN_NÚT</th></tr>
<tr><td>Đếm nút</td><td><code>1</code></td><td>Tổng giá trị</td><td><code>t->duLieu</code></td></tr>
<tr><td>Đếm nút lẻ</td><td><code>(t->duLieu % 2 != 0)</code></td><td>Tổng nút dương</td><td><code>(t->duLieu &gt; 0 ? t->duLieu : 0)</code></td></tr>
<tr><td>Đếm nút chẵn</td><td><code>(t->duLieu % 2 == 0)</code></td><td>Đếm nút dương</td><td><code>(t->duLieu &gt; 0)</code></td></tr>
<tr><td>Đếm chia hết 3</td><td><code>(t->duLieu % 3 == 0)</code></td><td>Đếm nút 2 con</td><td><code>(t->trai &amp;&amp; t->phai)</code></td></tr></table>
<div class="two sm">
<div><b>Đếm lá:</b> nếu cả 2 con NULL trả 1, còn lại <code>demLa(trai) + demLa(phai)</code>.</div>
<div><b>Chiều cao:</b> <code>1 + max(chieuCao(trai), chieuCao(phai))</code>; rỗng = 0, chỉ gốc = 1.</div>
<div><b>Cây Câu 8:</b> 9 nút · 4 lá (−2, 4, 7, 14) · cao 4 · 3 nút lẻ (3, 1, 7) · tổng 51.</div>
<div class="box warn" style="margin:0"><b>Hay mất điểm:</b> viết <code>(t->duLieu &gt; 0)</code> mà quên nhân/cộng giá trị thì chỉ <i>đếm</i> chứ không <i>tổng</i>. Lẻ phải viết <code>!= 0</code>, không viết <code>== 1</code>.</div>
</div>

<h3>Duyệt cây: ba hàm chỉ khác vị trí dòng <code>cout</code></h3>
{code('''
void duyetTruoc(nutCay *t) { if (t) { cout << t->duLieu << " ";  duyetTruoc(t->trai);  duyetTruoc(t->phai); } }
void duyetGiua (nutCay *t) { if (t) { duyetGiua(t->trai);  cout << t->duLieu << " ";  duyetGiua(t->phai); } }
void duyetSau  (nutCay *t) { if (t) { duyetSau(t->trai);  duyetSau(t->phai);  cout << t->duLieu << " "; } }''')}

<h2>⑥ Lỗi hay mất điểm, kiểm trước khi nộp</h2>
<div class="two sm">
<ul><li>Duyệt cây: đọc đúng thứ tự (trước = gốc đầu, sau = gốc cuối), thăm hết <b>mọi</b> nút, nhớ cây có nút âm (−2).</li>
<li>Khai báo: <code>struct nutCay</code> đủ 3 trường, kết thúc bằng <code>;</code>; con trỏ <code>trai</code>, <code>phai</code> kiểu <code>nutCay *</code>.</li>
<li>Hàm đệ quy: <b>có điều kiện dừng</b> (<code>t == NULL</code>), hai lần gọi trái và phải, trả đúng kiểu.</li>
<li>Tổng nút dương: cộng <code>t->duLieu</code>, đừng chỉ đếm. Nút lẻ: <code>% 2 != 0</code>.</li></ul>
<ul><li>BST: bổ sung dùng <code>nutCay *&amp;t</code> (tham chiếu), không dùng <code>nutCay *t</code>.</li>
<li>Hủy nút hai con: chép khóa thế mạng lên, hủy nút thế mạng cũ. Nói rõ dùng cách một hay cách hai.</li>
<li>Tìm nhị phân: nhắc mảng phải tăng dần. Sắp giảm dần: đảo dấu so sánh, không đảo cả vòng lặp.</li>
<li>Vẽ cây: nhị phân tìm kiếm không có khóa trùng; mỗi bước dựng cây ghi rõ khóa đang thêm.</li></ul></div>
<div class="pagebreak"></div>
<h2>③ Cây nhị phân tìm kiếm (BST)</h2>
<div class="two">
<div><b class="t">Quy tắc:</b> trái &lt; gốc &lt; phải (mọi nút). Dựng: thêm lần lượt, nhỏ đi trái, lớn đi phải, gặp chỗ trống thì đặt. Trùng thì bỏ qua.
{code('''
void boSung(nutCay *&t, int x)
{
    if (t == NULL) t = taoNut(x);
    else if (x < t->duLieu) boSung(t->trai, x);
    else if (x > t->duLieu) boSung(t->phai, x);
}''')}</div>
<div><b class="t">Hủy nút x</b> (tìm x trước, rồi xét số con):
<ol class="sm"><li><b>Lá:</b> bỏ luôn (cha trỏ NULL).</li>
<li><b>Một con:</b> cha trỏ thẳng tới con đó.</li>
<li><b>Hai con:</b> chọn nút thế mạng, chép khóa của nó lên nút cần hủy, rồi hủy nút thế mạng cũ.
 <br>· <b>Cách hai:</b> trái nhất của cây con phải.<br>· <b>Cách một:</b> phải nhất của cây con trái.</li></ol>
<span class="sm">Tìm min: đi mãi sang trái. Tìm max: đi mãi sang phải. Duyệt giữa của BST luôn tăng dần.</span></div></div>
<div class="fig">
{tree_fig(b1, 'Bài 1a: dựng từ 18 13 15 12 20 11 30 19 28 14', mark={30: 'del'}, hg=26, vg=38, r=12)}
{tree_fig(a1, 'Sau hủy 30 rồi 20 (cách hai): 28 thế chỗ', mark={28: 'rep'}, hg=26, vg=38, r=12)}
{tree_fig(delete(delete(dup(b1), 30, 2), 20, 1), 'Cùng bài, cách một: 19 thế chỗ', mark={19: 'rep'}, hg=26, vg=38, r=12)}
</div>

<div class="fig">
{tree_fig(b2, 'Bài 2a: dựng từ 51 31 43 29 65 10 20 36 78 59 15 45 55', mark={36: 'del', 43: 'del'}, hg=26, vg=36, r=12)}
{tree_fig(c2, 'Sau hủy 36 (lá) rồi 43 (một con): 45 nối lên', mark={45: 'rep'}, hg=26, vg=36, r=12)}
</div>

<h2>④ Sắp xếp: nhớ ý tưởng + sửa dấu để giảm dần</h2>
<div class="sm" style="margin-bottom:1mm">Phần tô <span style="background:#ffe08a;outline:.2mm solid #b88a00;padding:0 1mm;font-family:Consolas">vàng</span> = chỗ cần đảo khi sắp <b>giảm dần</b> (code bên dưới là <b>tăng dần</b>; muốn <b>giảm dần</b> chỉ đảo các dấu tô vàng: &lt; ↔ &gt;, &lt;= ↔ &gt;=, nhỏ nhất ↔ lớn nhất).</div>
<table><tr><th>Thuật toán</th><th>Ý tưởng một câu</th><th>Tốt nhất</th><th>Xấu nhất</th><th>Ổn định</th></tr>
<tr><td>Chọn</td><td>Mỗi lượt chọn phần tử nhỏ nhất đưa về đầu phần chưa sắp</td><td class="c">n²</td><td class="c">n²</td><td class="c">không</td></tr>
<tr><td>Chèn</td><td>Lấy a[i] chèn vào đúng chỗ trong phần đầu đã sắp</td><td class="c">n</td><td class="c">n²</td><td class="c">có</td></tr>
<tr><td>Nổi bọt</td><td>So sánh cặp kề, đổi chỗ; phần tử lớn nhất nổi về cuối</td><td class="c">n²*</td><td class="c">n²</td><td class="c">có</td></tr>
<tr><td>Trộn</td><td>Chia đôi, sắp từng nửa, trộn hai nửa đã sắp</td><td class="c">n log n</td><td class="c">n log n</td><td class="c">có</td></tr>
<tr><td>Nhanh</td><td>Chọn pivot, chia ≤ pivot bên trái, ≥ pivot bên phải, sắp hai phía</td><td class="c">n log n</td><td class="c">n²</td><td class="c">không</td></tr></table>
<div class="sm">* Bản có cờ dừng sớm (không đổi chỗ thì dừng) tốt nhất là n. Trộn cần thêm mảng phụ O(n).</div>
<div class="pagebreak"></div>
<h2>④ (tiếp) Code năm thuật toán, sắp tăng dần</h2>
<div class="two">
{code(S.SELECTION, 'tiny nocom')}
{code(S.INSERTION, 'tiny nocom')}
{code(S.BUBBLE, 'tiny nocom')}
{code(S.QUICK, 'tiny nocom')}
{code(S.MERGE, 'tiny nocom')}
</div>
<div class="box sm"><b class="t">Ghi nhớ:</b> Chọn: tìm min của phần còn lại rồi <code>swap</code> về vị trí <code>i</code> · Chèn: dồn phần tử lớn hơn <code>x</code> sang phải rồi đặt <code>x</code> · Nổi bọt: vòng trong chạy tới <code>n-1-i</code> · Nhanh: pivot là phần tử giữa, hai con trỏ <code>i</code>, <code>j</code> tiến vào nhau rồi gọi đệ quy hai phía · Trộn: <code>giua = (dau+cuoi)/2</code>, sắp hai nửa rồi <code>Merge</code>.</div>

<h2>⑤ Tìm kiếm</h2>
<div class="two">
{code(S.TIM, 'tiny nocom')}
<div class="sm"><b>Tuần tự:</b> duyệt từ đầu, gặp x thì trả vị trí. O(n), mảng bất kỳ.<br>
<b>Nhị phân:</b> mảng <b>đã tăng dần</b>. Lấy giữa, so với x, bỏ một nửa. O(log n). Quên sắp xếp trước thì kết quả sai.
<div class="box" style="margin-top:1.6mm"><b class="t">Ví dụ 5 (cô):</b> A = −8 −5 0 4 15 20 50 63 75 98, x = 20 (vị trí đếm từ 1)<br>
Lượt 1: [1..10], giữa = vị trí 5 → 15 &lt; 20 → [6..10] &nbsp;·&nbsp; Lượt 2: giữa = vị trí 8 → 63 &gt; 20 → [6..7]<br>
Lượt 3: giữa = vị trí 6 → 20 = x → <b>có trong mảng</b>. <span class="sm">(code 0-based trả chỉ số 5)</span></div></div></div>

"""
    extra = '''body{font-size:9pt;line-height:1.34} h1{font-size:17pt} h2{font-size:11.5pt;margin:2.6mm 0 1.4mm;padding:.8mm 2.4mm}
    h3{font-size:9.6pt;margin:2mm 0 1mm} .fig{flex-wrap:nowrap;margin:1mm 0} .fig svg{max-width:100%}
    pre.tiny{font-size:7.3pt} pre.code{font-size:7.8pt;line-height:1.26;padding:1mm 1.8mm;margin:1mm 0} table{font-size:8.2pt;margin:1mm 0} th,td{padding:.4mm 1.4mm}
    .box{padding:1.2mm 2.4mm;margin:1.2mm 0} .two{column-gap:4mm} p{margin:.6mm 0} .sm{font-size:8pt}'''
    return write_pdf('co-hong_cheatsheet', 'Cheatsheet DSA – cô Hồng', body, extra)


if __name__ == '__main__':
    print(cheatsheet())
