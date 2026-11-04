# -*- coding: utf-8 -*-
"""Thu vien dung chung: cay, ve SVG, mo phong sap xep, CSS."""
import copy
import re
import html as _h


# ---------------------------------------------------------------- cay
class N:
    def __init__(s, v, l=None, r=None):
        s.v, s.l, s.r = v, l, r


def insert(t, x):
    if t is None:
        return N(x)
    if x < t.v:
        t.l = insert(t.l, x)
    elif x > t.v:
        t.r = insert(t.r, x)
    return t


def build(seq):
    t = None
    for x in seq:
        t = insert(t, x)
    return t


def manual(spec):
    """spec = (v, left, right) long nhau."""
    if spec is None:
        return None
    v, l, r = spec
    return N(v, manual(l), manual(r))


def pre(t):
    return [] if t is None else [t.v] + pre(t.l) + pre(t.r)


def ino(t):
    return [] if t is None else ino(t.l) + [t.v] + ino(t.r)


def post(t):
    return [] if t is None else post(t.l) + post(t.r) + [t.v]


def delete(t, x, mode):
    if t is None:
        return None
    if x < t.v:
        t.l = delete(t.l, x, mode)
    elif x > t.v:
        t.r = delete(t.r, x, mode)
    else:
        if t.l is None:
            return t.r
        if t.r is None:
            return t.l
        if mode == 2:           # cach hai: trai nhat cua cay con phai
            q = t.r
            while q.l:
                q = q.l
            t.v = q.v
            t.r = delete(t.r, q.v, mode)
        else:                   # cach mot: phai nhat cua cay con trai
            q = t.l
            while q.r:
                q = q.r
            t.v = q.v
            t.l = delete(t.l, q.v, mode)
    return t


def dup(t):
    return copy.deepcopy(t)


def svg_tree(t, badges=None, mark=None, hg=36, vg=50, r=15, note=None):
    """badges: {gia_tri: so_thu_tu}; mark: {gia_tri: 'del'|'new'|'rep'}"""
    badges = badges or {}
    mark = mark or {}
    pos = {}

    def place(n, d, le):
        """tra ve (x, rong); x tinh theo don vi hg, can giua con."""
        if n is None:
            return None, 0
        if n.l is None and n.r is None:
            pos[id(n)] = (le + 0.5, d)
            return le + 0.5, 1
        if n.l is not None and n.r is not None:
            xl, wl = place(n.l, d + 1, le)
            xr, wr = place(n.r, d + 1, le + wl)
            x = (xl + xr) / 2
            pos[id(n)] = (x, d)
            return x, wl + wr
        if n.l is not None:
            xl, wl = place(n.l, d + 1, le)
            pos[id(n)] = (xl + 0.5, d)
            return xl + 0.5, wl + 0.5
        xr, wr = place(n.r, d + 1, le + 0.5)
        pos[id(n)] = (xr - 0.5, d)
        return xr - 0.5, wr + 0.5

    _, total = place(t, 0, 0)
    maxd = max(d for _, d in pos.values())
    pad = r + 8
    W = total * hg + 2 * pad
    H = maxd * vg + 2 * pad
    xy = lambda n: (pad + pos[id(n)][0] * hg, pad + pos[id(n)][1] * vg)
    edges, nodes = [], []

    def walk(n):
        if n is None:
            return
        x, y = xy(n)
        for c in (n.l, n.r):
            if c is not None:
                cx, cy = xy(c)
                edges.append(f'<line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}"/>')
                walk(c)
        cls = mark.get(n.v, '')
        nodes.append(f'<circle class="nd {cls}" cx="{x}" cy="{y}" r="{r}"/>'
                     f'<text class="tv" x="{x}" y="{y + 4.5}">{n.v}</text>')
        if n.v in badges:
            bx, by = x + r - 1, y - r + 1
            nodes.append(f'<circle class="bd" cx="{bx}" cy="{by}" r="8.5"/>'
                         f'<text class="bt" x="{bx}" y="{by + 3.4}">{badges[n.v]}</text>')

    walk(t)
    cap = f'<text class="cap" x="{W / 2}" y="{H - 1}">{note}</text>' if note else ''
    return (f'<svg class="tree" viewBox="0 0 {W} {H + (10 if note else 0)}" width="{W}" height="{H + (10 if note else 0)}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<g class="ed">{"".join(edges)}</g>{"".join(nodes)}{cap}</svg>')


def order_badges(seq):
    return {v: i + 1 for i, v in enumerate(seq)}


