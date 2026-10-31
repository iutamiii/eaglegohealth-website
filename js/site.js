(function(){
  var WA = "628117732325";
  var t = document.querySelector(".menu-toggle"), m = document.getElementById("menu");
  if (t && m) t.addEventListener("click", function(){
    var open = m.classList.toggle("open"); t.setAttribute("aria-expanded", open);
  });

  // Hospitals filter
  var dir = document.getElementById("dir");
  if (dir) {
    var chips = document.querySelectorAll(".chip"), q = document.getElementById("hsearch"), empty = document.getElementById("empty"), current = "all";
    function apply(){
      var term = (q.value || "").trim().toLowerCase(), any = false;
      dir.querySelectorAll(".country").forEach(function(sec){
        var okC = current === "all" || sec.dataset.country === current, shown = 0;
        sec.querySelectorAll("li").forEach(function(li){
          var ok = !term || li.textContent.toLowerCase().indexOf(term) > -1 || sec.querySelector("h2").textContent.toLowerCase().indexOf(term) > -1;
          li.hidden = !ok; if (ok) shown++;
        });
        sec.hidden = !(okC && shown); if (!sec.hidden) any = true;
      });
      empty.hidden = any;
    }
    function pick(c){
      current = c;
      chips.forEach(function(ch){ ch.setAttribute("aria-pressed", ch.dataset.country === c); });
      apply();
    }
    chips.forEach(function(ch){ ch.addEventListener("click", function(){ pick(ch.dataset.country); }); });
    q.addEventListener("input", apply);
    var h = location.hash.replace("#","");
    if (h && document.querySelector('.chip[data-country="'+h+'"]')) pick(h);
    window.addEventListener("hashchange", function(){
      var h2 = location.hash.replace("#","");
      if (document.querySelector('.chip[data-country="'+h2+'"]')) pick(h2);
    });
  }

  // Patient testimonials, loaded live from the published Google Sheet
  function parseCSV(t){
    var rows = [], row = [], cell = "", q = false;
    for (var i = 0; i < t.length; i++) {
      var c = t[i];
      if (q) { if (c === '"') { if (t[i+1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
      else if (c === '"') q = true;
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n" || c === "\r") { if (c === "\r" && t[i+1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += c;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows;
  }
  function esc(x){ var d = document.createElement("div"); d.textContent = x || ""; return d.innerHTML; }
  document.querySelectorAll(".testi-section[data-csv]").forEach(function(sec){
    var url = sec.getAttribute("data-csv");
    if (!url) return;
    fetch(url, {cache: "no-store"}).then(function(r){ if (!r.ok) throw 0; return r.text(); }).then(function(txt){
      var rows = parseCSV(txt), head = (rows.shift() || []).map(function(h){ return h.trim().toLowerCase(); });
      var ix = function(k){ return head.indexOf(k); };
      var items = rows.filter(function(r){ return r[ix("nama")] && r[ix("cerita")]; });
      var box = sec.querySelector(".testis");
      if (!items.length) { sec.hidden = true; return; }
      box.innerHTML = items.map(function(r){
        return '<figure class="testi"><blockquote>' + esc(r[ix("cerita")]) + '</blockquote><figcaption><b>' + esc(r[ix("nama")]) +
          '</b><span>' + esc(r[ix("kota")]) + '</span><span>' + esc(r[ix("rumah_sakit")]) + '</span></figcaption></figure>';
      }).join("");
      box.classList.toggle("single", items.length === 1);
      sec.hidden = false;
    }).catch(function(){ /* keep the fallback already on the page */ });
  });
})();
