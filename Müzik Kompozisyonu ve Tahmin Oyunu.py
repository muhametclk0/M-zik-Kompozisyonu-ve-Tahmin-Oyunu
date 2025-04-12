from pydub import AudioSegment
from pydub.generators import Sine
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# Ritim ve melodi üretme
bpm = 120
notlar = ["C", "E", "G", "B", "C5", "G", "E", "C"]  # Farklı notalar
süre_ms = int(60000 / bpm)  # Nota süresi

# Ses üretme işlemi
şarkı = AudioSegment.silent(süre=0)  # Başlangıçta sessiz

for not_ in notlar:
    frekans = random.choice([261.63, 329.63, 392.00, 523.25, 440.00, 349.23])  # Sine wave frekansı
    ton = Sine(frekans).to_audio_segment(duration=süre_ms).fade_in(20).fade_out(20)
    şarkı += ton  # Melodiye ekle

# Şarkıyı kaydetme
şarkı.export("generated_loop.wav", format="wav")
print("✅ Melodi oluşturuldu ve generated_loop.wav dosyasına kaydedildi")

# **Hızlandırma işlemi** (1.5x hız)
sped_up_audio = şarkı.speedup(playback_speed=1.5)
sped_up_audio.export("sped_up_loop.wav", format="wav")
print("✅ Hızlandırılmış melodi oluşturuldu ve sped_up_loop.wav dosyasına kaydedildi")

# **Şarkının bir kısmını kesme** (ilk 10 saniye)
section = şarkı[:10000]  # 10 saniyelik kesit
section.export("section.wav", format="wav")
print("✅ Şarkının bir kısmı kesildi ve section.wav dosyasına kaydedildi")

# **Kaydırma işlemi** (5 saniye sağa kaydırma)
shifted_audio = şarkı + 5000  # 5 saniye sağa kaydırma
shifted_audio.export("shifted_loop.wav", format="wav")
print("✅ Kaydırılmış melodi oluşturuldu ve shifted_loop.wav dosyasına kaydedildi")

# **Melodi Analizi ve Görselleştirme** - Ses dalga formu çizimi
time_samples = np.linspace(0, len(şarkı) / 1000.0, len(şarkı))  # Zaman aralığı
data = np.array(şarkı.get_array_of_samples())  # Ses verisi

plt.figure(figsize=(10, 4))
plt.plot(time_samples, data)
plt.title("Melodi Dalga Formu")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.savefig("waveform_plot.png")
print("✅ Melodi dalga formu kaydedildi: waveform_plot.png")

# **Melodi Frekans Spektrumu** - FFT (Hızlı Fourier Dönüşümü)
fft_data = np.fft.fft(data)
fft_freq = np.fft.fftfreq(len(fft_data), 1/44100)  # 44.1kHz örnekleme hızı

# Güç spektrumunu hesaplama
fft_magnitude = np.abs(fft_data)[:len(fft_data)//2]
fft_freq = fft_freq[:len(fft_freq)//2]

plt.figure(figsize=(10, 4))
plt.plot(fft_freq, fft_magnitude)
plt.title("Melodi Frekans Spektrumu")
plt.xlabel("Frekans (Hz)")
plt.ylabel("Magnitüd")
plt.grid(True)
plt.savefig("spectrum_plot.png")
print("✅ Frekans spektrumu kaydedildi: spectrum_plot.png")

# Melodi oynatma (örnek olarak)
from pydub.playback import play
play(şarkı)  # Şarkıyı çal