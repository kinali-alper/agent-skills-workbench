#!/usr/bin/env python3
"""iteration-4 ön-tarama: report.md içinde F1–F19'un anahtar sözcük izlerini arar. Yalnız ÖN tarama; her kaçırma ve zor satırlar elle doğrulanır.
Kullanım: python prescan.py <report.md> [--json]   → satır adları ve toplam"""
import re,sys,json,pathlib
F={
 'F1 h1 yok':r'\bh1\b|başlık.{0,30}div|div.{0,30}başlık|heading',
 'F2 alt yok':r'\balt\b',
 'F3 kontrast':r'kontrast|contrast|9a9a9a',
 'F4 placeholder-etiket':r'placeholder.{0,60}(etiket|label)|(etiket|label).{0,60}placeholder|label.{0,40}yok|etiket.{0,40}yok|htmlfor|<label',
 'F5 renk-tek-sinyal':r'yalnız(ca)? renk|sadece renk|renk(le)? (tek|yalnız)|color.only|tek sinyal|kırmızı kenarlık',
 'F6 outline none':r'outline',
 'F7 select etiketsiz':r'select.{0,80}(etiket|label)|(etiket|label).{0,80}select|sınıf seçin',
 'F8 div buton':r'div.{0,40}(onclick|buton|button)|(onclick|buton|button).{0,40}div|fake-btn|native',
 'F9 emoji buton adsız':r'🗑|emoji|icon-only|aria-label|erişilebilir ad',
 'F10 16px hedef':r'16\s*[×x]\s*16|16 ?px|24\s*[×x]\s*24|hedef boyut|target size|2\.5\.8',
 'F11 reduced-motion':r'reduced.motion|pulse|animasyon',
 'F12 tablo th/caption':r'caption|<th|\bth\b|scope=|tablo başlı|th scope',
 'F13 buraya tıklayın':r'buraya tıklayın',
 'F14 U1 kaydet sessiz':r'geri bildirim|durum mesaj|role="?status|hiçbir şey olm|sonuç üret|başarı mesaj|onay mesaj|işleyici boş|\(\) => \{\}|boş (işleyici|handler)',
 'F15 U2 iptal yok':r'iptal|geri (yolu|bağlant|düğme|butonu)|çıkış yolu|vazgeç|cancel',
 'F16 U3 TC ipucu':r'inputmode|11 (hane|rakam)|pattern|tc kimlik.{0,100}(ipucu|format|rakam|hane|maxlength)',
 'F17 U4 zorunlu/hata tutarsız':r'zorunlu.{0,140}(kırmızı|tutars|çeliş|hata|karış)|(tutars|çeliş).{0,140}zorunlu|\*.{0,40}zorunlu|required.{0,60}(marker|işaret)',
 'F18 U5 onaysız silme':r'onay(sız| sor| iste| olmadan| almadan)|confirm|geri al(ma|ınamaz)|undo',
 'F19 U6 yeni bağlamsız':r'yeni!?.{0,120}(bağlam|ne(yin)? yeni|belirsiz|anlamsız|neye|ilgisiz|hiçbir|referans)|(bağlam|belirsiz).{0,80}yeni',
}
def scan(path):
    t=pathlib.Path(path).read_text(encoding='utf-8',errors='replace').lower()
    hits={k:bool(re.search(v,t,re.S)) for k,v in F.items()}
    verdict_block=bool(re.search(r'kontrol listesi hükümleri|hüküm',t))
    n_verdict=len(re.findall(r'\b(a1[0-3]|a[1-9]|u[1-8])\b\s*(ihlal|uygun|uygulanamaz|doğrulanamaz)',t))
    return hits,verdict_block,n_verdict,len(t.splitlines())
if __name__=='__main__':
    h,vb,nv,lines=scan(sys.argv[1]); n=sum(h.values())
    if '--json' in sys.argv: print(json.dumps({'prescan_found':n,'missed':[k for k,v in h.items() if not v],'verdict_block':vb,'verdicts_counted':nv,'lines':lines},ensure_ascii=False)); sys.exit()
    print(f"{n}/19 ön-tarama · hüküm bloğu: {vb} · sayılan hüküm: {nv} · {lines} satır"); print("kaçırılan:",[k for k,v in h.items() if not v] or '—')