# ---------------------------------------------------------------- code
def code(src, cls=''):
    src = src.strip('\n')
    if 'nocom' in cls:
        src = '\n'.join(re.sub(r'\s*//.*$', '', ln) for ln in src.split('\n'))
        src = '\n'.join(re.sub(r'^( +)', lambda m: ' ' * (len(m.group(1)) // 2), ln) for ln in src.split('\n'))
    s = _h.escape(src)
    s = s.replace('«', '<span class="flip">').replace('»', '</span>')
    return f'<pre class="code {cls}">{s}</pre>'


# ---------------------------------------------------------------- mang
def cells(a, hl=None, dim=None, sorted_=None, pivot=None):
    hl = hl or set()
    dim = dim or set()
    sorted_ = sorted_ or set()
    out = []
    for i, v in enumerate(a):
        c = 'c'
        if i in sorted_:
            c += ' s'
        if i in hl:
            c += ' h'
        if i in dim:
            c += ' d'
        if pivot is not None and i == pivot:
            c += ' p'
        out.append(f'<span class="{c}">{v}</span>')
    return '<span class="arr">' + ''.join(out) + '</span>'


def row(label, arr_html, note=''):
    n = f' <span class="note">{note}</span>' if note else ''
    return f'<div class="tr"><span class="lb">{label}</span>{arr_html}{n}</div>'


def selection_trace(a):
    a = a[:]
    n = len(a)
    rows = [row('đầu', cells(a))]
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
        note = f'min = {a[i]}, ' + (f'đổi vị trí {i} ↔ {m}' if m != i else 'đã đúng chỗ')
        rows.append(row(f'i={i}', cells(a, hl={i, m} if m != i else set(), sorted_=set(range(i + 1))), note))
    return rows


def bubble_trace(a):
    a = a[:]
    n = len(a)
    rows = [row('đầu', cells(a))]
    for i in range(n - 1):
        sw = 0
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                sw += 1
        rows.append(row(f'lượt {i + 1}', cells(a, sorted_=set(range(n - 1 - i, n))), f'{sw} lần đổi chỗ'))
        if sw == 0:
            rows[-1] = row(f'lượt {i + 1}', cells(a, sorted_=set(range(n))), '0 lần đổi chỗ, đã xong (các lượt sau không đổi)')
            break
    return rows


def insertion_trace(a):
    a = a[:]
    n = len(a)
    rows = [row('đầu', cells(a))]
    for i in range(1, n):
        x, j = a[i], i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
        rows.append(row(f'i={i}', cells(a, hl={j + 1}, sorted_=set(range(i + 1))), f'chèn {x} vào vị trí {j + 1}'))
    return rows


def merge_trace(a):
    a = a[:]
    split_lines, merge_lines = [], []

    def ms(l, r, d):
        seg = a[l:r + 1]
        split_lines.append('&nbsp;&nbsp;' * d + '[' + ' '.join(map(str, seg)) + ']')
        if l < r:
            m = (l + r) // 2
            ms(l, m, d + 1)
            ms(m + 1, r, d + 1)
            L, R = a[l:m + 1], a[m + 1:r + 1]
            res = sorted(L + R)
            merge_lines.append(f'[{" ".join(map(str, L))}] + [{" ".join(map(str, R))}] → <b>[{" ".join(map(str, res))}]</b>')
            a[l:r + 1] = res

    ms(0, len(a) - 1, 0)
    return split_lines, merge_lines


def quick_trace(a):
    a = a[:]
    rows = [row('đầu', cells(a))]

    def qs(l, r):
        i, j = l, r
        x = a[(l + r) // 2]
        while i <= j:
            while a[i] < x:
                i += 1
            while a[j] > x:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1
        rows.append(row(f'[{l}..{r}]', cells(a, dim=set(range(len(a))) - set(range(l, r + 1))),
                        f'pivot x = {x}; sau chia: trái [{l}..{j}], phải [{i}..{r}]'))
        if l < j:
            qs(l, j)
        if i < r:
            qs(i, r)

    qs(0, len(a) - 1)
    return rows


# ---------------------------------------------------------------- css
CSS = r"""
@page { size: A4; margin: 13mm 12mm 15mm 12mm;
  @bottom-center { content: counter(page) " / " counter(pages); font: 8pt 'Segoe UI', Arial, sans-serif; color:#667; }
  @bottom-left { content: var(--foot); font: 8pt 'Segoe UI', Arial, sans-serif; color:#667; } }
:root { --ink:#18222e; --accent:#1c4a78; --soft:#edf1f5; --rule:#b4bfca; --hot:#d9e6f2; --warn:#fbeed0; --foot:"Cốt Đê · Ôn tập DSA"; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: var(--ink); font-size: 10.2pt; line-height: 1.42; margin: 0; }
h1 { font-size: 21pt; margin: 0 0 2mm; color: var(--accent); letter-spacing: .2px; }
h1 small { display:block; font-size: 10pt; font-weight: 400; color:#556; margin-top: 1mm; }
h2 { font-size: 13.5pt; margin: 6mm 0 2.2mm; padding: 1.2mm 3mm; background: var(--accent); color: #fff; border-radius: 1.2mm; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 4mm 0 1.4mm; color: var(--accent); border-bottom: 1px solid var(--rule); page-break-after: avoid; }
h4 { font-size: 10pt; margin: 2.6mm 0 1mm; page-break-after: avoid; }
p { margin: 1.2mm 0; }
ul, ol { margin: 1mm 0 1.6mm; padding-left: 5mm; } li { margin: .4mm 0; }
code { font-family: Consolas, 'Courier New', monospace; font-size: .92em; background: var(--soft); padding: 0 1mm; border-radius: .8mm; }
pre.code { font-family: Consolas, 'Courier New', monospace; font-size: 8.6pt; line-height: 1.32; background: #f6f8fa; border: .3mm solid var(--rule); border-left: 1.2mm solid var(--accent); border-radius: 1mm; padding: 1.6mm 2.4mm; margin: 1.6mm 0; white-space: pre; page-break-inside: avoid; overflow: hidden; }
pre.code .flip { background: #ffe08a; font-weight: 700; padding: 0 .4mm; border-radius: .5mm; outline: .2mm solid #b88a00; }
pre.tiny { font-size: 7.4pt; line-height: 1.25; padding: 1mm 1.6mm; margin: 1mm 0; }
.box { border: .3mm solid var(--rule); background: var(--soft); border-radius: 1.4mm; padding: 2mm 3mm; margin: 2mm 0; page-break-inside: avoid; }
.box.warn { background: var(--warn); border-color: #d8b25a; }
.box.ans { background: #eaf5ec; border-color: #86b58f; }
.box b.t { color: var(--accent); }
.fig { display: flex; flex-wrap: wrap; gap: 3mm; justify-content: center; align-items: flex-end; margin: 2mm 0; page-break-inside: avoid; }
.fig figure { margin: 0; text-align: center; }
.fig figcaption { font-size: 8.4pt; color: #445; margin-top: .6mm; }
svg.tree { max-width: 100%; height: auto; }
svg.tree line { stroke: #4a5a6a; stroke-width: 1.4; }
svg.tree circle.nd { fill: #fff; stroke: #1c4a78; stroke-width: 1.6; }
svg.tree circle.nd.del { fill: #f6cccc; stroke: #a02020; stroke-width: 2.2; stroke-dasharray: 3 2; }
svg.tree circle.nd.new { fill: #cfe9d4; stroke: #2a7a3a; stroke-width: 2.2; }
svg.tree circle.nd.rep { fill: #ffe9a8; stroke: #a07800; stroke-width: 2.2; }
svg.tree text.tv { font: 700 12.5px 'Segoe UI', Arial, sans-serif; text-anchor: middle; fill: #18222e; }
svg.tree circle.bd { fill: #1c4a78; }
svg.tree text.bt { font: 700 10px 'Segoe UI', Arial, sans-serif; text-anchor: middle; fill: #fff; }
svg.tree text.cap { font: 10px 'Segoe UI', Arial, sans-serif; text-anchor: middle; fill: #445; }
table { border-collapse: collapse; width: 100%; margin: 1.6mm 0; font-size: 9.2pt; page-break-inside: avoid; }
th, td { border: .3mm solid var(--rule); padding: .9mm 1.8mm; vertical-align: top; text-align: left; }
th { background: var(--hot); }
td.c { text-align: center; }
.arr { display: inline-flex; vertical-align: middle; }
.arr .c { min-width: 6.1mm; height: 5.6mm; line-height: 5.6mm; text-align: center; border: .25mm solid #7d8a97; margin-right: -.25mm; font-size: 8.8pt; background: #fff; font-family: Consolas, monospace; }
.arr .c.s { background: #e1e8ef; }
.arr .c.h { background: #ffe08a; font-weight: 700; }
.arr .c.d { color: #aab; background: #f3f3f3; }
.tr { display: flex; align-items: center; gap: 2mm; margin: .6mm 0; page-break-inside: avoid; }
.tr .lb { width: 17mm; font-size: 8.2pt; color: #445; text-align: right; flex: none; }
.tr .note { font-size: 8.2pt; color: #445; }
.trace { margin: 1.2mm 0 3mm; }
.mono { font-family: Consolas, monospace; font-size: 8.6pt; line-height: 1.35; }
.merge { display:grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.merge > div { border: .3mm solid var(--rule); border-radius: 1mm; padding: 1.4mm 2mm; background: #fafbfc; }
.merge h5 { margin: 0 0 1mm; font-size: 8.6pt; color: var(--accent); }
.pagebreak { page-break-before: always; }
.kv { display:grid; grid-template-columns: auto 1fr; gap: .6mm 3mm; font-size: 9.2pt; }
.kv b { color: var(--accent); }
.two { column-count: 2; column-gap: 6mm; }
.two > * { break-inside: avoid; }
.sm { font-size: 8.8pt; }
.three { display:grid; grid-template-columns: repeat(3, 1fr); gap: 0 2.4mm; align-items: start; }
.three .s2 { grid-column: span 2; }
.tag { display:inline-block; font-size: 7.8pt; font-weight:700; background: var(--accent); color:#fff; border-radius: 1mm; padding: 0 1.4mm; margin-right: 1mm; }
"""

PAGE = """<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>{title}</title>
<style>{css}{extra}</style></head><body>{body}</body></html>"""
