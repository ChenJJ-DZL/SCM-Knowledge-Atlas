"""Generate individual book pages for SCM-Knowledge-Atlas"""
import os, re

css_file = '_new_css.css'
css = open(css_file, 'r', encoding='utf-8').read()

# Add back-link CSS
back_link_css = '''

/* Back to main link */
.back-link {
  position: fixed; top: 14px; left: 18px; z-index: 55;
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,254,249,.92); backdrop-filter: blur(10px);
  border: 1px solid var(--line); border-radius: 999px;
  padding: 8px 16px; font-size: 13px; font-weight: 600;
  color: var(--bk1); text-decoration: none;
  box-shadow: var(--shadow); transition: all .2s;
}
.back-link:hover { background: var(--bk1); color: #fff; transform: translateX(-2px); }
.back-link svg { width: 16px; height: 16px; fill: currentColor; }

/* Book page hero */
.book-hero {
  background: linear-gradient(135deg,#1e3a5f 0%,#2c5f7c 40%,#3a6a5e 100%);
  color: #fff; padding: 48px 22px 36px; position: relative; overflow: hidden;
}
.book-hero::after { content:""; position:absolute; right:-40px; top:-40px; width:160px; height:160px; border-radius:50%; background:rgba(255,255,255,.08) }
.book-hero .tag { display:inline-block; font-size:11px; letter-spacing:2px; background:rgba(255,255,255,.15); padding:3px 10px; border-radius:999px; margin-bottom:12px }
.book-hero h1 { font-size:24px; line-height:1.3; margin:0 0 8px; font-weight:800 }
.book-hero p { font-size:14px; opacity:.9; margin:4px 0; max-width:660px }
.book-hero .edit { font-size:12px; opacity:.7; margin-top:8px }
.book-main { max-width: 780px; margin: 0 auto; padding: 0 18px 80px; }
.book-main h2 { font-size:20px; font-weight:800; color:var(--ink); margin:36px 0 12px; display:flex; align-items:center; gap:8px }
.book-main h2::before { content:""; width:4px; height:18px; background:var(--bk1); border-radius:3px; display:inline-block }
.book-main h3 { font-size:15px; font-weight:700; color:var(--ink); margin:20px 0 8px }
.book-main p { font-size:14.5px; color:var(--ink-2); margin:8px 0; line-height:1.78 }
.book-toc { background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:16px 20px; margin:16px 0; box-shadow:var(--shadow) }
.book-toc ol { margin:8px 0; padding-left:24px; font-size:14px; color:var(--ink-2); line-height:1.9 }
.book-toc li { margin:2px 0 }
.highlight-box { background:var(--bk1-light); border-left:4px solid var(--bk1); padding:14px 18px; border-radius:0 12px 12px 0; margin:16px 0; font-size:14px; color:var(--ink); line-height:1.8 }
'''

# Build CSS with back-link
full_css = css + back_link_css

# JavaScript (same as main page)
js = open('_build.py','r',encoding='utf-8').read()
js_start = js.find("js = '''") + 6
js_end = js.find("</script>'''", js_start)
shared_js = js[js_start:js_end].strip()

# Back link HTML
back_link = '''
<a href="index.html" class="back-link">
  <svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
  回到主线
</a>
'''

# Three tool buttons HTML
tools = '''
<div id="right-tools">
  <button id="top" class="tool-btn show" title="回到顶部">
    <svg viewBox="0 0 24 24"><path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z"/></svg>
  </button>
  <button id="btn-search" class="tool-btn show" title="搜索 (Ctrl+K)">
    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
  </button>
  <button id="btn-toc" class="tool-btn show" title="目录">
    <svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>
  </button>
</div>
'''

