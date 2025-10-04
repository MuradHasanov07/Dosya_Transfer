📁 Dosya Transfer Uygulaması (C# | TCP/UDP | Socket Programming)

Bu proje, C# dili ve .NET Framework kullanılarak geliştirilmiş bir ağ tabanlı dosya transfer sistemidir.
İstemci–sunucu mimarisiyle çalışan uygulama, TCP ve UDP protokolleri üzerinden güvenli ve hızlı veri aktarımı sağlar.

✨ Özellikler

📤 Dosya gönderme ve alma (her boyutta dosya desteği)

🔄 TCP/UDP protokol seçimi

📡 Çoklu istemci bağlantı desteği

🧱 Dosya bütünlüğü kontrolü (checksum)

🚫 Bağlantı kesilse bile yeniden gönderim desteği

🔒 Güvenli bağlantı yönetimi

💬 Gerçek zamanlı aktarım durumu ve log kaydı

🧠 Mimarisi

Uygulama client–server yapısında geliştirilmiştir:

Client  →  TCP/UDP Socket  →  Server


Server: Dosya alımlarını yönetir, bağlantıları dinler, gelen verileri kaydeder.

Client: Dosya seçer, sunucuya bağlanır ve aktarımı başlatır.

Her iki taraf da socket tabanlı veri akışı yönetimini gerçekleştirir.

🚀 Kurulum

Depoyu klonlayın:

git clone https://github.com/kullanici-adi/dosya-transfer.git
cd dosya-transfer


Visual Studio'da projeyi açın

Server uygulamasını başlatın

Client uygulamasını çalıştırın

IP adresi ve portu girerek bağlantıyı başlatın

🛠️ Kullanılan Teknolojiler

C# (.NET Framework / .NET Core)

TCP ve UDP Sockets

Multithreading (BackgroundWorker / Task)

Windows Forms (UI)

Exception Handling ve Event-Driven Architecture

🧩 Örnek Kullanım

Server.exe başlatıldığında, belirlenen portu dinlemeye başlar

Client.exe dosya seçtikten sonra “Gönder” butonuna tıklar

Aktarım ilerlemesi yüzde olarak görüntülenir

📂 Proje Yapısı
src/
├── Server/
│   ├── Program.cs
│   ├── ServerForm.cs
│   └── ServerSocket.cs
├── Client/
│   ├── Program.cs
│   ├── ClientForm.cs
│   └── FileSender.cs
└── Shared/
    └── PacketUtils.cs

🧪 Geliştirme Odakları

Socket bağlantı stabilitesi

Hata yönetimi ve bağlantı geri kazanımı

UI thread güvenliği (Invoke / async-await)
