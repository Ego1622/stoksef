from supabase import create_client, Client

url = "https://ncyczupghtvnobnpqxrt.supabase.co"
key = "sb_publishable_bhKixUuCynD8TeXZfvcwBQ_SXRCIkdB"
supabase = create_client(url, key)

# Veritabanındaki tüm ürünleri çekelim
response = supabase.table("product").select("*").execute()
urunler = response.data

print(f"Veritabanında toplam {len(urunler)} ürün var.\n--- EN UCUZ ÜRÜNLER LİSTESİ ---")

# Her kategori için en ucuz ürünü bulan akıllı mantık
kategoriler = {}
for urun in urunler:
    kat = urun["category"]
    fiyat = urun["price"]
    
    if kat not in kategoriler:
        kategoriler[kat] = []
    kategoriler[kat].append(urun)

# Her kategorideki en ekonomik seçeneği yazdıralım
toplam_maliyet = 0
for kat, liste in kategoriler.items():
    # Fiyata göre sırala
    en_ucuz = min(liste, key=lambda x: x["price"])
    toplam_maliyet += en_ucuz["price"]
    print(f"[{kat}] -> {en_ucuz['product_name']} ({en_ucuz['market_name']}): {en_ucuz['price']} TL")

print(f"\nAkıllı Sepet Toplam Maliyeti: {toplam_maliyet:.2f} TL")