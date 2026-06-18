# Whisperকোলাব

Whisperট্ৰান্সক্ৰিপচনৰ বাবে বহুভাষিক Google Colabবহী।

## বৈশিষ্ট্যসমূহ

- **ব্যৱহাৰ কৰিবলৈ বিনামূলীয়া:** এই বহীখনে [openai/whisper](https://github.com/openai/whisper)ব্যৱহাৰ কৰে, যিটো OpenAIএ ১৭ জানুৱাৰী, ২০২৩ তাৰিখে মুক্ত-উৎস লাভ কৰিছিল, Google Colabৰ বিনামূলীয়া GPUৰানটাইমৰ সৈতে একেলগে।
- **কোনো নিৰ্দিষ্ট বহী-পক্ষৰ নথিপত্ৰৰ আকাৰ সীমা নাই:** ডাঙৰ ডাঙৰ অডিঅ’ আৰু ভিডিঅ’ ফাইল প্ৰচেছ কৰিব পাৰি।
- **বেচ প্ৰচেছিং:** এটা ৰানত একাধিক অডিঅ' আৰু ভিডিঅ' ফাইল প্ৰচেছ কৰিব পাৰি।
- **Google Driveসমৰ্থন:** ফাইলসমূহ পোনপটীয়াকৈ আপলোড কৰিব পাৰি, বা Google Driveত সংৰক্ষণ কৰা অডিঅ'/ভিডিঅ' ফাইলসমূহ প্ৰক্ৰিয়া কৰিব পাৰি।
- **সম্পূৰ্ণ অনলাইন:** ডাউনলোড আৰু প্ৰচেছিং Google Colabত কৰা হয়। কোনো স্থানীয় কম্পিউটিং সম্পদ ব্যৱহাৰ কৰা নহয়।
- **একাধিক আউটপুট বিন্যাস:** নোটবুকে মূল JSONট্ৰান্সক্ৰিপ্ট আৰু ডেৰাইভেট TXT, CSV, মাৰ্কডাউন, Excel, আৰু SRTউপশিৰোনামা ফাইলসমূহ আউটপুট কৰে।

## ভাষাসমূহ

| ভাষা | README | বহী |
| --- | --- | --- |
| English | [`README.md`](../../README.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_en.ipynb) |
| 日本語 | [`README.ja.md`](README.ja.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ja.ipynb) |
| 简体中文 | [`README.zh-CN.md`](README.zh-CN.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_zh-CN.ipynb) |
| 繁體中文 | [`README.zh-TW.md`](README.zh-TW.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_zh-TW.ipynb) |
| German | [`README.de.md`](README.de.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_de.ipynb) |
| Spanish | [`README.es.md`](README.es.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_es.ipynb) |
| Russian | [`README.ru.md`](README.ru.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ru.ipynb) |
| Korean | [`README.ko.md`](README.ko.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ko.ipynb) |
| French | [`README.fr.md`](README.fr.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_fr.ipynb) |
| Portuguese | [`README.pt.md`](README.pt.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_pt.ipynb) |
| Turkish | [`README.tr.md`](README.tr.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_tr.ipynb) |
| Polish | [`README.pl.md`](README.pl.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_pl.ipynb) |
| Catalan | [`README.ca.md`](README.ca.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ca.ipynb) |
| Dutch | [`README.nl.md`](README.nl.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_nl.ipynb) |
| Arabic | [`README.ar.md`](README.ar.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ar.ipynb) |
| Swedish | [`README.sv.md`](README.sv.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sv.ipynb) |
| Italian | [`README.it.md`](README.it.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_it.ipynb) |
| Indonesian | [`README.id.md`](README.id.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_id.ipynb) |
| Hindi | [`README.hi.md`](README.hi.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_hi.ipynb) |
| Finnish | [`README.fi.md`](README.fi.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_fi.ipynb) |
| Vietnamese | [`README.vi.md`](README.vi.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_vi.ipynb) |
| Hebrew | [`README.he.md`](README.he.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_he.ipynb) |
| Ukrainian | [`README.uk.md`](README.uk.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_uk.ipynb) |
| Greek | [`README.el.md`](README.el.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_el.ipynb) |
| Malay | [`README.ms.md`](README.ms.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ms.ipynb) |
| Czech | [`README.cs.md`](README.cs.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_cs.ipynb) |
| Romanian | [`README.ro.md`](README.ro.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ro.ipynb) |
| Danish | [`README.da.md`](README.da.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_da.ipynb) |
| Hungarian | [`README.hu.md`](README.hu.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_hu.ipynb) |
| Tamil | [`README.ta.md`](README.ta.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ta.ipynb) |
| Norwegian | [`README.no.md`](README.no.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_no.ipynb) |
| Thai | [`README.th.md`](README.th.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_th.ipynb) |
| Urdu | [`README.ur.md`](README.ur.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ur.ipynb) |
| Croatian | [`README.hr.md`](README.hr.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_hr.ipynb) |
| Bulgarian | [`README.bg.md`](README.bg.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_bg.ipynb) |
| Lithuanian | [`README.lt.md`](README.lt.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_lt.ipynb) |
| Latin | [`README.la.md`](README.la.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_la.ipynb) |
| Maori | [`README.mi.md`](README.mi.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mi.ipynb) |
| Malayalam | [`README.ml.md`](README.ml.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ml.ipynb) |
| Welsh | [`README.cy.md`](README.cy.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_cy.ipynb) |
| Slovak | [`README.sk.md`](README.sk.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sk.ipynb) |
| Telugu | [`README.te.md`](README.te.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_te.ipynb) |
| Persian | [`README.fa.md`](README.fa.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_fa.ipynb) |
| Latvian | [`README.lv.md`](README.lv.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_lv.ipynb) |
| Bengali | [`README.bn.md`](README.bn.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_bn.ipynb) |
| Serbian | [`README.sr.md`](README.sr.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sr.ipynb) |
| Azerbaijani | [`README.az.md`](README.az.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_az.ipynb) |
| Slovenian | [`README.sl.md`](README.sl.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sl.ipynb) |
| Kannada | [`README.kn.md`](README.kn.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_kn.ipynb) |
| Estonian | [`README.et.md`](README.et.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_et.ipynb) |
| Macedonian | [`README.mk.md`](README.mk.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mk.ipynb) |
| Breton | [`README.br.md`](README.br.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_br.ipynb) |
| Basque | [`README.eu.md`](README.eu.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_eu.ipynb) |
| Icelandic | [`README.is.md`](README.is.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_is.ipynb) |
| Armenian | [`README.hy.md`](README.hy.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_hy.ipynb) |
| Nepali | [`README.ne.md`](README.ne.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ne.ipynb) |
| Mongolian | [`README.mn.md`](README.mn.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mn.ipynb) |
| Bosnian | [`README.bs.md`](README.bs.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_bs.ipynb) |
| Kazakh | [`README.kk.md`](README.kk.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_kk.ipynb) |
| Albanian | [`README.sq.md`](README.sq.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sq.ipynb) |
| Swahili | [`README.sw.md`](README.sw.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sw.ipynb) |
| Galician | [`README.gl.md`](README.gl.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_gl.ipynb) |
| Marathi | [`README.mr.md`](README.mr.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mr.ipynb) |
| Punjabi | [`README.pa.md`](README.pa.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_pa.ipynb) |
| Sinhala | [`README.si.md`](README.si.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_si.ipynb) |
| Khmer | [`README.km.md`](README.km.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_km.ipynb) |
| Shona | [`README.sn.md`](README.sn.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sn.ipynb) |
| Yoruba | [`README.yo.md`](README.yo.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_yo.ipynb) |
| Somali | [`README.so.md`](README.so.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_so.ipynb) |
| Afrikaans | [`README.af.md`](README.af.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_af.ipynb) |
| Occitan | [`README.oc.md`](README.oc.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_oc.ipynb) |
| Georgian | [`README.ka.md`](README.ka.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ka.ipynb) |
| Belarusian | [`README.be.md`](README.be.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_be.ipynb) |
| Tajik | [`README.tg.md`](README.tg.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_tg.ipynb) |
| Sindhi | [`README.sd.md`](README.sd.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sd.ipynb) |
| Gujarati | [`README.gu.md`](README.gu.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_gu.ipynb) |
| Amharic | [`README.am.md`](README.am.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_am.ipynb) |
| Yiddish | [`README.yi.md`](README.yi.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_yi.ipynb) |
| Lao | [`README.lo.md`](README.lo.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_lo.ipynb) |
| Uzbek | [`README.uz.md`](README.uz.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_uz.ipynb) |
| Faroese | [`README.fo.md`](README.fo.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_fo.ipynb) |
| Haitian Creole | [`README.ht.md`](README.ht.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ht.ipynb) |
| Pashto | [`README.ps.md`](README.ps.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ps.ipynb) |
| Turkmen | [`README.tk.md`](README.tk.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_tk.ipynb) |
| Nynorsk | [`README.nn.md`](README.nn.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_nn.ipynb) |
| Maltese | [`README.mt.md`](README.mt.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mt.ipynb) |
| Sanskrit | [`README.sa.md`](README.sa.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_sa.ipynb) |
| Luxembourgish | [`README.lb.md`](README.lb.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_lb.ipynb) |
| Myanmar | [`README.my.md`](README.my.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_my.ipynb) |
| Tibetan | [`README.bo.md`](README.bo.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_bo.ipynb) |
| Tagalog | [`README.tl.md`](README.tl.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_tl.ipynb) |
| Malagasy | [`README.mg.md`](README.mg.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_mg.ipynb) |
| Assamese | [`README.as.md`](README.as.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_as.ipynb) |
| Tatar | [`README.tt.md`](README.tt.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_tt.ipynb) |
| Hawaiian | [`README.haw.md`](README.haw.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_haw.ipynb) |
| Lingala | [`README.ln.md`](README.ln.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ln.ipynb) |
| Hausa | [`README.ha.md`](README.ha.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ha.ipynb) |
| Bashkir | [`README.ba.md`](README.ba.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_ba.ipynb) |
| Javanese | [`README.jw.md`](README.jw.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_jw.ipynb) |
| Sundanese | [`README.su.md`](README.su.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_su.ipynb) |
| Cantonese | [`README.yue.md`](README.yue.md) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piccoripico/whisper-colab/blob/main/notebooks/Whisper_Colab_yue.ipynb) |

