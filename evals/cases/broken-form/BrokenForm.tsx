export default function BrokenForm() {
  return (
    <div className="broken">
      <div style={{ fontSize: 28, fontWeight: 700 }}>Öğrenci Kayıt</div>
      <img src="https://picsum.photos/seed/okul/320/120" width={320} height={120} />
      <p style={{ color: '#9a9a9a', background: '#fff' }}>
        Lütfen tüm alanları doldurun. Zorunlu alanlar kırmızı ile işaretlidir.
      </p>
      <input type="text" placeholder="Ad Soyad" />
      <input type="email" placeholder="E-posta" />
      <input type="text" placeholder="TC Kimlik No" style={{ border: '2px solid red' }} />
      <select style={{ outline: 'none' }} defaultValue="">
        <option value="" disabled>Sınıf seçin</option>
        <option>5. Sınıf</option>
        <option>6. Sınıf</option>
      </select>
      <div className="fake-btn" onClick={() => {}}>Kaydet</div>
      <button className="icon-only" onClick={() => document.querySelectorAll<HTMLInputElement>('.broken input').forEach(i => (i.value = ''))}>🗑</button>
      <a href="#sil" style={{ display: 'inline-block', width: 16, height: 16, fontSize: 10, lineHeight: '16px' }}>x</a>
      <div className="pulse" aria-hidden="false">Yeni!</div>
      <table>
        <tbody>
          <tr><td>Matematik</td><td>85</td></tr>
          <tr><td>Türkçe</td><td>92</td></tr>
        </tbody>
      </table>
      <a href="#detay">buraya tıklayın</a>
    </div>
  )
}
