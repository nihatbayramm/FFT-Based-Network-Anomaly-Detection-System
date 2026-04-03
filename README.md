# 🛡️ FFT Anomaly Detection System - v4.0

FFT is an advanced cybersecurity analysis tool that detects suspicious activity and DDoS attacks in network traffic using the **Fast Fourier Transform (FFT)**.

Unlike classic signature-based systems, it detects anomalies by analyzing the rhythm and frequency spectrum of traffic.

---

## 🚀 Key Features

- **Spectral Analysis:**

Captures periodic attack signatures by transferring network packets from the time domain to the frequency domain.

- **Real-Time Visualization:**

Presents packet density and FFT spectrum in real-time graphs.

- **Advanced Anomaly Engine:**

Calculates packet changes within seconds statistically and generates an **"Anomaly Score"**.

- **Cybersecurity Dashboard:**

Professional *Dark Mode* interface and terminal-based reporting system.

- **Fast PCAP Processing:**

Scapy analyzes thousands of packets in seconds without slowing down the computer, thanks to its `PcapReader` architecture.

---

## 🛠️ Technical Infrastructure

The system treats network traffic as a **signal**.

- Random human traffic → *White Noise*

- Bots / flood tools → Repeating signals at a fixed frequency

Thanks to this difference, the system detects attacks based on frequency.

### Technologies Used

- Python 3.12+
- Scapy → Packet parsing and PCAP reading
- NumPy & SciPy → FFT and statistical analysis
- Matplotlib → Graph plotting
- Tkinter → Interface and threading support

---

## 💻 Installation and Running

### 1️⃣ Required Libraries

```

pip install scapy numpy scipy matplotlib

```

### 2️⃣ Start the System

```
python3 main_program.py

```

### 🧪 Generating Test Data (Optional)

15-second attack traffic simulation:

```

sudo hping3 -S -p 80 --flood 127.0.0.1

```

### 📊 Analysis Outputs

**📈 Time Series**

**Traffic intensity second by second**

**⚡ FFT Spectrum**

**If there is a sharp spike at a specific frequency → most likely an attack**

**Flat distribution → normal traffic**

***This project was developed for educational and cybersecurity research purposes.***

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/6f110f8f-ff2d-4115-b80b-15872710eb4c" />

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/4177bbc7-5063-4c5c-bb81-8f13db8fdbfb" />

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/241348db-7a98-49e3-ae16-fc60c8ca8d67" />

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/b97ed62f-806d-475e-99b5-d34b6b6761d8" />

<img width="600" height="500" alt="image" src="https://github.com/user-attachments/assets/3d653992-c907-4513-9193-d83bcb366229" />



### 👨‍💻 Developer

***Nihat Bayram***

**Version: 4.0 (Stable)**
