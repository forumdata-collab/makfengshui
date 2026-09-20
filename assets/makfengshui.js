/* ── makfengshui.js — 年份切換 + 犯太歲 + 九宮飛星 + 生肖運程卡片渲染 ── */

var ZODIACS = [
  {cn:'鼠',en:'Rat',   icon:'🐭'}, {cn:'牛',en:'Ox',    icon:'🐮'},
  {cn:'虎',en:'Tiger', icon:'🐯'}, {cn:'兔',en:'Rabbit', icon:'🐰'},
  {cn:'龍',en:'Dragon',icon:'🐲'}, {cn:'蛇',en:'Snake',  icon:'🐍'},
  {cn:'馬',en:'Horse', icon:'🐴'}, {cn:'羊',en:'Goat',   icon:'🐑'},
  {cn:'猴',en:'Monkey',icon:'🐵'}, {cn:'雞',en:'Rooster',icon:'🐔'},
  {cn:'狗',en:'Dog',   icon:'🐶'}, {cn:'豬',en:'Pig',    icon:'🐷'}
];

var SECTIONS = [
  {key:'整體運勢', icon:'☯️'},
  {key:'事業運',   icon:'💼'},
  {key:'財運',     icon:'💰'},
  {key:'感情運',   icon:'❤️'},
  {key:'健康運',   icon:'💪'},
  {key:'開運攻略', icon:'🧧'}
];

/* 九宮方位順序（洛書） */
var FLY_DIRS = ['東南','南','西南','東','中宮','西','東北','北','西北'];

var STAR_NATURE_ICON = {'吉':'🟢','凶':'🔴','平':'🟡'};

/* ── 十二生肖開運攻略（全部 12 生肖，含冇犯太歲者） ── */
function renderLuck(year) {
  var luck = ((window.SITE_EXTRA || {}).luck || {})[String(year)];
  var grid = document.getElementById('luck-grid');
  if (!grid) return;
  grid.innerHTML = '';

  ZODIACS.forEach(function(z) {
    var info = (luck && luck[z.cn]) || null;
    var card = document.createElement('div');
    card.className = 'luck-card collapsed';

    var header = document.createElement('div');
    header.className = 'luck-head';
    header.innerHTML =
      '<span class="luck-icon">' + z.icon + '</span>' +
      '<span class="luck-z">屬' + z.cn + '</span>' +
      (info
        ? '<span class="luck-stars"><span class="ls-good">吉 ' + esc(info.auspicious) + '</span><span class="ls-bad">凶 ' + esc(info.inauspicious) + '</span></span>'
        : '<span class="luck-na">暫無資料</span>') +
      '<span class="card-toggle">▾</span>';
    header.addEventListener('click', function() { card.classList.toggle('collapsed'); });
    card.appendChild(header);

    if (info) {
      var bodyEl = document.createElement('div');
      bodyEl.className = 'luck-body';
      if (info.overview) {
        bodyEl.innerHTML += '<div class="luck-overview">' + esc(info.overview) + '</div>';
      }
      (info.tips || []).forEach(function(t) {
        bodyEl.innerHTML += '<div class="luck-sec"><div class="luck-sec-title">' + esc(t.title) + '</div>' +
          '<div class="luck-sec-text">' + esc(t.text) + '</div></div>';
      });
      card.appendChild(bodyEl);
    }
    grid.appendChild(card);
  });
}

function esc(s) {
  var d = document.createElement('div');
  d.textContent = (s || '');
  return d.innerHTML;
}

/* ── 犯太歲速查 ── */
function renderTaiSui(year) {
  var body = document.getElementById('tai-sui-body');
  if (!body) return;
  var extra = (window.SITE_EXTRA || {}).tai_sui || {};
  var ts = extra[String(year)];
  if (!ts) { body.innerHTML = '<p class="dim">暫無資料</p>'; return; }

  var h = [];
  h.push('<div class="tai-summary">👑 值年太歲：<b>' + ts.tai_sui + '</b>（' + ts.year_label + '） — ' + ts.summary + '</div>');

  // 犯太歲生肖卡片
  h.push('<div class="tai-grid">');
  (ts.offenders || []).forEach(function(o) {
    var icon = '🐾';
    ZODIACS.forEach(function(z) { if (z.cn === o.zodiac) icon = z.icon; });
    h.push('<div class="tai-card">' +
      '<div class="tai-head"><span class="tai-icon">' + icon + '</span>' +
      '<span class="tai-z">' + o.zodiac + '</span>' +
      '<span class="tai-type">' + o.type + '</span></div>' +
      '<p class="tai-desc">' + o.desc + '</p>' +
      '<div class="tai-remedy">🧧 ' + o.remedy + '</div>' +
      '</div>');
  });
  h.push('</div>');

  // 通用化解三法
  h.push('<div class="tai-methods">');
  h.push('<div class="tai-methods-title">化解方法（麥氏錦囊）</div>');
  (ts.methods || []).forEach(function(m) {
    h.push('<div class="tai-method">• ' + m + '</div>');
  });
  h.push('</div>');

  body.innerHTML = h.join('');
}

