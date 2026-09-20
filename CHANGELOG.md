## 2026-09-20 — Site v3: 2026-2030 年份擴展

- **2026 丙午馬年 full content** (from《麥玲玲 2026 馬年運程》scanned book): 12 生肖運程 (6 sections), 12 開運攻略, 犯太歲 (馬值/鼠沖/兔破/牛害 + 飾物配對), 九宮飛星 (一白入中). Vision-extracted.
- **2027-2030 rule-derived data** (marked 「推演」): 犯太歲 + 飾物配對 + 九宮飛星 + 太歲/歲破/三煞方位, computed from the Mak-system rules verified against 2023-2026 books (地支六沖/三刑/六害/六破/值 + 洛書順飛, 入中星逐年逆退). Fortune/luck text shows 「待原著」 until books available. Cross-checked: 2027 九紫入中 + 羊值/牛沖/狗刑/鼠害 matches the independently-OCR'd sokman-2027 data.
- Year selector now 2023-2030 (8 years). OCR backup updated with 2026 extraction (12 zodiac + 12 luck + tai + fly).

## 2026-09-20 — Site v2.1: 十二生肖開運攻略 (all 12 zodiacs, 3 years)

- **🧧 十二生肖開運攻略** section added: 麥玲玲〈十二生肖開運攻略〉for ALL 12 zodiacs (including non-犯太歲 ones) — 概述 / 吉星 / 凶星 / 開運攻略 sub-sections (佩戴飾物、顏色、方位、習慣). Covers 2023/2024/2025 (36 entries, vision-extracted from book pages 27-40).
- Section is default-collapsed (click header to expand); quick-index bar gains 🧧 開運攻略 anchor.
- OCR backup refreshed with luck data: SHA256 `8afe3c9715cd5ff26cca49bd90ff0892054cd4d552349531d7d24ad42d87340b` (183 MB, incl. 2023_gl/2024_gl/2025_gl), re-uploaded to GDrive folder ocr-backups-mak-sok.

# CHANGELOG

## 2026-09-20 — Site v2: 犯太歲速查 + 九宮飛星布局 + 預設收折

Major update referencing the 蘇氏 website format, with 麥氏 (Mak Ling Ling) solutions as authority:

- **⚡ 犯太歲速查** section: per-year 值年太歲, 犯太歲生肖 (值/沖/刑/害/破) with descriptions, and 麥氏飾物配對 + 化解三法 (沖喜／謹慎部署／佩戴合生肖飾物), from each book's 〈犯太歲化解錦囊〉.
- **✦ 九宮飛星布局** section: per-year 入中宮星 + 9-palace flying star grid, each direction's star/五行/吉凶 + 麥氏化解或催旺物品 + 方位注意事項, from each book's 九宮飛星圖 + 〈家居全方位風水陣〉. 適用期 = 該年立春起計.
- **預設收折**: 12 生肖運程卡片 default-collapsed (click header to expand).
- **主頁索引及返回頂部**: quick-index bar (犯太歲/飛星/12生肖 anchors) + back-to-top button.
- build_site.py now also reads `content/site_extra.json` (犯太歲 + 飛星 data); build verified reproducible from repo content alone (external data dir only preferred when present locally).

## OCR 備份 (local only, not committed — scanned-book derived text)

`~/makfengshui-data/makfengshui-ocr-backup.tar.gz` — 36 per-zodiac extraction JSONs (3 years × 12) + fortune_data.json + site_extra.json + page renders.

- SHA256: `77d8a89d168f76ec0a2acb512689fd2a3916c964b80a93b33934f141a5d9b3a4`
- Size: 124,506,416 bytes (91 entries)
- Regenerate: `tar czf makfengshui-ocr-backup.tar.gz ocr/ fortune_data.json site_extra.json`

## 2026-09-20 — Initial release

Site framework + full fortune data extraction from 麥玲玲 2023/2024/2025 運程書 (36 zodiac entries × 6 sections: 整體運勢/事業運/財運/感情運/健康運/開運攻略).