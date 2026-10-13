import os
import json
import time
import requests
import hashlib

APP_KEY = "549832"
SECRET = os.environ.get("ALI_SECRET", "")

LISTA_PRODUSE_ID = [
    "1005008384803828", 
    "1005007341784572",
    "1005010701830877",
    "1005008156418926"
]

def genereaza_semnatura(parametri, secret):
    if not secret: return ""
    sir_sortat = "".join(f"{k}{v}" for k, v in sorted(parametri.items()))
    sir_final = f"{secret}{sir_sortat}{secret}"
    return hashlib.md5(sir_final.encode("utf-8")).hexdigest().upper()

def obtine_date_produs(id_uri_produse):
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
    sign = genereaza_semnatura(parametri, SECRET)
    if sign: parametri["sign"] = sign
    
    try:
        raspuns = requests.get(url_api, params=parametri, timeout=15)
        if raspuns.status_code == 200: return raspuns.json()
        return None
    except:
        return None

def genereaza_pagina_produs_seo(prod):
    os.makedirs("produse", exist_ok=True)
    titlu_curat = prod["titlu"].replace('"', '&quot;')
    html_content = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titlu_curat}</title>
    <style>
        body {{ font-family: system-ui, sans-serif; background: #f9fafb; padding: 20px; }}
        .container {{ max-width: 800px; margin: 40px auto; background: white; padding: 30px; border-radius: 24px; display: flex; flex-wrap: wrap; gap: 30px; border: 1px solid #f3f4f6; }}
        img {{ width: 350px; height: 350px; object-fit: cover; border-radius: 16px; }}
        .details {{ flex: 1; min-width: 300px; display: flex; flex-direction: column; justify-content: space-between; }}
        h1 {{ font-size: 22px; font-weight: 800; }}
        .price {{ font-size: 28px; font-weight: 900; color: #dc2626; margin: 20px 0; }}
        .btn {{ display: block; text-align: center; background: #f97316; color: white; padding: 15px; border-radius: 12px; text-decoration: none; font-weight: 800; }}
    </style>
</head>
<body>
    <a href="../index.html" style="color:#f97316; text-decoration:none; font-weight:bold;">← Înapoi</a>
    <div class="container">
        <img src="{prod['imagine']}" alt="">
        <div class="details">
            <div>
                <h1>{prod['titlu']}</h1>
                <div class="price">{prod['pret']} {prod['valuta']}</div>
            </div>
            <a href="{prod['link_afiliat']}" target="_blank" class="btn">Cumpără de pe AliExpress →</a>
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
        except:
            pass

    # REZERVĂ DE SIGURANȚĂ: Dacă API-ul e gol, forțăm 2 produse demo superbe ca să pornească site-ul vizual
    if len(rezultate_noi) == 0:
        produs_demo1 = {
            "id": "1005006429381742",
            "titlu": "Cameră de Securitate Inteligentă Wi-Fi 4K Outdoor",
            "pret": "24.99",
            "valuta": "EUR",
            "link_afiliat": "https://aliexpress.com",
            "imagine": "https://alicdn.com"
        }
        produs_demo2 = {
            "id": "1005005834891122",
            "titlu": "Căști Wireless Pro Sound Bluetooth 5.3",
            "pret": "15.45",
            "valuta": "EUR",
            "link_afiliat": "https://aliexpress.com",
            "imagine": "https://alicdn.com"
        }
        rezultate_noi.append(produs_demo1)
        rezultate_noi.append(produs_demo2)
        genereaza_pagina_produs_seo(produs_demo1)
        genereaza_pagina_produs_seo(produs_demo2)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(rezultate_noi, f, indent=4, ensure_ascii=False)
    print(f"Finalizat cu {len(rezultate_noi)} produse.")

if __name__ == "__main__":
    porneste_actualizarea()




