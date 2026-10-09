function toggleSidebar(){document.getElementById('sidebar')?.classList.toggle('open')}
window.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('form').forEach(form=>form.addEventListener('submit',()=>{const btn=form.querySelector('button[type="submit"]');if(btn){btn.disabled=true;btn.dataset.original=btn.textContent;btn.textContent='Processing...';setTimeout(()=>{btn.disabled=false;btn.textContent=btn.dataset.original},3500)}}));
});
