# Whisperகோலாப்

Whisperடிரான்ஸ்கிரிப்ஷனுக்கான பன்மொழி Google Colabகுறிப்பேடுகள்.

## அம்சங்கள்

- **பயன்படுத்த இலவசம்:** This notebook uses [openai/whisper](https://github.com/openai/whisper), which OpenAIopen-sourced on January 17, 2023, together with Google Colab's free GPUruntime.
- **நிலையான நோட்புக் பக்க கோப்பு அளவு வரம்பு இல்லை:** பெரிய ஆடியோ மற்றும் வீடியோ கோப்புகளை செயலாக்க முடியும்.
- **தொகுதி செயலாக்கம்:** ஒரே ஓட்டத்தில் பல ஆடியோ மற்றும் வீடியோ கோப்புகளை செயலாக்க முடியும்.
- **Google Drivesupport:** Files can be uploaded directly, or audio/video files stored in Google Drivecan be processed.
- **முழுமையாக ஆன்லைனில்:** Downloads and processing are performed on Google Colab. உள்ளூர் கணினி ஆதாரங்கள் எதுவும் பயன்படுத்தப்படவில்லை.
- **பல வெளியீடு வடிவங்கள்:** The notebook outputs the original JSONtranscript and derived TXT, CSV, Markdown, Excel, and SRTsubtitle files.

## மொழிகள்

| மொழி | README | நோட்புக் |
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

## களஞ்சிய அமைப்பு

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

READMEஎன்பது ஆங்கில நுழைவுப் புள்ளியாகும், மேலும் docs/READMEஎன்பது உள்ளூர்மயமாக்கப்பட்ட READMEகோப்புகளைக் கொண்டுள்ளது. டெம்ப்ளேட் நோட்புக் மூல நோட்புக் மற்றும் `{{cell1.title}}`போன்ற ஒதுக்கிடங்களைக் கொண்டுள்ளது. லோகேல் கோப்புகள் மொழி சார்ந்த READMEமற்றும் கோலாப்-முகம் கொண்ட நகலை வழங்கும். உருவாக்கப்பட்ட குறிப்பேடுகள் உறுதி செய்யப்பட்டுள்ளன, எனவே Colab இணைப்புகள் நிலையானதாக இருக்கும்.

## கட்டுங்கள்

```bash
python scripts/sync_locales.py
python scripts/build_readmes.py
python scripts/build_notebooks.py
```

## காசோலைகள்

```bash
python scripts/check_notebooks.py
```

CI பணிப்பாய்வு டெம்ப்ளேட் மற்றும் லோகேல் கோப்புகளிலிருந்து READMEகோப்புகள் மற்றும் குறிப்பேடுகளை மீண்டும் உருவாக்குகிறது, நோட்புக் JSONஐ சரிபார்க்கிறது, வெற்று வெளியீடுகளை சரிபார்க்கிறது, குறியீடு கலங்களில் பைதான் தொடரியல் சரிபார்க்கிறது, வெளிப்படையான தற்செயலான ரகசியங்களை ஸ்கேன் செய்கிறது மற்றும் உருவாக்கப்படாத கோப்புகள் தோல்வியடையும்.

## CI என்ன சோதனை செய்யலாம்

- உள்ளூர் கோப்புகளிலிருந்து READMEதலைமுறை
- டெம்ப்ளேட் மற்றும் லோகேல் கோப்புகளிலிருந்து நோட்புக் உருவாக்கம்
- நோட்புக் JSONசெல்லுபடியாகும்
- வெற்று செயலாக்க வெளியீடுகள்
- குறியீடு கலங்களில் பைதான் தொடரியல்
- வெளிப்படையான தற்செயலான இரகசியங்கள்
- உருவாக்கப்படும் READMEமற்றும் நோட்புக் கோப்புகள் ஆதாரங்களுடன் பொருந்தும்

முழு டிரான்ஸ்கிரிப்ஷன் பாதைக்கு Colab-சார்ந்த APIகள், மாதிரி பதிவிறக்கங்கள், GPUகிடைக்கும் தன்மை மற்றும் பயனர் வழங்கிய மீடியா கோப்புகள் தேவை. உருவாக்கப்பட்ட கோப்பு சரிபார்ப்புகளுக்குப் பிறகு அந்தப் பாதையை கைமுறையாக Colab புகைப் பரிசோதனையாகக் கருதுங்கள்.

## உரிமம்

இந்தக் களஞ்சியத்தின் READMEஜெனரேட்டர், நோட்புக் டெம்ப்ளேட், லோக்கல் கோப்புகள், உருவாக்கப்பட்ட நோட்புக்குகள் மற்றும் பராமரிப்பு ஸ்கிரிப்டுகள் MITஉரிமத்தின் கீழ் வெளியிடப்படுகின்றன. Whisperமாதிரிகள் மற்றும் மூன்றாம் தரப்பு சார்புகள் அந்தந்த உரிமங்களால் நிர்வகிக்கப்படுகின்றன.
