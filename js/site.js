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

  // Inquiry form to WhatsApp
  var f = document.getElementById("inquiry");
  if (f) f.addEventListener("submit", function(ev){
    ev.preventDefault();
    var g = function(id){ return document.getElementById(id).value.trim(); };
    var err = document.getElementById("f-error");
    if (!g("f-name") || !g("f-msg")) { err.hidden = false; return; }
    err.hidden = true;
    var text = "Hello Eagle Go, my name is " + g("f-name") + (g("f-city") ? " from " + g("f-city") : "") +
      ".\nAsking for: " + g("f-who") + "\nPreferred country: " + g("f-country") + "\n\n" + g("f-msg");
    var a = document.createElement("a");
    a.href = "https://wa.me/" + WA + "?text=" + encodeURIComponent(text);
    a.target = "_blank"; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
