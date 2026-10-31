import os, re, html, json, glob, datetime
import markdown  # pip install --break-system-packages markdown

# Site is built into the repository root (one level above /tools)
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://eaglegohealth.com"
WA = "628117732325"
WA_SHOW = "+62 811-773-2325"
EMAIL = "ccare@eaglegohealth.com"
ADDRESS = "Jln Potlot III Gg. H. Riin no.17, Duren Tiga, Pancoran, Jakarta Selatan 12760"
FORM_URL = "https://forms.gle/GANTI-DENGAN-LINK-GOOGLE-FORM"
WA_MSG = "Hello Eagle Go, I would like to ask about medical treatment abroad."
WA_LINK = "https://wa.me/%s?text=%s" % (WA, WA_MSG.replace(" ", "%20").replace(",", "%2C"))

ICON = {
"wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.3c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.3 8.3 0 1 1 12 20.3z"/></svg>',
"arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
"heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21.5l8.8-8.8a5 5 0 0 0 0-7.1z"/></svg>',
"globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
"pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
"mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
"search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
"menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

NAV = [("", "Home"), ("hospitals/", "Hospitals"), ("for-hospitals/", "For Hospitals"), ("blog/", "Blog"), ("about/", "About")]

PARTNERS = [("mayapada","Mayapada Hospital"),("awal-bros","RS Awal Bros"),("max","Max Healthcare"),("artemis","Artemis Hospitals"),
("thomson-medical","Thomson Medical"),("mount-miriam","Mount Miriam Cancer Hospital"),("optimax","Optimax Eye Specialist"),
("mahkota","Mahkota Medical Centre"),("regency","Regency Specialist Hospital"),("asia-one","Asia One Healthcare"),
("thomson-hospital","Thomson Hospital Kota Damansara")]

HOSPITALS = [
("Malaysia", ["KPJ Healthcare Group (28 Facilities)","Asia One Healthcare Group","Subang Jaya Medical Centre","Columbia Asia Ara Damansara Medical Centre","ALTY Orthopaedic Hospital","Sunway Medical Centre Kuala Lumpur","Sunway Medical Centre Velocity","Thomson Hospital Kota Damansara","Regency Specialist Hospital, Johor","Mahkota Medical Centre, Melaka","Mount Miriam Cancer Hospital, Penang","Optimax Eye Specialist","Genesis IVF","IHEAL Medical Centre","Oasis Eye Specialist","Gleneagles Hospital Group","Monash IVF","Prince Court Medical Centre","Island Hospital, Penang"]),
("Indonesia", ["Mayapada Hospital","RS Awal Bros"]),
("India", ["Artemis Hospital Group (6 Facilities)","Max Healthcare (22 Facilities)","Apollo Hospitals","Fortis Healthcare","Rainbow Children’s Hospital","MIOT International Hospital","Medanta, The Medicity","NeuroGen Brain & Spine Institute","Accord Hospital","HCG Hospitals","Kokilaben Dhirubhai Ambani Hospital","Manipal Hospitals"]),
("Thailand", ["Phyathai 2 Hospital","Phyathai Hospital","B.Care Medical Center","BIDH Dental Hospital","Bumrungrad International Hospital","Holistic Medical Centre","Kasemrad Hospital","Samitivej Hospital","Samitivej Children’s Hospital","Sukhumvit Hospital","Yanhee International Hospital","VitaLife Scientific Wellness Center","RXV Wellness Village Sampran"]),
("United Arab Emirates", ["American Hospital Dubai","NMC Hospital","Burjeel Hospitals","Mediclinic Middle East","Aster Hospitals","King’s College Hospital London, Dubai","Saudi German Hospital","Moorfields Eye Hospital Dubai","Cosmesurge","The Face Aesthetic Clinic","Fakih IVF","Fakeeh University Hospital","Bourn Hall Fertility Clinic","Tajmeel Clinics","Max Healthcare"]),
("Turkey", ["Anadolu Medical Center","Medipol Hospital","Acıbadem Group of Hospitals","Acıbadem Beauty Centre","Memorial Healthcare Group","Liv Hospital","Turan & Turan Health Group","Quartz Clinique","Istanbul Aesthetic Centre","WestDent Clinic"]),
("United Kingdom", ["The London Clinic","Blackheath Hospital","The Alexandra Hospital","London Independent Hospital","Beaumont Hospital","Albyn Hospital","Ross Hall Hospital","Bishops Wood Hospital Cancer Centre","The Priory Hospital","Clementine Churchill Hospital","Circle Rehabilitation"]),
("Egypt", ["As-Salam International Hospital","Dar Al Fouad Hospital","Andalusia Hospitals","Cleopatra Hospital","Ganzouri Hospital"]),
("South Korea", ["JW Plastic Surgery","JK Plastic Surgery"]),
("Spain", ["Clínica Tambre","Dexeus University Hospital"]),
("Saudi Arabia", ["Saudi German Hospital","Andalusia Hospitals, Saudi Arabia"]),
("Kenya", ["Gertrude’s Children’s Hospital","HCG CCK Cancer Centre","Victoria IVF & Fertility Centre"]),
("Switzerland", ["Hirslanden Private Hospital Group"]),
("Czech Republic", ["Hospital Horovice"]),
("Israel", ["Sheba Medical Center"]),
("Vietnam", ["Vinmec Healthcare System"]),
("Mauritius", ["C-Care Hospitals & Clinics"]),
("Nigeria", ["Reddington Multispecialist Hospital"]),
("Uganda", ["International Hospital Kampala"]),
]
PARTNER_NAMES = ["Asia One Healthcare Group","Thomson Hospital Kota Damansara","Regency Specialist Hospital, Johor","Mahkota Medical Centre, Melaka","Mount Miriam Cancer Hospital, Penang","Optimax Eye Specialist","Mayapada Hospital","RS Awal Bros","Artemis Hospital Group (6 Facilities)","Max Healthcare (22 Facilities)"]
TOTAL = sum(len(h) for _, h in HOSPITALS)

BULAN = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]

