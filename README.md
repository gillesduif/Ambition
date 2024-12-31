# Holonoid

Holonoid is een AI-avatar systeem dat holografische technologie combineert met geavanceerde AI-modellen. Het project biedt een interactieve webapp waarbij gebruikers afbeeldingen kunnen uploaden, de afbeelding in real-time manipuleren via een canvas, en gebruik kunnen maken van bewegingsdetectie met een webcam.

---

## Functies
- **AI-gestuurde avatars**: Creëer en bestuur avatars met behulp van AI-modellen.
- **Webapp functionaliteiten**:
  - Upload afbeeldingen.
  - Manipuleer afbeeldingen via een interactieve canvas.
  - Gebruik een webcam voor real-time bewegingsdetectie.
- **Frontend**: Gebouwd met HTML, CSS en JavaScript, met een dynamisch 3x3 raster voor holografische video-integratie.
- **Backend**: Gebouwd met Python en ondersteund door frameworks zoals Flask en TensorFlow.

---

## Front-end Overzicht
De front-end gebruikt een 3x3 rasterlayout voor het renderen van video's die holografische projecties ondersteunen. Het ontwerp past zich dynamisch aan verschillende schermformaten aan en garandeert dat de video's altijd vierkant blijven. Elke cel met een video heeft een specifieke rotatie om de holografische illusie te creëren.

### **Kenmerken**
1. **Volledig responsief design**:
   - Het raster past zich aan aan het kleinste vensterformaat (`vmin`) om consistentie te garanderen.
2. **Rotaties voor holografisch effect**:
   - Top: Geen rotatie.
   - Linkerzijde: 90° rotatie tegen de klok in.
   - Rechterzijde: 90° rotatie met de klok mee.
   - Onderkant: 180° rotatie.
3. **Holografische video-integratie**:
   - Video's worden afgespeeld in specifieke rastercellen om de illusie van een hologram te creëren.

---

## Back-end Overzicht
De back-end zal verantwoordelijk zijn voor:
- **AI-functionaliteiten**:
  - Real-time beeldverwerking en AI-interactie.
  - Gebarenherkenning en stemcommando's.
- **Data-opslag en verwerking**:
  - Beheer van geüploade afbeeldingen en configuratiegegevens.
- **API-integratie**:
  - Verbinden van externe datasets of services voor geavanceerde functionaliteit.

---

## Projectstructuur
```plaintext
holonoid/
├── backend/
│   ├── app.py                 # Hoofd backend-script
│   ├── models/                # AI-modellen
│   ├── utils/                 # Hulpfuncties
│   ├── data/                  # Data-opslag
│   ├── tests/                 # Unit-tests voor backend
│   └── requirements.txt       # Vereiste Python-pakketten
├── frontend/
│   ├── index.html             # Hoofdpagina
│   ├── styles.css             # Styling
│   ├── scripts.js             # Logica
├── shared/
│   ├── assets/                # Gedeelde bestanden (bijv. afbeeldingen)
│   ├── config/                # Configuratiebestanden
├── README.md                  # Projectbeschrijving
└── .gitignore                 # Git-ignore instellingen