/* ── 九宮飛星布局 ── */
function renderFly(year) {
  var grid = document.getElementById('fly-grid');
  var label = document.getElementById('fly-label');
  if (!grid) return;
  var extra = (window.SITE_EXTRA || {}).fly_stars || {};
  var info = (window.SITE_EXTRA || {}).star_info || {};
  var fd = extra[String(year)];
  if (!fd) { grid.innerHTML = '<p class="dim">暫無資料</p>'; return; }

  if (label) {
    label.textContent = fd.label + ' · ' + fd.center + '入中宮 · 適用期：' + fd.apply;
  }

  var h = [];
  FLY_DIRS.forEach(function(dir) {
    var cell = (fd.grid || {})[dir];
    if (!cell) return;
    var si = info[cell.star] || {name: cell.star, alias: '', el: '', nature: '', scope: ''};
    var nat = si.nature === '吉' ? 'good' : (si.nature === '凶' ? 'bad' : 'mid');
    h.push('<div class="fly-cell ' + nat + '">' +
      '<div class="fly-dir">' + dir + '</div>' +
      '<div class="fly-star">' + cell.star + '</div>' +
      '<div class="fly-name">' + si.name + (si.alias ? '<br><small>' + si.alias + '</small>' : '') + '</div>' +
      '<div class="fly-scope">' + (si.scope || '') + '</div>' +
      '<div class="fly-item">🧧 化解／催旺：' + cell.item + '</div>' +
      '<div class="fly-note">' + (cell.note || '') + '</div>' +
      '</div>');
  });
  grid.innerHTML = h.join('');
}

/* ── 生肖運程卡片（預設收折） ── */
function renderCards(year) {
  var grid = document.getElementById('zodiac-grid');
  if (!grid) return;
  var data = (window.FORTUNE_DATA || {}).fortune || {};
  var yearData = data[String(year)] || {};
  grid.innerHTML = '';

  ZODIACS.forEach(function(z) {
    var card = document.createElement('div');
    card.className = 'zodiac-card collapsed';
    card.id = z.cn;

    // 卡片頭部（點擊展開/收折）
    var header = document.createElement('div');
    header.className = 'card-header';
    header.innerHTML =
      '<div class="z-icon">' + z.icon + '</div>' +
      '<div class="z-info"><div class="z-cn">屬' + z.cn + '</div>' +
      '<div class="z-en">' + z.en + '</div></div>' +
      '<div class="card-toggle">▾</div>';
    header.addEventListener('click', function() {
      card.classList.toggle('collapsed');
    });
    card.appendChild(header);

    // 六大運程段落
    var body = document.createElement('div');
    body.className = 'card-body';

    SECTIONS.forEach(function(sec) {
      var secDiv = document.createElement('div');
      secDiv.className = 'fortune-sec' + (sec.key === '開運攻略' ? ' open-luck' : '');
      var hasBook = yearData[z.cn] && yearData[z.cn][sec.key];
      var text;
      if (hasBook) {
        text = hasBook;
      } else if (yearData[z.cn] && yearData[z.cn]._derived) {
        text = '2027-2030 為按麥氏規則推演，詳細運程待原著出版後補齊';
      } else {
        text = '暫無資料';
      }
      secDiv.innerHTML =
        '<div class="fs-label"><span class="fs-icon">' + sec.icon + '</span>' +
        '<span class="fs-title">' + sec.key + '</span></div>' +
        '<div class="fs-text">' + text + '</div>';
      body.appendChild(secDiv);
    });

    card.appendChild(body);
    grid.appendChild(card);
  });
}

/* ── 年份選單切換 ── */
function switchYear() {
  var sel = document.getElementById('year-select');
  if (!sel) return;
  var year = sel.value;

  // 高亮對應的 year-card
  document.querySelectorAll('.year-card').forEach(function(c) {
    c.classList.toggle('active', c.getAttribute('data-year') === year);
  });

  renderTaiSui(year);
  renderFly(year);
  renderLuck(year);
  renderCards(year);

  // 更新 hero 小標題
  var badge = document.querySelector('.hero-badge');
  if (badge) {
    badge.textContent = '麥玲玲 十二生肖運程 · ' + year + ' ' + getYearLabel(year);
  }
}

function getYearLabel(y) {
  var labels = {'2023':'癸卯兔年','2024':'甲辰龍年','2025':'乙巳蛇年','2026':'丙午馬年',
                '2027':'丁未羊年','2028':'戊申猴年','2029':'己酉雞年','2030':'庚戌狗年'};
  return labels[y] || '';
}

/* ── 返回頂部 ── */
(function() {
  var btn = document.getElementById('toTop');
  if (!btn) return;
  window.addEventListener('scroll', function() {
    btn.classList.toggle('show', (window.pageYOffset || document.documentElement.scrollTop) > 400);
  }, {passive: true});
  btn.addEventListener('click', function() {
    window.scrollTo({top: 0, behavior: 'smooth'});
  });
})();

/* ── 初始渲染 ── */
document.addEventListener('DOMContentLoaded', function() {
  var sel = document.getElementById('year-select');
  if (sel) switchYear();
});