# Panel HTML (TOC + Search)
panels = '''
<div class="panel-overlay" id="toc-overlay"></div>
<div class="panel" id="toc-panel">
  <div class="panel-header"><h3>📑 本书目录</h3><button class="panel-close" id="toc-close">✕</button></div>
  <div class="panel-body"><div id="toc-list"></div></div>
</div>
<div class="panel-overlay" id="search-overlay"></div>
<div class="panel" id="search-panel">
  <div class="panel-header"><h3>🔍 内容查找</h3><button class="panel-close" id="search-close">✕</button></div>
  <div class="search-box-sm">
    <input type="text" class="search-input" id="search-input" placeholder="搜索本书内容...">
    <div class="search-nav">
      <button class="search-nav-btn" id="search-prev" disabled>▲</button>
      <span class="search-count" id="search-count">0/0</span>
      <button class="search-nav-btn" id="search-next" disabled>▼</button>
    </div>
    <button class="search-clear" id="search-clear">✕</button>
  </div>
  <div class="panel-body" id="search-results"></div>
</div>
'''

# ===== BOOK DATA =====
books = []

# Book 1: 采购与供应链管理 第4版
books.append({
    'file': 'bk1.html',
    'hero_class': 'book-hero',
    'title': '采购与供应链管理：一个实践者的角度',
    'subtitle': '第4版（2024）',
    'author': '刘宝红（Bob Liu）',
    'publisher': '机械工业出版社 | ISBN: 978-7-111-75428-2',
    'pages': '380页',
    'color': '#1e3a5f',
    'intro': '聚焦经济增速放缓下如何系统改善供应链的成本、交付和资产周转。贯穿全书的主线：<strong>通过改变能力来改变行为，通过改变行为来改变结果。</strong>',
    'toc': [
        '第一篇 供应链的全局观',
        '  第1章 多角度透视供应链（三流集成、日本起源、垂直整合解体）',
        '  第2章 供应链的本质是协作（强相关指标、集成供应链）',
        '  第3章 供应链与产品/业务的战略匹配（经济型/响应型、推拉结合、模块化）',
        '  第4章 供应链与设计的闭环集成（IPD、设计优化、供应商早期介入）',
        '  第5章 供应链与营销的闭环集成（S&OP、闭环交付信息化）',
        '  第6章 供应链的牛鞭效应（四成因及应对）',
        '  第7章 管理复杂的供应链（汽车行业、小批量行业）',
        '  第8章 供应链的全球化和反全球化',
        '第二篇 管好供应商，才能管好供应链',
        '  第9章 供应商管理的三大误区（多权分立、采购额分散、有选择没管理）',
        '  第10章 供应商分类：区别对待重点管理（五分法、2016年小米案例）',
        '  第11章 供应商评估：识别短板敦促改进（财务/质量/生产/物料评估）',
        '  第12章 供应商选择：制定合格供应商清单（一品一点、规模效益）',
        '  第13章 供应商绩效管理：QCDSTAP七大指标（成本/质量/交付/服务/技术/资产/流程）',
        '  第14章 供应商集成：最高层次（早期介入、降本三台阶）',
        '  第15章 关键下级供应商的管理（客户指定供应商、本田苹果案例）',
        '第三篇 从"小采购"到"大采购"，影响总成本',
        '  第16章 从"小采购"到"大采购"（五阶段模型、猎人vs牧人）',
        '  第17章 "大采购"的组织建设（两层分离、跨职能团队、人才先行）',
        '  第18章 采购的集中与分散（集中采购、混合采购陷阱、变革管理）',
    ],
    'highlights': [
        ('核心方法论贯穿全书', '改变方法论而非更努力："老方法自然会产生老结果。不能光更努力，而是要不一样。"通过管好需求做好计划、对接产品设计优化成本、选好管好供应商获取规模效益——从根本解决基本面问题。'),
        ('标志性案例', '苹果供应链成功（库克打造供应链核心竞争力）、戴尔直销模式兴衰（推拉结合的经典教训）、小米三星2016年战略供应商危机（雷军四次飞韩国）、摩托罗拉复杂度致死（100+种电池型号）、振华重工增长陷阱案例。'),
        ('关于本书', '第4版相较第3版更加聚焦"为什么"，通过探究根因来更好地回答"怎么办"。坚持三项准则：不宣传走捷径、不宣传最佳实践、填补学者与实践者之间的空白。'),
    ]
})

