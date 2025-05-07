from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re, threading, requests, subprocess, signal, os, platform, time
import tkinter as tk
from tkinter import messagebox

URL = "https://app.hyperate.io/{HeartRateID}"  # Substitua pelo URL correto
THRESHOLD_BPM = 130
POLL_INTERVAL = 10


def kill_obs():
    try:
        system = platform.system()
        if system == "Windows":
            # Usando o taskkill pra aniquilar o OBS
            subprocess.run(["taskkill", "/F", "/IM", "obs64.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/F", "/IM", "obs32.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("OBS crashed by taskkill command on Windows.")
        elif system == "Darwin" or system == "Linux":
            output = subprocess.check_output(["pgrep", "-f", "obs"], text=True).strip()
            if output:
                for pid_str in output.splitlines():
                    pid = int(pid_str)
                    os.kill(pid, signal.SIGKILL)
                print("Matando o processo OBS no UNIX, boa sorte :P")
            else:
                print("OBS process not found")
        else:
            print(f"Sistema Operacional não suportado: {system}. Não foi possível fechar o OBS.")
    except Exception as e:
        print(f"Falha Crítica ao Derrubar o OBS! : {e}")

def get_heart_rate(driver):
    driver.get(URL)
    time.sleep(3)
    body_text = driver.find_element("tag name", "body").text
    matches = re.findall(r"\b(\d{2,3})\b", body_text)
    if matches:
        return int(matches[0])
    return None

def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)  # or webdriver.Firefox()

    try:
        while True:
            hr = get_heart_rate(driver)
            if hr is not None:
                print(f"Batimendo Cardíaco: {hr}")
                if hr > THRESHOLD_BPM:
                    print(f"HAHAHAHAHAHA! Crashing OBS.")
                    kill_obs()
                    break
            else:
                print("Não foi possível encontrar a frequência cardíaca, está com o link correto?")
            time.sleep(POLL_INTERVAL)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
