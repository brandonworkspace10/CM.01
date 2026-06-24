#!/usr/bin/env python3
"""Injects the sitewide 'Request a callback' floating widget into every
marketing HTML page. Idempotent — safe to re-run after new pages are added."""

import glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
MARKER = '<!-- CALLBACK-WIDGET -->'
END_MARKER = '<!-- /CALLBACK-WIDGET -->'

# ---------------------------------------------------------------------------
# English snippet — pill + slide-up panel, namespaced to avoid colliding with
# index.html's existing #contactModal / openContact() / closeContact().
# Positioned bottom-LEFT specifically to avoid the mobile-only
# .lang-float-mob language switcher, which sits bottom-right.
# ---------------------------------------------------------------------------

FULL_SNIPPET = MARKER + '''
<div id="cmCallbackPill" style="position:fixed;bottom:24px;left:18px;z-index:480;display:flex;align-items:center;gap:8px;background:var(--bg-2,#151310);border:1px solid var(--line,#2A2620);border-radius:999px;padding:11px 18px 11px 14px;box-shadow:0 4px 20px rgba(0,0,0,.45);cursor:pointer;font-family:var(--sans,sans-serif);font-size:13px;font-weight:500;color:var(--fg,#F6F2EB);" onclick="openCmCallback()" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform=''">
  <span style="width:8px;height:8px;border-radius:50%;background:var(--accent,#E89B6C);flex:none;"></span>
  Request a callback
</div>

<div id="cmCallbackPanel" style="display:none;position:fixed;bottom:24px;left:18px;z-index:481;width:320px;max-width:calc(100vw - 36px);background:var(--bg-2,#151310);border:1px solid var(--line,#2A2620);border-radius:18px;padding:22px 20px;box-shadow:0 20px 50px rgba(0,0,0,.55);transform:translateY(16px);opacity:0;transition:transform .3s cubic-bezier(.2,.7,.2,1),opacity .3s ease;">
  <button onclick="closeCmCallback()" aria-label="Close" style="position:absolute;top:10px;right:10px;width:26px;height:26px;border-radius:50%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);color:var(--fg-dim,#A6A097);font-size:15px;display:grid;place-items:center;cursor:pointer;line-height:1;">&times;</button>
  <div style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-mute,#6E685F);margin-bottom:6px;">Quick request</div>
  <h4 style="font-family:var(--serif,serif);font-size:21px;font-weight:400;margin:0 0 14px;color:var(--fg,#F6F2EB);">We'll call you back.</h4>
  <form id="cmCallbackForm" style="display:flex;flex-direction:column;gap:10px;">
    <div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;" aria-hidden="true">
      <label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    </div>
    <input name="name" required placeholder="Your name" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <input name="phone" type="tel" required placeholder="Phone number" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <input name="email" type="email" placeholder="Email (optional)" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <select name="type" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;appearance:none;">
      <option value="">Business type&hellip;</option>
      <option>HVAC</option><option>Plumbing</option><option>Electrical</option><option>Roofing</option><option>Cleaning</option><option>Other Home Service</option>
    </select>
    <button type="submit" id="cmCallbackSubmit" style="background:var(--accent,#E89B6C);color:#1a0e00;border:0;border-radius:999px;padding:12px 18px;font-size:13px;font-weight:600;font-family:var(--sans,sans-serif);cursor:pointer;margin-top:4px;">Request a callback &rarr;</button>
    <div id="cmCallbackStatus" style="text-align:center;font-size:11px;color:var(--fg-mute,#6E685F);display:none;"></div>
  </form>
</div>
<script>
(function(){
  function $(id){return document.getElementById(id);}
  var pill = $('cmCallbackPill');
  function isMobile(){ return window.matchMedia('(max-width: 780px)').matches; }
  var peekTimer;
  function cmPeek(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '0.22';
    pill.style.transform = 'translateX(-62%)';
  }
  function cmReveal(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '1';
    pill.style.transform = 'translateX(0)';
    clearTimeout(peekTimer);
    peekTimer = setTimeout(cmPeek, 5000);
  }
  if (pill) {
    pill.style.transition = 'opacity .6s ease, transform .6s ease, box-shadow .2s ease';
    if (isMobile()) { cmPeek(); setTimeout(cmReveal, 1200); }
  }
  window.openCmCallback = function(){
    cmReveal();
    var p = $('cmCallbackPanel'); if(!p) return;
    p.style.display='block';
    requestAnimationFrame(function(){ p.style.transform='translateY(0)'; p.style.opacity='1'; });
  };
  window.closeCmCallback = function(){
    var p = $('cmCallbackPanel'); if(!p) return;
    p.style.transform='translateY(16px)'; p.style.opacity='0';
    setTimeout(function(){ p.style.display='none'; }, 300);
    cmPeek();
  };
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') window.closeCmCallback(); });
  var f = $('cmCallbackForm');
  if (f) f.addEventListener('submit', async function(e){
    e.preventDefault();
    var btn = $('cmCallbackSubmit'), status = $('cmCallbackStatus');
    var data = Object.fromEntries(new FormData(f));
    btn.textContent='Sending…'; btn.disabled=true; status.style.display='none';
    try {
      var res = await fetch('/api/contact', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
      if (res.ok) {
        f.innerHTML = '<div style="text-align:center;padding:18px 0;color:var(--fg,#F6F2EB);font-size:14px;">Got it — we\\'ll call you back shortly.</div>';
      } else {
        var err = await res.json().catch(function(){return {};});
        throw new Error(err.error || 'Send failed');
      }
    } catch(err) {
      btn.textContent='Request a callback →'; btn.disabled=false;
      status.textContent = (err.message||'Something went wrong') + ' — or email hi@callingmatrix.com';
      status.style.display='block'; status.style.color='#ff6b6b';
    }
  });
})();
</script>
''' + END_MARKER + '\n'

