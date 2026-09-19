#!/usr/bin/env python3
"""將 fortune_data.json 組合成自包含單頁靜態站（麥玲玲十二生肖運程，暗色金主題）。"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CONTENT = ROOT / "content"
OUT = ROOT / "index.html"

# ── 數據來源：外置目錄優先（更新時不必進 repo），fallback 至 content/ ──
EXTERNAL_DATA = pathlib.Path("/home/ubuntu/makfengshui-data/fortune_data.json")
LOCAL_DATA = CONTENT / "fortune_data.json"

YEARS = [2023, 2024, 2025]
YEAR_CN = {2023: "癸卯·兔年", 2024: "甲辰·龍年", 2025: "乙巳·蛇年"}
ZODIAC_ORDER = ["鼠","牛","虎","兔","龍","蛇","馬","羊","猴","雞","狗","豬"]
ZODIAC_EN = {
    "鼠":"Rat","牛":"Ox","虎":"Tiger","兔":"Rabbit","龍":"Dragon","蛇":"Snake",
    "馬":"Horse","羊":"Goat","猴":"Monkey","雞":"Rooster","狗":"Dog","豬":"Pig",
}
ZODIAC_ICON = {
    "鼠":"🐭","牛":"🐮","虎":"🐯","兔":"🐰","龍":"🐲","蛇":"🐍",
    "馬":"🐴","羊":"🐑","猴":"🐵","雞":"🐔","狗":"🐶","豬":"🐷",
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
    for z in ZODIAC_ORDER:
        lines.append(f'<a href="#{z}">{z}</a>')
    lines.append('</div>')
    return "\n".join(lines)


def load_fortune_data():
    """依優先順序載入運程數據，回傳 dict。"""
    for p in (EXTERNAL_DATA, LOCAL_DATA):
        if p.exists():
            raw = json.loads(p.read_text(encoding="utf-8"))
            print(f"  數據來源：{p}")
            return normalise(raw)
    raise FileNotFoundError(
        f"找不到 fortune_data.json — 請在以下任一位置提供：\n  {EXTERNAL_DATA}\n  {LOCAL_DATA}"
    )


def normalise(raw):
    """容錯正規化：支持 {'years':[...],'fortune':{y:{z:{sec:txt}}}} 或直接 {y:{...}}"""
    # 舊格式：dict top-level by year
    if "fortune" not in raw and all(str(k).isdigit() for k in raw.keys()):
        return {"years": sorted(int(k) for k in raw.keys()), "fortune": {str(k): v for k, v in raw.items()}}
    # 正常格式
    return raw


def build():
    css = (ASSETS / "makfengshui.css").read_text(encoding="utf-8")
    js = (ASSETS / "makfengshui.js").read_text(encoding="utf-8")
    fortune_data = load_fortune_data()

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
<meta name="description" content="麥玲玲十二生肖運程速覽 — 2023-2025年整體運勢、事業、財運、感情、健康及開運攻略。">
<title>麥玲玲 十二生肖運程</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<div class="hero">
<div class="hero-badge">麥玲玲 十二生肖運程 · {default_year} {YEAR_CN[default_year]}</div>
<h1>🧧 麥玲玲 十二生肖運程速覽</h1>
<p>綜合麥玲玲師傅生肖運程著作，整理 2023-2025 年十二生肖整體運勢、事業、財運、感情、健康及開運攻略</p>
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

<div class="zodiac-grid" id="zodiac-grid">
<!-- JS 動態渲染 12 張生肖運程卡片 -->
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
</script>
<script>{js}</script>
</body>
</html>"""

    OUT.write_text(html, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"✓ index.html: {size_kb:.0f} KB ({n_years} 年份, 12 生肖)")


if __name__ == "__main__":
    build()
