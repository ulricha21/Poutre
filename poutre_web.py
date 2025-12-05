<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Logiciel de calcul béton armé en ligne - Poutres, Poteaux, Dalles, Escaliers, Réservoirs - Eurocode 2 + Annexe Nationale France">
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
</head>
<body>

<!-- ==================== HEADER ==================== -->
<header class="header">
    <div class="container">
        <div class="logo-section">
            <div class="logo">A</div>
            <div class="brand">
                <h1>Ing. ANDRIAMANAMPISOA</h1>
                <p>Bureau d'Études Structure & Béton Armé</p>
            </div>
        </div>
        <nav class="nav">
            <a href="#accueil">Accueil</a>
            <a href="#logiciel">Logiciel</a>
            <a href="#modules">Modules</a>
            <a href="#contact">Contact</a>
        </nav>
    </div>
</header>

<!-- ==================== HERO ==================== -->
<section id="accueil" class="hero">
    <div class="container">
        <h2>Calculs Béton Armé<br><span class="highlight">Professionnels & Gratuits</span></h2>
        <p class="subtitle">Eurocode 2 + Annexe Nationale France | 9 Modules Complets</p>
        <div class="hero-features">
            <span>✓ Poutres</span>
            <span>✓ Poteaux</span>
            <span>✓ Voiles</span>
            <span>✓ Dalles</span>
            <span>✓ Escaliers</span>
            <span>✓ Réservoirs</span>
        </div>
        <a href="#logiciel" class="btn-primary">LANCER LE LOGICIEL GRATUIT</a>
    </div>
</section>