def load_posts():
    """Read every article in content/posts/*.md (front matter + markdown body), newest first."""
    posts = []
    for f in glob.glob(os.path.join(OUT, "content", "posts", "*.md")):
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        if meta.get("draft", "").lower() == "true":
            continue
        d = datetime.date.fromisoformat(meta["date"])
        body = m.group(2).strip()
        words = len(re.findall(r"\w+", body))
        posts.append({
            "slug": os.path.splitext(os.path.basename(f))[0],
            "title": meta["title"], "category": meta.get("category", "Kesehatan"),
            "date": d, "date_id": "%d %s %d" % (d.day, BULAN[d.month-1], d.year),
            "excerpt": meta.get("excerpt", ""), "description": meta.get("description", meta.get("excerpt", "")),
            "cover": meta.get("cover", ""), "cover_alt": meta.get("cover_alt", ""),
            "minutes": max(1, round(words / 200)),
            "html": markdown.markdown(body, extensions=["extra", "sane_lists"]),
        })
    return sorted(posts, key=lambda p: p["date"], reverse=True)

POSTS = load_posts()

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
e = html.escape

def page(path, title, desc, body, current, lang="en", head_extra=""):
    depth = path.count("/") + 1 if path else 0
    base = "../" * depth
    nav = "".join('<li><a href="%s"%s>%s</a></li>' % ((base + href) or "./", ' aria-current="page"' if href == current else "", label) for href, label in NAV)
    nav = nav.replace('href="../"', 'href="../"')
    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{base}images/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@500;600;700&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="{base}css/style.css">
<link rel="canonical" href="{SITE_URL}/{path + "/" if path else ""}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}/{path + "/" if path else ""}">
<meta property="og:site_name" content="Eagle Go Health">{head_extra}
</head>
<body>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="{base or './'}" aria-label="Eagle Go home">
      <img src="{base}images/logo-mark.png" alt="" width="46" height="42">
      <span class="brand-text"><strong>EAGLE GO</strong><span>care you can trust</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu">{ICON["menu"]}</button>
    <ul class="menu" id="menu">{nav}<li class="menu-cta"><a href="{base}contact/"{' aria-current="page"' if current=="contact/" else ""}>Contact Us</a></li></ul>
  </div>
