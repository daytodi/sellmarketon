import os
import json
import re
from aliexpress_api import AliexpressApi, models

# 1. Configurare chei secrete și API
api_key = os.environ.get('ALIEXPRESS_APP_KEY')
api_secret = os.environ.get('ALIEXPRESS_APP_SECRET')
tracking_id = "ID_TAU_DE_AFILIAT" # Pune ID-ul tău de afiliat AliExpress aici

aliexpress = AliexpressApi(api_key, api_secret, models.Language.EN, models.Currency.EUR, tracking_id)

# Funcție simplă pentru a transforma titlul produsului într-un link frumos (SEO URL)
# Exemplu: "Ceas Inteligent Rezistent la Apă!" -> "ceas-inteligent-rezistent-la-apa"
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

# 2. Creăm folderul pentru paginile individuale dacă nu există
os.makedirs('produse', existent_ok=True)

print("Se descarcă produsele din AliExpress...")
# Preluăm produsele (poți repeta cererea pentru categorii diferite ca să strângi 5000)
produse_ali = aliexpress.get_hot_products(keywords="gadgets", page_size=50) 

sitemap_links = []
produse_pentru_homepage = []

# 3. Șablonul HTML pentru PAGINA INDIVIDUALĂ a fiecărui produs
TEMPLATE_PRODUS = """<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titlu} | SellMarketON</title>
    <meta name="description" content="Cumpără {titlu} la cel mai bun preț pe SellMarketON. Reduceri exclusive AliExpress, poze și detalii tehnice comerciale.">
    <link rel="stylesheet" href="../style.css"> <!-- Stilul tău global -->
</head>
<body>
    <header>
        <a href="../index.html">⬅️ Înapoi la SellMarketON</a>
    </header>
    
    <main class="product-container">
        <div class="product-image">
            <img src="{imagine_url}" alt="{titlu}">
        </div>
        <div class="product-details">
            <h1>{titlu}</h1>
            <p class="price">Preț: {pret} EUR</p>
            <a href="{link_afiliat}" target="_blank" rel="nofollow sponsored" class="buy-button">
                Vezi Oferta pe AliExpress 🛒
            </a>
        </div>
    </main>
</body>
</html>
"""

# 4. Generarea automată a celor 5.000 de pagini separate
for prod in Aegean_ali:
    titlu_curat = prod.product_title
    url_prietenos = slugify(titlu_curat) + "-" + str(prod.product_id) + ".html"
    cale_fisier = os.path.join('produse', url_prietenos)
    
    # Completăm șablonul cu datele acestui produs specific
    html_produs = TEMPLATE_PRODUS.format(
        titlu=titlu_curat,
        imagine_url=prod.product_main_image_url,
        pret=prod.target_sale_price,
        link_afiliat=prod.promotion_link
    )
    
    # Salvăm pagina fizică pe GitHub (.html separat!)
    with open(cale_fisier, 'w', encoding='utf-8') as f:
        f.write(html_produs)
        
    # Salvăm link-ul pentru sitemap (SEO) și pentru prima pagină
    sitemap_links.append(f"https://github.io{url_prietenos}")
    produse_pentru_homepage.append({
        "titlu": titlu_curat,
        "url": f"produse/{url_prietenos}",
        "imagine": prod.product_main_image_url,
        "pret": prod.target_sale_price
    })

# 5. Generăm și fișierul sitemap.xml automat pentru Google
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://sitemaps.org">\n')
    for link in sitemap_links:
        f.write(f'  <url><loc>{link}</loc><changefreq>daily</changefreq></url>\n')
    f.write('</urlset>')

# 6. Actualizăm și lista globală JSON pentru index.html (dacă ai nevoie de ea)
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(produse_pentru_homepage, f, indent=4, ensure_ascii=False)

print(f"Succes! S-au generat paginile individuale și sitemap-ul.")

