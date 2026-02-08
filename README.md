# 📁 Dosya Transfer (Flask + PeerJS)

Bu uygulama, tarayıcılar arası P2P (Eşten Eşe) dosya transferi yapan, kullanıcı yönetimi ve oturum yapısı içeren modern bir Flask uygulamasıdır. Gönderici ve alıcı arasında doğrudan WebRTC bağlantısı kurarak veriyi sunucuya yüklemeden aktarır.

🚀 Canlı Demo
Uygulamaya şu bağlantı üzerinden ulaşabilirsiniz:
👉 https://dosya-transfer.onrender.com

## Özellikler

- Kullanıcı kayıt / giriş / çıkış akışı
- Her kullanıcı için benzersiz **Connection ID** ile eşleşme
- PeerJS üzerinden tarayıcılar arasında dosya gönderimi
- Aktarım sırasında ilerleme çubuğu
- Alınan dosyaları listede gösterme ve indirme
- Flask + SQLAlchemy ile kullanıcı ve dosya kayıtlarının saklanması
- Render (gunicorn) uyumlu dağıtım konfigürasyonu

## Teknoloji Yığını

- **Backend:** Flask, Flask-SQLAlchemy
- **Veritabanı:** MySQL (PyMySQL)
- **Frontend:** HTML, Bootstrap 5, Vanilla JavaScript
- **Gerçek zamanlı iletişim:** PeerJS (WebRTC)
- **Deploy:** gunicorn + Render (`render.yaml`)

## Proje Yapısı

```text
.
├── app.py                # Uygulama oluşturma, route'lar, oturum yönetimi
├── models.py             # User ve File modelleri
├── extensions.py         # SQLAlchemy nesnesi
├── config.py             # Ortam bazlı yapılandırmalar
├── wsgi.py               # WSGI giriş noktası
├── render.yaml           # Render deploy ayarları
├── requirements.txt      # Python bağımlılıkları
└── templates/
    ├── login.html
    ├── register.html
    └── transfer.html
```

## Kurulum (Lokal)

> Aşağıdaki adımlar Linux/macOS için örneklenmiştir. Windows'ta sanal ortam aktivasyonu farklılık gösterebilir.

1. Depoyu klonlayın:

```bash
git clone <repo-url>
cd Dosya_Transfer
```

2. Sanal ortam oluşturun ve aktif edin:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Bağımlılıkları kurun:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Ortam değişkenlerini tanımlayın:

```bash
export FLASK_ENV=development
export SECRET_KEY='guclu-bir-gizli-anahtar'
export DB_PASSWORD='mysql-sifreniz'
export UPLOAD_FOLDER='./uploads'
```

5. Uygulamayı başlatın:

```bash
python app.py
```

Varsayılan olarak uygulama `http://127.0.0.1:5000` adresinde çalışır.

## Ortam Değişkenleri

| Değişken | Açıklama |
|---|---|
| `SECRET_KEY` | Flask session ve güvenlik anahtarı |
| `DB_PASSWORD` | MySQL bağlantısı için parola |
| `UPLOAD_FOLDER` | Yüklenen dosyaların diskte tutulacağı klasör |
| `FLASK_ENV` | `development` veya `production` |

## Kullanım Akışı

1. Kullanıcı kayıt olur ve giriş yapar.
2. Transfer sayfasında kendi **Connection ID** değerini görür.
3. Gönderen kullanıcı alıcının Connection ID bilgisini girer ve dosyayı seçer.
4. Dosya WebRTC üzerinden parçalara bölünerek aktarılır.
5. Alıcı tarafta dosya listede görünür ve indirilebilir.