</header>
<main>
{body.replace("{base}", base)}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <span class="logo-chip"><img src="{base}images/logo-mark-white.png" alt="" width="52" height="48"><strong>EAGLE GO<small>care you can trust</small></strong></span>
        <p>Indonesia-based cross-border healthcare coordination. We connect patients with trusted international hospitals.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul><li><a href="{base}hospitals/">Hospitals</a></li><li><a href="{base}for-hospitals/">For Hospitals</a></li><li><a href="{base}blog/">Blog</a></li><li><a href="{base}about/">About</a></li></ul>
      </div>
      <div>
        <h4>Help</h4>
        <ul><li><a href="{FORM_URL}" target="_blank" rel="noopener">Send a medical inquiry</a></li><li><a href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></li></ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul><li>WhatsApp: <a href="{WA_LINK}" target="_blank" rel="noopener">{WA_SHOW}</a></li><li>Email: {EMAIL}</li><li>{ADDRESS}</li></ul>
      </div>
    </div>
    <div class="foot-note">
      <span>&copy; 2026 Eagle Go Health. All rights reserved.</span>
      <span>Eagle Go provides non-clinical coordination. We do not give medical advice or make treatment decisions.</span>
    </div>
  </div>
</footer>
<a class="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with Eagle Go on WhatsApp">{ICON["wa"]}</a>
<script src="{base}js/site.js"></script>
</body>
</html>
'''
    full = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)

def logo_track(base_alt=True):
    imgs = "".join('<img class="logo-%s" src="{base}images/partners/%s.png" alt="%s" loading="lazy">' % (f, f, e(n)) for f, n in PARTNERS)
    hidden = "".join('<img class="logo-%s" src="{base}images/partners/%s.png" alt="" aria-hidden="true" loading="lazy">' % (f, f) for f, _ in PARTNERS)
    return imgs + hidden

def post_cards(featured=False, limit=None, exclude=None):
    items = [p for p in POSTS if p["slug"] != exclude][:limit]
    out = []
    for p in items:
        out.append(f'''<a class="post" href="{{base}}blog/{p["slug"]}/">
  <div style="display:grid;gap:10px;align-content:start"><span class="tag">{e(p["category"])}</span><h3>{e(p["title"])}</h3><time datetime="{p["date"].isoformat()}">{p["date_id"]}</time></div>
  <div style="display:grid;gap:12px;align-content:start"><p>{e(p["excerpt"])}</p><span class="more">Baca artikel</span></div>