## ভঁৰালৰ বিন্যাস

```text
.github/
  workflows/
    ci.yml
docs/
  README/
    README.<language-code>.md
locales/
  *.json
notebook_template/
  Whisper_Colab.template.ipynb
notebooks/
  Whisper_Colab_<language-code>.ipynb
scripts/
  build_notebooks.py
  build_readmes.py
  check_notebooks.py
  languages.py
  repair_translated_locales.py
  sync_locales.py
  translate_full_locales.py
.gitattributes
.gitignore
LICENSE
README.md
```

ৰূট READMEহৈছে ইংৰাজী প্ৰৱেশ বিন্দু, আৰু docs/READMEত সৃষ্টি কৰা স্থানীয়কৃত READMEফাইলসমূহ আছে। সাঁচ বহী হৈছে উৎস বহী আৰু ইয়াত `{{cell1.title}}`ৰ দৰে স্থানধাৰী থাকে। স্থানীয় ফাইলসমূহে ভাষা-নিৰ্দিষ্ট READMEআৰু Colab-মুখী কপি প্ৰদান কৰে। সৃষ্টি কৰা বহীসমূহ কমিট কৰা হয় যাতে Colab সংযোগসমূহ সুস্থিৰ থাকে।

## নিৰ্মাণ কৰক

