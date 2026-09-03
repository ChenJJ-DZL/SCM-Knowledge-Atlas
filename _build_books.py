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

/* 核心知识详解 */
.knowledge-block { margin:0 0 8px }
.book-main h3 { font-size:15.5px; font-weight:700; color:var(--ink); margin:22px 0 6px; display:flex; align-items:center; gap:8px }
.book-main h3::before { content:""; width:4px; height:16px; background:var(--bk1); border-radius:3px; display:inline-block }
.knowledge-block h4 { font-size:14px; font-weight:700; color:var(--bk1); margin:14px 0 4px }
.knowledge-block ul { margin:6px 0 10px; padding-left:20px; font-size:14.5px; color:var(--ink-2); line-height:1.8 }
.knowledge-block li { margin:4px 0 }
.knowledge-block li strong { color:var(--ink) }

/* STAR 法则案例 */
.star-case { background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:18px 18px 12px; margin:16px 0; box-shadow:var(--shadow) }
.star-case .sc-name { font-size:15px; font-weight:800; color:var(--ink); margin:0 0 10px; display:flex; align-items:center; gap:8px; line-height:1.5 }
.star-case .sc-name::before { content:"★"; color:var(--amber); font-size:16px }
.star-step { border-left:4px solid; padding:10px 14px; margin:10px 0; border-radius:0 12px 12px 0; font-size:14px; line-height:1.7; color:var(--ink-2) }
.star-step .sl { display:inline-flex; align-items:center; justify-content:center; width:22px; height:22px; border-radius:50%; color:#fff; font-size:12px; font-weight:800; margin-right:8px; vertical-align:middle }
.star-step b { color:var(--ink); font-weight:700; letter-spacing:.3px }
.star-step p { margin:4px 0 0; font-size:14px; color:var(--ink-2) }
.star-step.s { border-color:var(--bk2); background:var(--bk2-light) }
.star-step.s .sl { background:var(--bk2) }
.star-step.s b { color:var(--bk2) }
.star-step.t { border-color:var(--amber); background:var(--amber-soft) }
.star-step.t .sl { background:var(--amber) }
.star-step.t b { color:var(--amber) }
.star-step.a { border-color:var(--tip); background:var(--tip-soft) }
.star-step.a .sl { background:var(--tip) }
.star-step.a b { color:var(--tip) }
.star-step.r { border-color:var(--indigo); background:var(--indigo-soft) }
.star-step.r .sl { background:var(--indigo) }
.star-step.r b { color:var(--indigo) }
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
    ],
    'knowledge': [
        {'heading': '一、先有全局观：供应链是三条流的集成',
         'body': '供应链不是"物流"，而是信息流、产品流、资金流三条流拧成的一根绳。多数企业只盯着产品流（货搬来搬去），却忽略了信息流（需求怎么传递）和资金流（钱怎么流动、库存占了多少现金）。三流一旦脱节，问题就出来了。',
         'points': ['信息流：需求预测、订单、计划逐级传递，牛鞭效应就是信息流失真的典型。', '产品流：从原材料到成品再到客户手中的实物流，决定交付速度与质量。', '资金流：库存占用现金、账期影响现金流，资产周转率是资金流的核心指标。', '供应链管理 = 管理这三条流的集成，而不是各自为战。']},
        {'heading': '二、管好供应商，才能管好供应链',
         'body': '供应链的核心竞争力，很大程度上是供应商管理的能力。多数企业的供应商管理有三个通病，先认清病根才能对症下药。',
         'points': ['三大误区：多权分立（采购分散在各业务单元）、采购额分散（雨露均沾）、有选择没管理（只选不用管）。', '供应商分类：用"采购额 × 供应风险"把供应商分成战略、瓶颈、杠杆、日常四类，区别对待。', '绩效管理：用 QCDSTAP 七大指标（成本/质量/交付/服务/技术/资产/流程）量化打分，识别短板敦促改进。', '一品一点：同一品类聚焦少数供应商，把量集中起来换取规模效益和议价权。']},
        {'heading': '三、从「小采购」到「大采购」',
         'body': '采购要从"下订单的办事员"升级为"影响总成本的战略职能"。这是一个从"小采购"（被动执行）到"大采购"（主动影响设计、供应商、需求）的五阶段演进。',
         'points': ['五阶段：供应管理→采购管理→供应商管理→供应商集成→供应链管理，层层递进。', '角色转变：从"猎人"（四处比价压价）变成"牧人"（长期培养供应商）。', '大采购要管住总成本（TCO），而不只是采购单价——设计阶段的成本决定占 70% 以上。', '组织上要"两层分离"：战略采购与日常下单分离，让专业人员做专业的事。']},
    ],
    'concepts': [
        {'term': '牛鞭效应', 'def': '需求信息沿供应链逐级传递时被逐级放大，终端小幅波动传导到上游变成剧烈波动，导致库存积压或断货。'},
        {'term': '集成供应链', 'def': '打破部门墙，把销售/计划/采购/制造/物流连成整体协同运作，而非各管一段各自优化。'},
        {'term': '战略供应商', 'def': '对成本、质量、交付影响大且难以替代的少数关键供应商，需要长期深度协同而非简单比价。'},
        {'term': '供应商四分法', 'def': '按"采购额 × 供应风险"把供应商分为战略型、瓶颈型、杠杆型、日常型，区别对待、重点管理。'},
        {'term': 'QCDSTAP', 'def': '供应商绩效的七大指标：质量(Q)、成本(C)、交付(D)、服务(S)、技术(T)、资产(A)、流程(P)。'},
        {'term': '一品一点', 'def': '同一品类集中由少数供应商供货，把采购量集中起来换取规模效益与议价能力。'},
        {'term': '规模效益', 'def': '采购量越大单位成本越低。分散采购会牺牲规模效益，是"有选择没管理"的直接后果。'},
        {'term': '总拥有成本(TCO)', 'def': '不止采购单价，还包括使用、维护、库存、质量损失等全生命周期的总成本。'},
    ],
    'star_cases': [
        {'name': '小米三星 2016 年战略供应商危机',
         'situation': '2016 年小米旗舰机因供应链失衡陷入交付危机，关键屏厂三星断供，多款机型缺货、销量下滑。',
         'task': '小米需要极短时间内稳住供应链、恢复旗舰机交付，同时重建与核心屏厂的关系。',
         'action': '雷军亲自接管供应链，多次飞韩国与三星高层谈判道歉，把供应商关系从"压价博弈"转向"战略协作"；同时压缩 SKU、聚焦爆款，降低复杂度。',
         'result': '2017 年小米手机出货量强势反弹，重返全球前列。教训：战略供应商必须当伙伴经营，不能一味压榨。'},
        {'name': '摩托罗拉：复杂度致死',
         'situation': '巅峰期的摩托罗拉手机拥有 100 多种电池型号、海量 SKU，复杂度失控。',
         'task': '需要在产品线膨胀与成本、库存之间找到平衡，避免被复杂度拖垮。',
         'action': '摩托罗拉未能有效收敛产品线与零部件的复杂度，供应链被海量型号拖累，成本与库存双双高企。',
         'result': '最终被对手超越、走向衰落。教训：复杂度是隐形成本，必须主动治理。'},
        {'name': '苹果：把供应链做成核心竞争力',
         'situation': '1998 年苹果濒临破产，库存高企、产品线混乱。',
         'task': '削减库存、聚焦产品、重建供应链，把供应链变成竞争壁垒。',
         'action': '库克主导供应链变革：砍掉海量 SKU、关闭自有工厂、把制造外包给富士康等专业供应商、用数据精细化管控库存与交付。',
         'result': '苹果库存周转天数降到行业顶尖水平，供应链成为苹果高利润率与新品快速上量的关键支撑。'},
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
    ],
    'knowledge': [
        {'heading': '一、前端防杂：向复杂度要成本',
         'body': '高成本的第一大元凶是产品复杂度。产品线越杂、设计越不标准，成本、库存、交付问题就越难根治。治理复杂度要从三个层次下手。',
         'points': ['复杂度的三个层次：产品线复杂（SKU 太多）、设计复杂（零部件不通用）、流程/组织复杂（多头管理）。', '标准化→系列化→模块化：先统一标准件，再归并成系列，最后用模块化组合出多样性，是复杂度治理的递进路径。', '判断标准：产品"分得清就留下，分不清就砍掉"——不能创造差异化价值的 SKU 就该淘汰。']},
        {'heading': '二、后端减重：向重资产要效率',
         'body': '很多企业习惯了"什么都自己造"，结果把现金流都砸进了厂房设备。重资产不是战略选择，而是供应链管理能力不足的替代品。',
         'points': ['重资产困境：需求单一导致规模效益低，封闭环境导致能力劣质化——"最差的供应商就是自家的生产线"。', '供应商管理三大误区：小优化（局部最优）、轻选择重淘汰、过度竞争（把供应商逼到死）。', '轻资产的必要条件：一流的供应商管理职能——选好、管好、集成好外部专业供应商。']},
        {'heading': '三、中间治乱：向库存要现金',
         'body': '库存是利润的坟墓。高库存不是仓库的问题，而是计划不准、流程不畅的集中体现。治库存要"三管齐下"。',
         'points': ['库存三管齐下：缩短周转周期（快周转）、控制不确定性（稳）、改善计划（准），三者缺一不可。', '需求计划"从数据出发、由判断结束"：先看历史数据，再让懂业务的人拍板纠偏。', '计划是供应链的"保护伞"：计划准，下游的采购、生产、库存才不乱。']},
    ],
    'concepts': [
        {'term': '增长陷阱', 'def': '生意越做越多、钱越赚越少——营收增长但利润率下滑，利润都变成了库存和产能。'},
        {'term': '产品复杂度', 'def': '产品线、设计、流程组织三个层面的复杂程度，是驱动成本和库存的隐形元凶。'},
        {'term': '模块化', 'def': '把产品拆成可复用的标准模块，通过模块组合出多样性，兼顾成本与灵活。'},
        {'term': '重资产', 'def': '企业自己大量投资厂房、设备、产线，固定成本高、灵活性差。'},
        {'term': '轻资产', 'def': '把非核心环节外包给专业供应商，企业聚焦核心能力，降低固定资产投入。'},
        {'term': '库存三管齐下', 'def': '同时缩短周转周期、控制不确定性、改善计划，三管齐下才能真正降库存。'},
        {'term': '需求计划', 'def': '对未来的需求做判断，驱动采购、生产、库存安排，是供应链的引擎。'},
    ],
    'star_cases': [
        {'name': '振华重工：重资产的增长陷阱',
         'situation': '振华重工一度占据全球港口起重机大部分份额，靠大规模自建产能支撑高增长。',
         'task': '在高速增长背后，如何避免利润被庞大的固定资产吞噬。',
         'action': '企业持续扩张自有产能，重资产模式在行业景气下行、需求波动时显得格外笨重。',
         'result': '陷入"增长陷阱"：规模越大、资产越重、利润越薄。教训：重资产是能力不足的替代品。'},
        {'name': '戴尔：用标准化控制复杂度',
         'situation': 'PC 行业 SKU 爆炸式增长，戴尔面临产品线复杂带来的成本与库存压力。',
         'task': '在满足客户多样化的同时，控制产品与零部件的复杂度。',
         'action': '戴尔通过直销模式 + 标准化零部件 + 按订单生产，把复杂度关进笼子里，同时保持零库存。',
         'result': '一度登顶全球 PC 第一，证明"用流程和标准化控制复杂度"是高利润的关键。'},
        {'name': '大众汽车：标准化→系列化→模块化',
         'situation': '大众旗下品牌和车型众多，零部件与平台各自为政，成本居高不下。',
         'task': '在保留多品牌差异化的同时，大幅摊薄研发与制造成本。',
         'action': '推进平台化战略（如 MQB 模块化平台），让不同车型共享底盘、动力总成等标准模块。',
         'result': '大幅降低单车成本、缩短新车开发周期，成为汽车行业模块化的标杆。'},
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
    ],
    'knowledge': [
        {'heading': '一、第一道防线：需求预测——从数据开始，由判断结束',
         'body': '预测是供应链的第一推动力，但"所有的预测都是错的"。要做的不是追求预测 100% 准，而是让预测错得少一点、纠偏快一点。',
         'points': ['预测的本质不是算准，而是管理偏差率："一路飞去，一路纠偏"。', '流程上"从数据开始，由判断结束"：先让系统给出基线，再让懂业务的人调整。', '一线销售做不好预测是常态——要设计机制（预测与销售目标分离）而不是怪人。']},
        {'heading': '二、第二道防线：库存计划——安全库存与库存四分法',
         'body': '预测不可能全准，所以要用安全库存来兜底。但安全库存不是拍脑袋，而是量化不确定性后算出来的。',
         'points': ['安全库存三步法：量化不确定性 → 量化目标服务水平 → 代入公式计算。', '库存四分法：把库存分成周转、安全、过剩、风险四类，区别对待、有的放矢。', '长尾产品是库存计划的终极挑战：用量少但种类多，需要专门的库存策略。']},
        {'heading': '三、第三道防线：供应链执行——催货是有学问的',
         'body': '前面两道防线被冲垮后，最后靠执行来兜底。执行不是"死命催"，而是有优先级、有方法地驱动供应商响应。',
         'points': ['催货三优先级体系：把催货需求分优先级，95% 由计划满足，只有 5% 靠执行层弥补。', '把自己做成大客户：用稳定的量、清晰的计划换取供应商的优先响应。', 'ERP/MRP 跑不起来，根子往往是主数据不准、计划逻辑没理顺，而非软件本身。']},
    ],
    'concepts': [
        {'term': '三道防线', 'def': '需求预测（第一道）、安全库存（第二道）、供应链执行（第三道），层层兜底，前道垮后道必垮。'},
        {'term': '需求预测', 'def': '对未来需求的判断，是供应链计划的起点，衡量标准是偏差率而非"准不准"。'},
        {'term': '安全库存', 'def': '为应对需求与供应的不确定性而额外持有的库存，是预测之外的缓冲。'},
        {'term': '库存四分法', 'def': '把库存分为周转、安全、过剩、风险四类，分类管理、精准处置。'},
        {'term': 'VMI', 'def': '供应商管理库存：供应商根据共享的销售/库存数据自主补货，降低双方库存。'},
        {'term': '服务水平', 'def': '在客户需要时能供货的概率，是设定安全库存的关键目标参数。'},
        {'term': '长尾产品', 'def': '种类多、单个需求量小的产品，库存计划的难点在于"少量多样"如何备货。'},
    ],
    'star_cases': [
        {'name': 'X 公司：6 年营收增 3 倍的计划变革',
         'situation': 'X 公司业务快速扩张但供应链计划混乱，交付与库存问题频发。',
         'task': '支撑营收高速增长的同时，把计划体系建起来、把库存和交付管住。',
         'action': '分三阶段推进：先建系统 → 再实现计划与执行分离 → 最后让供应链渗透前端，全程配套组织与流程变革。',
         'result': '营收 6 年增长 3 倍，供应链从"救火队"变成"增长引擎"，成为完整的计划变革样板。'},
        {'name': '飞利浦：催货的三优先级体系',
         'situation': '飞利浦供应商众多、催货需求庞杂，执行层疲于奔命。',
         'task': '把有限的催货资源用在刀刃上，避免"什么都急、什么都催不动"。',
         'action': '建立三优先级体系，按紧急程度和影响分级催货；绝大多数需求靠计划前置满足，只有极少数才走执行层催货。',
         'result': '催货变得有序高效，执行层从"救火"转向"例外管理"，交付稳定性显著提升。'},
        {'name': '某制造商：库存四分法挖出 1 亿风险库存',
         'situation': '某制造商库存居高不下，但说不清哪些库存是合理的、哪些是问题库存。',
         'task': '把库存结构看清楚，找到真正该削减的那部分。',
         'action': '用库存四分法把库存按周转/安全/过剩/风险分类核算，逐类分析成因与处置方案。',
         'result': '一次性识别出 1 亿元风险库存，为后续削减提供了清晰的优先级和抓手。'},
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
    ],
    'knowledge': [
        {'heading': '一、为什么重资产难逃劣质化',
         'body': '垂直整合看起来"什么都能自己掌控"，但长期看有两大结构性缺陷，几乎注定让内部能力走向劣质化。',
         'points': ['需求单一、规模效益低：内部供应的需求只来自自家，摊不薄成本。', '竞争不充分、能力劣质化：封闭环境里没动力也没能力持续改进——"最差的供应商就是自家的生产线"。', '英特尔芯片制造落后台积电，就是垂直整合劣质化的典型例证。']},
        {'heading': '二、外包的三层境界',
         'body': '外包不是"把活甩出去"这么简单，而是分三个层次递进：从低附加值的订单外包，到产品外包，再到结构性外包。',
         'points': ['订单外包：只把生产订单交给别人，最浅层。', '产品外包：把整个产品的设计与制造交给专业供应商。', '结构性外包：把整条能力链剥离出去，企业只保留最核心的部分，是最彻底、收益最大的层次。']},
        {'heading': '三、外包前先想清楚：什么是核心竞争力',
         'body': '"做，要从不做开始。"不是问"哪些该外包"，而是问"哪些必须自己做"。判断标准是核心竞争力三问。',
         'points': ['延展性：这项能力能否帮企业进入更多市场？', '有用性：客户愿不愿意为它买单？', '独特性：别人能不能轻易模仿？三者缺一不可，才是核心竞争力。', '警惕代工变对手：华硕给戴尔代工，最终自己下场做品牌，说明外包方与被外包方的边界会漂移。']},
    ],
    'concepts': [
        {'term': '垂直整合', 'def': '企业自己包办上下游多个环节，什么都能自己造，但容易陷入重资产与能力劣质化。'},
        {'term': '外包三层', 'def': '订单外包 → 产品外包 → 结构性外包，由浅入深的三种外包层次。'},
        {'term': '结构性外包', 'def': '把整条能力链剥离给专业供应商，企业只保留核心能力，是外包的最高层次。'},
        {'term': '核心竞争力三维度', 'def': '延展性、有用性、独特性三问，用来判断一项能力是否值得自己做。'},
        {'term': '模块化', 'def': '把产品拆成标准化模块，为外包提供清晰接口，是外包得以实现的技术前提。'},
        {'term': '供应商集成', 'def': '与供应商深度协同，让外部供应商像内部部门一样参与设计与交付。'},
    ],
    'star_cases': [
        {'name': '泛林研发 vs 应用材料：全面外包的胜利',
         'situation': '同处半导体设备行业，泛林研发与应用材料采用了截然不同的资产策略。',
         'task': '在重资产、高波动的行业里，谁能保持更高的利润率和股东回报。',
         'action': '泛林研发把制造等非核心环节全面外包，聚焦研发与核心能力；应用材料坚持传统重资产一体化模式。',
         'result': '泛林净利率达 21.8%、股价 384 美元，远超应用材料的 64 美元——用数据证明轻资产的价值。'},
        {'name': 'IBM：倒贴 15 亿也要剥离芯片制造',
         'situation': 'IBM 芯片制造业务持续亏损，成为拖累整体业绩的重资产包袱。',
         'task': '甩掉亏损的制造环节，把资源集中到更高价值的业务上。',
         'action': 'IBM 不惜倒贴 15 亿美元，把芯片制造业务剥离给专业代工厂。',
         'result': '摆脱重资产拖累，聚焦软件与服务等高价值领域，实现战略转身。'},
        {'name': '华硕与戴尔：代工企业变竞争对手',
         'situation': '华硕长期为戴尔等品牌代工，熟悉设计与制造全流程。',
         'task': '戴尔需要在借力代工与防止养大竞争对手之间找到平衡。',
         'action': '戴尔继续外包制造，华硕在代工中积累能力后，顺势推出自有品牌进入市场。',
         'result': '华硕从代工厂变成戴尔的直接对手。教训：外包会复制能力，边界必须用设计、品牌、生态来守住。'},
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
    ],
    'knowledge': [
        {'heading': '一、预测的技术路线：从简单到季节模型',
         'body': '预测不是越复杂的模型越好，而是"够用就好"。针对不同需求模式，选最合适的模型。所有案例都可以在 Excel 里完成。',
         'points': ['数据是基础：先定义需求历史、清洗数据、处理极端值，垃圾数据进、垃圾结果出。', '平稳需求用移动平均、简单指数平滑；带趋势用霍尔特法/线性回归；带季节用霍尔特-温特法。', '评估模型优劣看两个维度：准确度 + 系统性偏差（是否有持续高估/低估）。']},
        {'heading': '二、高度不确定时怎么办：德尔菲法',
         'body': '当需求高度不确定、历史数据不可靠时，硬套模型反而危险。这时候靠"群策群力"避免大错。',
         'points': ['德尔菲法：让多个懂行的人独立判断，再汇总收敛，避免个人偏见和从众。', '"避免大错，靠人脑；追求精益，靠电脑"——不确定性越高，越要依靠判断而非纯算法。', '核心比喻："瓶子里有多少颗糖"，众人的平均判断往往比单个专家更接近真相。']},
        {'heading': '三、预测不准，靠安全库存和再订货点兜底',
         'body': '既然预测不可能全准，就要用安全库存和补货机制来兜底，这是"三分技术"里最关键的可落地动作。',
         'points': ['安全库存应对三种不确定性：仅需求不确定、仅供应不确定、两者都不确定，公式各不相同。', '再订货点机制：定量补货、定期补货、VMI 水位设置，选对机制比死盯预测更省心。', '新品预测"尽量做准、尽快纠偏"：开发期、预售期滚动纠偏，别指望一次预测到位。']},
    ],
    'concepts': [
        {'term': '移动平均', 'def': '用最近若干期需求的平均值做预测，适合平稳、无明显趋势和季节的需求。'},
        {'term': '指数平滑', 'def': '给近期数据更高权重、逐期衰减的预测方法，比简单平均更灵敏。'},
        {'term': '霍尔特-温特法', 'def': '同时处理趋势和季节性的预测模型，是季节性需求预测的主力工具。'},
        {'term': '德尔菲法', 'def': '多位专家独立判断、多轮汇总收敛的结构化预测法，适合高度不确定场景。'},
        {'term': '安全库存', 'def': '为应对需求/供应不确定性而持有的缓冲库存，量化不确定性后计算得出。'},
        {'term': '再订货点', 'def': '当库存降到某个阈值就触发补货的机制，是库存补货的自动触发器。'},
        {'term': '服务水平', 'def': '在客户需要时能供货的概率，是设定安全库存的核心目标参数。'},
        {'term': '长尾产品', 'def': '种类多、单量小的产品，需用泊松分布等专门方法做库存计划。'},
    ],
    'star_cases': [
        {'name': '一家电商：中心仓择优的预测优化',
         'situation': '某电商 SKU 极多、需求波动大，统一用单一预测模型效果很差。',
         'task': '为不同需求模式的海量 SKU 找到各自最优的预测方法。',
         'action': '按需求模式把 SKU 分类，对每类分别测试移动平均、指数平滑、季节模型，选择误差最小的方法，并在中心仓层面统一执行。',
         'result': '预测准确度显著提升，库存与缺货双双改善，验证了"分类择优"比"一刀切"有效。'},
        {'name': '新品预测：尽量做准，尽快纠偏',
         'situation': '新品没有历史数据，传统预测模型无从下手，容易大起大落。',
         'task': '在新品上市前后尽可能做准预测，并随销售反馈快速修正。',
         'action': '开发期用类比同类产品 + 专家判断做初始预测，预售期开始按真实订单滚动纠偏，逐步逼近真实需求。',
         'result': '新品库存错配大幅减少，避免"一上市就断货"或"一上市就积压"的两种极端。'},
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
    ],
    'knowledge': [
        {'heading': '一、初入职场：打好基础，进入快车道',
         'body': '职业生涯的头几年决定快慢车道。这一阶段的关键不是"选对岗位"，而是把基本功打扎实、把习惯养好。',
         'points': ['聚焦"如何解决"：多干、多听、多问，用具体交付积累口碑——"你是你自己最好的广告"。', '大公司与小公司不同：大公司靠流程驱动，学规范和系统；小公司靠人驱动，练综合和速度。', '做"三语人才"：专业语言 + 业务语言 + 数据语言，三者都能说，才走得远。']},
        {'heading': '二、平台期：日子不好也不坏，怎么办',
         'body': '工作八到十年后，很多人陷入"不好也不坏"的平台期。要突破，先搞清楚自己缺的是经验、能力，还是意愿。',
         'points': ['自我诊断三问：你缺的是经验（见得少）、能力（做不到）、还是意愿（不想做）？对症下药。', '"不作为也是风险"：在变化加速的环境里，原地不动本身就是一种倒退。', '拒绝做"差不多先生"：追求卓越和"歪才"式急功近利，是两条截然不同的路。']},
        {'heading': '三、成为专家：实现范式转移',
         'body': '从"有知"到"有知"的跨越，靠的不是积累更多技巧，而是范式转移——改变看待问题的方法论和基本假设。',
         'points': ['范式转移的基础：改变方法论和基本假设，而非在旧框架里更努力。', '从"如何解决"到能解决"不愿解决"的问题：专家不只是会做，而是能让别人也做对。', '后记的终极选择：要么成为领袖，要么成为专家——两条路都要耐得住寂寞。']},
    ],
    'concepts': [
        {'term': '三语人才', 'def': '同时掌握专业语言、业务语言、数据语言的复合型人才，是供应链人的核心竞争力。'},
        {'term': '范式转移', 'def': '改变看问题的方法论和基本假设，从而获得质的突破，而非量的积累。'},
        {'term': '高德纳25强', 'def': '高德纳(Gartner)评选的全球供应链最佳实践企业榜单，是学习的标杆。'},
        {'term': 'CPIM/CSCP', 'def': '供应链与库存管理领域的国际认证，是职业晋升的重要背书。'},
        {'term': '流程驱动 vs 人员驱动', 'def': '大公司靠流程和系统运转，小公司靠关键人物推动，选择时看自己更适合哪种。'},
    ],
    'star_cases': [
        {'name': '平台期突围：一个供应链经理的八年之痒',
         'situation': '一位供应链经理工作八年，职位和薪资都"不好也不坏"，陷入迷茫，不确定该继续深耕还是转型。',
         'task': '判断自己缺的到底是经验、能力还是意愿，找到突破方向。',
         'action': '按"三问"诊断：发现自己缺的不是能力，而是意愿和视野；于是主动跨出舒适区，主动对标行业标杆（"精心挑选你的敌人"），补齐数据语言短板。',
         'result': '从"差不多先生"转向工匠，最终实现范式转移，进入专家行列。'},
        {'name': '大公司还是小公司：一次职业选择',
         'situation': '一位应届供应链毕业生同时拿到大公司和小公司的 offer，纠结该去哪。',
         'task': '在"流程规范的大平台"和"机会多的小舞台"之间做出符合自身阶段的选择。',
         'action': '用"流程驱动 vs 人员驱动"框架评估：自己当前更需要系统方法论和职业背书，于是先选大公司打基础。',
         'result': '在大公司建立系统的专业框架和行业视野，为日后进入快车道或创业打下扎实根基。'},
    ]
})