</a>''')
    return '<div class="posts%s">%s</div>' % (" featured" if featured else "", "".join(out))

def cta_band(title, text):
    return f'''<section class="section"><div class="wrap"><div class="cta-band">
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="btn-row"><a class="btn btn-light" href="{WA_LINK}" target="_blank" rel="noopener">{ICON["wa"]}Chat on WhatsApp</a><a class="btn btn-outline-light" href="{FORM_URL}" target="_blank" rel="noopener">Send an inquiry</a></div>
</div></div></section>'''

# ---------------- HOME ----------------
dest = "".join(f'<a class="dest" href="{{base}}hospitals/#{slug(c)}"><b>{c}</b><span>{len(h)} {"hospital" if len(h)==1 else "hospitals"}</span></a>' for c, h in HOSPITALS)
home = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow">Medical care abroad, coordinated</span>
      <h1>Your bridge to <em>world-class</em> medical care</h1>
      <p class="lead">Seamless coordination, trusted hospitals and patient-focused support. We help you and your family reach the right international hospital with a clear plan at every step.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="{WA_LINK}" target="_blank" rel="noopener">{ICON["wa"]}Talk to our team</a>
        <a class="btn btn-ghost" href="{{base}}hospitals/">See our hospitals</a>
      </div>
      <div class="facts">
        <div class="fact"><b>{len(HOSPITALS)}</b><span>countries</span></div>
        <div class="fact"><b>{TOTAL}+</b><span>hospitals and clinics</span></div>
        <div class="fact"><b>{len(PARTNERS)}</b><span>hospital partners</span></div>
      </div>
    </div>
    <div class="hero-media">
      <div class="photo"><img src="{{base}}images/patient-care.jpg" alt="A smiling patient in a wheelchair with two hospital staff" width="984" height="656"></div>
      <div class="hero-badge"><span class="cross" aria-hidden="true"></span><p><strong>Care you can trust</strong>From first inquiry until you are back home</p></div>
    </div>
  </div>
</section>

<section class="logos" aria-label="Hospital partners">
  <div class="wrap">
    <p>Working with hospitals including</p>
    <div class="marquee"><div class="marquee-track">{logo_track()}</div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Why Eagle Go</span><h2>Trust, clarity and care in every case</h2><p>We focus on patient-focused coordination so you can access international medical care with confidence and peace of mind.</p></div>
    <div class="why-grid">
      <article class="why"><span class="icon">{ICON["shield"]}</span><h3>Trusted medical network</h3><p>We work closely with reputable hospitals, specialists and licensed medical partners, so you are connected only to recognized healthcare providers.</p></article>
      <article class="why"><span class="icon">{ICON["heart"]}</span><h3>Personal support for every patient</h3><p>Every situation is different. We tailor our help to the medical need, the urgency and your own preferences, and we support the family too.</p></article>
      <article class="why"><span class="icon">{ICON["globe"]}</span><h3>Cross-border coordination</h3><p>We manage communication, scheduling and logistics between you and the hospital abroad, so the process stays clear and efficient.</p></article>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="head"><span class="eyebrow">How it works</span><h2>Four steps from inquiry to treatment</h2><p>Seeking care across borders does not have to be complicated. We guide each step so you can focus on your health.</p></div>
    <div class="steps">
      <div class="step"><span class="step-num">1</span><h3>Medical inquiry and case review</h3><p>Share your medical reports and tell us what you need. We check the documents so your case is ready to send to hospitals.</p></div>
      <div class="step"><span class="step-num">2</span><h3>Hospital and doctor matching</h3><p>We send your case to suitable hospitals and help you compare the options that come back.</p></div>
      <div class="step"><span class="step-num">3</span><h3>Appointment and treatment coordination</h3><p>Once you decide, we arrange the appointment and keep communication with the hospital clear.</p></div>
      <div class="step"><span class="step-num">4</span><h3>Medical travel and care support</h3><p>We help you plan the trip and stay in touch during treatment and after you return home.</p></div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Medical destinations</span><h2>Trusted hospitals in {len(HOSPITALS)} countries</h2><p>We support access to hospitals in established medical tourism destinations. Choose a country to see the hospitals we coordinate with.</p></div>
    <div class="dest-grid">{dest}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="media"><img src="{{base}}images/doctor-heart.jpg" alt="A doctor holding a red heart with a medical cross" loading="lazy"></div>
    <div class="copy">
      <span class="eyebrow">Need medical guidance?</span>
      <h2>Let Eagle Go help you plan your next step</h2>
      <p>Our team helps you understand your options, coordinates with the hospital and plans the next steps with you. Send us your medical reports and we will get back to you.</p>
      <p class="disclaimer">Our role is non-clinical. Diagnosis and treatment decisions always stay with the doctors at the hospital.</p>
      <div class="btn-row"><a class="btn btn-primary" href="{WA_LINK}" target="_blank" rel="noopener">{ICON["wa"]}Chat on WhatsApp</a><a class="btn btn-ghost" href="{FORM_URL}" target="_blank" rel="noopener">Send an inquiry</a></div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Health insights</span><h2>Latest articles</h2><p>Articles to help you understand medical conditions and treatment options abroad.</p></div>
    {post_cards(limit=3)}
  </div>
</section>
'''
page("", "Eagle Go Health", "Eagle Go helps patients from Indonesia access trusted international hospitals, with clear coordination from first inquiry to treatment and recovery.", home, "")

# ---------------- HOSPITALS ----------------
chips = '<button class="chip" type="button" data-country="all" aria-pressed="true">All<small>' + str(TOTAL) + '</small></button>' + "".join(
    f'<button class="chip" type="button" data-country="{slug(c)}" aria-pressed="false">{c}<small>{len(h)}</small></button>' for c, h in HOSPITALS)
blocks = ""
for c, hs in HOSPITALS:
    lis = "".join('<li%s>%s</li>' % (' class="partner"' if n in PARTNER_NAMES else "", e(n)) for n in hs)
    blocks += f'<section class="country" id="{slug(c)}" data-country="{slug(c)}"><div><h2>{c}</h2><p class="count">{len(hs)} {"hospital" if len(hs)==1 else "hospitals"} and clinics</p></div><ul class="h-list">{lis}</ul></section>'