# Book 2: 高成本高库存重资产 第2版
books.append({
    'file': 'bk2.html',
    'hero_class': 'book-hero',
    'title': '供应链管理：高成本、高库存、重资产的解决方案',
    'subtitle': '第2版（2023）',
    'author': '刘宝红（Bob Liu）',
    'publisher': '机械工业出版社 | ISBN: 978-7-111-72591-6',
    'pages': '260页',
    'color': '#2c5f7c',
    'intro': '提出"<strong>前端防杂、后端减重、中间治乱</strong>"的系统解决方案，从产品管理、需求管理和供应管理多角度解决高成本、高库存、重资产运营问题。',
    'toc': [
        '引言 高速增长的盛宴渐趋结束，面临"增长陷阱"怎么办',
        '第一篇 前端防杂：强化产品管理和标准化设计，降低复杂度驱动的成本',
        '  产品复杂度的三个层次（产品线/设计/流程组织）',
        '  国内外案例：戴尔控制复杂度、乐柏美"分得清就留下"、高乐氏"好库存坏库存"',
        '  标准化→系列化→模块化（大众汽车三阶段递进）',
        '第二篇 后端减重：提高供应商管理能力，走轻资产运作之路',
        '  重资产运作困境（振华重工/比亚迪案例）',
        '  供应商管理三大误区（小优化/轻选择重淘汰/过度竞争）',
        '  轻资产必要条件：一流的供应商管理职能',
        '第三篇 中间治乱：改善供应链计划，控制库存，有效平衡需求与供应',
        '  库存三管齐下（缩短周转周期/控制不确定性/改善计划）',
        '  需求计划：从数据出发，由判断结束',
        '  供应链指标体系：计划是"保护伞"',
    ],
    'highlights': [
        ('"三管齐下"框架', '前端防杂——降低产品复杂度驱动的成本（精简产品线、推动标准化系列化模块化）；后端减重——降低重资产带来的固定成本（聚焦核心竞争力、依靠专业供应商）；中间治乱——降低库存和运营成本（有效对接销售与运营、提高计划准确度）。三者交互影响、盘根错节。'),
        ('"增长陷阱"深入剖析', '许多企业生意越做越多、钱越赚越少，利润都变成了库存和产能。核心逻辑：高增长+高成本→规模膨胀→营收增速放缓→成本无法成比例降低→利润率下滑。中国500强收入利润率仅4.24%，近1/4净资产回报率不如一年定期。'),
        ('关键名言', '"最糟糕的供应商就是自家的生产线"；"可以骑马打天下，但不能骑马治天下"；"公司大了，滴滴打车就不是解决方案"；"头顶磨盘——吃力不讨好"。'),
    ]
})

