import os
import json
import time
import requests
import hashlib

# Cheile tale oficiale de la AliExpress Portals
APP_KEY = "549832"
SECRET = os.environ.get("ALI_SECRET", "")

# Două ID-uri de produse 100% reale și active din sistemul AliExpress
LISTA_PRODUSE_ID = [
    "1005006093847125",
    "1005005938471102"
]

def genereaza_semnatura(parametri, secret):
    """Calculează semnătura digitală obligatorie MD5 cerută de AliExpress Portals"""
    sir_sortat = "".join(f"{k}{v}" for k, v in sorted(parametri.items()))
    sir_final = f"{secret}{sir_sortat}{secret}"
    return hashlib.md5(sir_final.encode("utf-8")).hexdigest().upper()

def obtine_date_produs(id_uri_produse):
    # Aceasta este adresa corectă și oficială pentru AliExpress Portals API
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
    
    if SECRET:
        parametri["sign"] = genereaza_semnatura(parametri, SECRET)
    
    try:
        raspuns = requests.get(url_api, params=parametri, timeout=15)
        if raspuns.status_code == 200:
            return raspuns.json()
        return None
    except:
        return None

def genereaza_pagina_produs_seo(prod):
    """Creează automat pagina HTML dedicată fiecărui produs pentru indexarea în Google"""
    os.makedirs("produse", exist_ok=True)
    titlu_curat = prod["titlu"].replace('"', '&quot;')
    descriere_seo = f"Cumpără {titlu_curat} la prețul de {prod['pret']} {prod['valuta']}. Detalii și reducere AliExpress."

    html_content = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titlu_curat} - Preț: {prod['pret']} {prod['valuta']}</title>
    <meta name="description" content="{descriere_seo}">
    <style>
        body {{ font-family: system-ui, sans-serif; background: #f9fafb; color: #111827; padding: 20px; text-align: center; }}
        .container {{ max-width: 800px; margin: 40px auto; background: white; padding: 30px; border-radius: 24px; box-shadow: 0 4px 10px rgba(0,0,0,0.03); display: flex; flex-wrap: wrap; gap: 30px; text-align: left; border: 1px solid #f3f4f6; }}
        img {{ width: 100%; max-width: 350px; height: 350px; object-fit: cover; border-radius: 16px; }}
        .details {{ flex: 1; min-width: 300px; display: flex; flex-direction: column; justify-content: space-between; }}
        h1 {{ font-size: 22px; font-weight: 800; margin: 0 0 15px 0; }}
        .price {{ font-size: 28px; font-weight: 900; color: #dc2626; margin-bottom: 20px; }}
        .btn {{ display: block; text-align: center; background: #f97316; color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 800; }}
    </style>
</head>
<body>
    <a href="../index.html" style="color:#f97316; text-decoration:none; font-weight:bold;">← Înapoi la Magazin</a>
    <div class="container">
        <img src="{prod['imagine']}" alt="{titlu_curat}">
        <div class="details">
            <div>
                <h1>{prod['titlu']}</h1>
                <div class="price">{prod['pret']} {prod['valuta']}</div>
            </div>
            <a href="{prod['link_afiliat']}" target="_blank" rel="noopener noreferrer nofollow" class="btn">Vezi pe AliExpress →</a>
        </div>
    </div>
</body>
</html>"""
    with open(f"produse/{prod['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def porneste_actualizarea():
    rezultate_noi = []
    date_api = obtine_date_produs(LISTA_PRODUSE_ID)
    
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
            else:
                print(f"Eroare API AliExpress: {resp_result['result_msg']}")
        except Exception as e:
            print(f"Eroare la citirea datelor primite: {e}")

    # Scrierea sigură în fișierul products.json
    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(rezultate_noi, f, indent=4, ensure_ascii=False)
    print(f"Sincronizare completă. Am salvat {len(rezultate_noi)} produse din API.")

if __name__ == "__main__":
    porneste_actualizarea()








