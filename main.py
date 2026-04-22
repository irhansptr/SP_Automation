import time
import os
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# ================= CONFIGURASI =================
TARGET_URL = "https://shopee.co.id/Celana-Jeans-Panjang-Pria-Model-Standar-Kualitas-Premium-i.506036565.20493538621"
JAM_MULAI = "22:49:00" 
USER_DATA_PATH = "/home/nikenokta/Desktop/bot/sp/temp_profile"
PROFILE_NAME = "Default"
# ===============================================

def bersihkan_chrome():
    print("[*] Membersihkan proses Chrome...")
    subprocess.run(["pkill", "-f", "chrome"], stderr=subprocess.DEVNULL)
    lock_file = os.path.join(USER_DATA_PATH, "SingletonLock")
    if os.path.exists(lock_file):
        try: os.remove(lock_file)
        except: pass

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={USER_DATA_PATH}")
    options.add_argument(f"--profile-directory={PROFILE_NAME}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Membuka dengan versi chrome kamu (v147)
    driver = uc.Chrome(options=options, version_main=147) 
    return driver

def jalankan_bot():
    os.system("clear")
    bersihkan_chrome()
    driver = setup_driver()
    wait = WebDriverWait(driver, 10) # Toleransi tunggu elemen 10 detik
    
    print(f"[*] Menuju Target: {TARGET_URL}")
    driver.get(TARGET_URL)

    # Logika tunggu waktu yang presisi
    print(f"[*] Standby... Menunggu jam {JAM_MULAI}")
    while True:
        now = time.strftime("%H:%M:%S")
        if now >= JAM_MULAI:
            print(f"[!] WAKTUNYA! Mulai Serangan...")
            driver.refresh()
            break
        time.sleep(0.05) # Cek setiap 50ms

    try:
        # 1. Pilih Varian (Menggunakan JavaScript agar pasti terklik)
        print("[*] Mencari dan klik varian pertama...")
        # XPath ini mencari tombol varian yang aktif (bukan yang buram/disabled)
        varian_xpath = '//*[@id="sll2-normal-pdp-main"]/div/div/div/div[2]/section/section[2]/div/div[4]/div/div[2]/div/section[1]/div/div/button[1]'
        varian = wait.until(EC.presence_of_element_located((By.XPATH, varian_xpath)))
        
        # 1. Pilih Varian 2 (Menggunakan JavaScript agar pasti terklik)
        print("[*] Mencari dan klik varian kedua...")
        # XPath ini mencari tombol varian yang aktif (bukan yang buram/disabled)
        varian2_xpath = '//*[@id="sll2-normal-pdp-main"]/div/div/div/div[2]/section/section[2]/div/div[4]/div/div[2]/div/section[2]/div/div[1]/button[1]'
        varian2 = wait.until(EC.presence_of_element_located((By.XPATH, varian2_xpath)))

        # Paksa klik pakai JavaScript (Bypass jika tombol tertutup elemen lain)
        driver.execute_script("arguments[0].click();", varian)
        driver.execute_script("arguments[0].click();", varian2)
        print("[+] Varian berhasil dipilih.")
        
        time.sleep(0.2) # Jeda sangat singkat untuk render

        # 2. Klik Beli Sekarang (Paksa JavaScript)
        print("[*] Mencoba klik Beli Sekarang...")
        beli_xpath = '//*[@id="sll2-normal-pdp-main"]/div/div/div/div[2]/section/section[2]/div/div[5]/div/div/button[2]'
        tombol_beli = wait.until(EC.presence_of_element_located((By.XPATH, beli_xpath)))
        
        driver.execute_script("arguments[0].click();", tombol_beli)
        print("[+] Tombol Beli berhasil diklik.")

        # 3. Klik Checkout
        print("[*] Menuju Checkout...")
        checkout_xpath = '//*[@id="main"]/div/div[2]/div/div/div/div[2]/section/div[7]/div[5]/button'
        tombol_checkout = wait.until(EC.presence_of_element_located((By.XPATH, checkout_xpath)))
        
        driver.execute_script("arguments[0].click();", tombol_checkout)
        print("[+] Masuk ke halaman pembayaran.")

        # 4. Buat Pesanan
        print("[*] Mencari tombol Buat Pesanan...")
        buat_pesanan_xpath = "//button[contains(text(), 'Buat Pesanan')] | //button[text()='Buat Pesanan']"
        buat_pesanan = wait.until(EC.presence_of_element_located((By.XPATH, buat_pesanan_xpath)))
        
        # JANGAN AKTIFKAN KECUALI SIAP BELI
        # driver.execute_script("arguments[0].click();", buat_pesanan)
        print("[SUCCESS] Sampai ke tahap akhir!")

    except Exception as e:
        print(f"[!] Gagal klik karena: {e}")
        # Ambil screenshot jika gagal untuk analisa
        driver.save_screenshot("error_klik.png")
        print("[*] Screenshot error disimpan sebagai error_klik.png")
        

    time.sleep(300)

if __name__ == "__main__":
    jalankan_bot()