/* animations.js
   Launch overlay, particle canvas, scroll reveal, and small parallax background.
*/

document.addEventListener('DOMContentLoaded', () => {
  // Launch overlay hide after DOM ready + small delay (simulate premium load)
  const overlay = document.getElementById('launch-overlay');
  setTimeout(() => {
    if (overlay) overlay.classList.add('hide');
    // remove from DOM after transition
    setTimeout(()=> overlay && overlay.remove(), 900);
  }, 900); // show ~900ms then fade (feel free to tweak)

  initParticles();      // draw subtle particle background
  initScrollReveal();    // reveal elements as you scroll
  initParallax();        // parallax minor effect on bg
});

// ---------- Scroll reveal ----------
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    for (const ent of entries) {
      if (ent.isIntersecting) {
        ent.target.classList.add('in-view');
      } else {
        // optional: keep in view once revealed; comment out to keep persistent reveal
        // ent.target.classList.remove('in-view');
      }
    }
  }, { threshold: 0.14 });

  document.querySelectorAll('.reveal, .section, .grocery-list-card, .recipe-results, .welcome-message').forEach(el => observer.observe(el));
}

// ---------- Simple parallax for bg-svg ----------
function initParallax() {
  const bg = document.querySelector('.bg-svg');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (bg) bg.style.transform = `translateY(${Math.min(y * -0.03, 20)}px)`;
  }, { passive: true });
}

// ---------- Cute particle engine (canvas) ----------
function initParticles() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w = canvas.width = innerWidth;
  let h = canvas.height = innerHeight;
  const particles = [];
  const colors = ['rgba(255,255,255,0.03)', 'rgba(255,240,220,0.03)', 'rgba(200,220,255,0.02)'];

  function onResize() { w = canvas.width = innerWidth; h = canvas.height = innerHeight; }
  addEventListener('resize', onResize);

  function spawn() {
    const x = Math.random()*w;
    const y = Math.random()*h;
    const s = 8 + Math.random()*24;
    const vx = (Math.random()-0.5)*0.15;
    const vy = -0.05 - Math.random()*0.2;
    particles.push({x,y,s,vx,vy,life: 200 + Math.random()*200, col: colors[Math.floor(Math.random()*colors.length)]});
  }

  // seed particles
  for (let i=0;i<40;i++) spawn();

  function step() {
    ctx.clearRect(0,0,w,h);
    if (particles.length < 20 && Math.random() > 0.4) spawn();
    for (let i = particles.length-1; i>=0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life--;
      const alpha = Math.max(0, Math.min(1, p.life/300));
      ctx.fillStyle = p.col.replace(/[^,]+\)$/,'') + `${alpha})`;
      // draw soft ellipse (food motif)
      ctx.beginPath();
      ctx.ellipse(p.x, p.y, p.s*0.6, p.s*0.35, Math.PI*0.2, 0, Math.PI*2);
      ctx.fill();
      if (p.life <= 0 || p.y < -50) particles.splice(i,1);
    }
    requestAnimationFrame(step);
  }
  step();
}
