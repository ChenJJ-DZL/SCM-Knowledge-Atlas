"""Build v5 index.html with redesigned UI"""
css = open('_new_css.css','r',encoding='utf-8').read()
old = open('index.html','r',encoding='utf-8').read()

start = old.find('<!-- 第1站 -->')
end = old.find('</footer>') + len('</footer>')
content = old[start:end]

js = '''<script>
(function(){var b=document.getElementById('progress');window.addEventListener('scroll',function(){var s=window.scrollY||document.documentElement.scrollTop,d=document.documentElement.scrollHeight-window.innerHeight;b.style.width=d?(s/d*100)+'%':'0%'});})();
(function(){var B=document.querySelectorAll('.tool-btn');window.addEventListener('scroll',function(){var s=window.scrollY||document.documentElement.scrollTop;B.forEach(function(b){b.classList.toggle('show',s>200);});});})();
(function(){document.getElementById('top').addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});})();
(function(){var links=document.querySelectorAll('#nav a'),secs=[];links.forEach(function(a){var id=a.getAttribute('href');if(id&&id.startsWith('#')){var s=document.querySelector(id);if(s)secs.push({link:a,section:s});}});window.addEventListener('scroll',function(){var st=window.scrollY||document.documentElement.scrollTop,cur=null;secs.forEach(function(item){if(item.section.offsetTop-100<=st)cur=item;});links.forEach(function(a){a.classList.remove('active');});if(cur)cur.link.classList.add('active');});})();
(function(){var rw=document.getElementById('resume-wrap'),rb=document.getElementById('resume-badge'),ri=document.getElementById('resume-ignore'),K='scm_scroll_pos';var st;window.addEventListener('scroll',function(){clearTimeout(st);st=setTimeout(function(){var s=window.scrollY;if(s>300)localStorage.setItem(K,s);},500);});window.addEventListener('load',function(){var p=localStorage.getItem(K);if(p&&parseInt(p)>300)rw.classList.add('show');});rb.addEventListener('click',function(){var p=localStorage.getItem(K);if(p){window.scrollTo({top:parseInt(p),behavior:'smooth'});}rw.classList.remove('show');});ri.addEventListener('click',function(){rw.classList.remove('show');});})();
(function(){var o=document.getElementById('toc-overlay'),pn=document.getElementById('toc-panel'),pc=document.getElementById('toc-close'),pl=document.getElementById('toc-list');function close(){o.classList.remove('show');pn.classList.remove('show');}pc.addEventListener('click',close);o.addEventListener('click',close);document.getElementById('btn-toc').addEventListener('click',function(){o.classList.add('show');pn.classList.add('show');});function build(){var h='',ss=document.querySelectorAll('.wrap section');ss.forEach(function(sec){var id=sec.id;if(!id)return;var h2=sec.querySelector('h2'),title=h2?h2.textContent:'',cn=sec.querySelector('.ch-num'),cnT=cn?cn.textContent:'';h+='<div class=toc-chapter>'+cnT+' '+title+'</div>';var h3s=sec.querySelectorAll('h3');h3s.forEach(function(h3){h+='<a class=toc-item l2 data-sid='+id+' data-txt='+encodeURIComponent(h3.textContent)+'>'+h3.textContent+'</a>';});});pl.innerHTML=h;pl.querySelectorAll('.toc-item').forEach(function(it){it.addEventListener('click',function(){var sid=this.getAttribute('data-sid'),txt=decodeURIComponent(this.getAttribute('data-txt')),sec=document.getElementById(sid);if(sec){var h3s=sec.querySelectorAll('h3'),f=false;h3s.forEach(function(h3){if(h3.textContent===txt&&!f){h3.scrollIntoView({behavior:'smooth',block:'start'});f=true;}});if(!f)sec.scrollIntoView({behavior:'smooth',block:'start'});}close();});});}build();var hiT;window.addEventListener('scroll',function(){clearTimeout(hiT);hiT=setTimeout(function(){var ss=document.querySelectorAll('.wrap section'),its=pl.querySelectorAll('.toc-item'),cur=null;ss.forEach(function(s){var r=s.getBoundingClientRect();if(r.top<=150&&r.bottom>150)cur=s.id;});its.forEach(function(it){it.classList.toggle('active',it.getAttribute('data-sid')===cur);});},200);});})();
(function(){var o=document.getElementById('search-overlay'),pn=document.getElementById('search-panel'),pc=document.getElementById('search-close'),inp=document.getElementById('search-input'),pr=document.getElementById('search-prev'),nx=document.getElementById('search-next'),cnt=document.getElementById('search-count'),clr=document.getElementById('search-clear'),res=document.getElementById('search-results');var hits=[],ci=-1,marks=[];function close(){o.classList.remove('show');pn.classList.remove('show');clearM();inp.value='';res.innerHTML='';hits=[];ci=-1;updN();}pc.addEventListener('click',close);o.addEventListener('click',close);document.getElementById('btn-search').addEventListener('click',function(){o.classList.add('show');pn.classList.add('show');setTimeout(function(){inp.focus();},300);});function clearM(){marks.forEach(function(m){var p=m.parentNode;if(p){p.replaceChild(document.createTextNode(m.textContent),m);p.normalize();}});marks=[];}function doSearch(q){clearM();hits=[];ci=-1;marks=[];if(!q||q.trim().length<2){res.innerHTML=q?'<p style=padding:20px;color:var(--ink-2);font-size:14px>请输入至少2个字符</p>':'';updN();return;}var ql=q.trim().toLowerCase(),body=document.querySelector('.wrap');if(!body){updN();return;}var w=document.createTreeWalker(body,NodeFilter.SHOW_TEXT,null,false),tns=[];while(w.nextNode()){var n=w.currentNode;if(n.parentElement&&!['SCRIPT','STYLE','NOSCRIPT','SVG'].includes(n.parentElement.tagName)&&!n.parentElement.closest('#search-panel')&&!n.parentElement.closest('.nav')){tns.push(n);}}tns.forEach(function(node){var t=node.textContent.toLowerCase(),i=t.indexOf(ql);if(i!==-1){var sec=node.parentElement.closest('section'),sid=sec?sec.id:'',stitle=sec&&sec.querySelector('h2')?sec.querySelector('h2').textContent:'',ctx=node.textContent.substring(Math.max(0,i-30),i+ql.length+30);hits.push({node:node,sid:sid,stitle:stitle,ctx:ctx,idx:i});}});hits.forEach(function(hit){var node=hit.node,t=node.textContent,ql2=ql.length,si=t.toLowerCase().indexOf(ql);if(si!==-1){var be=t.substring(0,si),ma=t.substring(si,si+ql2),af=t.substring(si+ql2),mk=document.createElement('mark');mk.className='search-hit';mk.textContent=ma;var p=node.parentNode;p.replaceChild(document.createTextNode(af),node);p.insertBefore(mk,p.childNodes[p.childNodes.length-1]);p.insertBefore(document.createTextNode(be),mk);marks.push(mk);hit.mark=mk;}});if(hits.length===0){res.innerHTML='<p style=padding:20px;color:var(--ink-2);font-size:14px>未找到匹配结果</p>';}else{var html='<div style=padding:8px>';hits.forEach(function(hit,i){html+='<div class="toc-item search-result-item" data-i='+i+' style=font-size:13px;padding:10px 20px;border-bottom:1px solid var(--line)>';html+='<div style=font-weight:600;color:var(--bk1);margin-bottom:4px>'+esc(hit.stitle||'正文')+'</div>';html+='<div style=color:var(--ink-2);font-size:12.5px;line-height:1.5>...'+esc(hit.ctx)+'...</div></div>';});html+='</div>';res.innerHTML=html;res.querySelectorAll('.search-result-item').forEach(function(item){item.addEventListener('click',function(){navTo(parseInt(this.getAttribute('data-i')));});});}updN();}function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}function navTo(idx){if(idx<0||idx>=hits.length)return;if(ci>=0&&ci<hits.length&&hits[ci].mark)hits[ci].mark.classList.remove('search-hit-current');ci=idx;var hit=hits[ci];if(hit.mark){hit.mark.classList.add('search-hit-current');hit.mark.scrollIntoView({behavior:'smooth',block:'center'});}updN();}function updN(){var t=hits.length,c=ci>=0?ci+1:0;cnt.textContent=t>0?c+'/'+t:'0/0';pr.disabled=t===0||ci<=0;nx.disabled=t===0||ci>=t-1;}var st;inp.addEventListener('input',function(){clearTimeout(st);st=setTimeout(function(){doSearch(inp.value);},300);});inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();if(hits.length>0)navTo(ci<0?0:ci);}});pr.addEventListener('click',function(){if(ci>0)navTo(ci-1);});nx.addEventListener('click',function(){if(ci<hits.length-1)navTo(ci+1);});clr.addEventListener('click',function(){inp.value='';doSearch('');inp.focus();});document.addEventListener('keydown',function(e){if((e.ctrlKey||e.metaKey)&&e.key==='k'){e.preventDefault();document.getElementById('btn-search').click();}});})();
</script>'''

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0,viewport-fit=cover"/>
<meta name="description" content="刘宝红供应链管理知识图谱——系统化学习手册，涵盖6本著作精华"/>
<title>刘宝红·供应链管理知识图谱</title>
<style>
''' + css + '''
</style>
</head>
<body>
<div id="progress"></div>