# ===== GENERATE PAGES =====
def build_knowledge_html(knowledge):
    """knowledge 是 [{"heading","body","points":[..]}] 列表，渲染「核心知识详解」。"""
    if not knowledge:
        return ''
    out = ['<h2>📚 核心知识详解</h2>']
    for b in knowledge:
        heading = b.get('heading', '')
        body = b.get('body', '')
        points = b.get('points', [])
        block = ['<div class="knowledge-block">']
        if heading:
            block.append(f'<h3>{heading}</h3>')
        if body:
            block.append(f'<p>{body}</p>')
        if points:
            block.append('<ul>' + ''.join(f'<li>{p}</li>' for p in points) + '</ul>')
        block.append('</div>')
        out.append(''.join(block))
    return ''.join(out)


def build_concepts_html(concepts):
    """concepts 是 [{"term","def"}] 列表，渲染「专有名词解释」。"""
    if not concepts:
        return ''
    items = ''.join(
        f'<div class="term"><div class="t">{c.get("term", "")}</div><div class="d">{c.get("def", "")}</div></div>'
        for c in concepts
    )
    return f'<h2>🔤 专有名词解释</h2>\n<div class="glossary">{items}</div>'


STAR_STEPS = [
    ('situation', 's', 'S', '情境 Situation'),
    ('task', 't', 'T', '任务 Task'),
    ('action', 'a', 'A', '行动 Action'),
    ('result', 'r', 'R', '结果 Result'),
]


