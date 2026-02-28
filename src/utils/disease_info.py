"""
disease_info.py
===============
Treatment & medicine database — keys match EXACTLY the 19 PlantVillage
class folder names found in data/raw/plantvillage dataset/color/.

Structure per entry
-------------------
  name               : Human-readable display name
  hindi_name         : Hindi name (bilingual UI)
  description        : Brief disease overview
  cause              : Causative agent
  symptoms           : List of visual symptoms
  chemical_treatment : Recommended chemical products
  organic_treatment  : Organic / biorational alternatives
  prevention         : Cultural & preventive practices

Public helpers
--------------
  get_disease_info(label)  → dict
  get_severity(confidence) → "Mild" | "Moderate" | "Severe"
  list_all_diseases()      → list[str]
"""

from __future__ import annotations

DISEASE_DATABASE: dict[str, dict] = {

    # ─────────────────────── APPLE (4 classes) ───────────────────────

    "Apple___Apple_scab": {
        "name": "Apple Scab",
        "hindi_name": "सेब का पपड़ी रोग",
        "description": (
            "One of the most economically important apple diseases worldwide, "
            "causing olive-brown scabby lesions on leaves and fruit."
        ),
        "cause": "Fungus Venturia inaequalis",
        "symptoms": [
            "Olive-green to brown velvety spots on upper leaf surface",
            "Spots on fruit turning scabby, corky, and cracked",
            "Infected leaves curl and drop early",
            "Severely infected fruitlets drop prematurely",
        ],
        "chemical_treatment": [
            "Captan 50 WP – 2.5 g/L; start at green tip stage",
            "Myclobutanil (Rally 40 WSP) – 0.4 g/L post-infection",
            "Dodine (Syllit) – 1.25 mL/L",
            "Trifloxystrobin – 0.15 g/L for curative action",
        ],
        "organic_treatment": [
            "Lime sulfur 1–2% during dormancy",
            "Copper hydroxide spray at budbreak",
            "Potassium bicarbonate – 5 g/L post-infection",
            "Kaolin clay particle film to deter spore germination",
        ],
        "prevention": [
            "Rake and destroy fallen leaves in autumn",
            "Prune to open canopy for rapid drying after rain",
            "Plant resistant varieties (Enterprise, GoldRush, Liberty)",
            "Apply protective sprays before rain events using disease models",
        ],
    },

    "Apple___Black_rot": {
        "name": "Apple Black Rot",
        "hindi_name": "सेब का काला सड़न",
        "description": (
            "A fungal disease affecting leaves, bark, and fruit; mummified fruit "
            "and cankers on limbs are characteristic signs."
        ),
        "cause": "Fungus Botryosphaeria obtusa",
        "symptoms": [
            "Purple spots on leaves enlarging with a brown center (frog-eye leaf spot)",
            "Fruit rot starting at calyx end, turning black and shriveling",
            "Cankers with sunken, red-brown bark on limbs",
            "Mummified black fruit clinging to branches through winter",
        ],
        "chemical_treatment": [
            "Captan 50 WP – 2.5 g/L from pink stage onwards",
            "Thiophanate-methyl (Topsin-M) – 1.5 g/L",
            "Azoxystrobin + Difenoconazole – 1 mL/L",
        ],
        "organic_treatment": [
            "Prune and burn infected wood; paint wounds with copper paste",
            "Bordeaux paste applied to all pruning cuts",
            "Remove mummified fruit promptly to eliminate inoculum",
        ],
        "prevention": [
            "Prune dead wood and cankers during dry weather",
            "Remove mummified fruit before bloom each spring",
            "Maintain tree vigor with balanced nutrition",
            "Train to open center for sunlight penetration",
        ],
    },

    "Apple___Cedar_apple_rust": {
        "name": "Apple Cedar-Apple Rust",
        "hindi_name": "सेब का देवदार-रस्ट रोग",
        "description": (
            "A fungal disease requiring two hosts (apple/crabapple and eastern red cedar "
            "or juniper) to complete its life cycle; causes bright orange leaf spots."
        ),
        "cause": "Fungus Gymnosporangium juniperi-virginianae",
        "symptoms": [
            "Bright orange-yellow spots on upper leaf surface in spring",
            "Tube-like structures (aecia) on lower leaf surface",
            "Distorted, cupped fruit with orange lesions",
            "Premature leaf drop in severe infections",
        ],
        "chemical_treatment": [
            "Myclobutanil (Rally) – 0.4 g/L at pink through petal fall",
            "Propiconazole (Bumper 41.8 EC) – 0.5 mL/L",
            "Trifloxystrobin + Propiconazole (Stratego) – 0.5 mL/L",
            "Mancozeb – 2.5 g/L as protective spray",
        ],
        "organic_treatment": [
            "Sulfur fungicide – 3 g/L at pink bud stage",
            "Copper hydroxide – 3 g/L as early protectant",
            "Remove nearby juniper/cedar galls before they release spores",
        ],
        "prevention": [
            "Remove eastern red cedar or juniper plants within 300 m if possible",
            "Plant resistant apple varieties (Liberty, Redfree, Enterprise)",
            "Time sprays using petal fall infection periods",
            "Avoid planting susceptible varieties near pine/juniper windbreaks",
        ],
    },

    "Apple___healthy": {
        "name": "Healthy Apple Tree",
        "hindi_name": "स्वस्थ सेब का पेड़",
        "description": "The apple tree appears healthy with no visible disease symptoms.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": [
            "Continue preventive dormant oil spray before budbreak",
            "Apply compost mulch at base to support soil health",
        ],
        "prevention": [
            "Annual dormant pruning for open canopy structure",
            "Rake and destroy leaf litter each autumn",
            "Monitor weekly for pest and disease pressure",
        ],
    },

    # ─────────────────────── BLUEBERRY (1 class) ─────────────────────

    "Blueberry___healthy": {
        "name": "Healthy Blueberry Plant",
        "hindi_name": "स्वस्थ ब्लूबेरी का पौधा",
        "description": "The blueberry plant appears healthy with no visible disease or pest damage.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": [
            "Maintain acidic soil pH (4.5–5.5) with sulfur amendments",
            "Apply pine bark mulch to retain moisture and prevent weeds",
        ],
        "prevention": [
            "Test soil pH annually",
            "Prune canes older than 6 years to encourage vigor",
            "Monitor for spotted wing drosophila during fruiting",
        ],
    },

    # ─────────────────────── CHERRY (2 classes) ──────────────────────

    "Cherry_(including_sour)___Powdery_mildew": {
        "name": "Cherry Powdery Mildew",
        "hindi_name": "चेरी का चूर्णिल आसिता",
        "description": (
            "A fungal disease forming a white powdery coating on young leaves and shoots, "
            "stunting growth and reducing fruit quality."
        ),
        "cause": "Fungus Podosphaera clandestina",
        "symptoms": [
            "White powdery fungal growth on upper leaf surface",
            "Curling, distortion, and stunting of new leaves and shoots",
            "Infected leaves may turn yellow and drop prematurely",
            "Russeting or powdery coating on young fruit",
        ],
        "chemical_treatment": [
            "Myclobutanil (Rally 40 WSP) – 0.4 g/L at first sign",
            "Trifloxystrobin (Flint 50 WG) – 0.14 g/L",
            "Quinoxyfen (Elite) – 0.5 mL/L",
            "Tebuconazole – 1 mL/L for moderate infections",
        ],
        "organic_treatment": [
            "Potassium bicarbonate – 5 g/L spray",
            "Neem oil (3%) + spreader-sticker every 7 days",
            "Sulfur 80 WP – 3 g/L; do not apply when temps > 32°C",
            "Baking soda (sodium bicarbonate) – 5 g/L + horticultural oil",
        ],
        "prevention": [
            "Choose powdery mildew-resistant cherry varieties",
            "Prune to improve air circulation inside canopy",
            "Avoid excess nitrogen (promotes lush, susceptible growth)",
            "Avoid wetting foliage; water at the base",
        ],
    },

    "Cherry_(including_sour)___healthy": {
        "name": "Healthy Cherry Tree",
        "hindi_name": "स्वस्थ चेरी का पेड़",
        "description": "The cherry tree appears healthy with no visible disease or pest damage.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": [
            "Apply dormant copper spray before bud swell as preventive",
        ],
        "prevention": [
            "Annual pruning for canopy openness",
            "Remove dead wood promptly to eliminate overwintering sites",
        ],
    },

    # ─────────────────────── CORN / MAIZE (4 classes) ─────────────────

    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "name": "Corn Gray Leaf Spot (Cercospora)",
        "hindi_name": "मक्का का धूसर पत्ती धब्बा",
        "description": (
            "One of the most yield-limiting maize diseases globally, causing rectangular "
            "tan-gray lesions that can cover entire leaves under warm, humid conditions."
        ),
        "cause": "Fungus Cercospora zeae-maydis",
        "symptoms": [
            "Small, necrotic spots with yellow halos on lower leaves initially",
            "Lesions enlarge into rectangular, grayish-tan strips bounded by leaf veins",
            "Lesions parallel to the leaf veins, up to 4 cm long",
            "Severe blighting of leaf area reducing photosynthesis significantly",
        ],
        "chemical_treatment": [
            "Azoxystrobin + Propiconazole (Quilt Xcel) – 1.5 mL/L at VT/R1",
            "Propiconazole (Tilt 250 EC) – 1 mL/L",
            "Pyraclostrobin + Metconazole (Trivapro) – 1 mL/L",
            "Trifloxystrobin (Stratego) – 0.5 mL/L",
        ],
        "organic_treatment": [
            "Trichoderma harzianum foliar spray",
            "Copper oxychloride – 3 g/L as a protectant",
        ],
        "prevention": [
            "Plant resistant hybrids with high GLS ratings",
            "Till crop residue → reduces overwintering spores (no-till increases risk)",
            "Rotate with non-host crops (soybean, wheat) for ≥1 year",
            "Avoid dense planting; ensure adequate spacing for airflow",
        ],
    },

    "Corn_(maize)___Common_rust_": {
        "name": "Corn Common Rust",
        "hindi_name": "मक्का का साधारण रस्ट",
        "description": (
            "A fungal disease producing characteristic brick-red pustules on both leaf "
            "surfaces, reducing grain yield in susceptible hybrids under cool conditions."
        ),
        "cause": "Fungus Puccinia sorghi",
        "symptoms": [
            "Oval to elongated brick-red/cinnamon pustules on both leaf surfaces",
            "Pustules turn blackish-brown as the season progresses",
            "Yellowing of heavily infected leaves",
            "Premature leaf death in severe cases with susceptible varieties",
        ],
        "chemical_treatment": [
            "Propiconazole (Tilt 250 EC) – 1 mL/L",
            "Azoxystrobin (Quadris) – 1 mL/L",
            "Mancozeb 75 WP – 2.5 g/L at early disease stage",
            "Trifloxystrobin + Propiconazole (Stratego) – 0.5 mL/L",
        ],
        "organic_treatment": [
            "Sulfur-based fungicide spray – 3 g/L",
            "Neem oil (5 mL/L) as a biorational option",
            "Potassium bicarbonate – 3 g/L spray",
        ],
        "prevention": [
            "Plant rust-resistant hybrid varieties",
            "Scout fields regularly from V7 growth stage onwards",
            "Avoid late planting to escape peak spore season",
            "Maintain balanced potassium fertilization to reduce susceptibility",
        ],
    },

    "Corn_(maize)___Northern_Leaf_Blight": {
        "name": "Corn Northern Leaf Blight",
        "hindi_name": "मक्का उत्तरी पत्ती झुलसन",
        "description": (
            "A major fungal disease of maize producing large cigar-shaped lesions that "
            "coalesce to destroy large portions of the leaf canopy."
        ),
        "cause": "Fungus Exserohilum turcicum (syn. Helminthosporium turcicum)",
        "symptoms": [
            "Long (5–15 cm), elliptical, grayish-green to tan lesions",
            "Lesions parallel to leaf veins with wavy, irregular margins",
            "Dark sporulation visible within lesions in humid weather",
            "Premature death of lower leaves progressing rapidly upward",
        ],
        "chemical_treatment": [
            "Propiconazole – 1 mL/L at VT/R1 growth stage",
            "Azoxystrobin + Propiconazole (Quilt Xcel) – 1.5 mL/L",
            "Pyraclostrobin (Headline) – 1 mL/L",
        ],
        "organic_treatment": [
            "Trichoderma harzianum soil/foliar application",
            "Copper-based fungicide as protectant spray",
        ],
        "prevention": [
            "Choose hybrids carrying the Ht resistance gene",
            "Till crop residues deeply after harvest (> 15 cm)",
            "Increase plant spacing for improved air circulation",
            "3-year crop rotation with non-host crops",
        ],
    },

    "Corn_(maize)___healthy": {
        "name": "Healthy Corn Plant",
        "hindi_name": "स्वस्थ मक्का का पौधा",
        "description": "The corn plant appears healthy with no disease or pest damage.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": ["Maintain balanced NPK fertilization"],
        "prevention": [
            "Continue scouting every 7–10 days",
            "Maintain weed-free field conditions throughout the season",
        ],
    },

    # ─────────────────────── GRAPE (4 classes) ───────────────────────

    "Grape___Black_rot": {
        "name": "Grape Black Rot",
        "hindi_name": "अंगूर का काला सड़न",
        "description": (
            "A widespread fungal disease causing leaf spots, shoot lesions, and "
            "shriveled mummified berries (raisins) that remain on the vine."
        ),
        "cause": "Fungus Guignardia bidwellii",
        "symptoms": [
            "Reddish-brown circular spots with dark borders on leaves",
            "Tiny black pycnidia (fruiting bodies) within lesions",
            "Infected berries turn brown, shrivel, and mummify — remain on vine",
            "Black streaks and cankers on young shoots and tendrils",
        ],
        "chemical_treatment": [
            "Myclobutanil (Rally 40 WSP) – 0.4 g/L; best applied at budbreak",
            "Captan 50 WP – 2.5 g/L",
            "Mancozeb + Metalaxyl – 2 g/L",
            "Tebuconazole – 1 mL/L for moderate infection",
        ],
        "organic_treatment": [
            "Bordeaux mixture (4:4:100) applied at budbreak and before bloom",
            "Lime sulfur spray during dormancy",
            "Remove and destroy all mummified berries before budbreak",
        ],
        "prevention": [
            "Prune to open canopy for good airflow and faster drying",
            "Remove mummified berries and infected canes in winter",
            "Apply mulch to prevent rainwater splash carrying spores",
            "Train vines on trellises to avoid ground contact",
        ],
    },

    "Grape___Esca_(Black_Measles)": {
        "name": "Grape Esca (Black Measles)",
        "hindi_name": "अंगूर का एस्का रोग",
        "description": (
            "A serious wood disease complex of grapevines caused by multiple fungi, "
            "leading to internal wood discolouration, leaf scorch, and sudden vine collapse."
        ),
        "cause": "Fungal complex: Phaeomoniella chlamydospora, Phaeoacremonium spp., Fomitiporia mediterranea",
        "symptoms": [
            "Inter-vein leaf chlorosis forming a tiger-stripe pattern",
            "Berries show dark spots or purple-black streaks ('black measles')",
            "Internal wood shows brown/black cross-sectional streaking",
            "Apoplexy: sudden collapse and wilting of entire vine in summer",
        ],
        "chemical_treatment": [
            "No fully curative chemical currently exists",
            "Fosetyl-Al (Aliette) – 2.5 g/L: reduces progression in some trials",
            "Sodium arsenite (where still permitted) – historical trunk paint",
            "Protect pruning wounds with thiophanate-methyl paste",
        ],
        "organic_treatment": [
            "Trichoderma atroviride (Esquive WP) – biological pruning wound protectant",
            "Biophenols / hot water treatment of dormant cuttings (50°C, 30 min)",
            "Grapevine surgery: excavate infected wood and treat with biologicals",
        ],
        "prevention": [
            "Protect all pruning wounds immediately with fungicide or wax",
            "Prune in dry weather to reduce infection window",
            "Use certified disease-free planting material",
            "Remove and destroy severely infected vines to limit spread",
            "Delay pruning as late as possible in winter/early spring",
        ],
    },

    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "name": "Grape Leaf Blight (Isariopsis Leaf Spot)",
        "hindi_name": "अंगूर पत्ती झुलसन",
        "description": (
            "A fungal leaf spot disease forming dark, angular spots on older leaves, "
            "causing premature defoliation and weakening vines before harvest."
        ),
        "cause": "Fungus Pseudocercospora vitis (Isariopsis clavispora)",
        "symptoms": [
            "Dark brown to black angular spots on upper leaf surface",
            "Grayish-brown sporulation visible on the underside of spots",
            "Lesions coalesce causing large dead areas on older leaves",
            "Premature leaf drop reducing fruit quality and vine reserves",
        ],
        "chemical_treatment": [
            "Copper oxychloride – 3 g/L every 10–14 days",
            "Chlorothalonil – 2.5 g/L",
            "Carbendazim – 1 g/L",
        ],
        "organic_treatment": [
            "Bordeaux mixture 0.5–1% as protective spray",
            "Neem oil (3%) + soap emulsifier",
        ],
        "prevention": [
            "Improve canopy management through leaf removal and hedging",
            "Avoid overhead irrigation; use drip systems",
            "Collect and burn fallen leaf litter after harvest",
        ],
    },

    "Grape___healthy": {
        "name": "Healthy Grape Vine",
        "hindi_name": "स्वस्थ अंगूर की बेल",
        "description": "The grape vine appears healthy with no visible disease symptoms.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": [
            "Continue preventive Bordeaux sprays at budbreak as insurance",
        ],
        "prevention": [
            "Prune annually to maintain open canopy structure",
            "Monitor for pests such as grape berry moth and leafhoppers",
        ],
    },

    # ─────────────────────── ORANGE (1 class) ────────────────────────

    "Orange___Haunglongbing_(Citrus_greening)": {
        "name": "Citrus Greening (Huanglongbing / HLB)",
        "hindi_name": "संतरा हरित रोग (HLB)",
        "description": (
            "The most destructive citrus disease in the world, caused by a bacterium "
            "transmitted by the Asian citrus psyllid; there is currently no cure."
        ),
        "cause": "Bacterium Candidatus Liberibacter asiaticus (spread by Diaphorina citri psyllid)",
        "symptoms": [
            "Asymmetric yellowing of leaves (blotchy mottle pattern)",
            "Fruit remains small, lopsided, green at the stylar end at maturity",
            "Bitter, off-flavour juice; aborted seeds inside fruit",
            "Premature fruit drop; dieback of shoots and branches",
        ],
        "chemical_treatment": [
            "Imidacloprid (Confidor) – 1 mL/L: controls the psyllid vector",
            "Thiamethoxam (Actara) – 0.2 g/L: systemic insecticide for psyllid",
            "Dimethoate – 2 mL/L for psyllid adults on flush growth",
            "Foliar zinc/micronutrient sprays to manage symptoms temporarily",
        ],
        "organic_treatment": [
            "Kaolin clay – 30 g/L on flush growth to repel psyllid adults",
            "Spinosad (Entrust) – 0.5 mL/L for psyllid nymph control",
            "Release Tamarixia radiata (parasitic wasp of psyllid) for biocontrol",
            "Remove and destroy infected trees to prevent further spread",
        ],
        "prevention": [
            "Inspect nursery stock carefully; source certified HLB-free budwood",
            "Install 50-mesh insect netting screens in nurseries",
            "Apply preventive psyllid insecticides on every new flush flush",
            "Monitor entire orchard for psyllid colonies every 2 weeks",
            "Remove severely infected trees immediately to reduce inoculum",
        ],
    },

    # ─────────────────────── PEACH (2 classes) ───────────────────────

    "Peach___Bacterial_spot": {
        "name": "Peach Bacterial Spot",
        "hindi_name": "आड़ू जीवाणु धब्बा",
        "description": (
            "A bacterial disease causing water-soaked lesions on leaves and fruit, "
            "leading to significant defoliation and unmarketable fruit under warm, wet conditions."
        ),
        "cause": "Xanthomonas arboricola pv. pruni",
        "symptoms": [
            "Small, angular, water-soaked spots on leaves turning brown to purple",
            "Shot-hole appearance as necrotic tissue falls out",
            "Sunken, dark, water-soaked pits on fruit surface",
            "Severe defoliation reducing fruit size and tree vigor",
        ],
        "chemical_treatment": [
            "Copper hydroxide (Kocide 3000) – 3 g/L; begin at petal fall",
            "Fixed copper + mancozeb tank mix at 10-day intervals",
            "Oxytetracycline (Mycoshield) – 200 ppm (where registered)",
            "Acibenzolar-S-methyl (Actigard) – 0.5 g/L (SAR inducer)",
        ],
        "organic_treatment": [
            "Copper octanoate (Cueva) – 5 mL/L",
            "Bordeaux mixture 0.5% applied at shuck split",
            "Select resistant or tolerant peach varieties at planting",
        ],
        "prevention": [
            "Plant resistant cultivars (Contender, Harrow Beauty, Redhaven)",
            "Avoid overhead sprinkler irrigation",
            "Prune to reduce canopy density and improve airflow",
            "Do not handle or prune trees when wet to avoid spread",
        ],
    },

    "Peach___healthy": {
        "name": "Healthy Peach Tree",
        "hindi_name": "स्वस्थ आड़ू का पेड़",
        "description": "The peach tree appears healthy with no visible disease or pest damage.",
        "cause": "N/A",
        "symptoms": ["No disease symptoms detected"],
        "chemical_treatment": ["No treatment required"],
        "organic_treatment": [
            "Apply dormant copper spray before budbreak for preventive protection",
        ],
        "prevention": [
            "Annual pruning to maintain open vase shape and canopy airflow",
            "Monitor for peach leaf curl and oriental fruit moth regularly",
        ],
    },

    # ─────────────────────── PEPPER (1 class) ────────────────────────

    "Pepper,_bell___Bacterial_spot": {
        "name": "Bell Pepper Bacterial Spot",
        "hindi_name": "शिमला मिर्च जीवाणु धब्बा",
        "description": (
            "A bacterial disease of pepper causing water-soaked spots on leaves and fruit "
            "scabs, reducing marketable yield significantly under warm, rainy weather."
        ),
        "cause": "Xanthomonas campestris pv. vesicatoria (multiple races)",
        "symptoms": [
            "Small, water-soaked spots on leaves turning brown with yellow halo",
            "Irregular lesions coalesce; leaves become ragged and drop",
            "Raised, corky, dark scabs on green fruit surface",
            "Defoliation and sunscald on exposed fruit in severe cases",
        ],
        "chemical_treatment": [
            "Copper hydroxide (Kocide 3000) – 3 g/L; apply preventively",
            "Fixed copper + mancozeb tank mix at 5–7 day intervals",
            "Acibenzolar-S-methyl (Actigard) – 0.5 g/L for SAR induction",
        ],
        "organic_treatment": [
            "Copper octanoate (Cueva) – 5 mL/L",
            "Hot water seed treatment – 52°C for 30 minutes before sowing",
            "Bacillus subtilis (Serenade) foliar spray every 7 days",
        ],
        "prevention": [
            "Use certified pathogen-free seeds or resistant race-specific varieties",
            "Avoid overhead irrigation; use drip or furrow systems",
            "3-year crop rotation away from all solanaceous crops",
            "Sanitize hands and tools between plants in infested fields",
        ],
    },

}