# Book 3: 供应链的三道防线
books.append({
    'file': 'bk3.html',
    'hero_class': 'book-hero',
    'title': '供应链的三道防线：需求预测、库存计划、供应链执行',
    'subtitle': '刘宝红 & 赵玲 合著',
    'author': '刘宝红（Bob Liu）、赵玲',
    'publisher': '机械工业出版社 | ISBN: 978-7-111-59514-4',
    'pages': '约360页',
    'color': '#b8453a',
    'intro': '聚焦供应链计划的"<strong>七分管理</strong>"。三道防线如同河流上的三道堤坝：需求预测（第一道）、安全库存（第二道）、供应链执行（第三道）。第一道被冲垮，后面两道注定也会垮。',
    'toc': [
        '引言 供应链的三道防线',
        '第一篇 供应链的第一道防线：需求预测',
        '  需求预测是"从数据开始，由判断结束"',
        '  销售vs计划谁的预测更准（短尾/中尾/长尾产品分析）',
        '  一线销售为什么做不好需求预测',
        '  快消品公司组织设计案例、X公司完整变革案例',
        '  长周期物料预测专题、需求预测的绩效考核',
        '第二篇 供应链的第二道防线：库存计划',
        '  安全库存设置三步法（量化不确定性→量化服务水平→计算）',
        '  库存四分法管控风险（周转/安全/过剩/风险库存）',
        '  长尾产品库存计划、VMI全维度分析',
        '  高库存高服务水平是怎么来的（"两高"企业机制分析）',
        '第三篇 供应链的第三道防线：供应链执行',
        '  催货是有学问的（三优先级体系+飞利浦案例）',
        '  把自己做成大客户驱动供应商响应',
        '  日本供应商供不了货案例',
        '  三管齐下缩短周转周期（跨国设备商完整案例）',
        '  ERP与信息系统（MRP为什么跑不起来）',
    ],
    'highlights': [
        ('最具特色的实战案例', '① X公司6年营收增3倍的完整变革（三阶段：系统建设→计划执行分离→供应链渗透前端）；② 飞利浦催货三优先级体系（95%由计划满足，5%由执行弥补）；③ 跨国设备商三管齐下缩短周转周期（六周计划+模块化+流程优化）；④ 某制造商库存四分法发现1亿元风险库存。'),
        ('核心理念', '"所有的预测都是错的，但错多错少可不一样"；"预测不是衡量准确性，而是偏差率——一路飞去，一路纠偏"；"所有的短缺，最后都是以过剩收尾"；"计划是供应链的第一推动力"。'),
        ('本书独特价值', '唯一一本系统阐述供应链执行层的专著。第三道防线内容——催货管理、ERP/MRP运作机制、电子商务供应商连接——是其他五本书都未深入覆盖的领域。'),
    ]
})

# Book 4: 重资产到轻资产
books.append({
    'file': 'bk4.html',
    'hero_class': 'book-hero',
    'title': '供应链管理：重资产到轻资产的解决方案',
    'subtitle': '',
    'author': '刘宝红（Bob Liu）',
    'publisher': '机械工业出版社',
    'pages': '255页',
    'color': '#2c5f7c',
    'intro': '系统阐述企业如何从重资产运作转型轻资产。核心论点：<strong>重资产是供应链管理能力不足的替代品</strong>——当没有能力选好管好供应商时，企业就不得不垂直整合。',
    'toc': [
        '第一章 垂直整合��，重资产难逃劣质化的宿命',
        '  两大结构性缺陷：需求单一规模效益低 + 竞争不充分能力劣质化',
        '  英特尔芯片制造落后台积电案例',
        '第二章 外包：剥离重资产，依赖专业供应商',
        '  订单外包→产品外包→结构性外包（三层框架）',
        '  京东物流轻-重-轻轮回、IBM倒贴15亿剥离芯片制造',
        '  海尔"去制造化"、泛林研发全面外包（股价10→384美元）',
        '第三章 外包的核心能力建设',
        '  核心竞争力三维度判定（延展性/有用性/独特性）',
        '  模块化与外包的关系模型',
        '  华硕与戴尔——代工企业变竞争对手的教训',
        '附录 改善运营效率，继续重资产的良性存在',
    ],
    'highlights': [
        ('核心洞察', '"最差的供应商就是自家的生产线"——内部供应商在封闭环境里没动力也没能力持续改进。"如动物一旦被驯化了，与野生动物相比整体能力就会下降。"'),
        ('外包关键原则', '"做，要从不做开始"——不是"哪些东西该外包"，而是"哪些东西该自己做"。核心竞争力三个维度：延展性（能否进入更多市场）、有用性（客户愿不愿意买单）、独特性（能否模仿）。京东物流满足前两项但不满足第三项——说明不是核心竞争力。'),
        ('经典案例对比', '泛林研发（全面外包，净利率21.8%，股价384美元）vs 应用材料（传统模式，股价64美元）；AMD剥离芯片制造（股价→92美元）vs 英特尔固守制造（7纳米掉队，股价跌16%）。'),
    ]
})

