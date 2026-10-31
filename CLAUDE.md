# Eagle Go Health website

Static website for eaglegohealth.com, published with GitHub Pages from the `main` branch (root folder). Every push to `main` goes live in 1 to 2 minutes, so only push after the owner (Indira) has approved the change.

## How the site is built

- `tools/build.py` generates every HTML page in the repository root (index.html, hospitals/, for-hospitals/, blog/, about/, contact/, blog/<slug>/), plus sitemap.xml, robots.txt and .nojekyll.
- Never edit generated HTML by hand. Change `tools/build.py`, `css/style.css`, `js/site.js` or `content/posts/*.md`, then rebuild:

```
pip install --break-system-packages markdown
python3 tools/build.py
```

- Shared look: `css/style.css` and `js/site.js`. Images live in `images/` as separate files (never embedded in HTML). Blog cover images go in `images/blog/`.
- All links are relative, so the site works both at the github.io address and on eaglegohealth.com.
- Hospital list, partner logos, contact details, WhatsApp number and the Google Form link are constants at the top of `tools/build.py`.

## Adding a blog article

1. Create `content/posts/<slug>.md`. The file name becomes the URL: `blog/<slug>/`. Use lowercase words joined by hyphens.
2. Front matter, then the article in Markdown:

```
---
title: Judul Artikel
date: 2026-11-05
category: Ginjal
excerpt: Satu atau dua kalimat untuk kartu artikel di Home dan halaman Blog.
description: Deskripsi untuk Google, sekitar 150 karakter.
cover: images/blog/<slug>.jpg
cover_alt: Deskripsi singkat gambar
---
Isi artikel...
```

   `cover` and `cover_alt` are optional. Add `draft: true` to keep an article out of the site.
3. Run `python3 tools/build.py`. Home shows the 3 newest articles, the Blog page lists all of them, and the sitemap updates itself.
4. Show the owner a preview and wait for approval before committing and pushing.

## Writing style for articles

- Bahasa Indonesia, written in Indira's own voice: warm, clear, plain words, short paragraphs. It must not read as AI-written.
- No em dashes and no quotation marks. Rephrase instead.
- Use `##` subheadings and plain bullet lists where they help scanning.
- Eagle Go is a non-clinical coordinator: never give medical advice, dosages, diagnoses or success-rate promises. Describe conditions and options in general terms and tell readers to decide with their doctors. The page template already adds a medical disclaimer at the end.
- End with one short paragraph on how Eagle Go can help (hospital search, preparing medical documents, coordination).
- Never put patient data, client documents, passwords or contracts in this repository. It is public.

## Patient testimonials

- Patients submit through the testimonial Google Form. Responses land in Google Sheet `1FYqnal6XR3bJIhjj3CWfUMh9HWCy9fAyizBeui80wz8`, tab `Form Responses 1` (columns: Timestamp, Nama, Kota Asal, Rumah Sakit dan Negara, Ceritakan pengalaman, Nomor WhatsApp).
- To publish one, add an entry to `TESTIMONIALS` in `tools/build.py` and rebuild. Only add a testimonial after the owner confirms it came from the patient and that they agreed to publication. Tidy spelling lightly; never change what the patient said.
- Never publish the WhatsApp number column.
