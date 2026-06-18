# WhisperColab

用于Whisper转录的多语言Google Colab笔记本。

## 特点

- **免费使用:** 该笔记本使用[openai/whisper](https://github.com/openai/whisper)（OpenAI于2023年1月17日开源），以及Google Colab的免费GPU运行时。
- **没有固定的笔记本端文件大小限制:** 可以处理大型音频和视频文件。
- **批量处理:** 一次运行可以处理多个音频和视频文件。
- **Google Drive支持:** 可以直接上传文件，也可以处理Google Drive中存储的音视频文件。
- **全面上线:** 下载和处理在Google Colab上执行。不使用本地计算资源。
- **多种输出格式:** 笔记本输出原始JSON转录本和派生的TXT、CSV、Markdown、Excel和SRT字幕文件。

## 语言

| 语言 | README | 笔记本 |
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

## 存储库布局

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

根README是英文入口点，docs/README包含生成的本地化README文件。模板笔记本是源笔记本，包含占位符，例如 `{{cell1.title}}`。区域设置文件提供特定于语言的 README和面向 Colab 的副本。生成的笔记本已提交，因此 Colab 链接保持稳定。

## 构建

```bash
python scripts/sync_locales.py
python scripts/build_readmes.py
python scripts/build_notebooks.py
```

## 支票

```bash
python scripts/check_notebooks.py
```

CI 工作流程从模板和区域设置文件重建 README文件和笔记本，检查笔记本 JSON，验证空输出，检查代码单元中的 Python 语法，扫描明显的意外秘密，并在未提交生成的文件时失败。

## CI 可以测试什么

- README从语言环境文件生成
- 从模板和区域设置文件生成笔记本
- 笔记本JSON有效期
- 空执行输出
- 代码单元中的 Python 语法
- 明显的意外秘密
- 提交生成的 README和与源匹配的笔记本文件

完整的转录路径需要 Colab 特定的 API、模型下载、GPU可用性以及用户提供的媒体文件。生成文件检查通过后，将该路径视为手动 Colab 冒烟测试。

## 许可证

此存储库的 README生成器、笔记本模板、区域设置文件、生成的笔记本和维护脚本是根据 MIT许可证发布的。 Whisper模型和第三方依赖项受其各自的许可证管辖。