# Book 5: 需求预测和库存计划
books.append({
    'file': 'bk5.html',
    'hero_class': 'book-hero',
    'title': '需求预测和库存计划：一个实践者的角度',
    'subtitle': '第2版（2025）',
    'author': '刘宝红（Bob Liu）',
    'publisher': '机械工业出版社 | ISBN: 978-7-111-78435-7',
    'pages': '339页',
    'color': '#1e3a5f',
    'intro': '计划是供应链的引擎。本书聚焦计划的"<strong>三分技术</strong>"，与《三道防线》的"七分管理"互补。<strong>所有案例都在Excel中完成</strong>——面向没有专业计划软件的绝大多数企业。',
    'toc': [
        '引言 计划是供应链的引擎（从"七分管理"到"三分技术"）',
        '第1章 数据是计划的基础（需求历史定义、数据清洗、极端值处理）',
        '第2章 移动平均法和简单指数平滑法',
        '第3章 评估预测方法的优劣（准确度、系统性偏差）',
        '第4章 趋势的预测（霍尔特法、线性回归）',
        '第5章 季节性需求的预测（霍尔特-温特法、三种方式对比案例）',
        '第6章 一家电商的预测方法优化（中心仓择优案例）',
        '第7章 高度不确定性下如何预测——德尔菲法',
        '  核心方法："瓶子里有多少颗糖"游戏→群策群力避免大错',
        '第8章 新品预测：尽量做准，尽快纠偏',
        '  新品开发期滚动纠偏、新品预售期滚动纠偏',
        '第9章 预测不准，设置安全库存来应对',
        '  三种不确定性组合（仅需求/仅供应/两者都不确定）',
        '第10章 再订货点和再订货机制（定量/定期补货、VMI水位设置）',
        '第11章 长尾产品：库存计划的终极挑战（泊松分布模拟）',
    ],
    'highlights': [
        ('核心方法论', '"避免大错，靠人脑；追求精益，靠电脑"——高度不确定的需求用德尔菲法群策群力；重复性高的需求清洗历史数据、选择预测模型优化。'),
        ('实用价值', '本书不是预测理论专著，而是为实践者量身打造的应用书。所有案例在Excel中完成。从移动平均、指数平滑到霍尔特-温特季节模型，再到安全库存计算和再订货点设置，手把手教你做计划。'),
        ('关键哲学', '"寻找更优，而不是最优的解决方案"——预测模型优化要提防过度拟合。"有时候，不预测就是最好的预测。"'),
    ]
})

