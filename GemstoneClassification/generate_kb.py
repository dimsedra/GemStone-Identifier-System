import json

classes = ["Alexandrite", "Almandine", "Amazonite", "Amber", "Amethyst", "Ametrine", "Andalusite", "Andradite", "Aquamarine", "Aventurine Green", "Aventurine Yellow", "Benitoite", "Beryl Golden", "Bixbite", "Bloodstone", "Blue Lace Agate", "Carnelian", "Cats Eye", "Chalcedony", "Chalcedony Blue", "Chrome Diopside", "Chrysoberyl", "Chrysocolla", "Chrysoprase", "Citrine", "Coral", "Danburite", "Diamond", "Diaspore", "Dumortierite", "Emerald", "Fluorite", "Garnet Red", "Goshenite", "Grossular", "Hessonite", "Hiddenite", "Iolite", "Jade", "Jasper", "Kunzite", "Kyanite", "Labradorite", "Lapis Lazuli", "Larimar", "Malachite", "Moonstone", "Morganite", "Onyx Black", "Onyx Green", "Onyx Red", "Opal", "Pearl", "Peridot", "Prehnite", "Pyrite", "Pyrope", "Quartz Beer", "Quartz Lemon", "Quartz Rose", "Quartz Rutilated", "Quartz Smoky", "Rhodochrosite", "Rhodolite", "Rhodonite", "Ruby", "Sapphire Blue", "Sapphire Pink", "Sapphire Purple", "Sapphire Yellow", "Scapolite", "Serpentine", "Sodalite", "Spessartite", "Sphene", "Spinel", "Spodumene", "Sunstone", "Tanzanite", "Tigers Eye", "Topaz", "Tourmaline", "Tsavorite", "Turquoise", "Variscite", "Zircon", "Zoisite"]

