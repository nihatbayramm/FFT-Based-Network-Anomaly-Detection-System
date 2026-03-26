import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import time

ctk.set_appearance_mode("Dark")

class CyberDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NİHAT FFT | Enterprise Intelligence v8.5")
        self.geometry("1550x950")
        self.configure(bg="#050505")

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SOL PANEL ---
        self.left_panel = ctk.CTkFrame(self, fg_color="#080808", corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.header = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self.header, text="NİHAT FFT ENGINE", font=("Consolas", 26, "bold"), text_color="#00d4ff").pack(side="left")
        self.btn_run = ctk.CTkButton(self.header, text="⚡ ANALİZİ BAŞLAT", fg_color="#238636", font=("Arial", 12, "bold"), command=self.analiz_thread_baslat)
        self.btn_run.pack(side="right", padx=10)
        ctk.CTkButton(self.header, text="📁 DOSYA SEÇ", fg_color="#1f1f1f", command=self.dosya_sec).pack(side="right", padx=10)

        # Grafik Alanı
        self.chart_container = ctk.CTkFrame(self.left_panel, fg_color="#0d0d0d", corner_radius=15)
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.setup_plot()

        # --- RADAR OVERLAY (KAYMAYI ENGELLEYEN KATMAN) ---
        self.overlay = tk.Canvas(self.chart_container, bg="#0d0d0d", highlightthickness=0)
        self.overlay_text = None

        # --- SAĞ PANEL ---
        self.right_panel = ctk.CTkFrame(self, fg_color="#0d0d15", corner_radius=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        ctk.CTkLabel(self.right_panel, text="📊 ANALİZ DETAYLARI", font=("Arial", 16, "bold"), text_color="#58a6ff").pack(pady=20)
        self.status_label = ctk.CTkLabel(self.right_panel, text="BEKLEMEDE", font=("Consolas", 14, "bold"), text_color="#8b949e")
        self.status_label.pack(pady=10)

        self.report_text = ctk.CTkTextbox(self.right_panel, fg_color="#010409", text_color="#3fb950", font=("Consolas", 13))
        self.report_text.pack(fill="both", expand=True, padx=20, pady=20)
        self.report_text.configure(state="disabled")

        self.is_scanning = False

    def setup_plot(self):
        plt.style.use('dark_background')
        self.fig, self.axs = plt.subplots(3, 1, figsize=(9, 12), facecolor='#0d0d0d')
        self.fig.tight_layout(pad=6.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_container)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)

    def dosya_sec(self):
        dosya = filedialog.askopenfilename(filetypes=[("Pcap", "*.pcap")])
        if dosya: self.target_path = dosya

    def analiz_thread_baslat(self):
        if not hasattr(self, 'target_path'): return
        self.is_scanning = True
        self.btn_run.configure(state="disabled")
        
        # Grafiklerin üzerini kapatan katmanı aktif et
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        threading.Thread(target=self.radar_loop, daemon=True).start()
        threading.Thread(target=self.analiz_execute, daemon=True).start()

    def radar_loop(self):
        """Grafiklerden bağımsız, sabit koordinatlı radar"""
        angle = 0
        symbols = ["◜", "◝", "◞", "◟"] # Dönen parça efekti
        while self.is_scanning:
            # Canvas'ı temizle ve yeniden çiz (Kayma ihtimali SIFIR)
            self.overlay.delete("all")
            w = self.overlay.winfo_width() / 2
            h = self.overlay.winfo_height() / 2
            
            # Radar Sembolü
            self.overlay.create_text(w, h, text="☢", fill="#00ff41", font=("Arial", 80), angle=angle)
            self.overlay.create_text(w, h + 100, text="SİNYAL İŞLENİYOR...", fill="#00ff41", font=("Consolas", 16, "bold"))
            
            angle = (angle + 15) % 360
            time.sleep(0.05)

    def analiz_execute(self):
        time.sleep(3) # Profesyonel bekleme süresi
        try:
            from analiz_motoru import pcap_analiz_et
            res = pcap_analiz_et(self.target_path)
            self.is_scanning = False
            # Katmanı kaldır
            self.after(0, lambda: self.overlay.place_forget())
            if res: self.after(0, lambda: self.render_charts(res))
        except Exception as e:
            self.is_scanning = False
            self.after(0, lambda: self.overlay.place_forget())
            self.after(0, lambda: messagebox.showerror("Hata", str(e)))
        self.after(0, lambda: self.btn_run.configure(state="normal"))
