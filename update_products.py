import os
import json
import requests
from aliexpress_api import AliexpressApi, models

# Preluăm cheile secrete din GitHub Secrets
APP_KEY = os.environ.get("ALI_APP_KEY")
APP_SECRET = os.environ.get("ALI_APP_SECRET")
TRACKING_ID = "sellmarketon_2026"  # ID-ul tău de urmărire (îl poți schimba cu cel din contul de afiliat)

def genereaza_magazin():
    # Inițializăm API-ul oficial AliExpress
    aliexpress = AliexpressApi(APP_KEY, APP_SECRET, models.Language.EN, models.Currency.USD, TRACKING_ID)
    
    # Creează folderul de produse pentru site dacă nu există
    if not os.path.exists("produse"):
        os.makedirs("produse")
        
    print("Se caută produse reale pe AliExpress...")
    
    try:
        # Căutăm produse reale după un cuvânt cheie ales de tine (ex: 'smartwatch')
        # Schimbă 'smartwatch' cu orice nișă dorești tu (ex: 'jewelry', 'gadgets', 'dresses')
        rezultat = aliexpress.get_products(keywords='smartwatch', page_size=20)
        
        if not rezultat or not hasattr(rezultat, 'products') or not rezultat.products:
            print("Nu s-au găsit produse sau API-ul nu a returnat date.")
            return

        produse_salvate = 0
        
        for prod in resultado.products:
            prod_id = getattr(prod, 'product_id', '')
            titlu = getattr(prod, 'product_title', 'Produs AliExpress')
            pret = getattr(prod, 'target_sale_price', '0.00')
            imagine = getattr(prod, 'product_main_image_url', '')
            
            # Generăm automat link-ul tău de afiliat pentru acest produs
            linkuri_afiliat = aliexpress.get_affiliate_links(getattr(prod, 'product_detail_url', ''))
            link_afiliat = linkuri_afiliat[0].promotion_link if linkuri_afiliat else getattr(prod, 'product_detail_url', '')

            # Structura paginii HTML gata formatată pentru SEO gratuit
            continut_html = f"""<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>{titlu} - Oferta SellMarketON</title>
    <meta name="description" content="Cumpără online {titlu} la prețul special de {pret} USD. Livrare prin AliExpress direct la tine acasă.">
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
        .prod-img {{ max-width: 300px; border-radius: 8px; }}
        .btn-cumpara {{ display: inline-block; background-color: #ff4747; color: white; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 5px; margin-top: 15px; }}
    </style>
</head>
<body>
    <h1>{titlu}</h1>
    <img src="{imagine}" class="prod-img" alt="{titlu}">
    <h2>Preț: {pret} USD</h2>
    <a href="{link_afiliat}" target="_blank" class="btn-cumpara">Cumpără de pe AliExpress</a>
</body>
</html>"""
            
            # Salvăm pagina fizică a produsului
            with open(f"produse/produs-{prod_id}.html", "w", encoding="utf-8") as f:
                f.write(continut_html)
            produse_salvate += 1

        print(f"Succes! S-au generat {produse_salvate} pagini de produse REALE și link-uri de afiliat.")
        
    except Exception as e:
        print(f"A apărut o eroare la interogarea API-ului real: {e}")

if __name__ == "__main__":
    genereaza_magazin()