base_properties = {
    # Beryl family
    "Aquamarine": {"mohs": 7.8, "ri": 1.58, "sg": 2.70},
    "Beryl Golden": {"mohs": 7.8, "ri": 1.58, "sg": 2.70},
    "Bixbite": {"mohs": 7.8, "ri": 1.58, "sg": 2.70},
    "Emerald": {"mohs": 7.8, "ri": 1.58, "sg": 2.71},
    "Goshenite": {"mohs": 7.8, "ri": 1.58, "sg": 2.71},
    "Morganite": {"mohs": 7.8, "ri": 1.58, "sg": 2.80},
    # Corundum family
    "Ruby": {"mohs": 9.0, "ri": 1.76, "sg": 4.00},
    "Sapphire Blue": {"mohs": 9.0, "ri": 1.76, "sg": 4.00},
    "Sapphire Pink": {"mohs": 9.0, "ri": 1.76, "sg": 4.00},
    "Sapphire Purple": {"mohs": 9.0, "ri": 1.76, "sg": 4.00},
    "Sapphire Yellow": {"mohs": 9.0, "ri": 1.76, "sg": 4.00},
    # Quartz family
    "Amethyst": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Ametrine": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Aventurine Green": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Aventurine Yellow": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Bloodstone": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Blue Lace Agate": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Carnelian": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Chalcedony": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Chalcedony Blue": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Chrysoprase": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Citrine": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Jasper": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Onyx Black": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Onyx Green": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Onyx Red": {"mohs": 7.0, "ri": 1.54, "sg": 2.60},
    "Quartz Beer": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Quartz Lemon": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Quartz Rose": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Quartz Rutilated": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Quartz Smoky": {"mohs": 7.0, "ri": 1.54, "sg": 2.65},
    "Tigers Eye": {"mohs": 7.0, "ri": 1.54, "sg": 2.64},
    # Garnet family
    "Almandine": {"mohs": 7.5, "ri": 1.79, "sg": 4.05},
    "Andradite": {"mohs": 6.8, "ri": 1.88, "sg": 3.85},
    "Garnet Red": {"mohs": 7.2, "ri": 1.78, "sg": 3.80},
    "Grossular": {"mohs": 7.0, "ri": 1.74, "sg": 3.60},
    "Hessonite": {"mohs": 7.0, "ri": 1.74, "sg": 3.60},
    "Pyrope": {"mohs": 7.2, "ri": 1.74, "sg": 3.70},
    "Rhodolite": {"mohs": 7.0, "ri": 1.76, "sg": 3.84},
    "Spessartite": {"mohs": 7.0, "ri": 1.81, "sg": 4.15},
    "Tsavorite": {"mohs": 7.0, "ri": 1.74, "sg": 3.60},
    # Others
    "Alexandrite": {"mohs": 8.5, "ri": 1.74, "sg": 3.72},
    "Amazonite": {"mohs": 6.0, "ri": 1.52, "sg": 2.56},
    "Amber": {"mohs": 2.5, "ri": 1.54, "sg": 1.08},
    "Andalusite": {"mohs": 7.5, "ri": 1.63, "sg": 3.15},
    "Benitoite": {"mohs": 6.5, "ri": 1.76, "sg": 3.65},
    "Cats Eye": {"mohs": 8.5, "ri": 1.74, "sg": 3.72},
    "Chrome Diopside": {"mohs": 5.5, "ri": 1.67, "sg": 3.29},
    "Chrysoberyl": {"mohs": 8.5, "ri": 1.74, "sg": 3.72},
    "Chrysocolla": {"mohs": 3.0, "ri": 1.50, "sg": 2.20},
    "Coral": {"mohs": 3.5, "ri": 1.48, "sg": 2.65},
    "Danburite": {"mohs": 7.0, "ri": 1.63, "sg": 3.00},
    "Diamond": {"mohs": 10.0, "ri": 2.42, "sg": 3.52},
    "Diaspore": {"mohs": 6.5, "ri": 1.70, "sg": 3.40},
    "Dumortierite": {"mohs": 8.0, "ri": 1.68, "sg": 3.30},
    "Fluorite": {"mohs": 4.0, "ri": 1.43, "sg": 3.18},
    "Hiddenite": {"mohs": 6.5, "ri": 1.66, "sg": 3.18},
    "Iolite": {"mohs": 7.0, "ri": 1.54, "sg": 2.61},
    "Jade": {"mohs": 6.5, "ri": 1.66, "sg": 3.34},
    "Kunzite": {"mohs": 6.5, "ri": 1.66, "sg": 3.18},
    "Kyanite": {"mohs": 5.0, "ri": 1.71, "sg": 3.60},
    "Labradorite": {"mohs": 6.0, "ri": 1.56, "sg": 2.70},
    "Lapis Lazuli": {"mohs": 5.5, "ri": 1.50, "sg": 2.75},
    "Larimar": {"mohs": 4.5, "ri": 1.59, "sg": 2.80},
    "Malachite": {"mohs": 4.0, "ri": 1.65, "sg": 3.80},
    "Moonstone": {"mohs": 6.0, "ri": 1.52, "sg": 2.58},
    "Opal": {"mohs": 6.0, "ri": 1.45, "sg": 2.10},
    "Pearl": {"mohs": 3.0, "ri": 1.53, "sg": 2.70},
    "Peridot": {"mohs": 6.5, "ri": 1.65, "sg": 3.34},
    "Prehnite": {"mohs": 6.0, "ri": 1.61, "sg": 2.85},
    "Pyrite": {"mohs": 6.0, "ri": 1.80, "sg": 5.00},
    "Rhodochrosite": {"mohs": 4.0, "ri": 1.60, "sg": 3.60},
    "Rhodonite": {"mohs": 6.0, "ri": 1.73, "sg": 3.60},
    "Scapolite": {"mohs": 6.0, "ri": 1.55, "sg": 2.60},
    "Serpentine": {"mohs": 4.0, "ri": 1.56, "sg": 2.60},
    "Sodalite": {"mohs": 5.5, "ri": 1.48, "sg": 2.20},
    "Sphene": {"mohs": 5.0, "ri": 1.90, "sg": 3.52},
    "Spinel": {"mohs": 8.0, "ri": 1.71, "sg": 3.60},
    "Spodumene": {"mohs": 6.5, "ri": 1.66, "sg": 3.18},
    "Sunstone": {"mohs": 6.0, "ri": 1.53, "sg": 2.65},
    "Tanzanite": {"mohs": 6.5, "ri": 1.69, "sg": 3.35},
    "Topaz": {"mohs": 8.0, "ri": 1.62, "sg": 3.53},
    "Tourmaline": {"mohs": 7.0, "ri": 1.62, "sg": 3.06},
    "Turquoise": {"mohs": 5.5, "ri": 1.61, "sg": 2.70},
    "Variscite": {"mohs": 4.5, "ri": 1.56, "sg": 2.50},
    "Zircon": {"mohs": 7.5, "ri": 1.93, "sg": 4.70},
    "Zoisite": {"mohs": 6.5, "ri": 1.69, "sg": 3.35}
}

kb = {}
for c in classes:
    if c in base_properties:
        kb[c] = base_properties[c]
    else:
        # Default rough average for unknown stones
        kb[c] = {"mohs": 6.0, "ri": 1.60, "sg": 3.00}

with open("knowledge_base.json", "w") as f:
    json.dump(kb, f, indent=4)
print("knowledge_base.json created.")