<!-- ==================== LOGICIEL PRINCIPAL ==================== -->
<section id="logiciel" class="logiciel-section">
    <div class="container">
        <h2 class="section-title">Logiciel de Calcul Béton Armé</h2>
        
        <!-- Onglets des modules -->
        <div class="tabs">
            <button class="tab active" onclick="changerModule('poutre')">Poutres</button>
            <button class="tab" onclick="changerModule('poteau')">Poteaux</button>
            <button class="tab" onclick="changerModule('voile')">Voiles</button>
            <button class="tab" onclick="changerModule('semelle')">Semelles</button>
            <button class="tab" onclick="changerModule('escalier')">Escaliers</button>
            <button class="tab" onclick="changerModule('dalle')">Dalles</button>
            <button class="tab" onclick="changerModule('reservoir')">Réservoirs</button>
            <button class="tab" onclick="changerModule('projet')">📁 Projet</button>
        </div>

        <!-- ========== MODULE POUTRE ========== -->
        <div id="module-poutre" class="module active">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom de la poutre</label>
                        <input type="text" id="p-nom" value="P1">
                    </div>
                    <div class="form-row">
                        <label>Largeur b (cm)</label>
                        <input type="number" id="p-b" value="30" min="15" max="100">
                    </div>
                    <div class="form-row">
                        <label>Hauteur h (cm)</label>
                        <input type="number" id="p-h" value="60" min="20" max="200">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="p-enrob" value="3.5" step="0.5" min="2" max="6">
                    </div>
                    <div class="form-row">
                        <label>Portée L (m)</label>
                        <input type="number" id="p-L" value="7" step="0.5" min="1" max="20">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="p-fck">
                            <option value="20">C20/25</option>
                            <option value="25">C25/30</option>
                            <option value="30">C30/37</option>
                            <option value="35" selected>C35/45</option>
                            <option value="40">C40/50</option>
                            <option value="45">C45/55</option>
                            <option value="50">C50/60</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures longitudinales (mm)</label>
                        <select id="p-diam-long">
                            <option value="10">HA 10</option>
                            <option value="12">HA 12</option>
                            <option value="14">HA 14</option>
                            <option value="16" selected>HA 16</option>
                            <option value="20">HA 20</option>
                            <option value="25">HA 25</option>
                            <option value="32">HA 32</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Étriers (mm)</label>
                        <select id="p-diam-etr">
                            <option value="6">Ø 6</option>
                            <option value="8" selected>Ø 8</option>
                            <option value="10">Ø 10</option>
                            <option value="12">Ø 12</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges ELU</h3>
                    <div class="form-row">
                        <label>Moment fléchissant Med (kN.m)</label>
                        <input type="number" id="p-Med" value="350" min="0">
                    </div>
                    <div class="form-row">
                        <label>Effort tranchant Ved (kN)</label>
                        <input type="number" id="p-Ved" value="220" min="0">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🔩 Attentes (optionnel)</h3>
                    <div class="form-row">
                        <label><input type="checkbox" id="p-attente-gauche"> Attente gauche (poteau/voile)</label>
                    </div>
                    <div class="form-row">
                        <label><input type="checkbox" id="p-attente-droite"> Attente droite (poteau/voile)</label>
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerPoutre()">CALCULER LA POUTRE</button>

            <!-- Résultats -->
            <div id="resultats-poutre" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-poutre-contenu"></div>
                
                <!-- Propositions armatures -->
                <div class="propositions" id="propositions-poutre"></div>

                <!-- Dessin coupe -->
                <div class="dessins">
                    <h4>Coupe transversale</h4>
                    <div id="coupe-poutre" class="dessin-container"></div>
                    
                    <h4>Vue longitudinale</h4>
                    <div id="longitudinal-poutre" class="dessin-container"></div>
                </div>

                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('poutre')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('poutre')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE POTEAU ========== -->
        <div id="module-poteau" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom du poteau</label>
                        <input type="text" id="pt-nom" value="PT1">
                    </div>
                    <div class="form-row">
                        <label>Type de section</label>
                        <select id="pt-type">
                            <option value="rect">Rectangulaire</option>
                            <option value="circ">Circulaire</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Largeur a (cm)</label>
                        <input type="number" id="pt-a" value="40" min="20">
                    </div>
                    <div class="form-row">
                        <label>Hauteur b (cm)</label>
                        <input type="number" id="pt-b" value="40" min="20">
                    </div>
                    <div class="form-row">
                        <label>Hauteur libre L0 (m)</label>
                        <input type="number" id="pt-L0" value="3.0" step="0.1">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="pt-enrob" value="3.5" step="0.5">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="pt-fck">
                            <option value="25">C25/30</option>
                            <option value="30">C30/37</option>
                            <option value="35" selected>C35/45</option>
                            <option value="40">C40/50</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures longitudinales (mm)</label>
                        <select id="pt-diam-long">
                            <option value="12">HA 12</option>
                            <option value="14">HA 14</option>
                            <option value="16" selected>HA 16</option>
                            <option value="20">HA 20</option>
                            <option value="25">HA 25</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Cadres/Épingles (mm)</label>
                        <select id="pt-diam-etr">
                            <option value="6">Ø 6</option>
                            <option value="8" selected>Ø 8</option>
                            <option value="10">Ø 10</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges ELU</h3>
                    <div class="form-row">
                        <label>Effort normal Ned (kN)</label>
                        <input type="number" id="pt-Ned" value="1500" min="0">
                    </div>
                    <div class="form-row">
                        <label>Moment en tête Mtête (kN.m)</label>
                        <input type="number" id="pt-Mtete" value="50" min="0">
                    </div>
                    <div class="form-row">
                        <label>Moment en pied Mpied (kN.m)</label>
                        <input type="number" id="pt-Mpied" value="30" min="0">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🔧 Conditions d'appui</h3>
                    <div class="form-row">
                        <label>Condition en tête</label>
                        <select id="pt-cond-tete">
                            <option value="libre">Libre</option>
                            <option value="articulé" selected>Articulé</option>
                            <option value="encastré">Encastré</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Condition en pied</label>
                        <select id="pt-cond-pied">
                            <option value="articulé">Articulé</option>
                            <option value="encastré" selected>Encastré</option>
                        </select>
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerPoteau()">CALCULER LE POTEAU</button>

            <div id="resultats-poteau" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-poteau-contenu"></div>
                <div class="propositions" id="propositions-poteau"></div>
                <div class="dessins">
                    <h4>Coupe transversale</h4>
                    <div id="coupe-poteau" class="dessin-container"></div>
                    <h4>Vue en élévation</h4>
                    <div id="elevation-poteau" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('poteau')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('poteau')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE VOILE ========== -->
        <div id="module-voile" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom du voile</label>
                        <input type="text" id="v-nom" value="V1">
                    </div>
                    <div class="form-row">
                        <label>Longueur L (m)</label>
                        <input type="number" id="v-L" value="4" step="0.1" min="1">
                    </div>
                    <div class="form-row">
                        <label>Hauteur H (m)</label>
                        <input type="number" id="v-H" value="3" step="0.1" min="2">
                    </div>
                    <div class="form-row">
                        <label>Épaisseur e (cm)</label>
                        <input type="number" id="v-e" value="20" min="15" max="40">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="v-enrob" value="3" step="0.5">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="v-fck">
                            <option value="25">C25/30</option>
                            <option value="30" selected>C30/37</option>
                            <option value="35">C35/45</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Armatures verticales</label>
                        <select id="v-diam-vert">
                            <option value="10">HA 10</option>
                            <option value="12" selected>HA 12</option>
                            <option value="14">HA 14</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Armatures horizontales</label>
                        <select id="v-diam-horiz">
                            <option value="8">HA 8</option>
                            <option value="10" selected>HA 10</option>
                            <option value="12">HA 12</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges ELU</h3>
                    <div class="form-row">
                        <label>Effort normal Ned (kN/m)</label>
                        <input type="number" id="v-Ned" value="500">
                    </div>
                    <div class="form-row">
                        <label>Effort horizontal Hed (kN)</label>
                        <input type="number" id="v-Hed" value="150">
                    </div>
                    <div class="form-row">
                        <label>Moment en base Med (kN.m)</label>
                        <input type="number" id="v-Med" value="200">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🪟 Ouvertures (optionnel)</h3>
                    <div class="form-row">
                        <label><input type="checkbox" id="v-ouverture"> Avec ouverture</label>
                    </div>
                    <div class="form-row">
                        <label>Largeur ouverture (cm)</label>
                        <input type="number" id="v-ouv-L" value="120">
                    </div>
                    <div class="form-row">
                        <label>Hauteur ouverture (cm)</label>
                        <input type="number" id="v-ouv-H" value="210">
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerVoile()">CALCULER LE VOILE</button>

            <div id="resultats-voile" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-voile-contenu"></div>
                <div class="dessins">
                    <h4>Vue en plan du voile</h4>
                    <div id="plan-voile" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('voile')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('voile')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE SEMELLE ========== -->
        <div id="module-semelle" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom de la semelle</label>
                        <input type="text" id="s-nom" value="S1">
                    </div>
                    <div class="form-row">
                        <label>Type de semelle</label>
                        <select id="s-type">
                            <option value="isolee">Isolée centrée</option>
                            <option value="excentree">Isolée excentrée</option>
                            <option value="filante">Filante</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Dimension poteau a (cm)</label>
                        <input type="number" id="s-a" value="40">
                    </div>
                    <div class="form-row">
                        <label>Dimension poteau b (cm)</label>
                        <input type="number" id="s-b" value="40">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="s-enrob" value="5">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🏔️ Sol</h3>
                    <div class="form-row">
                        <label>Contrainte admissible σsol (MPa)</label>
                        <input type="number" id="s-sigma" value="0.25" step="0.05" min="0.1">
                    </div>
                    <div class="form-row">
                        <label>Profondeur d'ancrage (m)</label>
                        <input type="number" id="s-prof" value="1.0" step="0.1">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="s-fck">
                            <option value="25" selected>C25/30</option>
                            <option value="30">C30/37</option>
                            <option value="35">C35/45</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures (mm)</label>
                        <select id="s-diam">
                            <option value="10">HA 10</option>
                            <option value="12" selected>HA 12</option>
                            <option value="14">HA 14</option>
                            <option value="16">HA 16</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges ELS</h3>
                    <div class="form-row">
                        <label>Effort normal Nser (kN)</label>
                        <input type="number" id="s-Nser" value="800">
                    </div>
                    <div class="form-row">
                        <label>Moment Mser (kN.m)</label>
                        <input type="number" id="s-Mser" value="50">
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerSemelle()">CALCULER LA SEMELLE</button>

            <div id="resultats-semelle" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-semelle-contenu"></div>
                <div class="dessins">
                    <h4>Vue en plan</h4>
                    <div id="plan-semelle" class="dessin-container"></div>
                    <h4>Coupe</h4>
                    <div id="coupe-semelle" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('semelle')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('semelle')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE ESCALIER ========== -->
        <div id="module-escalier" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom de l'escalier</label>
                        <input type="text" id="e-nom" value="ESC1">
                    </div>
                    <div class="form-row">
                        <label>Type d'escalier</label>
                        <select id="e-type">
                            <option value="droit">Droit</option>
                            <option value="balance">Balancé</option>
                            <option value="helicoidal">Hélicoïdal</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Hauteur à franchir H (m)</label>
                        <input type="number" id="e-H" value="3.0" step="0.1" min="2">
                    </div>
                    <div class="form-row">
                        <label>Longueur en plan L (m)</label>
                        <input type="number" id="e-L" value="4.5" step="0.1">
                    </div>
                    <div class="form-row">
                        <label>Largeur de volée (cm)</label>
                        <input type="number" id="e-larg" value="120" min="80" max="200">
                    </div>
                    <div class="form-row">
                        <label>Épaisseur paillasse (cm)</label>
                        <input type="number" id="e-ep" value="18" min="12" max="25">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🪜 Marches</h3>
                    <div class="form-row">
                        <label>Hauteur marche h (cm)</label>
                        <input type="number" id="e-hm" value="17" min="14" max="21">
                    </div>
                    <div class="form-row">
                        <label>Giron g (cm)</label>
                        <input type="number" id="e-g" value="28" min="24" max="35">
                    </div>
                    <div class="form-row">
                        <label>Nombre de marches</label>
                        <input type="number" id="e-nb" value="18" min="5" max="25" readonly>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="e-fck">
                            <option value="25" selected>C25/30</option>
                            <option value="30">C30/37</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures principales</label>
                        <select id="e-diam">
                            <option value="10">HA 10</option>
                            <option value="12" selected>HA 12</option>
                            <option value="14">HA 14</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges</h3>
                    <div class="form-row">
                        <label>Charge permanente G (kN/m²)</label>
                        <input type="number" id="e-G" value="6" step="0.5">
                    </div>
                    <div class="form-row">
                        <label>Charge exploitation Q (kN/m²)</label>
                        <input type="number" id="e-Q" value="2.5" step="0.5">
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerEscalier()">CALCULER L'ESCALIER</button>

            <div id="resultats-escalier" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-escalier-contenu"></div>
                <div class="dessins">
                    <h4>Vue en élévation</h4>
                    <div id="elevation-escalier" class="dessin-container"></div>
                    <h4>Coupe paillasse</h4>
                    <div id="coupe-escalier" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('escalier')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('escalier')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE DALLE ========== -->
        <div id="module-dalle" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom de la dalle</label>
                        <input type="text" id="d-nom" value="D1">
                    </div>
                    <div class="form-row">
                        <label>Type de dalle</label>
                        <select id="d-type">
                            <option value="pleine">Pleine</option>
                            <option value="nervuree">Nervurée</option>
                            <option value="champignon">Champignon</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Portée Lx (m)</label>
                        <input type="number" id="d-Lx" value="5" step="0.1">
                    </div>
                    <div class="form-row">
                        <label>Portée Ly (m)</label>
                        <input type="number" id="d-Ly" value="6" step="0.1">
                    </div>
                    <div class="form-row">
                        <label>Épaisseur h (cm)</label>
                        <input type="number" id="d-h" value="20" min="12" max="35">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="d-enrob" value="3">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🔗 Conditions d'appui</h3>
                    <div class="form-row">
                        <label>Appui côté Lx (gauche)</label>
                        <select id="d-app-Lx1">
                            <option value="simple">Appui simple</option>
                            <option value="encastre">Encastré</option>
                            <option value="libre">Libre</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Appui côté Lx (droite)</label>
                        <select id="d-app-Lx2">
                            <option value="simple">Appui simple</option>
                            <option value="encastre">Encastré</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Appui côté Ly (bas)</label>
                        <select id="d-app-Ly1">
                            <option value="simple">Appui simple</option>
                            <option value="encastre">Encastré</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Appui côté Ly (haut)</label>
                        <select id="d-app-Ly2">
                            <option value="simple">Appui simple</option>
                            <option value="encastre">Encastré</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="d-fck">
                            <option value="25" selected>C25/30</option>
                            <option value="30">C30/37</option>
                            <option value="35">C35/45</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures</label>
                        <select id="d-diam">
                            <option value="8">HA 8</option>
                            <option value="10" selected>HA 10</option>
                            <option value="12">HA 12</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>⚡ Charges</h3>
                    <div class="form-row">
                        <label>Charge permanente G (kN/m²)</label>
                        <input type="number" id="d-G" value="6" step="0.5">
                    </div>
                    <div class="form-row">
                        <label>Charge exploitation Q (kN/m²)</label>
                        <input type="number" id="d-Q" value="2.5" step="0.5">
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerDalle()">CALCULER LA DALLE</button>

            <div id="resultats-dalle" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-dalle-contenu"></div>
                <div class="dessins">
                    <h4>Plan de ferraillage</h4>
                    <div id="plan-dalle" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('dalle')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('dalle')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE RESERVOIR ========== -->
        <div id="module-reservoir" class="module">
            <div class="form-grid">
                <div class="form-section">
                    <h3>📐 Géométrie</h3>
                    <div class="form-row">
                        <label>Nom du réservoir</label>
                        <input type="text" id="r-nom" value="RES1">
                    </div>
                    <div class="form-row">
                        <label>Type de réservoir</label>
                        <select id="r-type">
                            <option value="enterre">Enterré</option>
                            <option value="aerien">Aérien (sur tour)</option>
                            <option value="surelevation">Sur surélévation</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Forme en plan</label>
                        <select id="r-forme">
                            <option value="rect">Rectangulaire</option>
                            <option value="circ">Circulaire</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Longueur/Diamètre L (m)</label>
                        <input type="number" id="r-L" value="6" step="0.5">
                    </div>
                    <div class="form-row">
                        <label>Largeur B (m)</label>
                        <input type="number" id="r-B" value="4" step="0.5">
                    </div>
                    <div class="form-row">
                        <label>Hauteur eau H (m)</label>
                        <input type="number" id="r-H" value="3" step="0.5">
                    </div>
                    <div class="form-row">
                        <label>Revanche (m)</label>
                        <input type="number" id="r-rev" value="0.3" step="0.1">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Épaisseurs</h3>
                    <div class="form-row">
                        <label>Épaisseur parois (cm)</label>
                        <input type="number" id="r-ep-paroi" value="25" min="20" max="40">
                    </div>
                    <div class="form-row">
                        <label>Épaisseur radier (cm)</label>
                        <input type="number" id="r-ep-radier" value="30" min="25" max="50">
                    </div>
                    <div class="form-row">
                        <label>Épaisseur couverture (cm)</label>
                        <input type="number" id="r-ep-couv" value="20" min="15" max="30">
                    </div>
                    <div class="form-row">
                        <label>Enrobage (cm)</label>
                        <input type="number" id="r-enrob" value="4">
                    </div>
                </div>

                <div class="form-section">
                    <h3>🧱 Matériaux</h3>
                    <div class="form-row">
                        <label>Classe béton fck (MPa)</label>
                        <select id="r-fck">
                            <option value="30" selected>C30/37</option>
                            <option value="35">C35/45</option>
                            <option value="40">C40/50</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Classe d'exposition</label>
                        <select id="r-expo">
                            <option value="XC2">XC2</option>
                            <option value="XC3" selected>XC3</option>
                            <option value="XC4">XC4</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <label>Ø Armatures</label>
                        <select id="r-diam">
                            <option value="12">HA 12</option>
                            <option value="14" selected>HA 14</option>
                            <option value="16">HA 16</option>
                        </select>
                    </div>
                </div>

                <div class="form-section">
                    <h3>🌍 Sol (si enterré)</h3>
                    <div class="form-row">
                        <label>Poids volumique terre (kN/m³)</label>
                        <input type="number" id="r-gamma-sol" value="18" step="1">
                    </div>
                    <div class="form-row">
                        <label>Angle de frottement φ (°)</label>
                        <input type="number" id="r-phi" value="30" min="20" max="40">
                    </div>
                    <div class="form-row">
                        <label>Hauteur de remblai (m)</label>
                        <input type="number" id="r-h-remblai" value="2.5" step="0.1">
                    </div>
                </div>
            </div>

            <button class="btn-calcul" onclick="calculerReservoir()">CALCULER LE RÉSERVOIR</button>

            <div id="resultats-reservoir" class="resultats hidden">
                <h3>📊 Résultats du calcul</h3>
                <div class="resultats-grid" id="resultats-reservoir-contenu"></div>
                <div class="dessins">
                    <h4>Coupe transversale</h4>
                    <div id="coupe-reservoir" class="dessin-container"></div>
                    <h4>Plan de ferraillage paroi</h4>
                    <div id="plan-reservoir" class="dessin-container"></div>
                </div>
                <div class="actions-resultats">
                    <button class="btn-secondary" onclick="ajouterAuProjet('reservoir')">➕ Ajouter au projet</button>
                    <button class="btn-secondary" onclick="exporterPDF('reservoir')">📄 Exporter PDF</button>
                </div>
            </div>
        </div>

        <!-- ========== MODULE PROJET ========== -->
        <div id="module-projet" class="module">
            <div class="projet-header">
                <h3>📁 Gestion du Projet</h3>
                <div class="projet-actions">
                    <button class="btn-secondary" onclick="nouveauProjet()">🆕 Nouveau</button>
                    <button class="btn-secondary" onclick="chargerProjet()">📂 Ouvrir</button>
                    <button class="btn-secondary" onclick="sauvegarderProjet()">💾 Sauvegarder</button>
                    <button class="btn-primary" onclick="exporterCahierComplet()">📕 Exporter Cahier Complet PDF</button>
                </div>
            </div>

            <div class="projet-info">
                <div class="form-row">
                    <label>Nom du projet</label>
                    <input type="text" id="projet-nom" value="Bâtiment R+3 - Antananarivo">
                </div>
                <div class="form-row">
                    <label>Client</label>
                    <input type="text" id="projet-client" value="Client XYZ">
                </div>
                <div class="form-row">
                    <label>Date</label>
                    <input type="date" id="projet-date">
                </div>
            </div>

            <h4>Liste des éléments calculés</h4>
            <table class="table-projet" id="table-projet">
                <thead>
                    <tr>
                        <th>N°</th>
                        <th>Type</th>
                        <th>Nom</th>
                        <th>Section</th>
                        <th>As (cm²)</th>
                        <th>Étriers</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="table-projet-body">
                    <tr>
                        <td colspan="7" class="empty-msg">Aucun élément. Ajoutez des éléments depuis les autres onglets.</td>
                    </tr>
                </tbody>
            </table>

            <div class="nomenclature" id="nomenclature">
                <h4>📋 Nomenclature Acier Totale</h4>
                <div id="nomenclature-contenu"></div>
            </div>
        </div>

    </div>