# ---------------------------------------------------------------------------
# Spanish snippet — same structure/fields/IDs, translated copy.
# ---------------------------------------------------------------------------

FULL_SNIPPET_ES = MARKER + '''
<div id="cmCallbackPill" style="position:fixed;bottom:24px;left:18px;z-index:480;display:flex;align-items:center;gap:8px;background:var(--bg-2,#151310);border:1px solid var(--line,#2A2620);border-radius:999px;padding:11px 18px 11px 14px;box-shadow:0 4px 20px rgba(0,0,0,.45);cursor:pointer;font-family:var(--sans,sans-serif);font-size:13px;font-weight:500;color:var(--fg,#F6F2EB);" onclick="openCmCallback()" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform=''">
  <span style="width:8px;height:8px;border-radius:50%;background:var(--accent,#E89B6C);flex:none;"></span>
  Solicitar una llamada
</div>

<div id="cmCallbackPanel" style="display:none;position:fixed;bottom:24px;left:18px;z-index:481;width:320px;max-width:calc(100vw - 36px);background:var(--bg-2,#151310);border:1px solid var(--line,#2A2620);border-radius:18px;padding:22px 20px;box-shadow:0 20px 50px rgba(0,0,0,.55);transform:translateY(16px);opacity:0;transition:transform .3s cubic-bezier(.2,.7,.2,1),opacity .3s ease;">
  <button onclick="closeCmCallback()" aria-label="Cerrar" style="position:absolute;top:10px;right:10px;width:26px;height:26px;border-radius:50%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);color:var(--fg-dim,#A6A097);font-size:15px;display:grid;place-items:center;cursor:pointer;line-height:1;">&times;</button>
  <div style="font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-mute,#6E685F);margin-bottom:6px;">Solicitud rapida</div>
  <h4 style="font-family:var(--serif,serif);font-size:21px;font-weight:400;margin:0 0 14px;color:var(--fg,#F6F2EB);">Te llamamos.</h4>
  <form id="cmCallbackForm" style="display:flex;flex-direction:column;gap:10px;">
    <div style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;" aria-hidden="true">
      <label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    </div>
    <input name="name" required placeholder="Tu nombre" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <input name="phone" type="tel" required placeholder="Numero de telefono" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <input name="email" type="email" placeholder="Correo (opcional)" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;">
    <select name="type" style="width:100%;background:var(--bg-3,#1C1915);border:1px solid var(--line,#2A2620);border-radius:9px;padding:10px 12px;color:var(--fg,#F6F2EB);font-family:var(--sans,sans-serif);font-size:13px;outline:none;appearance:none;">
      <option value="">Tipo de negocio&hellip;</option>
      <option>HVAC</option><option>Plomeria</option><option>Electrico</option><option>Techado</option><option>Limpieza</option><option>Otro servicio del hogar</option>
    </select>
    <button type="submit" id="cmCallbackSubmit" style="background:var(--accent,#E89B6C);color:#1a0e00;border:0;border-radius:999px;padding:12px 18px;font-size:13px;font-weight:600;font-family:var(--sans,sans-serif);cursor:pointer;margin-top:4px;">Solicitar una llamada &rarr;</button>
    <div id="cmCallbackStatus" style="text-align:center;font-size:11px;color:var(--fg-mute,#6E685F);display:none;"></div>
  </form>
</div>
<script>
(function(){
  function $(id){return document.getElementById(id);}
  var pill = $('cmCallbackPill');
  function isMobile(){ return window.matchMedia('(max-width: 780px)').matches; }
  var peekTimer;
  function cmPeek(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '0.22';
    pill.style.transform = 'translateX(-62%)';
  }
  function cmReveal(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '1';
    pill.style.transform = 'translateX(0)';
    clearTimeout(peekTimer);
    peekTimer = setTimeout(cmPeek, 5000);
  }
  if (pill) {
    pill.style.transition = 'opacity .6s ease, transform .6s ease, box-shadow .2s ease';
    if (isMobile()) { cmPeek(); setTimeout(cmReveal, 1200); }
  }
  window.openCmCallback = function(){
    cmReveal();
    var p = $('cmCallbackPanel'); if(!p) return;
    p.style.display='block';
    requestAnimationFrame(function(){ p.style.transform='translateY(0)'; p.style.opacity='1'; });
  };
  window.closeCmCallback = function(){
    var p = $('cmCallbackPanel'); if(!p) return;
    p.style.transform='translateY(16px)'; p.style.opacity='0';
    setTimeout(function(){ p.style.display='none'; }, 300);
    cmPeek();
  };
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') window.closeCmCallback(); });
  var f = $('cmCallbackForm');
  if (f) f.addEventListener('submit', async function(e){
    e.preventDefault();
    var btn = $('cmCallbackSubmit'), status = $('cmCallbackStatus');
    var data = Object.fromEntries(new FormData(f));
    btn.textContent='Enviando…'; btn.disabled=true; status.style.display='none';
    try {
      var res = await fetch('/api/contact', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
      if (res.ok) {
        f.innerHTML = '<div style="text-align:center;padding:18px 0;color:var(--fg,#F6F2EB);font-size:14px;">Listo — te llamaremos pronto.</div>';
      } else {
        var err = await res.json().catch(function(){return {};});
        throw new Error(err.error || 'Error al enviar');
      }
    } catch(err) {
      btn.textContent='Solicitar una llamada →'; btn.disabled=false;
      status.textContent = (err.message||'Algo salio mal') + ' — o escribe a hi@callingmatrix.com';
      status.style.display='block'; status.style.color='#ff6b6b';
    }
  });
})();
</script>
''' + END_MARKER + '\n'