# Book 6: 实践者的专家之路
books.append({
    'file': 'bk6.html',
    'hero_class': 'book-hero',
    'title': '供应链管理：实践者的专家之路',
    'subtitle': '',
    'author': '刘宝红（Bob Liu）',
    'publisher': '机械工业出版社 | ISBN: 978-7-111-56439-3',
    'pages': '约300页',
    'color': '#1e3a5f',
    'intro': '聚焦供应链人的<strong>职业发展三阶段</strong>：初入职场打好基础进入快车道→工作八到十年后日子不好也不坏→成为专家实现范式转移。',
    'toc': [
        '引言 供应链管理：认识这个领域（从"三个三"谈起）',
        '第一章 初入供应链：打好基础，进入快车道',
        '  大公司与小公司的不同（流程驱动vs人员驱动）',
        '  供应链管理最好的公司（高德纳全球供应链25强）',
        '  供应链管理的职业机会与认证（C.P.M./CPIM/CSCP）',
        '  做供应链管理的"三语人才"',
        '  影响你的那几个人：精心挑选你的"敌人"',
        '  追求卓越，拒绝做差不多先生',
        '第二章 工作了八年或十年后，日子不好也不坏',
        '  你缺的不是经验、缺能力还是缺意愿',
        '  跨出一步：不作为也是风险',
        '  维德必危：不做人人都喜欢的人',
        '第三章 成为专家：实现范式转移，从有知到有知',
        '  范式转移的基础：改变方法论和基本假设',
        '  从"如何解决"到能够解决"不愿解决"的问题',
        '后记 要么成为领袖，要么成为专家',
    ],
    'highlights': [
        ('职业三阶段', '初入职场——聚焦"如何解决"具体问题，多干多听多问，"你是你自己最好的广告"；平台期——成为工匠但陷入迷茫，"你缺的不是经验"；专家阶段——实现范式转移，既知道怎么解决也能解决不愿解决的问题。'),
        ('关键建议', '"宁做钝才，不做歪才"——不急功近利；"耐得住寂寞"——22岁时大家起点差不多，差异来自持续积累；"做供应链管理的三语人才"——专业语言+业务语言+数据语言；"精心挑选你的敌人"——对标优秀的人。'),
        ('实用资源', '职业认证路径推荐、供应链管理核心书单、大公司vs小公司的选择判断。"学历替代不了经历，经历也替代不了学历。想逃避，创业不是归宿。"'),
    ]
})


# ===== GENERATE PAGES =====
def build_page(book):
    """Generate a complete book HTML page"""
    toc_html = '<div class="book-toc"><h3>📖 完整目录</h3><ol>'
    for item in book['toc']:
        if item.startswith('  '):
            toc_html += f'<li style="margin-left:16px;list-style-type:circle">{item.strip()}</li>'
        else:
            toc_html += f'<li style="font-weight:600;color:var(--ink);margin-top:8px">{item}</li>'
    toc_html += '</ol></div>'
    
    highlights_html = ''
    for title, content in book['highlights']:
        highlights_html += f'<div class="highlight-box"><strong>{title}</strong><br>{content}</div>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0,viewport-fit=cover"/>
<meta name="description" content="{book['title']} —— 刘宝红供应链管理著作"/>
<title>{book['title']} · 刘宝红</title>
<style>
{full_css}
</style>
</head>
<body>
<div id="progress"></div>

{back_link}

<header class="{book['hero_class']}">
  <div class="tag">刘宝红 · 供应链实践者丛书</div>
  <h1>{book['title']}</h1>
  <p>{book['subtitle']}<br>{book['intro']}</p>
  <p class="edit">作者：{book['author']}<br>出版社：{book['publisher']} · {book['pages']}</p>
</header>

<div class="book-main">
  <h2>本书概述</h2>
  {highlights_html}
  
  {toc_html}
  
  <h2>阅读建议</h2>
  <p>本书是刘宝红"供应链实践者丛书"的核心组成部分。建议与系列其他著作配合阅读，形成从全局观→计划→采购→轻资产→技术深化→职业成长的完整知识体系。更多内容请返回<a href="index.html" style="color:var(--bk1)">主线知识图谱</a>查看各书精华的综合整理。</p>
  
  <p style="margin-top:24px;padding-top:16px;border-top:1px solid var(--line);font-size:13px;color:var(--ink-3)">
    本页面为书籍目录与概要介绍。如需深入学习，建议购买正版书籍。本章节内容仅供个人学习参考。
  </p>
</div>

{tools}
{panels}

