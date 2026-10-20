import requests
from supabase import create_client

# Supabase Bağlantısı
url = "https://ncyczupghtvnobnpqxrt.supabase.co"
key = "sb_publishable_bhKixUuCynD8TeXZfvcwBQ_SXRCIkdB"
supabase = create_client(url, key)

def zengin_urunleri_yukle():
    zengin_urun_listesi = [
        # --- ET VE PROTEİN ---
        {"product_name": "Banvit Tavuk Göğsü 1000g", "market_name": "Migros", "price": 139.90, "category": "Et/Protein"},
        {"product_name": "Şenpiliç Fileto 500g", "market_name": "Şok", "price": 74.50, "category": "Et/Protein"},
        {"product_name": "Erpiliç But Pirzola 750g", "market_name": "A101", "price": 110.00, "category": "Et/Protein"},
        {"product_name": "Dana Kıymalık Et 400g", "market_name": "Migros", "price": 199.90, "category": "Et/Protein"},
        {"product_name": "SuperFresh Ton Balığı 2x160g", "market_name": "CarrefourSA", "price": 129.90, "category": "Et/Protein"},
        
        # --- SÜT VE SÜT ÜRÜNLERİ ---
        {"product_name": "İçim Günlük Süt 1 L", "market_name": "Migros", "price": 34.90, "category": "Süt Ürünleri"},
        {"product_name": "Birşah Tam Yağlı Süt 1 L", "market_name": "A101", "price": 31.50, "category": "Süt Ürünleri"},
        {"product_name": "Mis Yarım Yağlı Yoğurt 2 Kg", "market_name": "Şok", "price": 59.90, "category": "Süt Ürünleri"},
        {"product_name": "Sütaş Tam Yağlı Yoğurt 2 Kg", "market_name": "Migros", "price": 64.50, "category": "Süt Ürünleri"},
        {"product_name": "İçim Kaşar Peyniri 700g", "market_name": "File", "price": 195.00, "category": "Süt Ürünleri"},
        
        # --- KAHVALTILIK ---
        {"product_name": "Torku Banada Kakao Fındık Kreması 400g", "market_name": "Migros", "price": 74.50, "category": "Kahvaltılık"},
        {"product_name": "Pınar Labne 400g", "market_name": "Şok", "price": 89.00, "category": "Kahvaltılık"},
        {"product_name": "Kızılay Yumurta 30'lu M Boy", "market_name": "A101", "price": 119.00, "category": "Kahvaltılık"},
        {"product_name": "Birlik Siyah Zeytin 1 Kg", "market_name": "Bim", "price": 95.00, "category": "Kahvaltılık"},
        
        # --- BAKLİYAT VE TEMEL GIDA ---
        {"product_name": "Efsane Osmancık Pirinç 2.5 Kg", "market_name": "A101", "price": 115.00, "category": "Bakliyat"},
        {"product_name": "Yayla Kırmızı Mercimek 1 Kg", "market_name": "Migros", "price": 48.90, "category": "Bakliyat"},
        {"product_name": "Barilla Burgu Makarna 500g", "market_name": "CarrefourSA", "price": 24.90, "category": "Temel Gıda"},
        {"product_name": "Ankara Makarna 500g", "market_name": "Şok", "price": 19.50, "category": "Temel Gıda"},
        {"product_name": "Torku Toz Şeker 3 Kg", "market_name": "Migros", "price": 115.00, "category": "Temel Gıda"},
        
        # --- MEYVE VE SEBZE ---
        {"product_name": "Patates 1 Kg", "market_name": "Migros", "price": 22.90, "category": "Meyve/Sebze"},
        {"product_name": "Soğan 1 Kg", "market_name": "Şok", "price": 19.90, "category": "Meyve/Sebze"},
        {"product_name": "Domates Salkim 1 Kg", "market_name": "File", "price": 45.00, "category": "Meyve/Sebze"},
        {"product_name": "Bavaria Muz 1 Kg", "market_name": "Migros", "price": 69.90, "category": "Meyve/Sebze"}
    ]

    print("🔄 Zenginleştirilmiş gerçek market ürünleri Supabase'e aktarılıyor...")
    
    for urun in zengin_urun_listesi:
        response = supabase.table("product").insert(urun).execute()
        print(f"✅ Eklendi: {urun['product_name']} ({urun['market_name']} - {urun['price']} TL)")

    print("🎉 Tüm genişletilmiş market ürünleri veritabanına başarıyla yüklendi!")

if __name__ == "__main__":
    zengin_urunleri_yukle()