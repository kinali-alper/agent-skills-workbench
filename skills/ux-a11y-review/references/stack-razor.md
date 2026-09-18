# ASP.NET Core Razor (.cshtml) reçeteleri

Adım 1'de dosya .cshtml ise okunur. Kurallar SKILL.md'de; burada yalnız Razor'a özgü düzeltme biçimleri.

| Kontrol | Razor'da düzeltme |
|---|---|
| A4 etiket | `<label asp-for="AdSoyad"></label>` — `asp-for` id/name üretir ama **label üretmez**; label helper ayrı yazılır |
| A5 hata metni | `<span asp-validation-for="TcKimlikNo" class="text-danger" role="alert"></span>`; `is-invalid` sınıfı tek başına yalnız renktir |
| A5 özet | `<div asp-validation-summary="ModelOnly" role="alert"></div>` formun üstünde |
| U1 durum | POST sonrası `TempData["Durum"]` → layout'ta `<p role="status">@TempData["Durum"]</p>`; ya da `RedirectToAction` ile onay sayfası |
| U2 iptal | `<a asp-action="Index" class="btn btn-link">İptal</a>` |
| U3 biçim | ViewModel'de `[RegularExpression(@"^\d{11}$", ErrorMessage = "…11 rakam…")]`; input'ta `inputmode="numeric"` |
| U5 onay | Erişilebilir `<dialog>`; en azından `type="reset"` + `confirm` |
| A7 native | `<button type="submit" class="btn btn-primary">Kaydet</button>` — `div onclick="$('form').submit()"` yerine |
| A11 tablo | `<table class="table"><caption>…</caption><thead><tr><th scope="col">` — `@foreach` yalnız `<tbody>` içinde |
| A1 landmark | `_Layout.cshtml` içinde `<main>@RenderBody()</main>` — sayfada tekrar `main` açma |
| A12 dil | `_Layout.cshtml`: `<html lang="tr">` |