def build_star_cases_html(star_cases):
    """star_cases 是 [{"name","situation","task","action","result"}] 列表，渲染 STAR 法则案例。"""
    if not star_cases:
        return ''
    out = ['<h2>🎯 经典案例拆解（STAR 法则）</h2>']
    for case in star_cases:
        name = case.get('name', '案例')
        out.append(f'<div class="star-case"><div class="sc-name">{name}</div>')
        for key, cls, letter, label in STAR_STEPS:
            text = case.get(key, '')
            if text:
                out.append(
                    f'<div class="star-step {cls}">'
                    f'<span class="sl">{letter}</span><b>{label}</b>'
                    f'<p>{text}</p></div>'
                )
        out.append('</div>')
    return ''.join(out)


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
    
    knowledge_html = build_knowledge_html(book.get('knowledge', []))
    concepts_html = build_concepts_html(book.get('concepts', []))
    star_cases_html = build_star_cases_html(book.get('star_cases', []))
    
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
  
  {knowledge_html}
  
  {star_cases_html}
  
  {concepts_html}
  
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

# Insert before the 延伸学习资源 section (幂等：已存在则不重复插入)
if '延伸学习资源' in main_html and '按单书阅读' not in main_html:
    main_html = main_html.replace('<h3>📚 延伸学习资源</h3>', book_links_html + '\n<h3>📚 延伸学习资源</h3>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(main_html)
print(f'Updated main index.html ({len(main_html)} chars)')

print('\n=== DONE ===')
print('Generated: bk1.html bk2.html bk3.html bk4.html bk5.html bk6.html')
