import { useState } from 'react'

type Field = 'ad' | 'eposta' | 'tc' | 'sinif'
type Values = Record<Field, string>

const TC_RE = /^\d{11}$/
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const EMPTY: Values = { ad: '', eposta: '', tc: '', sinif: '' }

// Her alan için kalıcı, Türkçe, "ne yanlış + nasıl düzelir" söyleyen mesaj.
function validate(v: Values): Partial<Record<Field, string>> {
  const e: Partial<Record<Field, string>> = {}
  if (!v.ad.trim()) e.ad = 'Öğrencinin adı soyadı gerekli.'
  if (!v.eposta.trim()) e.eposta = 'Veli e-postası gerekli — onay bu adrese gidecek.'
  else if (!EMAIL_RE.test(v.eposta)) e.eposta = 'E-posta biçimi geçersiz (örn. ayse@ornek.com).'
  if (!v.tc) e.tc = 'TC Kimlik No gerekli.'
  else if (!TC_RE.test(v.tc)) e.tc = 'TC Kimlik No 11 rakamdan oluşmalıdır (örn. 12345678901).'
  if (!v.sinif) e.sinif = 'Sınıf seçin.'
  return e
}

export default function FixedForm() {
  const [values, setValues] = useState<Values>(EMPTY)
  const [touched, setTouched] = useState<Partial<Record<Field, boolean>>>({})
  const [submitted, setSubmitted] = useState(false)
  const [status, setStatus] = useState('')

  const errors = validate(values)
  const dirty = Object.values(values).some(Boolean)
  // Hata yalnız alan terk edildikten ya da gönderim denendikten sonra görünür; yazarken kesmez.
  const shown = (f: Field) => (touched[f] || submitted) ? errors[f] : undefined

  const set = (f: Field) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setValues(v => ({ ...v, [f]: e.target.value }))
  const blur = (f: Field) => () => setTouched(t => ({ ...t, [f]: true }))

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setSubmitted(true)
    const first = (Object.keys(errors) as Field[])[0]
    if (first) {
      setStatus('Kayıt yapılamadı: aşağıda işaretli alanları düzeltin.')
      document.getElementById(first)?.focus()
      return
    }
    setStatus('Kayıt alındı. Onay e-postası gönderildi.')
  }

  function onReset(e: React.FormEvent<HTMLFormElement>) {
    if (!confirm('Formdaki tüm bilgiler silinecek. Devam edilsin mi?')) { e.preventDefault(); return }
    setValues(EMPTY); setTouched({}); setSubmitted(false)
    setStatus('Form temizlendi.')
  }

  function onCancel(e: React.MouseEvent<HTMLAnchorElement>) {
    if (dirty && !confirm('Girdiğiniz bilgiler kaybolacak. Çıkılsın mı?')) e.preventDefault()
  }

  // Ortak alan sarmalayıcı: label + kontrol + ipucu/hata (aria-describedby ile bağlı)
  function field(f: Field, label: string, control: (a: Record<string, unknown>) => React.ReactNode, hint?: string) {
    const err = shown(f)
    const descId = err ? `${f}-err` : hint ? `${f}-hint` : undefined
    return (
      <>
        <label htmlFor={f}>{label} *</label>
        {control({ id: f, name: f, value: values[f], onChange: set(f), onBlur: blur(f), required: true,
                   'aria-required': true, 'aria-invalid': !!err, 'aria-describedby': descId })}
        {!err && hint && <p id={`${f}-hint`} className="hint">{hint}</p>}
        {err && <p id={`${f}-err`} className="error"><span aria-hidden="true">⚠ </span>{err}</p>}
      </>
    )
  }

  return (
    <main className="fixed">
      <h1>Öğrenci Kayıt</h1>

      <img src="https://picsum.photos/seed/okul/320/120" width={320} height={120} alt="" />

      <p style={{ color: '#4a4a4a', background: '#fff' }}>
        Lütfen tüm alanları doldurun. Yıldızla (*) işaretli alanlar zorunludur.
      </p>

      <form noValidate onSubmit={onSubmit} onReset={onReset}>
        {field('ad', 'Öğrencinin adı soyadı', a => <input type="text" autoComplete="off" {...a} />)}
        {field('eposta', 'Veli e-postası', a => <input type="email" autoComplete="email" spellCheck={false} {...a} />)}
        {field('tc', 'Öğrencinin TC Kimlik No', a => <input inputMode="numeric" maxLength={11} {...a} />, '11 rakam, boşluksuz.')}
        {field('sinif', 'Sınıf', a => (
          <select {...a}>
            <option value="" disabled>Sınıf seçin</option>
            <option>5. Sınıf</option>
            <option>6. Sınıf</option>
          </select>
        ))}

        <div className="actions">
          <button type="submit">Kaydet</button>
          <button type="reset">🗑 Formu temizle</button>
          <a href="/" className="cancel" onClick={onCancel}>İptal</a>
        </div>
        <p role="status" aria-live="polite" className="status">{status}</p>
      </form>

      <p><span className="badge">Yeni</span> Sınıf listesi 2026-27 dönemine güncellendi. <a href="#detay">Kayıt koşullarını görüntüle</a></p>

      <table>
        <caption>Son sınav notları</caption>
        <thead><tr><th scope="col">Ders</th><th scope="col">Not</th></tr></thead>
        <tbody>
          <tr><th scope="row">Matematik</th><td>85</td></tr>
          <tr><th scope="row">Türkçe</th><td>92</td></tr>
        </tbody>
      </table>

      <section id="detay">
        <h2>Kayıt koşulları</h2>
        <p>Kayıt, veli onayı ve okul yönetiminin kontenjan kontrolü sonrasında kesinleşir.</p>
      </section>
    </main>
  )
}