hosp = f'''
<section class="banner"><div class="wrap">
  <span class="eyebrow">Hospitals</span>
  <h1>Healthcare providers we work with</h1>
  <p>A selection of reputable hospitals and medical centers that Eagle Go coordinates with, across {len(HOSPITALS)} countries. Hospitals marked Partner have a direct partnership with us.</p>
</div></section>
<section class="section" style="padding-top:44px">
  <div class="wrap">
    <div class="dir-tools">
      <label class="search" for="hsearch">{ICON["search"]}<input id="hsearch" type="search" placeholder="Search a hospital or city" autocomplete="off"></label>
    </div>
    <div class="chips" role="group" aria-label="Filter by country" style="margin-bottom:28px">{chips}</div>
    <div id="dir">{blocks}</div>
    <p class="empty" id="empty" hidden>No hospital matches your search. Try another name, or ask us on WhatsApp.</p>
  </div>
</section>
{cta_band("Not sure which hospital fits your case?", "Send us your medical reports and we will help you shortlist suitable hospitals.")}
'''
page("hospitals", "Hospitals | Eagle Go Health", "Reputable hospitals and medical centers in %d countries that Eagle Go coordinates with, including Malaysia, India, Thailand, Turkey and the UK." % len(HOSPITALS), hosp, "hospitals/")

