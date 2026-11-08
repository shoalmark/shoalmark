// shoalmark's blog: two small behaviours. The script makes no request of its own: the only loads it causes are the
// figures' image addresses and a preload hint, both ordinary markup the browser loads.
(()=>{
// 1. The contents follow the section being read: the last heading above the top third of the window is current,
//    marked aria-current="location" (drawn in --ink). Driven by scroll and resize, with no animation frame.
const toc=document.querySelector('.toc');
if(toc){
  const links=[...toc.querySelectorAll('a[href^="#"]')];
  const by=new Map(links.map(a=>[decodeURIComponent(a.hash.slice(1)),a]));
  const heads=[...document.querySelectorAll('.post h2[id],.post h3[id]')].filter(h=>by.has(h.id));
  let cur=null,queued=false;
  const pick=()=>{queued=false;let best=null;const line=innerHeight/3;
    for(const h of heads){if(h.getBoundingClientRect().top<=line)best=h;else break;}
    const a=best?by.get(best.id):null;if(a===cur)return;
    if(cur)cur.removeAttribute('aria-current');cur=a;
    if(a){a.setAttribute('aria-current','location');
      const box=toc.getBoundingClientRect(),r=a.getBoundingClientRect();   // keep it in sight in a long list
      if(r.top<box.top||r.bottom>box.bottom)toc.scrollTop+=r.top-box.top-box.height/3;}};
  const soon=()=>{if(!queued){queued=true;setTimeout(pick,60);}};
  addEventListener('scroll',soon,{passive:true});addEventListener('resize',soon);pick();
}
// 2b. The figures play once: each plays when 60 % of it is in view, then rests on its lit end; its control
//    stops it or plays it again. A screen ahead, a preload hint warms its file; a replay takes a fresh address.
//    Readers who ask for reduced motion get the stills and no control.
if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
// 2a. The hero: the share video loops, muted, while it is in view; its control stops it or plays it again. With
//     reduced motion the script has already returned, so the poster, the still, is all that shows.
const hero=document.querySelector('.hero video');
if(hero){const hb=document.querySelector('.hero .again');let held=false;
  const go=()=>{const p=hero.play();if(p&&p.catch)p.catch(()=>{});hb.textContent='stop';hb.setAttribute('aria-pressed','false');};
  const halt=()=>{hero.pause();hb.textContent='play again';hb.setAttribute('aria-pressed','true');};
  hb.hidden=false;hb.addEventListener('click',()=>{held=!hero.paused;held?halt():go();});
  new IntersectionObserver(es=>{for(const e of es){if(e.isIntersecting&&!held)go();else if(!e.isIntersecting&&!hero.paused)hero.pause();}}).observe(hero);}
const phone=matchMedia('(max-width: 640px)');
const els=p=>[...p.querySelectorAll('[data-once]')];
const put=(p,k,q='')=>els(p).forEach(e=>{const v=e.dataset[k]+q;if(e.tagName==='IMG')e.src=v;else e.srcset=v;});
const btn=p=>p.closest('figure').querySelector('.again');
function word(p,playing){const b=btn(p),f=b.dataset.f;b.hidden=false;b.textContent=playing?'stop':'play again';
  b.setAttribute('aria-label',playing?'stop '+f:'play '+f+' again');}
function play(p){
  clearTimeout(p._t);p.dataset.st='load';word(p,true);
  const img=p.querySelector('img');
  img.addEventListener('load',()=>{if(p.dataset.st!=='load')return;p.dataset.st='play';
    const ms=+(phone.matches?p.querySelector('source[data-once]'):img).dataset.ms;p._t=setTimeout(()=>rest(p),ms);},{once:true});
  put(p,'once',p._n?'?r='+(++p._n):(p._n=1,''));
}
function rest(p){clearTimeout(p._t);p.dataset.st='rest';put(p,'still');word(p,false);}
const io=new IntersectionObserver(es=>{for(const e of es){const p=e.target.closest('picture');
  if(p.dataset.st!=='wait'||!e.isIntersecting)continue;
  if(e.intersectionRect.height>=0.6*Math.min(e.boundingClientRect.height,innerHeight)){io.unobserve(e.target);play(p);}}},
  {threshold:[0,.2,.4,.6,.8,1]});
const warm=new IntersectionObserver(es=>{for(const e of es){if(!e.isIntersecting)continue;warm.unobserve(e.target);
  const p=e.target.closest('picture'),s=phone.matches&&p.querySelector('source[data-once]')||e.target;
  const l=document.createElement('link');l.rel='preload';l.as='image';l.href=s.dataset.once;document.head.appendChild(l);}},
  {rootMargin:'100% 0px'});
for(const img of document.querySelectorAll('.post figure img[data-once]')){const p=img.closest('picture');
  p.dataset.st='wait';io.observe(img);warm.observe(img);
  btn(p).addEventListener('click',()=>p.dataset.st==='rest'?play(p):rest(p));}
})();
