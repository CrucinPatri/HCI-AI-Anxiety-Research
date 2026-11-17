import requests
from bs4 import BeautifulSoup
import pandas as pd

# Înlocuiește cu link-urile tale reale de pe GitHub Pages
# Exemplu: "https://CrucinPatri.github.io/HCI-AI-Anxiety-Research/prototypes/scenario_a.html"
URLS = {
    "Scenariul A (Control)": "https://crucinPatri.github.io/HCI-AI-Anxiety-Research/prototypes/scenario_a.html",
    "Scenariul B (Dark Patterns)": "https://crucinPatri.github.io/HCI-AI-Anxiety-Research/prototypes/scenario_b.html",
    "Scenariul C (UI Spoofing)": "https://crucinPatri.github.io/HCI-AI-Anxiety-Research/prototypes/scenario_c.html"
}

audit_results = []

for name, url in URLS.items():
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        
        if status == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. verificăm transparența: prezența unui mesaj de informare pt scenariu A
            has_transparency = bool(soup.find(class_="info-note"))
            
            # 2. verificăm urgența și confirm-shaming pentru scenariile B și C
            has_timer = bool(soup.find(id="timer"))
            has_prechecked_box = bool(soup.find("input", {"type": "checkbox", "checked": True}))
            has_confirm_shaming = bool(soup.find(class_="btn-shame"))
            
            # 3. Verificăm UI Spoofing: dialog fals de securitate 
            has_spoof_dialog = bool(soup.find(class_="spoof-dialog"))
            
            audit_results.append({
                "Prototip": name,
                "Status HTTP": status,
                "Transparență (A)": has_transparency,
                "Urgență/Timer (B)": has_timer,
                "Pre-bifat (B)": has_prechecked_box,
                "Confirm-Shaming (B)": has_confirm_shaming,
                "UI Spoofing Modal (C)": has_spoof_dialog
            })
        else:
            audit_results.append({"Prototip": name, "Status HTTP": status, "Eroare": "Pagina nu este accesibilă"})
            
    except Exception as e:
        audit_results.append({"Prototip": name, "Status HTTP": "Eroare conexiune", "Eroare": str(e)})

# afisare raport
audit_df = pd.DataFrame(audit_results)
print("=== RAPORT AUDIT AUTOMAT & VALIDARE URL-URI (WEB SCRAPING) ===")
print(audit_df.to_string(index=False))