# ... (Üst kısımdaki importlar ve setup_plot fonksiyonu öncekiyle aynı) ...

   # ... (Üst kısımdaki importlar ve setup_plot aynı kalacak) ...

    def render_charts(self, res):
        ax1, ax2, ax3 = self.axs
        for ax in self.axs: ax.clear()
        
        # --- 1. ZAMAN DOMAİN (TRAFİK AKIŞI) ---
        ax1.plot(res["zaman_ekseni"], res["sinyal"], color='#00d4ff', linewidth=2, label='Anlık Akış')
        ax1.fill_between(res["zaman_ekseni"], res["sinyal"], color='#00d4ff', alpha=0.1)
        ax1.set_title("AĞ TRAFİK YOĞUNLUĞU (Zaman Domain)", color="#00d4ff", fontsize=11, fontweight='bold')
        ax1.set_xlabel("Gözlem Süresi (Saniye)", fontsize=9, color="#8b949e")
        ax1.set_ylabel("Paket Sayısı", fontsize=9, color="#8b949e")
        ax1.grid(True, linestyle='--', alpha=0.2)

        # --- 2. POISSON ANALİZİ (İSTATİSTİKSEL KANIT) ---
        # Poisson çubuklarını tekrar görünür yaptık
        ax2.bar(res["x_pois"][:20], res["y_pois"][:20], color='#58a6ff', alpha=0.6, label="Beklenen (Poisson)", width=0.8)
        ax2.step(range(len(res["sinyal"][:20])), res["sinyal"][:20], color='#ffcc00', where='mid', label="Gerçekleşen", linewidth=2.5)
        ax2.set_title("İSTATİSTİKSEL MODEL UYUMU (Poisson Analizi)", color="#ffcc00", fontsize=11, fontweight='bold')
        ax2.set_xlabel("Paket/Dilim Oranı", fontsize=9, color="#8b949e")
        ax2.set_ylabel("Oluşma Sıklığı", fontsize=9, color="#8b949e")
        ax2.legend(loc='upper right', fontsize=8)

        # --- 3. FFT (SPEKTRAL İMZA / SALDIRI RİTMİ) ---
        ax3.plot(res["xf"], res["yf"], color='#f85149', linewidth=1.5)
        ax3.set_title("SPEKTRAL ANALİZ (FFT - Frekans Domain)", color="#f85149", fontsize=11, fontweight='bold')
        ax3.set_xlabel("Frekans (Hz) - Saniyedeki Vuruş Sayısı", fontsize=9, color="#8b949e")
        ax3.set_ylabel("Sinyal Gücü (Genlik)", fontsize=9, color="#8b949e")
        
        # Eğer saldırı varsa en yüksek frekansı okla işaretle
        if res["vo"] > 3:
            peak_f = res["xf"][np.argmax(res["yf"][1:])+1]
            ax3.annotate(f'SALDIRI ODAĞI: {peak_f:.1f} Hz', xy=(peak_f, np.max(res["yf"][1:])), 
                         xytext=(peak_f+5, np.max(res["yf"][1:])),
                         arrowprops=dict(facecolor='white', shrink=0.05, width=1),
                         color='white', fontweight='bold', fontsize=9)

        self.canvas.draw()
        
        # --- SAĞ PANEL GÜNCELLEME ---
        self.status_label.configure(
            text=res["durum"], 
            text_color="#f85149" if "SALDIRI" in res["durum"] else "#3fb950"
        )
        
        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, res["bilgi"])
        self.report_text.configure(state="disabled")

# ... (Kalan kısımlar aynı) ...

if __name__ == "__main__":
    app = CyberDashboard(); app.mainloop()