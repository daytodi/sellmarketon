import os
import json
import time
import requests
import hashlib

APP_KEY = os.environ.get("ALI_APP_KEY", "549832")
SECRET = os.environ.get("ALI_SECRET")

# INTRODUCE MAI JOS ID-URILE PRODUSELOR (Adaugă câte vrei, separate prin virgulă, maxim 2000-3000)
LISTA_PRODUSE_ID = [
    "1005008384803828", 
    "1005007341784572",
    "1005010701830877",
    "1005008156418926"
]

def genereaza_semnatura(parametri, secret):
    sir_sortat = "".join(f"{k}{v}" for k, v in sorted(parametri.items()))
    sir_final = f"{secret}{sir_sortat}{secret}"
    return hashlib.md5(sir_final.encode("utf-8")).hexdigest().upper()

def obtine_date_produs(id_uri_produse):
    # Folosim gateway-ul stabil global
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
        return raspuns.json()
    except Exception as e:
        print(f"Eroare API: {e}")
        return None

def genereaza_pagina_produs_seo(prod):
    """Creează o pagină HTML independentă și perfect optimizată SEO pentru Google"""
    os.makedirs("produse", exist_ok=True)
    
    titlu_curat = prod["titlu"].replace('"', '&quot;')
    descriere_seo = f"Cumpără {titlu_curat} la cel mai bun preț de {prod['pret']} {prod['valuta']}. Vezi recenzii, imagini și oferta de afiliat AliExpress."

    html_content = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titlu_curat} - Cel Mai Bun Preț: {prod['pret']} {prod['valuta']}</title>
    <meta name="description" content="{descriere_seo}">
    <script src="https://jsdelivr.net"></script>
    <link rel="stylesheet" href="https://cloudflare.com">
    
    <!-- Meta-taguri SEO OpenGraph pentru Facebook/WhatsApp/Google -->
    <meta property="og:title" content="{titlu_curat}">
    <meta property="og:description" content="{descriere_seo}">
    <meta property="og:image" content="{prod['imagine']}">
    <meta property="og:type" content="product">
</head>
<body class="bg-gray-50 text-gray-900 font-sans">
    <header class="bg-white shadow-sm py-4 mb-8">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <a href="../index.html" class="text-xl font-bold text-orange-500"><i class="fa-solid fa-arrow-left"></i> Înapoi la Catalog</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-6 bg-white rounded-3xl shadow-xs border border-gray-100 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
            <img src="{prod['imagine']}" alt="{titlu_curat}" class="w-full h-auto rounded-2xl object-cover shadow-sm">
        </div>
        <div class="flex flex-col justify-between">
            <div>
                <h1 class="text-xl sm:text-2xl font-black text-gray-900 mb-4 leading-tight">{prod['titlu']}</h1>
                <p class="text-sm text-gray-500 mb-2">ID Produs: <span class="font-mono text-xs">{prod['id']}</span></p>
                <div class="inline-block bg-red-50 text-red-700 px-4 py-2 rounded-2xl font-bold text-xl mb-6">
                    Preț: {prod['pret']} {prod['valuta']}
                </div>
            </div>
            
            <a href="{prod['link_afiliat']}" target="_blank" rel="noopener noreferrer nofollow" class="w-full bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white font-extrabold text-center py-4 rounded-2xl transition-all shadow-md block text-lg">
                Vezi Oferta pe AliExpress <i class="fa-solid fa-up-right-from-square ml-2 text-sm"></i>
            </a>
        </div>
    </main>
</body>
</html>"""

    with open(f"produse/{prod['id']}.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def porneste_actualizarea():
    print("Curățare fișiere vechi și inițiere import API...")
    rezultate_noi = []
    
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
                            "valuta": prod.get("target_sale_price_currency", "USD"),
                            "link_afiliat": prod.get("promotion_link"),
                            "imagine": prod.get("product_main_image_url")
                        }
                        rezultate_noi.append(item)
                        # Generăm automat fișierul HTML pentru SEO
                        genereaza_pagina_produs_seo(item)
            except Exception as e:
                print(f"Eroare la procesarea structurii: {e}")
        
        time.sleep(1.5)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(rezultate_noi, f, indent=4, ensure_ascii=False)
    
    print(f"Sincronizare finalizată cu succes pentru {len(rezultate_noi)} produse.")

if __name__ == "__main__":
    if not SECRET:
        print("EROARE CRITICĂ: Lipsește secretul de securitate ALI_SECRET!")
    else:
        porneste_actualizarea()
