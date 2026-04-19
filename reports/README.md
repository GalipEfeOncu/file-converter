# 📋 reports/

Bu klasör, AI agent'ların ve insan ekip üyelerinin çalışma raporlarını barındırır.
**Hiçbir uygulama kodu burada bulunmaz.**

## 📁 Klasör Yapısı

```
reports/
├── README.md                  # Bu dosya
├── agent-runs/                # Her agent çalıştırması için bir rapor
│   └── issue-<N>-<üye>-<YYYY-MM-DD>.md
└── weekly/                    # (Opsiyonel) ekip üyelerinin haftalık raporları
    └── <üye>-<YYYY-WW>.md
```

## 🤖 agent-runs/ Konvansiyonu

Her agent, bir issue üzerinde çalışmaya başlamadan **önce** rapor dosyasını oluşturur
ve görev ilerledikçe doldurur.

### Dosya Adı Şablonu

```
issue-<ISSUE_NUMARASI>-<ÜYE_KISA_AD>-<YYYY-MM-DD>.md
```

**Üye kısa adları:**

| Üye | Kısa Ad |
|:---|:---|
| Galip Efe Öncü | `galip` |
| Said Hamza Turan | `said` |
| Abdulkadir Sar | `abdulkadir` |
| Samet Demir | `samet` |
| Muhammed Ali Avcı | `ali` |

**Örnek:** `agent-runs/issue-12-said-2026-04-20.md`

### Rapor İçerik Şablonu

Agent prompt'unda belirtilen 8 bölüm zorunludur:

1. Anladığım Görev
2. Plan (Kabul Kriterlerine Karşılık)
3. Değiştirilen / Eklenen Dosyalar
4. Atlanan / Yapılamayan Maddeler
5. Test Sonuçları
6. Dökümantasyonda Fark Ettiğim Sorunlar
7. Önerilen Commit Mesajı
8. Koordinasyon / Delegasyon Notları

> Tam şablon için Scrum Master tarafından sağlanan agent görev prompt'una bakın.

## 🔒 Kurallar

- Raporlar **append-only**'dir; geçmişe dönük raporlar düzenlenmez (yazım hatası
  hariç). Yeni bilgi varsa yeni rapor oluşturulur.
- Hassas bilgi (API key, kullanıcı verisi vb.) **asla** rapora yazılmaz.
- Raporlar `git`'e commit edilir; Scrum Master'ın retrospektif analizi için kalıcı
  kayıttır.
- Agent'lar `git commit` / `git push` çalıştırmaz; sadece raporun 7. bölümünde
  commit mesajı **önerir**. Commit'i Scrum Master atar.

## 📊 İndeks (Manuel Güncelleme)

Yeni rapor eklendikçe aşağıdaki tabloyu Scrum Master günceller.

| Tarih | Issue | Üye | Sprint | Durum | Rapor |
|:---|:---|:---|:---|:---|:---|
| _Henüz rapor yok_ | | | | | |