<script>
(function(){{var b=document.getElementById('progress');window.addEventListener('scroll',function(){{var s=window.scrollY||document.documentElement.scrollTop,d=document.documentElement.scrollHeight-window.innerHeight;b.style.width=d?(s/d*100)+'%':'0%'}});}})();
(function(){{var B=document.querySelectorAll('.tool-btn');window.addEventListener('scroll',function(){{var s=window.scrollY||document.documentElement.scrollTop;B.forEach(function(b){{b.classList.toggle('show',s>200);}});}});}})();
(function(){{document.getElementById('top').addEventListener('click',function(){{window.scrollTo({{top:0,behavior:'smooth'}});}});}})();
(function(){{var o=document.getElementById('toc-overlay'),pn=document.getElementById('toc-panel'),pc=document.getElementById('toc-close');function close(){{o.classList.remove('show');pn.classList.remove('show');}}pc.addEventListener('click',close);o.addEventListener('click',close);document.getElementById('btn-toc').addEventListener('click',function(){{o.classList.add('show');pn.classList.add('show');}});}})();
(function(){{var o=document.getElementById('search-overlay'),pn=document.getElementById('search-panel'),pc=document.getElementById('search-close'),inp=document.getElementById('search-input'),pr=document.getElementById('search-prev'),nx=document.getElementById('search-next'),cnt=document.getElementById('search-count'),clr=document.getElementById('search-clear'),res=document.getElementById('search-results');var hits=[],ci=-1,marks=[];function close(){{o.classList.remove('show');pn.classList.remove('show');clearM();inp.value='';res.innerHTML='';hits=[];ci=-1;updN();}}pc.addEventListener('click',close);o.addEventListener('click',close);document.getElementById('btn-search').addEventListener('click',function(){{o.classList.add('show');pn.classList.add('show');setTimeout(function(){{inp.focus();}},300);}});function clearM(){{marks.forEach(function(m){{var p=m.parentNode;if(p){{p.replaceChild(document.createTextNode(m.textContent),m);p.normalize();}}}});marks=[];}}function doSearch(q){{clearM();hits=[];ci=-1;marks=[];if(!q||q.trim().length<2){{res.innerHTML=q?'<p style=padding:20px;color:var(--ink-2);font-size:14px>请输入至少2个字符</p>':'';updN();return;}}var ql=q.trim().toLowerCase(),body=document.querySelector('.book-main');if(!body){{updN();return;}}var w=document.createTreeWalker(body,NodeFilter.SHOW_TEXT,null,false),tns=[];while(w.nextNode()){{var n=w.currentNode;if(n.parentElement&&!['SCRIPT','STYLE','NOSCRIPT','SVG'].includes(n.parentElement.tagName)&&!n.parentElement.closest('#search-panel')){{tns.push(n);}}}}tns.forEach(function(node){{var t=node.textContent.toLowerCase(),i=t.indexOf(ql);if(i!==-1){{var ctx=node.textContent.substring(Math.max(0,i-30),i+ql.length+30);hits.push({{node:node,ctx:ctx,idx:i}});}}}});hits.forEach(function(hit){{var node=hit.node,t=node.textContent,ql2=ql.length,si=t.toLowerCase().indexOf(ql);if(si!==-1){{var be=t.substring(0,si),ma=t.substring(si,si+ql2),af=t.substring(si+ql2),mk=document.createElement('mark');mk.className='search-hit';mk.textContent=ma;var p=node.parentNode;p.replaceChild(document.createTextNode(af),node);p.insertBefore(mk,p.childNodes[p.childNodes.length-1]);p.insertBefore(document.createTextNode(be),mk);marks.push(mk);hit.mark=mk;}}}});if(hits.length===0){{res.innerHTML='<p style=padding:20px;color:var(--ink-2);font-size:14px>未找到匹配结果</p>';}}else{{var html='<div style=padding:8px>';hits.forEach(function(hit,i){{html+='<div class="toc-item search-result-item" data-i='+i+' style=font-size:13px;padding:10px 20px;border-bottom:1px solid var(--line)>';html+='<div style=color:var(--ink-2);font-size:12.5px;line-height:1.5>...'+esc(hit.ctx)+'...</div></div>';}});html+='</div>';res.innerHTML=html;res.querySelectorAll('.search-result-item').forEach(function(item){{item.addEventListener('click',function(){{navTo(parseInt(this.getAttribute('data-i')));}});}});}}updN();}}function esc(s){{var d=document.createElement('div');d.textContent=s;return d.innerHTML;}}function navTo(idx){{if(idx<0||idx>=hits.length)return;if(ci>=0&&ci<hits.length&&hits[ci].mark)hits[ci].mark.classList.remove('search-hit-current');ci=idx;var hit=hits[ci];if(hit.mark){{hit.mark.classList.add('search-hit-current');hit.mark.scrollIntoView({{behavior:'smooth',block:'center'}});}}updN();}}function updN(){{var t=hits.length,c=ci>=0?ci+1:0;cnt.textContent=t>0?c+'/'+t:'0/0';pr.disabled=t===0||ci<=0;nx.disabled=t===0||ci>=t-1;}}var st;inp.addEventListener('input',function(){{clearTimeout(st);st=setTimeout(function(){{doSearch(inp.value);}},300);}});inp.addEventListener('keydown',function(e){{if(e.key==='Enter'){{e.preventDefault();if(hits.length>0)navTo(ci<0?0:ci);}}}});pr.addEventListener('click',function(){{if(ci>0)navTo(ci-1);}});nx.addEventListener('click',function(){{if(ci<hits.length-1)navTo(ci+1);}});clr.addEventListener('click',function(){{inp.value='';doSearch('');inp.focus();}});document.addEventListener('keydown',function(e){{if((e.ctrlKey||e.metaKey)&&e.key==='k'){{e.preventDefault();document.getElementById('btn-search').click();}}}});}})();
</script>
</body>
</html>'''
    return html


# Write all book pages
for book in books:
    html = build_page(book)
    filepath = book['file']
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Generated: {filepath} ({len(html)} chars)')

# Now update the main index.html to add book links
# Add a "单书阅读" section at the end of 第8站, before the footer
with open('index.html', 'r', encoding='utf-8') as f:
    main_html = f.read()

book_links_html = '''
<h3>📕 按单书阅读</h3>
<p>以下页面为每本著作的独立目录与内容概要，方便按原书结构深入学习：</p>
<div class="concept-grid">
  <a href="bk1.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">📗</div>
    <h4>采购与供应链管理：一个实践者的角度</h4>
    <p>第4版(2024) · 380页 · 供应链全局观+采购管理+供应商管理</p>
  </a>
  <a href="bk3.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">📙</div>
    <h4>供应链的三道防线</h4>
    <p>需求预测·库存计划·供应链执行 · 聚焦计划的"七分管理"</p>
  </a>
  <a href="bk2.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">📘</div>
    <h4>高成本、高库存、重资产的解决方案</h4>
    <p>第2版(2023) · 260页 · 前端防杂·后端减重·中间治乱</p>
  </a>
  <a href="bk4.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">📓</div>
    <h4>重资产到轻资产的解决方案</h4>
    <p>255页 · 外包战略·供应商管理·轻资产转型</p>
  </a>
  <a href="bk5.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">📊</div>
    <h4>需求预测和库存计划：一个实践者的角度</h4>
    <p>第2版(2025) · 339页 · 预测模型·安全库存·所有案例在Excel中完成</p>
  </a>
  <a href="bk6.html" class="concept-card" style="text-decoration:none">
    <div class="cc-icon">👤</div>
    <h4>供应链管理：实践者的专家之路</h4>
    <p>职业发展三阶段·认证路径·职场建议</p>
  </a>
</div>
'''

# Insert before the 延伸学习资源 section
if '延伸学习资源' in main_html:
    main_html = main_html.replace('<h3>📚 延伸学习资源</h3>', book_links_html + '\n<h3>📚 延伸学习资源</h3>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(main_html)
print(f'Updated main index.html ({len(main_html)} chars)')

print('\n=== DONE ===')
print('Generated: bk1.html bk2.html bk3.html bk4.html bk5.html bk6.html')
