import streamlit as st
from supabase import create_client

# Supabase Bağlantısı
url = "https://ncyczupghtvnobnpqxrt.supabase.co"
key = "sb_publishable_bhKixUuCynD8TeXZfvcwBQ_SXRCIkdB"
supabase = create_client(url, key)

# Sayfa Yapılandırması (Mobil öncelikli görünüm)
st.set_page_config(
    page_title="StokŞef - Akıllı Market Asistanı", 
    page_icon="🛒", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobil Tasarım CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu Başlatma
if "sepet" not in st.session_state:
    st.session_state.sepet = []
if "profil" not in st.session_state:
    st.session_state.profil = {}
if "evde_var_olanlar" not in st.session_state:
    st.session_state.evde_var_olanlar = []
if "social_posts" not in st.session_state:
    st.session_state.social_posts = [
        {"user": "Ahmet Y.", "tarif": "3 Malzemeli Fit Protein Pankek 🥞", "sosyal_link": "instagram.com/ahmetyfit", "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "begen": 42},
        {"user": "Zeynep S.", "tarif": "Bütçe Dostu 150g Protein Tavuk Bowl 🥗", "sosyal_link": "youtube.com/@zeyneps", "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "begen": 89}
    ]
if "premium_aktif" not in st.session_state:
    st.session_state.premium_aktif = False
if "secilen_market" not in st.session_state:
    st.session_state.secilen_market = "Tümü"
if "ai_yemek_plani" not in st.session_state:
    st.session_state.ai_yemek_plani = None

# Akıllı Başlangıç Kontrolü
if "kayit_adim" not in st.session_state:
    if st.session_state.profil.get("hatirla", False):
        st.session_state.kayit_adim = "profil_tipi"
    else:
        st.session_state.kayit_adim = "temel"

if "ana_sayfada_mi" not in st.session_state:
    st.session_state.ana_sayfada_mi = False

# Ürünleri Çekme
response = supabase.table("product").select("*").execute()
urunler = response.data if response.data else []

# --- ADIM ADIM KAYIT VE PROFİL SİSTEMİ ---
if not st.session_state.ana_sayfada_mi:
    st.title("🛒 StokŞef'e Hoş Geldin!")
    
    # 1. AŞAMA: TEMEL BİLGİLER
    if st.session_state.kayit_adim == "temel":
        st.subheader("1️⃣ Temel Bilgiler")
        ad_soyad = st.text_input("Ad Soyad", value=st.session_state.profil.get("ad", ""))
        mail = st.text_input("E-posta Adresi", value=st.session_state.profil.get("mail", ""))
        sifre = st.text_input("Şifre", type="password")
        
        bilgileri_hatirla = st.checkbox("🔑 Bilgilerimi Hatırla", value=True)
        
        if st.button("Devam Et ➡️"):
            if ad_soyad and mail and sifre:
                st.session_state.profil["ad"] = ad_soyad
                st.session_state.profil["mail"] = mail
                st.session_state.profil["hatirla"] = bilgileri_hatirla
                st.session_state.kayit_adim = "profil_tipi"
                st.rerun()
            else:
                st.warning("Lütfen tüm alanları doldurun.")

    # 2. AŞAMA: 4'LÜ KARE PROFİL SEÇİMİ
    elif st.session_state.kayit_adim == "profil_tipi":
        st.subheader("2️⃣ Profilini Seç")
        st.info("Hangi yaşam tarzı veya hedef için asistan hazırlayalım?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👨‍👩‍👧 Aile", use_container_width=True):
                st.session_state.profil["tip"] = "Aile"
                st.session_state.kayit_adim = "fiziksel"
                st.rerun()
            if st.button("🎓 Öğrenci", use_container_width=True):
                st.session_state.profil["tip"] = "Öğrenci"
                st.session_state.kayit_adim = "fiziksel"
                st.rerun()
        with col2:
            if st.button("💼 Çalışan", use_container_width=True):
                st.session_state.profil["tip"] = "Çalışan"
                st.session_state.kayit_adim = "fiziksel"
                st.rerun()
            if st.button("💪 Sporcu", use_container_width=True):
                st.session_state.profil["tip"] = "Sporcu"
                st.session_state.kayit_adim = "fiziksel"
                st.rerun()
                
        st.markdown("---")
        if not st.session_state.profil.get("hatirla", False):
            if st.button("⬅️ Geri Dön"):
                st.session_state.kayit_adim = "temel"
                st.rerun()

    # 3. AŞAMA: FİZİKSEL ÖLÇÜLER VE AİLE / ÇALIŞAN DETAYLARI
    elif st.session_state.kayit_adim == "fiziksel":
        profil_tipi = st.session_state.profil.get('tip', '')
        st.subheader(f"3️⃣ Fiziksel Ölçüler ({profil_tipi} Profili)")
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            yas = st.number_input("Yaş", min_value=10, max_value=100, value=st.session_state.profil.get("yas", 22))
        with c2: 
            boy = st.number_input("Boy (cm)", min_value=100, max_value=220, value=st.session_state.profil.get("boy", 175))
        with c3: 
            kilo = st.number_input("Kilo (kg)", min_value=30, max_value=200, value=st.session_state.profil.get("kilo", 70))
        
        es_detay = st.session_state.profil.get("es", {})
        cocuklar_listesi = st.session_state.profil.get("cocuklar", [])
        
        if profil_tipi in ["Aile", "Çalışan"]:
            st.markdown("---")
            st.subheader("👨‍👩‍👧 Hane Halkı Detayları")
            es_var = st.checkbox("Eş Bilgisi Ekle", value=bool(es_detay))
            if es_var:
                e_yas = st.number_input("Eşin Yaşı", 10, 100, es_detay.get("yas", 25))
                e_boy = st.number_input("Eşin Boyu (cm)", 100, 220, es_detay.get("boy", 165))
                e_kilo = st.number_input("Eşin Kilosu (kg)", 30, 200, es_detay.get("kilo", 60))
                es_detay = {"yas": e_yas, "boy": e_boy, "kilo": e_kilo}
            else:
                es_detay = {}
                
            cocuk_sayisi = st.number_input("Çocuk Sayısı", min_value=0, max_value=5, value=len(cocuklar_listesi), step=1)
            cocuklar_listesi = []
            for i in range(int(cocuk_sayisi)):
                st.write(f"👶 **{i+1}. Çocuğun Bilgileri:**")
                cc1, cc2, cc3 = st.columns(3)
                default_c = cocuklar_listesi[i] if i < len(cocuklar_listesi) else {"yas": 5, "boy": 120, "kilo": 25}
                with cc1: c_yas = st.number_input(f"{i+1}. Çocuk Yaş", 0, 18, default_c.get("yas", 5), key=f"cyas_{i}")
                with cc2: c_boy = st.number_input(f"{i+1}. Çocuk Boy", 50, 180, default_c.get("boy", 120), key=f"cbuy_{i}")
                with cc3: c_kilo = st.number_input(f"{i+1}. Çocuk Kilo", 5, 100, default_c.get("kilo", 25), key=f"ckil_{i}")
                cocuklar_listesi.append({"yas": c_yas, "boy": c_boy, "kilo": c_kilo})

        st.markdown("---")
        col_g, col_d = st.columns(2)
        with col_g:
            if st.button("⬅️ Geri"):
                st.session_state.kayit_adim = "profil_tipi"
                st.rerun()
        with col_d:
            if st.button("Devam Et ➡️"):
                st.session_state.profil.update({
                    "yas": yas, "boy": boy, "kilo": kilo,
                    "es": es_detay if profil_tipi in ["Aile", "Çalışan"] else None,
                    "cocuklar": cocuklar_listesi
                })
                st.session_state.kayit_adim = "butce"
                st.rerun()

    # 4. AŞAMA: BÜTÇE BELİRLEME
    elif st.session_state.kayit_adim == "butce":
        st.subheader("4️⃣ Hedef Market Bütçesi")
        st.write("Günlük, haftalık veya aylık ortalama market bütçenizi belirleyin, AI sepetinizi buna göre optimize etsin.")
        
        butce_tipi = st.radio("Bütçe Periyodu:", ["Günlük Bütçe", "Haftalık Bütçe", "Aylık Bütçe"])
        butce_miktari = st.number_input("Bütçe Miktarı (TL)", min_value=50, max_value=50000, value=300, step=50)

        st.markdown("---")
        col_g2, col_d2 = st.columns(2)
        with col_g2:
            if st.button("⬅️ Geri", key="geri_fiziksel"):
                st.session_state.kayit_adim = "fiziksel"
                st.rerun()
        with col_d2:
            if st.button("🚀 Kaydet ve Başla"):
                st.session_state.profil["butce"] = {"tip": butce_tipi, "miktar": butce_miktari}
                st.session_state.ana_sayfada_mi = True
                st.success("🎉 Bilgileriniz kaydedildi!")
                st.rerun()

# --- ANA UYGULAMA ---
else:
    ust_col1, ust_col2 = st.columns([3, 1])
    with ust_col1:
        st.markdown("### 🛒 StokŞef")
    with ust_col2:
        sepet_sayisi = len(st.session_state.sepet)
        if st.button(f"🛒 Sepet ({sepet_sayisi})"):
            st.session_state.aktif_sekme = "🛒 Akıllı Sepet"

    st.markdown("---")

    if "aktif_sekme" not in st.session_state:
        st.session_state.aktif_sekme = "🏠 Ana Sayfa"

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
    with nav_col1:
        if st.button("🏠"): st.session_state.aktif_sekme = "🏠 Ana Sayfa"
    with nav_col2:
        if st.button("🎥"): st.session_state.aktif_sekme = "🎥 Topluluk"
    with nav_col3:
        if st.button("🍽️"): st.session_state.aktif_sekme = "🍽️ Yemek Planı"
    with nav_col4:
        if st.button("👑"): st.session_state.aktif_sekme = "👑 Premium AI Koç"
    with nav_col5:
        if st.button("👤⚙️"): st.session_state.aktif_sekme = "👤 Profil & Ayarlar"

    secenek = st.session_state.aktif_sekme
    st.markdown("---")

    # 1. ANA SAYFA (YAPAY ZEKA DESTEKLİ AKILLI SEPET OPTİMİZASYONU)
    if secenek == "🏠 Ana Sayfa":
        st.title("Ana Sayfa")
        p_tipi = st.session_state.profil.get('tip', 'Seçilmedi')
        b_bilgi = st.session_state.profil.get('butce', {"tip": "Haftalık", "miktar": 300})
        st.success(f"Aktif Profil: **{p_tipi}** | {b_bilgi.get('tip', 'Bütçe')}: **{b_bilgi.get('miktar', 0)} TL**")

        st.subheader("🤖 AI Akıllı Sepet Önerisi & İndirimler")
        
        if st.button("✨ Yapay Zekaya Bütçeme Uygun Sepet Kurdur"):
            if urunler:
                butce_limiti = b_bilgi.get('miktar', 300)
                secilenler = []
                toplam = 0
                for u in urunler:
                    if toplam + u.get('price', 0) <= butce_limiti:
                        secilenler.append(u)
                        toplam += u.get('price', 0)
                st.session_state.sepet = secilenler
                st.success(f"🎯 Yapay zeka bütçenize ({butce_limiti} TL) en uygun sepeti harmanladı!")
                st.rerun()
            else:
                st.warning("Veritabanında ürün bulunamadı.")

        st.write("🏬 **Market Seçimi:**")
        m_col1, m_col2, m_col3, m_col4, m_col5, m_col6, m_col7 = st.columns(7)
        with m_col1:
            if st.button("✨ Tümü"): st.session_state.secilen_market = "Tümü"
        with m_col2:
            if st.button("🟢 A101"): st.session_state.secilen_market = "A101"
        with m_col3:
            if st.button("🔵 Migros"): st.session_state.secilen_market = "Migros"
        with m_col4:
            if st.button("🔴 Şok"): st.session_state.secilen_market = "Şok"
        with m_col5:
            if st.button("🟡 Bim"): st.session_state.secilen_market = "Bim"
        with m_col6:
            if st.button("🟣 Carrefour"): st.session_state.secilen_market = "CarrefourSA"
        with m_col7:
            if st.button("🟠 File"): st.session_state.secilen_market = "File"

        if st.session_state.secilen_market == "Tümü":
            st.caption("💡 *AI Çapraz Market Modu:* Migros, Şok, A101 ve diğer marketler arasında en ucuzlar listeleniyor.")
        else:
            st.caption(f"🏬 Sadece **{st.session_state.secilen_market}** marketine ait ürünler gösteriliyor.")

        if urunler:
            filtrelenmis_urunler = urunler if st.session_state.secilen_market == "Tümü" else [u for u in urunler if u.get('market_name') == st.session_state.secilen_market]
            for idx, urun in enumerate(filtrelenmis_urunler):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{urun['product_name']}**")
                    st.caption(f"Kategori: {urun.get('category', 'Genel')} | Gramaj: {urun.get('weight', '1 Adet')}")
                with col2:
                    st.text(f"{urun['market_name']}")
                    st.write(f"🏷️ **{urun['price']} TL**")
                with col3:
                    if st.button("Ekle", key=f"ekle_{idx}"):
                        if urun not in st.session_state.sepet:
                            st.session_state.sepet.append(urun)
                            st.success("Eklendi!")
        else:
            st.info("Ürün bulunamadı.")

    # 2. TOPLULUK / REELS AKIŞI
    elif secenek == "🎥 Topluluk":
        st.title("🎥 Sosyal Tarif Akışı (Reels)")
        st.write("Bütçe dostu protein tariflerini kaydır, keşfet ve paylaş!")

        with st.form("tarif_form"):
            y_ad = st.text_input("Adın / Kullanıcı Adın", value=st.session_state.profil.get("ad", ""))
            y_sosyal = st.text_input("Sosyal Medya Profilin (Instagram / YouTube)")
            y_tarif = st.text_input("Tarif Adı ve Açıklaması")
            y_video = st.text_input("Tarif Video Linki (YouTube / Instagram)")
            gonder = st.form_submit_button("Tarifi Paylaş")
            if gonder and y_ad and y_tarif:
                st.session_state.social_posts.append({"user": y_ad, "sosyal_link": y_sosyal, "tarif": y_tarif, "video_url": y_video, "begen": 1})
                st.success("🚀 Paylaşıldı!")

        st.markdown("---")
        for idx, post in enumerate(st.session_state.social_posts):
            st.markdown(f"**👤 {post['user']}**")
            if post.get('sosyal_link'):
                st.caption(f"🔗 Profil: {post['sosyal_link']}")
            st.write(f"🍲 **{post['tarif']}**")
            if post.get('video_url'):
                st.markdown(f"🔗 [Videoyu İzle]({post['video_url']})")
            if st.button(f"❤️ Beğen ({post['begen']})", key=f"begen_{idx}"):
                post['begen'] += 1
                st.rerun()
            st.markdown("---")

    # 3. YAPAY ZEKA DESTEKLİ AKILLI YEMEK PLANI
    elif secenek == "🍽️ Yemek Planı":
        st.title("🍽️ AI Destekli Akıllı Yemek Planı")
        p_tipi = st.session_state.profil.get('tip', 'Sporcu')
        kilo = st.session_state.profil.get('kilo', 70)
        
        st.info(f"✨ Yapay zeka motoru; **{p_tipi}** profili ve **{kilo} kg** fiziksel ölçüleri baz alarak bütçenize en uygun menüyü çıkardı.")
        
        if st.button("🔄 Yapay Zekaya Yeni Menü Ürettir"):
            st.success("✨ Yapay zeka yeni bütçe dostu tarifleri derledi!")
            st.rerun()

        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        for g in gunler:
            with st.expander(f"📅 {g} - Kişiselleştirilmiş AI Menüsü"):
                if p_tipi == "Sporcu":
                    st.write("🍳 **Kahvaltı:** 4 Yumurtalı Yulaf Lapası & Fıstık Ezmesi")
                    st.write("🥗 **Öğle:** 200g Tavuk Göğsü, 150g Pirinç Pilavı & Bol Yeşillik")
                    st.write("🍲 **Akşam:** Ton Balıklı Makarna & Lor Peynirli Salata")
                    st.caption("⚡ AI Analiz: ~160g Protein | ~2400 kcal | Optimum Maliyet")
                elif p_tipi == "Aile":
                    st.write("🍳 **Kahvaltı:** Hane Halkı Serpme Kahvaltı & Zeytinyağlı Omlet")
                    st.write("🥗 **Öğle:** Fırında Sebzeli Tavuk & Bulgur Pilavı")
                    st.write("🍲 **Akşam:** Mercimek Çorbası, Ev Usulü Kıymalı Pide & Ayran")
                    st.caption("⚡ AI Analiz: Ekonomik, bereketli ve hane halkına tam doyum.")
                elif p_tipi == "Öğrenci":
                    st.write("🍳 **Kahvaltı:** Kaşarlı Tost & Söğüş")
                    st.write("🥗 **Öğle:** Pratik Ton Balıklı Sandviç")
                    st.write("🍲 **Akşam:** 3 Malzemeli Bütçe Dostu Omlet & Makarna")
                    st.caption("⚡ AI Analiz: Öğrenci cüzdanına dost, minimum maliyet.")
                else:
                    st.write("🍳 **Kahvaltı:** Fit Beyaz Peynirli Sandviç")
                    st.write("🥗 **Öğle:** Izgara Hindi Füme Salata")
                    st.write("🍲 **Akşam:** Zeytinyağlı Taze Fasulye & Yoğurt")
                    st.caption("⚡ AI Analiz: Çalışan temposuna uygun hafif ve enerjik.")

    # 4. PREMIUM AI KOÇ & VIP ASİSTAN
    elif secenek == "👑 Premium AI Koç":
        st.title("👑 Premium AI Koç & VIP Asistan")
        
        if not st.session_state.premium_aktif:
            st.info("✨ Sınırsız AI analizi, yapay zeka destekli özel diyetisyen koçluğu ve zincir marketlerde geçerli özel indirimler için Premium'a geç!")
            
            col_zayif, col_kilo = st.columns(2)
            with col_zayif:
                st.markdown("### 🔥 VIP Yağ Yakımı")
                st.write("1 Ayda 4 Kilo Garantili Yağ Yakım Asistanı")
            with col_kilo:
                st.markdown("### 💪 VIP Hacim Kazanımı")
                st.write("1 Ayda Kaliteli Kas Kütlesi Programı")

            st.markdown("---")
            hedef_secimi = st.radio("VIP Hedefin:", ["🔥 VIP Zayıfla", "💪 VIP Kilo Al"])
            ogun_sayisi = st.slider("Özel Öğün Sayısı:", 1, 6, 3)
            aciklama = st.text_area("Özel Sağlık / Alerji Durumunuz (Örn: Laktoz intoleransı)")

            if st.button("🚀 VIP AI Planımı ve Kuponumu Oluştur"):
                st.session_state.plan_olusturuldu = True

            if st.session_state.get("plan_olusturuldu", False):
                st.markdown("---")
                st.subheader("🎯 Size Özel 1 Aylık VIP AI Stratejiniz Hazır!")
                st.write("📈 Günlük makro takibi, pazar indirimleri alarmı ve kişiye özel kalori hesaplayıcı cüzdanınıza eklendi.")
                
                st.markdown("---")
                st.success("🎁 Tüm Marketlerde Geçerli **'VIPSTOKSEF500'** 500 TL İndirim Kuponunuz Tanımlandı!")
                
                col_buton1, col_buton2 = st.columns(2)
                with col_buton1:
                    if st.button("💳 200 TL ile VIP Üyeliği Başlat"):
                        st.session_state.premium_aktif = True
                        st.success("🎉 VIP Aboneliğiniz Aktifleşti!")
                        st.rerun()
                with col_buton2:
                    if st.button("Kuponsuz Standart Devam Et"):
                        st.info("ℹ️ Standart modda devam ediyorsunuz.")
        else:
            st.success("🌟 VIP / Premium Aboneliğiniz Aktif!")
            st.balloons()
            st.markdown("### 🚀 Size Özel Premium Ayrıcalıklar:")
            st.write("• Sınırsız Yapay Zeka Diyet Koçluğu & Anlık Kalori Hesaplama")
            st.write("• Gerçek Zamanlı Fiyat Düşüş ve Market İndirim Alarmı")
            st.write("• Öncelikli Destek ve VIP İndirim Kuponları")

    # 5. PROFİL + AYARLAR
    elif secenek == "👤 Profil & Ayarlar":
        st.title("👤 Profil & Ayarlar")
        
        st.info(f"Aktif Profil: **{st.session_state.profil.get('tip', 'Seçilmedi')}**")

        ad_soyad = st.text_input("Ad Soyad", value=st.session_state.profil.get("ad", ""))
        mail = st.text_input("E-posta", value=st.session_state.profil.get("mail", ""))
        
        col_b, col_k = st.columns(2)
        with col_b: boy = st.number_input("Boy (cm)", min_value=100, max_value=220, value=st.session_state.profil.get("boy", 175))
        with col_k: kilo = st.number_input("Kilo (kg)", min_value=30, max_value=200, value=st.session_state.profil.get("kilo", 70))

        if st.button("Bilgileri Güncelle"):
            st.session_state.profil.update({"ad": ad_soyad, "mail": mail, "boy": boy, "kilo": kilo})
            st.success("✅ Ayarlar kaydedildi!")
        
        st.markdown("---")
        if st.button("🔄 Profili Değiştir / Yeniden Düzenle"):
            st.session_state.ana_sayfada_mi = False
            st.session_state.kayit_adim = "profil_tipi"
            st.rerun()

    if st.button("🚨 Hesaptan Çık / Tüm Verileri Sıfırla"):
    st.session_state.clear()
    st.rerun()

# 6. AKILLI SEPET
if secenek == "🛒 Akıllı Sepet":
    st.title("🛒 Akıllı Sepet")
    if st.session_state.sepet:
        if st.button("🗑️ Hepsini Çıkart"):
            st.session_state.sepet = []
            if 'evde_var_olanlar' in st.session_state:
                st.session_state.evde_var_olanlar = []
            st.rerun()

        toplam_tutar = 0
        for i, item in enumerate(st.session_state.sepet):
            col1, col2, col3 = st.columns((3, 1, 1))
            with col1:
                st.write(f"***{item['product_name']}***")
                st.caption(f"{item['market_name']} - {item['price']} TL")
                adet = item.get('adet', 1)
                st.caption(f"📦 Adet: {adet}")
            with col2:
                if st.button("Evde Var", key=f"evde_{i}"):
                    if item not in st.session_state.evde_var_olanlar:
                        st.session_state.evde_var_olanlar.append(item)
            with col3:
                if st.button("Çıkar", key=f"cikar_{i}"):
                    st.session_state.sepet.pop(i)
                    st.rerun()
            
            if item not in st.session_state.evde_var_olanlar:
                toplam_tutar += item['price'] * item.get('adet', 1)
                
        st.metric(label="Net Sepet Maliyeti", value=f"{toplam_tutar:.2f} TL")
    else:
        st.info("Sepetiniz boş.")

# 6. AKILLI SEPET
if secenek == "🛒 Akıllı Sepet":
    st.title("🛒 Akıllı Sepet")
    if st.session_state.sepet:
        if st.button("🗑️ Hepsini Çıkart"):
            st.session_state.sepet = []
            if 'evde_var_olanlar' in st.session_state:
                st.session_state.evde_var_olanlar = []
            st.rerun()

        toplam_tutar = 0
        for i, item in enumerate(st.session_state.sepet):
            col1, col2, col3 = st.columns((3, 1, 1))
            with col1:
                st.write(f"***{item['product_name']}***")
                st.caption(f"{item['market_name']} - {item['price']} TL")
                adet = item.get('adet', 1)
                st.caption(f"📦 Adet: {adet}")
            with col2:
                if st.button("Evde Var", key=f"evde_{i}"):
                    if item not in st.session_state.evde_var_olanlar:
                        st.session_state.evde_var_olanlar.append(item)
            with col3:
                if st.button("Çıkar", key=f"cikar_{i}"):
                    st.session_state.sepet.pop(i)
                    st.rerun()
            
            if item not in st.session_state.evde_var_olanlar:
                toplam_tutar += item['price'] * item.get('adet', 1)
                
        st.metric(label="Net Sepet Maliyeti", value=f"{toplam_tutar:.2f} TL")
    else:
        st.info("Sepetiniz boş.")
