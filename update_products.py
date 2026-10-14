<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SellMarketON - Catalog Oferte AliExpress</title>
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; background-color: #f9fafb; color: #111827; margin: 0; padding: 0; }
        header { background-color: white; border-bottom: 1px solid #f3f4f6; padding: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: 900; color: #f97316; text-decoration: none; }
        .logo span { color: #111827; }
        main { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .hero { text-align: center; padding: 30px 0; }
        .hero h1 { font-size: 32px; font-weight: 800; margin-bottom: 10px; }
        .hero p { color: #6b7280; font-size: 16px; margin: 0; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(245px, 1fr)); gap: 20px; padding: 20px 0; }
        .card { background: white; border: 1px solid #f3f4f6; border-radius: 16px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.02); transition: transform 0.2s; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .img-container { position: relative; padding-top: 100%; background: #f3f4f6; }
        .img-container img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; }
        .info { padding: 15px; flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between; }
        .title { font-size: 14px; font-weight: 600; color: #1f2937; margin: 0 0 10px 0; text-decoration: none; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; height: 40px; }
        .title:hover { color: #f97316; }
        .price-row { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }
        .price { font-size: 18px; font-weight: 900; color: #dc2626; }
        .btn { background: #f97316; color: white; padding: 8px 14px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: 700; transition: background 0.2s; }
        .btn:hover { background: #ea580c; }
    </style>
</head>
<body>

    <header>
        <div class="nav-container">
            <a href="index.html" class="logo">SellMarket<span>ON</span></a>
        </div>
    </header>

    <main>
        <section class="hero">
            <h1>Catalog Produse AliExpress</h1>
            <p>Cele mai bune oferte de marketing afiliat selectate special pentru tine.</p>
        </section>

        <!-- Catalogul tau real de produse -->
        <div id="productsGrid" class="grid">
            
            <!-- PRODUSUL 1: Modifică datele de mai jos cu produsul tău real -->
            <div class="card">
                <div class="img-container">
                    <!-- Aici pui linkul imaginii oficiale oferit de AliExpress Portals (care se termina in .jpg) -->
                    <img src="https://alicdn.com" alt="Produs 1">
                </div>
                <div class="info">
                    <!-- Aici scrii titlul real al produsului tau -->
                    <a href="https://aliexpress.com" target="_blank" rel="noopener noreferrer nofollow" class="title">Încărcător Auto Rapid Baseus 65W USB Type C Inteligent</a>
                    <div class="price-row">
                        <!-- Prețul estimat. Când vizitatorul dă click, pe AliExpress va vedea prețul redus din acea zi -->
                        <span class="price">12.99 EUR</span>
                        <a href="https://aliexpress.com" target="_blank" rel="noopener noreferrer nofollow" class="btn">Cumpără</a>
                    </div>
                </div>
            </div>

            <!-- PRODUSUL 2: Al doilea produs real al tău -->
            <div class="card">
                <div class="img-container">
                    <img src="https://alicdn.com" alt="Produs 2">
                </div>
                <div class="info">
                    <a href="https://aliexpress.com" target="_blank" rel="noopener noreferrer nofollow" class="title">Brățară Inteligentă Fitness Monitorizare Ritm Cardiac și Somn</a>
                    <div class="price-row">
                        <span class="price">19.50 EUR</span>
                        <a href="https://aliexpress.com" target="_blank" rel="noopener noreferrer nofollow" class="btn">Cumpără</a>
                    </div>
                </div>
            </div>

        </div>
    </main>

</body>
</html>