# ---------------------------------------------------------------------------
# index.html only: pill that reuses the page's existing #contactModal /
# openContact() instead of building a second modal on the same page.
# ---------------------------------------------------------------------------

PILL_ONLY_SNIPPET = MARKER + '''
<div id="cmCallbackPill" style="position:fixed;bottom:24px;left:18px;z-index:480;display:flex;align-items:center;gap:8px;background:var(--bg-2,#151310);border:1px solid var(--line,#2A2620);border-radius:999px;padding:11px 18px 11px 14px;box-shadow:0 4px 20px rgba(0,0,0,.45);cursor:pointer;font-family:var(--sans,sans-serif);font-size:13px;font-weight:500;color:var(--fg,#F6F2EB);" onclick="openContact()" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform=''">
  <span style="width:8px;height:8px;border-radius:50%;background:var(--accent,#E89B6C);flex:none;"></span>
  Request a callback
</div>
<script>
(function(){
  var pill = document.getElementById('cmCallbackPill');
  function isMobile(){ return window.matchMedia('(max-width: 780px)').matches; }
  var peekTimer;
  function cmPeek(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '0.22';
    pill.style.transform = 'translateX(-62%)';
  }
  function cmReveal(){
    if (!pill || !isMobile()) return;
    pill.style.opacity = '1';
    pill.style.transform = 'translateX(0)';
    clearTimeout(peekTimer);
    peekTimer = setTimeout(cmPeek, 5000);
  }
  if (pill) {
    pill.style.transition = 'opacity .6s ease, transform .6s ease, box-shadow .2s ease';
    if (isMobile()) { cmPeek(); setTimeout(cmReveal, 1200); }
    pill.addEventListener('click', cmReveal);
  }
})();
</script>
''' + END_MARKER + '\n'