# ─────────────────────────────────────────────────────────
# Public Helper Functions
# ─────────────────────────────────────────────────────────

def get_disease_info(label: str) -> dict:
    """
    Retrieve disease information for a given class label.

    Parameters
    ----------
    label : str
        PlantVillage class folder name, e.g. "Apple___Apple_scab"

    Returns
    -------
    Full disease info dict, or a generic fallback if label not found.
    """
    return DISEASE_DATABASE.get(
        label,
        {
            "name": label.replace("_", " ").replace("  ", " "),
            "hindi_name": "अज्ञात",
            "description": "Detailed information for this class is not yet in the database.",
            "cause": "Unknown",
            "symptoms": ["Consult a local agricultural extension officer."],
            "chemical_treatment": ["Consult a local agronomist for treatment."],
            "organic_treatment": ["Remove affected parts; monitor plant health."],
            "prevention": [
                "Practice good agricultural hygiene.",
                "Use certified disease-free planting material.",
            ],
        },
    )


def get_severity(confidence: float) -> str:
    """
    Map prediction confidence to a human-readable severity label.

    Parameters
    ----------
    confidence : float  — Model probability in [0, 1]

    Returns
    -------
    "Mild" | "Moderate" | "Severe"
    """
    if confidence < 0.75:
        return "Mild"
    elif confidence < 0.90:
        return "Moderate"
    else:
        return "Severe"


def list_all_diseases() -> list[str]:
    """Return all disease labels present in the database."""
    return list(DISEASE_DATABASE.keys())