# ---------------- FOR HOSPITALS ----------------
plogos = "".join('<div><img src="{base}images/partners/%s.png" alt="%s" loading="lazy"></div>' % (f, e(n)) for f, n in PARTNERS)
forh = f'''
<section class="banner"><div class="wrap">
  <span class="eyebrow">For hospital partners</span>
  <h1>Structured access to Indonesia's outbound patient market</h1>
  <p>Eagle Go Health is an Indonesia-based cross-border healthcare coordination and market access company. We help international hospitals receive Indonesian patients through structured, compliant and transparent referral coordination.</p>
  <div class="btn-row" style="margin-top:8px"><a class="btn btn-light" href="{{base}}contact/">Partner with us</a></div>
</div></section>

<section class="section">
  <div class="wrap">
    <div class="head"><span class="eyebrow">The market</span><h2>One of Southeast Asia's largest outbound healthcare markets</h2><p>Patient mobility is driven by rising health awareness, a growing upper middle income segment and gaps in domestic specialization. Malaysia and Singapore remain the main destinations, while Thailand, India and advanced markets serve cost-sensitive or complex cases.</p></div>
    <div class="stats">
      <div class="stat"><b>1 to 2 million</b><span>Indonesians seek treatment abroad every year</span></div>
      <div class="stat"><b>USD 10 billion</b><span>spent on medical treatment abroad each year</span></div>
      <div class="stat"><b>Fragmented</b><span>most referrals still run through personal networks and informal intermediaries</span></div>
    </div>
    <p class="source">Sources: <a href="https://finance.detik.com/berita-ekonomi-bisnis/d-7960801/2-juta-wni-pilih-berobat-ke-ln-sektor-kesehatan-ri-bocor-rp-162-t" target="_blank" rel="noopener">Detik Finance</a>, <a href="https://www.imarcgroup.com/indonesia-medical-tourism-market" target="_blank" rel="noopener">IMARC Group</a></p>
  </div>
</section>

<section class="section tint">
  <div class="wrap split">
    <div class="copy">
      <span class="eyebrow">Our institutional function</span>
      <h2>A coordination bridge, strictly non-clinical</h2>
      <p>Informal referrals mean limited visibility, inconsistent documents and unpredictable conversions. We work as a structured bridge between international institutions and Indonesian patients, with defined workflows and ethical engagement standards.</p>
      <ul class="ticks">
        <li>Pre-case coordination and documentation alignment</li>
        <li>Structured communication flow management</li>
        <li>Referral pathway standardization</li>
        <li>Distribution channel management within defined governance frameworks</li>
      </ul>
      <p class="disclaimer">We do not provide medical advice or treatment decisions. Clinical authority stays with the hospital.</p>
    </div>
    <div class="media"><img src="{{base}}images/stethoscope.jpg" alt="A stethoscope, notebook and keyboard on a white desk" loading="lazy"></div>
  </div>
</section>

<section class="section dark">
  <div class="wrap split">
    <div class="copy">
      <span class="eyebrow">Operating model</span>
      <h2>Our referral framework</h2>
      <p style="color:var(--on-dark-muted)">Every case moves through the same five stages, so partner hospitals receive structured and reliable referrals.</p>
    </div>
    <ol class="process">
      <li><b>Market engagement and lead qualification</b></li>
      <li><b>Pre-case information alignment</b></li>
      <li><b>Institutional referral coordination</b></li>
      <li><b>Structured communication management</b></li>
      <li><b>Post-referral continuity support</b></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Market access and distribution</span><h2>Two layers that reach patients across Indonesia</h2><p>We combine digital channels with a network of sub-agents. The digital layer identifies interest and screens cases. Sub-agents handle local intake, first document collection and structured handovers under clear operational guidelines.</p></div>
    <div class="stats">
      <div class="stat"><b>130,000+</b><span>followers across the founder's social media and education channels</span></div>
      <div class="stat"><b>20</b><span>regions covered by our sub-agent network</span></div>
      <div class="stat"><b>{len(HOSPITALS)}</b><span>destination countries in our hospital network</span></div>
    </div>
    <ul class="ticks" style="margin-top:36px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
      <li>Wider coverage across Indonesia</li><li>Early-stage case screening</li><li>Documents prepared before referral</li><li>A more controlled referral workflow</li>
    </ul>
  </div>
</section>

<section class="section tint">
  <div class="wrap split">
    <div class="copy">
      <span class="eyebrow">Value for hospital partners</span>
      <h2>What partner hospitals get</h2>
      <ul class="ticks">
        <li>Predictable access to qualified Indonesian outbound patients</li>
        <li>Better pre-consultation case readiness and documentation flow</li>
        <li>Less administrative work in cross-border coordination</li>
        <li>Clear and controlled communication channels</li>
        <li>Scalable market reach through structured distribution channels</li>
      </ul>
    </div>
    <div class="copy">
      <span class="eyebrow">What makes us different</span>
      <h2>How we work</h2>
      <ul class="ticks">
        <li>Institutional-first model</li><li>Non-clinical boundaries</li><li>Structured coordination</li><li>Ethical and transparent</li><li>Long-term partnership</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Governance</span><h2>Vision, mission and values</h2></div>
    <div class="vm" style="margin-bottom:20px">
      <div><h3>Vision</h3><p>To position Indonesia as a professionally managed and institutionally aligned outbound healthcare market within the regional and global medical ecosystem.</p></div>
      <div><h3>Mission</h3><p>To provide structured and compliant access to the Indonesian outbound healthcare market by aligning international institutions with transparent coordination frameworks and sustainable referral governance.</p></div>
    </div>
    <div class="values">
      <div class="value"><h3>Integrity</h3><p>Transparency, ethical standards and clear role boundaries in every cross-border engagement.</p></div>
      <div class="value"><h3>Structure</h3><p>Documented processes and accountable coordination frameworks for consistency and clarity.</p></div>
      <div class="value"><h3>Institutional alignment</h3><p>Partnerships built on aligned objectives, clear communication and long-term collaboration.</p></div>
      <div class="value"><h3>Governance</h3><p>Respect for clinical authority and regulatory boundaries, so every referral stays professionally managed and compliant.</p></div>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Our hospital partners</span><h2>Hospitals already working with us</h2></div>
    <div class="logo-grid">{plogos}</div>
  </div>
</section>
{cta_band("Interested in partnering with Eagle Go?", "Contact us to discuss a referral partnership for your hospital or healthcare institution.")}
'''
page("for-hospitals", "For Hospitals | Eagle Go Health", "Eagle Go Health helps international hospitals access Indonesian outbound patients through structured, compliant and transparent referral coordination.", forh, "for-hospitals/")

# ---------------- BLOG ----------------
blog = f'''
<section class="banner"><div class="wrap">
  <span class="eyebrow">Blog</span>
  <h1>Medical insights and health updates</h1>
  <p>Guidance to help you understand medical conditions, treatment options and international healthcare pathways, so you can make informed decisions with more confidence.</p>
</div></section>
<section class="section"><div class="wrap">{post_cards(featured=True)}</div></section>
{cta_band("Have a question about a condition?", "Tell us about your case and we will help you find hospitals that treat it.")}
'''
page("blog", "Blog | Eagle Go Health", "Medical insights and health updates from Eagle Go to help you understand conditions, treatment options and care abroad.", blog, "blog/")