# get-a-quote.html already has its own dedicated lead form — the floating
# widget would be a redundant second CTA on that page.
EXCLUDE = {'get-a-quote.html'}


def target_files():
    files = []
    files += glob.glob(os.path.join(ROOT, '*.html'))
    files += glob.glob(os.path.join(ROOT, 'blog', '*.html'))
    files += glob.glob(os.path.join(ROOT, 'lp', '*.html'))
    files += glob.glob(os.path.join(ROOT, 'es', '*.html'))
    files = [f for f in files if os.path.relpath(f, ROOT) not in EXCLUDE]
    return sorted(files)


def pick_snippet(path):
    rel = os.path.relpath(path, ROOT)
    if rel == 'index.html':
        return PILL_ONLY_SNIPPET
    if rel.startswith('es' + os.sep):
        return FULL_SNIPPET_ES
    return FULL_SNIPPET


def inject(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    snippet = pick_snippet(path)

    if MARKER in html:
        start = html.find(MARKER)
        end_idx = html.find(END_MARKER, start)
        if end_idx == -1:
            return 'malformed'
        end = end_idx + len(END_MARKER)
        existing_block = html[start:end]
        if existing_block == snippet.rstrip('\n'):
            return 'unchanged'
        new_html = html[:start] + snippet.rstrip('\n') + html[end:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return 'updated'

    idx = html.rfind('</body>')
    if idx == -1:
        return 'no-body-tag'
    new_html = html[:idx] + snippet + html[idx:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return 'injected'


def main():
    results = {}
    for path in target_files():
        results[os.path.relpath(path, ROOT)] = inject(path)
    injected = [k for k, v in results.items() if v == 'injected']
    updated = [k for k, v in results.items() if v == 'updated']
    unchanged = [k for k, v in results.items() if v == 'unchanged']
    failed = [k for k, v in results.items() if v not in ('injected', 'updated', 'unchanged')]
    print(f"Injected: {len(injected)}  Updated: {len(updated)}  Unchanged: {len(unchanged)}  Failed: {len(failed)}")
    if failed:
        print("FAILED FILES:", [(k, results[k]) for k in failed])


if __name__ == '__main__':
    main()
