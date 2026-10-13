import os
import json
import time
import requests
import hashlib

# Configurații API AliExpress (Preluat automat din GitHub Secrets)
APP_KEY = os.environ.get("ALI_APP_KEY", "549832")
SECRET = os.environ.get("ALI_SECRET")

# Lista ta cu cele 4 produse reale de pe AliExpress
LISTA_PRODUSE_ID = [
    "1005006429381742",
    "1005005834891122",
    "1005006012445588",
    "1005005991223344"
]

def genereaza_semnatura(parametri, secret):
    """Generează semnătura digitală MD5 obligatorie pentru AliExpress Open API"""
    sir_sortat = "".join(f"{k}{v}" for k, v in sorted(parametri.items()))
    sir_final = f"{secret}{sir_sortat}{secret}"
    return hashlib.md5(sir_final.encode("utf-8")).hexdigest().upper()

def obtine_date_produs(id_uri_produse):
    # Endpoint-ul API corect și oficial global
    url_api = "https://aliexpress.com"
    
    parametri = {
        "app_key": APP_KEY,
        "method": "aliexpress.affiliate.productinfo.get",
        "timestamp": str(int(time.time() * 1000)),
        "format": "json",
        "v": "2.0",
        "sign_method": "md5",
        "product_ids": ",".join(id_uri_produse)
    }
    
    parametri["sign"] = genereaza_semnatura(parametri, SECRET)
    
    try:
        raspuns = requests.get(url_api, params=parametri, timeout=15)
        if raspuns.status_code == 200:
            return raspuns.json()
        else:
            print(f"Eroare server AliExpress: {raspuns.status_code}")
            return None
    except Exception as e:
        print(f"Eroare de conexiune: {e}")
        return None

def genereaza_pagina_produs_seo(prod):
    """Creează o pagină HTML independentă pentru fiecare produs"""
    os.makedirs("produse", exist_ok=True)
    
    titlu_curat = prod["titlu"].replace('"', '&quot;')
    descriere_seo = f"Cumpără {titlu_curat} la cel mai bun preț de {prod['pret']} {prod['valuta']}."

    # Acoladele au fost corectate pentru a nu mai bloca rularea scriptului Python
    html_content = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titlu_curat} - Preț: {prod['pret']} {prod['valuta']}</title>
    <meta name="description" content="{descriere_seo}">
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; background: #f9fafb; color: #111827; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 40px auto; background: white; padding: 30px; border-radius: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); display: flex; flex-wrap: wrap; gap: 30px; border: 1px solid #f3f4f6; }}
        .back-link {{ display: block; max-width: 800px; margin: 0 auto 20px auto; color: #f97316; text-decoration: none; font-weight: 700; }}
        img {{ max-width: 100%; width: 350px; height: 350px; object-fit: cover; border-radius: 16px; }}
        .details {{ flex: 1; min-width: 300px; display: flex; flex-direction: column; justify-content: space-between; }}
        h1 {{ font-size: 22px; font-weight: 800; line-height: 1.4; margin: 0 0 15px 0; }}
        .price {{ font-size: 28px; font-weight: 900; color: #dc2626; margin-bottom: 20px; }}
        .btn {{ display: block; text-align: center; background: linear-gradient(to right, #f97316, #ae1111); color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 800; font-size: 16px; }}
    </style>
</head>
<body>
    <a href="../index.html" class="back-link">← Înapoi la Catalog</a>
    <main class="container">
        <img src="{prod['imagine']}" alt="{titlu_curat}">
        <div class="details">
            <div>
                <h1>{prod['titlu']}</h1>
                <div class="price">{prod['pret']} {prod['valuta']}</div>
            </div>
            <a href="{prod['link_afiliat']}" target="_blank" rel="noopener noreferrer nofollow" class="btn">Cumpără de pe AliExpress →</a>
        </div>
    </main>
</body>
</html>"""

    with open(f"produse/{prod['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def porneste_actualizarea():
    print("Se curăță baza de date și se pornește importul...")
    rezultate_noi =
    
    for i in range(0, len(LISTA_PRODUSE_ID), 100):
        lot_produse = LISTA_PRODUSE_ID[i:i+100]
        date_api = obtine_date_produs(lot_produse)
        
        if date_api and "aliexpress_affiliate_productinfo_get_response" in date_api:
            try:
                resp_result = date_api["aliexpress_affiliate_productinfo_get_response"]["resp_result"]
                if resp_result["result_code"] == 200:
                    produse = resp_result["result"]["products"]["product"]
                    for prod in produse:
                        item = {
                            "id": str(prod.get("product_id")),
                            "titlu": prod.get("product_title"),
                            "pret": prod.get("target_sale_price"),
                            "valuta": prod.get("target_sale_price_currency", "EUR"),
                            "link_afiliat": prod.get("promotion_link"),
                            "imagine": prod.get("product_main_image_url")
                        }
                        rezultate_noi.append(item)
                        genereaza_pagina_produs_seo(item)
            except Exception as e:
                print(f"Eroare la citirea datelor interne: {e}")
        
        time.sleep(1.5)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(rezultate_noi, f, indent=4, ensure_ascii=False)
    
    print(f"Gata! Am salvat {len(rezultate_noi)} produse în products.json.")

if __name__ == "__main__":
    if not SECRET:
        print("EROARE: Lipsește codul tău secret ALI_SECRET în GitHub Settings!")
    else:
        porneste_actualizarea()

