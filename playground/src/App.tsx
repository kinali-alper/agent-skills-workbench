import BrokenForm from './pages/BrokenForm'
import FixedForm from './pages/FixedForm'

// ?page=broken | ?page=fixed  (varsayılan: broken)
export default function App() {
  const page = new URLSearchParams(location.search).get('page') ?? 'broken'
  return (
    <>
      <nav aria-label="Sayfa seçimi" className="switch">
        <a href="?page=broken" aria-current={page === 'broken' ? 'page' : undefined}>Hatalı</a>
        <a href="?page=fixed" aria-current={page === 'fixed' ? 'page' : undefined}>Düzeltilmiş</a>
      </nav>
      {page === 'fixed' ? <FixedForm /> : <BrokenForm />}
    </>
  )
}