# ---------------- ABOUT ----------------
about = f'''
<section class="banner"><div class="wrap">
  <span class="eyebrow">About Eagle Go</span>
  <h1>Helping patients reach care they cannot find at home</h1>
  <p>Many patients face limited access to the facilities, technology or specialist doctors they need in their home country. That often leaves families confused and worried when further treatment is needed.</p>
</div></section>

<section class="section">
  <div class="wrap split">
    <div class="copy">
      <span class="eyebrow">What we do</span>
      <h2>A medical tourism facilitator you can rely on</h2>
      <p>Eagle Go helps patients access trusted and technologically advanced international hospitals. We support you in finding the right hospital, coordinating the medical care and staying with you during treatment, so every step is clearer.</p>
      <p class="disclaimer">Our role is non-clinical. We do not give medical advice or make treatment decisions.</p>
    </div>
    <div class="media"><img src="{{base}}images/support.jpg" alt="An Eagle Go coordinator on a headset call" loading="lazy"></div>
  </div>
</section>

<section class="section tint">
  <div class="wrap ceo">
    <div class="portrait"><img src="{{base}}images/ceo.jpg" alt="Indira Utami, CEO of Eagle Go" loading="lazy"></div>
    <div class="copy">
      <span class="eyebrow">Meet our CEO</span>
      <h2>Led by Indira Utami</h2>
      <p>Indira Utami has long been involved in medical tourism through her initiative, Berobat ke Luar Negeri, assisting and referring many patients to receive treatment in Malaysia. That experience is the foundation of Eagle Go's responsible, patient-centered approach.</p>
      <p>She oversees the development of cross-border healthcare partnerships, building on her experience connecting Indonesian audiences with global institutions across several sectors.</p>
      <p class="name">Indira Utami<span>Chief Executive Officer, Eagle Go Health</span></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="vm" style="margin-bottom:56px">
      <div><span class="eyebrow">Vision</span><p>To become a trusted medical tourism facilitator in Asia that connects patients with international healthcare services.</p></div>
      <div><span class="eyebrow">Mission</span><p>To provide professional, clear and patient-centered cross-border medical assistance and coordination.</p></div>
    </div>
    <div class="head"><span class="eyebrow">Core values</span><h2>What guides our work</h2></div>
    <div class="values">
      <div class="value"><h3>Trust</h3><p>Work only with reputable hospitals and be open with patients about every step.</p></div>
      <div class="value"><h3>Clarity and coordination</h3><p>Give clear guidance and well-coordinated processes.</p></div>
      <div class="value"><h3>Professionalism</h3><p>Handle medical coordination with responsible professional standards.</p></div>
      <div class="value"><h3>Patient-centered care</h3><p>Put the needs, comfort and safety of patients first.</p></div>
    </div>
  </div>
</section>
{cta_band("Let us help you plan your treatment", "Talk to our team about your case and the hospitals that can help.")}
'''
page("about", "About | Eagle Go Health", "Eagle Go is a medical tourism facilitator led by Indira Utami, helping patients access trusted international hospitals.", about, "about/")

# ---------------- CONTACT ----------------
countries = "".join(f"<option>{c}</option>" for c, _ in HOSPITALS)
contact = f'''
<section class="banner"><div class="wrap">
  <span class="eyebrow">Contact us</span>
  <h1>We are here to help with your medical journey</h1>
  <p>Reach out for trusted guidance and personal support. Patients, families and hospital partners are all welcome.</p>
</div></section>
<section class="section">
  <div class="wrap contact-grid">
    <div class="info">
      <div class="info-item">{ICON["wa"]}<div><b>WhatsApp</b><a href="{WA_LINK}" target="_blank" rel="noopener">{WA_SHOW}</a></div></div>
      <div class="info-item">{ICON["mail"]}<div><b>Email</b><span>{EMAIL}</span></div></div>
      <div class="info-item">{ICON["pin"]}<div><b>Office</b><span>{ADDRESS}</span></div></div>
      <div class="media" style="border-radius:var(--radius);overflow:hidden;aspect-ratio:16/10"><img src="{{base}}images/doctor.jpg" alt="A doctor holding a stethoscope" style="width:100%;height:100%;object-fit:cover" loading="lazy"></div>
    </div>
    <div class="form-card">
      <span class="eyebrow">Medical inquiry</span>
      <h2>Tell us about your case</h2>
      <p>Fill in our short inquiry form. It takes about 3 minutes and helps our team understand your needs before we contact you.</p>
      <ul class="ticks">
        <li>Patient details and current condition</li>
        <li>Medical reports you already have</li>
        <li>Preferred country and timing</li>
      </ul>
      <div class="btn-row"><a class="btn btn-light" href="{FORM_URL}" target="_blank" rel="noopener">Fill in the inquiry form</a></div>
      <p style="font-size:.92rem">Prefer to chat? Message us on <a href="{WA_LINK}" target="_blank" rel="noopener" style="color:#fff">WhatsApp</a>.</p>
    </div>
  </div>
</section>
'''
page("contact", "Contact | Eagle Go Health", "Contact Eagle Go by WhatsApp or email for guidance on medical treatment abroad.", contact, "contact/")