</section>

<!-- ==================== CONTACT ==================== -->
<section id="contact" class="contact-section">
    <div class="container">
        <h2 class="section-title">Contact</h2>
        <div class="contact-grid">
            <div class="contact-info">
                <h3>Ing. ANDRIAMANAMPISOA</h3>
                <p>📍 Lot III 45 Bis Ampasampito - Antananarivo</p>
                <p>📞 +261 34 XX XXX XX</p>
                <p>✉️ contact@andriamanampisoa.mg</p>
                <p>🌐 www.andriamanampisoa-beton.pro</p>
            </div>
            <form class="contact-form" onsubmit="envoyerMessage(event)">
                <input type="text" placeholder="Votre nom" required>
                <input type="email" placeholder="Votre email" required>
                <input type="text" placeholder="Sujet">
                <textarea placeholder="Votre message" rows="5" required></textarea>
                <button type="submit" class="btn-primary">Envoyer le message</button>
            </form>
        </div>
    </div>
</section>

<!-- ==================== FOOTER ==================== -->
<footer class="footer">
    <div class="container">
        <p>© 2025 Ingénieur ANDRIAMANAMPISOA - Bureau d'Études Structure & Béton Armé</p>
        <p>Calculs conformes à l'Eurocode 2 (EN 1992-1-1) + Annexe Nationale France</p>
        <p>Tous droits réservés</p>
    </div>
</footer>

<script src="js/app.js"></script>
</body>
</html>