```bash
python scripts/sync_locales.py
python scripts/build_readmes.py
python scripts/build_notebooks.py
```

## চেক কৰে

```bash
python scripts/check_notebooks.py
```

CI কাৰ্য্যপ্ৰবাহে READMEফাইলসমূহ আৰু নোটবুকসমূহ সাঁচ আৰু লোকেল ফাইলসমূহৰ পৰা পুনৰ নিৰ্মাণ কৰে, নোটবুক JSONপৰীক্ষা কৰে, খালী আউটপুটসমূহ পৰীক্ষা কৰে, ক'ড কোষসমূহত পাইথন বাক্যবিন্যাস পৰীক্ষা কৰে, স্পষ্ট আকস্মিক গোপনীয়তাৰ বাবে স্কেন কৰে, আৰু বিফল হয় যেতিয়া সৃষ্টি কৰা ফাইলসমূহ কমিট কৰা নহয়।

## চিআইয়ে কি পৰীক্ষা কৰিব পাৰে

- স্থানীয় ফাইলসমূহৰ পৰা READMEপ্ৰজন্ম
- সাঁচ আৰু লোকেল ফাইলসমূহৰ পৰা বহী সৃষ্টি
- নোটবুক JSONবৈধতা
- খালী এক্সিকিউচন আউটপুটসমূহ
- ক'ড কোষত পাইথন বাক্যবিন্যাস
- স্পষ্ট আকস্মিক গোপনীয়তা
- committed সৃষ্টি কৰা READMEআৰু উৎসসমূহৰ সৈতে মিল থকা নোটবুক ফাইলসমূহ

সম্পূৰ্ণ ট্ৰান্সক্ৰিপচন পথৰ বাবে Colab-নিৰ্দিষ্ট APIসমূহ, মডেল ডাউনলোডসমূহ, GPUউপলব্ধতা, আৰু ব্যৱহাৰকাৰী-প্ৰদান কৰা মাধ্যম ফাইলসমূহৰ প্ৰয়োজন। সৃষ্টি কৰা-ফাইল পৰীক্ষাসমূহ পাছৰ পিছত সেই পথটোক এটা হাতৰ দ্বাৰা কোলাব ধোঁৱা পৰীক্ষা হিচাপে গণ্য কৰক।

## অনুজ্ঞাপত্ৰ

এই ভঁৰালৰ READMEজেনেৰেটৰ, নোটবুক সাঁচ, লোকেল ফাইলসমূহ, সৃষ্টি কৰা নোটবুকসমূহ, আৰু ৰক্ষণাবেক্ষণ স্ক্ৰিপ্টসমূহ MITঅনুজ্ঞাৰ অধীনত মুকলি কৰা হয়। Whisperমডেল আৰু তৃতীয়-পক্ষ নিৰ্ভৰশীলতাসমূহ নিজ নিজ অনুজ্ঞাপত্ৰৰ দ্বাৰা পৰিচালিত হয়।
