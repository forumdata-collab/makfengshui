/* ── makfengshui.js — 年份切換 + 生肖運程卡片渲染 ── */

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

/* ── 主渲染：年份切換 → 重建全部卡片 ── */
function renderCards(year) {
  var grid = document.getElementById('zodiac-grid');
  if (!grid) return;
  var data = (window.FORTUNE_DATA || {}).fortune || {};
  var yearData = data[String(year)] || {};
  grid.innerHTML = '';

  ZODIACS.forEach(function(z) {
    var card = document.createElement('div');
    card.className = 'zodiac-card';
    card.id = z.cn;

    // 卡片頭部
    var header = document.createElement('div');
    header.className = 'card-header';
    header.innerHTML =
      '<div class="z-icon">' + z.icon + '</div>' +
      '<div class="z-info"><div class="z-cn">屬' + z.cn + '</div>' +
      '<div class="z-en">' + z.en + '</div></div>';
    card.appendChild(header);

    // 六大運程段落
    var body = document.createElement('div');
    body.className = 'card-body';

    SECTIONS.forEach(function(sec) {
      var secDiv = document.createElement('div');
      secDiv.className = 'fortune-sec' + (sec.key === '開運攻略' ? ' open-luck' : '');
      var text = (yearData[z.cn] && yearData[z.cn][sec.key]) || '暫無資料';
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

  renderCards(year);

  // 更新 hero 小標題
  var badge = document.querySelector('.hero-badge');
  if (badge) {
    var info = (window.FORTUNE_DATA || {});
    var years = info.years || [2023,2024,2025];
    if (years.includes(+year)) badge.textContent = '麥玲玲 十二生肖運程 · ' + year + ' ' + getYearLabel(year);
  }
}

function getYearLabel(y) {
  var labels = {'2023':'癸卯兔年','2024':'甲辰龍年','2025':'乙巳蛇年'};
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