<header class="hero">
  <div class="tag">供应链管理 · 知识图谱</div>
  <h1>刘宝红 · 供应链管理知识图谱</h1>
  <p>系统化学习手册——从供应链全景图、三道防线、降本三台阶到采购五阶段<br>整合6本著作精华，含详细理论、真实案例拆解和核心模型</p>
  <p class="meta">内容来源 <a href="https://scm-blog.com" target="_blank">scm-blog.com</a> · <a href="https://github.com/ChenJJ-DZL/SCM-Knowledge-Atlas" target="_blank">GitHub</a></p>
</header>

<nav class="nav">
  <div class="nav-inner" id="nav">
    <a href="#c1">全景图</a>
    <a href="#c2">采购与供应商</a>
    <a href="#c3">前端防杂</a>
    <a href="#c4">后端减重</a>
    <a href="#c5">中间治乱</a>
    <a href="#c6">防线一</a>
    <a href="#c7">防线二三</a>
    <a href="#c8">工具包</a>
  </div>
</nav>

<div class="wrap">
''' + content + '''
</div>

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

<div id="resume-wrap">
  <div id="resume-badge">📍 继续上次阅读 <span class="arrow-down">↓</span></div>
  <button id="resume-ignore">✕</button>
</div>

<div class="panel-overlay" id="toc-overlay"></div>
<div class="panel" id="toc-panel">
  <div class="panel-header"><h3>📑 目录导航</h3><button class="panel-close" id="toc-close">✕</button></div>
  <div class="panel-body"><div id="toc-list"></div></div>
</div>

<div class="panel-overlay" id="search-overlay"></div>
<div class="panel" id="search-panel">
  <div class="panel-header"><h3>🔍 内容查找</h3><button class="panel-close" id="search-close">✕</button></div>
  <div class="search-box-sm">
    <input type="text" class="search-input" id="search-input" placeholder="输入关键词搜索...">
    <div class="search-nav">
      <button class="search-nav-btn" id="search-prev" disabled>▲</button>
      <span class="search-count" id="search-count">0/0</span>
      <button class="search-nav-btn" id="search-next" disabled>▼</button>
    </div>
    <button class="search-clear" id="search-clear">✕</button>
  </div>
  <div class="panel-body" id="search-results"></div>
</div>

''' + js + '''
</body>
</html>'''

with open('index_new.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'HTML written: {len(html)} chars')
