## 2026-09-22 — 2027 真書換版 + v3 星曜重算 2028-2030 + 星名統一

- **2027 真書（羊年）全文上線**：12 肖五節運程（`real2026/fort_text`）＋開運錦囊 ★ 建議 60 條（`real2026/luck_tips`，逐肖 5 條）＋吉凶星（`real2026/ext`，逐粒雙讀核對）。2027 由「推演」改標原著，`DERIVED_YEARS=[2028,2029,2030]`，hero 改「原著年份：2023-2027」。
- **引擎選擇以 out-of-sample 實測決定**：真書 2027（12 肖吉凶星）作唯一未見過測試集 — v2 命中 54／多推 19／漏推 10；**v3 命中 61／多推 14／漏推 3（採用）**；v4（用 2023-2026 重提資料重建）54／19／10 無進步。比較工具 `derive/compare_engines_2027.py`。
- **2028-2030 用 v3 星曜重算**：30/36 肖星曜有變（2028 九肖、2029 十二肖、2030 九肖），散文由 writer agent 逐年改寫至只用該肖清單內星曜；`audit_gen.py` 四年 **0 錯 0 提示**。
- **修正 2030 全部 12 肖方位整組反轉**（與早前 2027 飛星 180° 反轉同類問題）＋2028 部分方位／化煞物品對回飛星盤；2028 馬由「吉星欠奉」變真有「天廚」，2028 狗、2029 蛇／羊、2030 雞 走正確「流年吉星欠奉，須借對宮吉星，力量約三成」路線（`auspicious` 合法留空 + 前端顯示「（欠奉）」）。
- **星名統一（依真書印刷字形）**：貴索→貫索、勾神→勾絞、飛簾→飛廉、扳殺／扳煞→扳鞍、咸池→咸池桃花。真書本身各頁寫法不一（星曜表印「勾絞」、散文印「勾神」）→ 統一在顯示層（`apply_2027_real.py` 內 `CANON`），`real2026/` 證據檔保持原樣。
- **修回歸**：`integrate.py` 舊版仍 loop 2027 → 每次重跑以推演版覆蓋真書（2027 開運錦囊由 60/60 跌到 2/60）。已剔除 2027 並在檔內註明。
- **OCR 記錄備份更新**：`makfengshui-OCR-備份(麥玲玲)-20260922.tar.gz`（318 檔、340 MB、SHA256 `636e4c8c…`、md5 `0cad67c4…`，GDrive `ocr-backups-mak-sok`，read-back md5 一致）。

## 2026-09-21 — Site v4: 流年星神規則逆向 + 2027-2030 全內容推演

- **流年星神系統逆向完成**: 由 2023-2026 四年實書的吉／凶星資料歸納出 77 粒星的排盤規則 — 45 粒純旋轉（星位 = 流年支 + k，即歲君十二神煞次第：太歲→太陽→喪門→太陰→官符→小耗→歲破→龍德→白虎→天德→吊客→病符）、9 粒鏡像（星位 = C − 流年支，例如紅鸞 C=卯、天喜 C=酉、天哭 C=午、披頭 C=辰）、23 粒三合／刑害關係制（將星=三合帝旺、華蓋=三合墓、驛馬=三合沖等）。
- **回測**: 引擎重算 2023-2026 共 48 個生肖年，47/48 完全覆蓋原書吉凶星（唯一差異為 2025 肖兔「地解」的歸類，書中文字顯示屬吉星）。三年同一三合局的年份互相印證一致。
- **2027-2030 十二生肖吉星／凶星全面推演**，按規則重算而非複製：旋轉星用 k、鏡像星用 C、三合關係星用同局年份的絕對星位（例：將星在亥卯未局固定於卯）。已另行核對 2027 值太歲生肖之凶星（太歲／劍鋒／伏屍）與坊間曆書一致。
- **2027-2030 運程全文 + 開運攻略上線**（48 生肖年 × 整體運勢／事業／財運／感情／健康 + 4 條開運攻略 + 開運攻略摘要），內容以推算星曜、生肖關係（值／沖／刑／害／破／合／三合）、當年九宮飛星方位及太歲／歲破／三煞方位為約束撰寫，卡片與開運攻略均加 **「推演」** 標籤區分原著年份。
- 自動審核腳本 (`derive/audit_gen.py`)：檢查星曜引用範圍、星曜—方位配對、干支年份、犯太歲化解飾物、字數 — 48 個檔案 0 錯誤 0 提示。

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

## 抽取／推演記錄備份 (local only, not committed)

`~/makfengshui-data/makfengshui-ocr-backup-<日期>.tar.gz` — 全部抽取與推演記錄：原著掃描 PDF（2023/2024/2025/2026 + 2027）、各年 per-zodiac 抽取 JSON、真書 2027 核對與運程全文（`real2026/{ext,fort_text,luck_tips,rex}`）、規則庫與引擎（`derive/*.json|py`）、生成內容（`derive/gen`）、MANIFEST.txt（含各 PDF SHA256）。排除可重生嘅 PNG 渲染。

- 最新（2026-09-21）: SHA256 `4e0f76f9aa735de6a3ec00dba09a0571f48fb0d48eabae7b4f7680618ec79d7b`，340 MB，244 檔
- 上傳位置：GDrive `ocr-backups-mak-sok`（`python3 derive/upload_dated_backup.py`，read-back 比對 md5）
- 打包：`python3 derive/build_backup.py`（自動產生 MANIFEST 與 SHA256）
- 舊版（2026-09-20）: `makfengshui-ocr-backup.tar.gz` — 517 MB，含 2023-2026 page renders（PNG 可由 PDF 重生，故新版不再收錄）

## 2026-09-20 — Initial release

Site framework + full fortune data extraction from 麥玲玲 2023/2024/2025 運程書 (36 zodiac entries × 6 sections: 整體運勢/事業運/財運/感情運/健康運/開運攻略).