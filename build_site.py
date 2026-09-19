#!/usr/bin/env python3
"""將 fortune_data.json + site_extra.json 組合成自包含單頁靜態站（麥玲玲十二生肖運程，暗色金主題）。

包含：生肖運程（預設收折）、犯太歲速查、九宮飛星布局（麥氏化解）。
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CONTENT = ROOT / "content"
OUT = ROOT / "index.html"

# ── 數據來源：content/ 內置（可複製構建）；外部目錄只在本地存在時優先 ──
EXTERNAL_DATA = pathlib.Path("/home/ubuntu/makfengshui-data/fortune_data.json")
LOCAL_DATA = CONTENT / "fortune_data.json"
EXTERNAL_EXTRA = pathlib.Path("/home/ubuntu/makfengshui-data/site_extra.json")
LOCAL_EXTRA = CONTENT / "site_extra.json"

YEARS = [2023, 2024, 2025]
YEAR_CN = {2023: "癸卯·兔年", 2024: "甲辰·龍年", 2025: "乙巳·蛇年"}
ZODIAC_ORDER = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]
ZODIAC_EN = {
    "鼠": "Rat", "牛": "Ox", "虎": "Tiger", "兔": "Rabbit", "龍": "Dragon", "蛇": "Snake",
    "馬": "Horse", "羊": "Goat", "猴": "Monkey", "雞": "Rooster", "狗": "Dog", "豬": "Pig",
}
ZODIAC_ICON = {
    "鼠": "🐭", "牛": "🐮", "虎": "🐯", "兔": "🐰", "龍": "🐲", "蛇": "🐍",
    "馬": "🐴", "羊": "🐑", "猴": "🐵", "雞": "🐔", "狗": "🐶", "豬": "🐷",
}


def year_options(selected=2025):
    return "\n".join(
        f'<option value="{y}"{" selected" if y == selected else ""}>{y} {YEAR_CN[y]}</option>'
        for y in YEARS
    )


def year_cards_html(selected=2025):
    lines = ['<div class="year-bar">']
    for y in YEARS:
        active = ' active' if y == selected else ''
        cn = YEAR_CN[y].split("·")[0]
        beast = YEAR_CN[y].split("·")[1]
        lines.append(
            f'<div class="year-card{active}" data-year="{y}">'
            f'<div class="y">{cn}</div>'
            f'<div class="g">{y} {beast}</div>'
            f'<div class="s">天干地支</div></div>'
        )
    lines.append('</div>')
    return "\n".join(lines)


def quick_index():
    lines = ['<div class="quick-index">', '<span class="qi-label">快速索引</span>']
    lines.append('<a href="#tai-sui">⚡ 犯太歲速查</a>')
    lines.append('<a href="#fly-stars">✦ 九宮飛星</a>')
    lines.append('<a href="#luck">🧧 開運攻略</a>')
    lines.append('<span class="qi-label" style="margin-left:6px">生肖</span>')
    for z in ZODIAC_ORDER:
        lines.append(f'<a href="#{z}">{z}</a>')
    lines.append('</div>')
    return "\n".join(lines)


def load_json(external, local, name):
    """依優先順序載入 JSON，回傳 dict。"""
    for p in (external, local):
        if p.exists():
            print(f"  數據來源：{p}")
            return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError(f"找不到 {name} — 請在以下任一位置提供：\n  {external}\n  {local}")


def build():
    css = (ASSETS / "makfengshui.css").read_text(encoding="utf-8")
    js = (ASSETS / "makfengshui.js").read_text(encoding="utf-8")
    fortune_data = load_json(EXTERNAL_DATA, LOCAL_DATA, "fortune_data.json")
    site_extra = load_json(EXTERNAL_EXTRA, LOCAL_EXTRA, "site_extra.json")

    # 統計
    n_years = len(fortune_data.get("years", []))
    total = sum(len(v) for v in fortune_data.get("fortune", {}).values())
    print(f"  {n_years} 個年份, {total} 個生肖條目")

    # 當前預設年份（取最新）
    default_year = max(fortune_data.get("years", [2025]))

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="麥玲玲十二生肖運程速覽 — 2023-2025年整體運勢、事業、財運、感情、健康、開運攻略、犯太歲速查及九宮飛星布局。">
<title>麥玲玲 十二生肖運程 · 犯太歲 · 九宮飛星</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<div class="hero">
<div class="hero-badge">麥玲玲 十二生肖運程 · {default_year} {YEAR_CN[default_year]}</div>
<h1>🧧 麥玲玲 十二生肖運程速覽</h1>
<p>綜合麥玲玲師傅生肖運程著作，整理 2023-2025 年十二生肖整體運勢、事業、財運、感情、健康及開運攻略；另附每年犯太歲速查及九宮飛星布局（以麥氏化解方法為依歸）</p>
<div class="disclaimer">
⚠️ <b>免責聲明</b>：本頁內容整理自麥玲玲師傅的生肖運程著作（包括《麥玲玲 2025 蛇年運程》等），僅供娛樂參考，並非專業命理建議。內容可能經 AI 輔助整理，如有疑問請諮詢專業風水師或參閱原著。
</div>
</div>

{year_cards_html(default_year)}

<div class="controls">
<label>選擇年份：</label>
<select id="year-select" onchange="switchYear()">
{year_options(default_year)}
</select>
</div>

{quick_index()}

<!-- ⚡ 犯太歲速查 -->
<div class="section" id="tai-sui">
<div class="section-title"><span class="zodiac-icon">⚡</span><span>犯太歲速查</span></div>
<p class="section-intro">每年犯太歲生肖、犯太歲類型與化解方法（沖喜／謹慎部署／佩戴合生肖飾物），以麥玲玲〈犯太歲化解錦囊〉為依歸。</p>
<div id="tai-sui-body"></div>
</div>

<!-- ✦ 九宮飛星布局 -->
<div class="section" id="fly-stars">
<div class="section-title"><span class="zodiac-icon">✦</span><span>九宮飛星布局</span></div>
<p class="section-intro">每年入中宮星及九宮飛星分佈，各方位的星曜吉凶與麥氏催旺／化解物品（見麥玲玲〈家居全方位風水陣〉）。適用期由該年立春起計。</p>
<div class="fly-year-label" id="fly-label"></div>
<div class="fly-grid" id="fly-grid"></div>
</div>

<!-- 🧧 十二生肖開運攻略 -->
<div class="section" id="luck">
<div class="section-title"><span class="zodiac-icon">🧧</span><span>十二生肖開運攻略</span></div>
<p class="section-intro">麥玲玲〈十二生肖開運攻略〉——十二生肖（包括冇犯太歲者）全年開運建議：佩戴飾物、顏色、方位及生活習慣。</p>
<div class="luck-grid" id="luck-grid">
<!-- JS 動態渲染 12 生肖開運卡（預設收折） -->
</div>
</div>

<div class="zodiac-grid" id="zodiac-grid">
<!-- JS 動態渲染 12 張生肖運程卡片（預設收折） -->
</div>

<div class="footer">
<p>內容整理自麥玲玲師傅生肖運程著作（2023-2025）· 僅供娛樂參考，不代表專業命理建議</p>
<p>如需準確運程，請參閱麥玲玲原著或諮詢專業風水師</p>
<p>© 2024-2025 麥玲玲運程速覽 · 非官方產品，與麥玲玲師傅無關</p>
</div>

<button id="toTop" aria-label="返回頂部">↑</button>
</div>

<script>
window.FORTUNE_DATA = {json.dumps(fortune_data, ensure_ascii=False)};
window.SITE_EXTRA = {json.dumps(site_extra, ensure_ascii=False)};
</script>
<script>{js}</script>
</body>
</html>"""

    OUT.write_text(html, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"✓ index.html: {size_kb:.0f} KB ({n_years} 年份, {total} 生肖 + 犯太歲 + 飛星)")


if __name__ == "__main__":
    build()