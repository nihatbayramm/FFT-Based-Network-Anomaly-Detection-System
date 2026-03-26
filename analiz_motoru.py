import numpy as np
from scapy.all import PcapReader
from scipy.fft import fft, fftfreq
from scipy.stats import poisson

def pcap_analiz_et(dosya_yolu):
    zamanlar = []
    try:
        with PcapReader(dosya_yolu) as reader:
            for i, paket in enumerate(reader):
                zamanlar.append(float(paket.time))
                if i > 50000: break 
    except: return None

    if len(zamanlar) < 5: return None

    zamanlar = np.array(zamanlar) - zamanlar[0]
    toplam_sure = zamanlar[-1]
    bin_sayisi = 50
    sinyal, _ = np.histogram(zamanlar, bins=bin_sayisi)
    
    # İstatistikler
    avg = np.mean(sinyal)
    var = np.var(sinyal)
    vo_ratio = var / (avg + 1e-9)
    
    # FFT
    N = len(sinyal)
    yf_raw = fft(sinyal)
    xf = fftfreq(N, toplam_sure/bin_sayisi)[:N//2]
    yf = 2.0/N * np.abs(yf_raw[0:N//2])
    
    # --- SALDIRI TÜRÜ TEŞHİS MANTIĞI ---
    saldiri_turu = "YOK (TEMİZ TRAFİK)"
    onlem = "Sistem normal. İzlemeye devam ediliyor."
    durum = "NORMAL TRAFİK ✅"

    if vo_ratio > 3:
        durum = "SALDIRI TESPİT EDİLDİ ⚠️"
        # Frekans analizi ile tür belirleme (Basit mantık)
        peak_f = xf[np.argmax(yf[1:])+1]
        
        if peak_f > 10:
            saldiri_turu = "YÜKSEK YOĞUNLUKLU UDP/ICMP FLOOD"
            onlem = "1. Rate Limiting aktif et.\n2. Kaynak IP'leri Firewall üzerinden drop et.\n3. ISP ile iletişime geç."
        elif peak_f > 1:
            saldiri_turu = "TCP SYN FLOOD (BOTNET)"
            onlem = "1. SYN Proxy aktif et.\n2. Yarı-açık bağlantı zaman aşımını düşür.\n3. Anormal paket boylarını engelle."
        else:
            saldiri_turu = "YAVAŞ HTTP (SLOWLORIS) SALDIRISI"
            onlem = "1. Minimum veri hızını kontrol et.\n2. Bağlantı ömrünü (Timeout) kısıtla.\n3. Load Balancer eşiklerini güncelle."

    # Rapor Metni
    rapor = (f"> [DURUM]      : {durum}\n"
             f"> [TÜR]        : {saldiri_turu}\n"
             f"> [ETKİ]       : %{min(100, int(vo_ratio*15))} Yoğunluk\n"
             f"------------------------------------\n"
             f"🛡️ ÖNERİLEN AKSİYONLAR:\n"
             f"{onlem}")

    return {
        "sinyal": sinyal, "zaman_ekseni": np.linspace(0, toplam_sure, bin_sayisi),
        "xf": xf, "yf": yf, "x_pois": np.arange(0, np.max(sinyal)+5), 
        "y_pois": poisson.pmf(np.arange(0, np.max(sinyal)+5), avg)*len(sinyal),
        "avg": avg, "vo": vo_ratio, "durum": durum, "bilgi": rapor
    }