# shared JS
os.makedirs(os.path.join(OUT, "js"), exist_ok=True)
open(os.path.join(OUT, "js", "site.js"), "w").write('''(function(){
  var WA = "%s";
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
      ".\\nAsking for: " + g("f-who") + "\\nPreferred country: " + g("f-country") + "\\n\\n" + g("f-msg");
    var a = document.createElement("a");
    a.href = "https://wa.me/" + WA + "?text=" + encodeURIComponent(text);
    a.target = "_blank"; a.rel = "noopener";
    document.body.appendChild(a); a.click(); a.remove();
  });
})();
''' % WA)
# ---------------- ARTICLES ----------------
for p in POSTS:
    cover = ""
    if p["cover"]:
        cover = f'<figure class="article-cover"><img src="{{base}}{p["cover"]}" alt="{e(p["cover_alt"])}"></figure>'
    related = post_cards(limit=2, exclude=p["slug"])
    schema = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p["title"],
        "datePublished": p["date"].isoformat(), "description": p["description"],
        "author": {"@type": "Organization", "name": "Eagle Go Health"},
        "publisher": {"@type": "Organization", "name": "Eagle Go Health"}}, ensure_ascii=False)
    body = f'''
<section class="article-head"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{{base}}blog/">Blog</a><span aria-hidden="true">/</span><span>{e(p["category"])}</span></nav>
  <h1>{e(p["title"])}</h1>
  <p class="post-meta"><time datetime="{p["date"].isoformat()}">{p["date_id"]}</time><span aria-hidden="true">&middot;</span><span>{p["minutes"]} menit baca</span><span aria-hidden="true">&middot;</span><span>Tim Eagle Go</span></p>
</div></section>
<section class="section" style="padding-top:40px"><div class="wrap article-layout">
  <article class="prose">
    {cover}
    {p["html"]}
    <p class="disclaimer article-note">Artikel ini untuk edukasi kesehatan dan tidak menggantikan konsultasi dengan dokter. Keputusan pengobatan tetap diambil bersama tim medis yang menangani.</p>
  </article>
  <aside class="article-side">
    <div class="side-card">
      <span class="eyebrow">Butuh bantuan?</span>
      <h3>Berobat ke luar negeri dengan pendampingan</h3>
      <p>Kirim hasil pemeriksaan, tim Eagle Go bantu carikan rumah sakit yang sesuai dan mengatur prosesnya.</p>
      <a class="btn btn-primary" href="{WA_LINK}" target="_blank" rel="noopener">{ICON["wa"]}Chat WhatsApp</a>
      <a class="btn btn-ghost" href="{FORM_URL}" target="_blank" rel="noopener">Isi form konsultasi</a>
    </div>
  </aside>
</div></section>
<section class="section tint"><div class="wrap">
  <div class="head"><span class="eyebrow">Baca juga</span><h2>Artikel lainnya</h2></div>
  {related}
</div></section>
'''
    page("blog/" + p["slug"], p["title"] + " | Eagle Go Health", p["description"], body, "blog/", lang="id",
         head_extra=f'\n<meta property="og:type" content="article">\n<script type="application/ld+json">{schema}</script>')

# ---------------- SITEMAP / ROBOTS ----------------
urls = ["", "hospitals/", "for-hospitals/", "blog/", "about/", "contact/"] + ["blog/%s/" % p["slug"] for p in POSTS]
today = datetime.date.today().isoformat()
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    lm = next((p["date"].isoformat() for p in POSTS if u == "blog/%s/" % p["slug"]), today)
    sm += "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (SITE_URL, u, lm)
sm += "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)
open(os.path.join(OUT, ".nojekyll"), "w").write("")

print("built", TOTAL, "hospitals in", len(HOSPITALS), "countries;", len(POSTS), "articles")
