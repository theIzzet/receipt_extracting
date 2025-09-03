PROMPT_TEMPLATE = """
Aşağıda bir alışveriş fişi görüntüsü verilmiştir. Fişlerde tipik ürün formatları şu şekildedir:
Jeli Port 114G       %01      *12,50
NSCF 3ü1 FINDIKLI 17       %01          *9,75
DOOY ANANAS       %10        *41,00 
ALIŞVERİŞ POŞETİ    %20     *0,50  
TEMEL GIDA MADDESİ       %01      *20,00
TAVUK    %1    327,00

Genel anlamda ürün formatı bu şekilde. Burada '%' işaretli kısımlar ürünün KDV oranıdır. 
Easyocr harf hataları yapabilir. Fişte Tarih yazıyor ama OCR Trih okuyabilir. Veya fişte A101 yazıyor ama sen bunu at01 gibi yanlış okuyor olabilirsin bunları düzelt.

Genel anlamda istisnalar hariş mağaza isimleri fişin en üstünden ürünlere kadar olan kısımdaki yazılarda yazar. Şok marketlER , A101 , Migros , 5M Migros, Bim Shell, Opet, Petrol Ofisi 
Görüntüdeki fişten aşağıdaki bilgileri çıkar:

Fiş tipi mağaza adı ve ürünlere göre belirlenmelidir:
- Market, yiyecek, içecek, temel gıda, poşet → "gida"
- Benzin, petrol, akaryakıt → "petrol"
- Giyim, kıyafet, LC Waikiki, Defacto vb. → "kiyafet"
- Elektronik, Teknosa, MediaMarkt vb. → "elektronik"
- Diğer durumlarda → "diger"

Görüntüdeki fişten aşağıdaki bilgileri çıkar:

- Tarih (fişteki tarih bilgisi). Fişte Tarih veya TARİH gibi yazılar yüksek oranda tarih bilgisini gösterir. Eğer Tarih ifadesi geçmiyorsa yazım formatina bakabilirsin. Örnek Tarih formatları genelde şu şekildedir: 13/05/2025 , 13.08.2025, 13-08-2025 formatlarında olabilir.
- Saat (fişteki saat bilgisi).
- Mağaza adı (Cafe, market, ticaret a.ş., pastane, Petrol gibi ifadelere dikkat edin). Mağaza adı bulurken genelde limited şirketleri, Aş., Ticaret A.Ş. ve buna bunzer şeyler olabilir.Genel anlamda istisnalar hariş mağaza isimleri fişin en üstünden ürünlere kadar olan kısımdaki yazılarda yazar. Bunlara dikkat et.
- Ürünler ve fiyatları (liste olarak: ürün adı - fiyat)
- Toplam KDV  Toplam kdv bilgisi fişte TopKDV , Toplamkdv, Toplam KDV, TOPKDV gibi kısımlarda tutulur. genelde bu şekildedir.
- Toplam tutar.Toplam bilgisi genelde Fişte Toplam tutar, Toplam, Alışveriş Tutarı gibi ifadelerde bulunur
- Fiş tipi (gida, petrol, kiyafet, elektronik, diger)

Lütfen görüntüyü dikkatlice inceleyip aşağıdaki JSON formatında yanıt verin:

{{
  "tarih": "...",
  "saat": "...",
  "magaza": "...",
  "urunler": [
    {{"ad": "...", "fiyat": "..."}}
  ],
  "toplam_kdv": "...",
  "toplam": "...",
  "fis_tipi": "..."
}}
"""