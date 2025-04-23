import csv
from colorsys import rgb_to_hls

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = rgb_to_hls(r, g, b)
    return (h * 360, s * 100, l * 100)

def hsl_distance(hsl1, hsl2, hue_weight=2.0, sat_weight=1.0, light_weight=1.0):
    h1, s1, l1 = hsl1
    h2, s2, l2 = hsl2
    dh = min(abs(h1 - h2), 360 - abs(h1 - h2)) / 180.0
    ds = abs(s1 - s2) / 100.0
    dl = abs(l1 - l2) / 100.0
    return (hue_weight * dh**2 + sat_weight * ds**2 + light_weight * dl**2) ** 0.5

# Reference basic colors
basic_colors = {
    
    # neutrals
    "White": "#ffffff",
    "Light Gray": "#c0c0c0",
    "Gray": "#808080",
    "Dark Gray": "#505050",
    "Black": "#000000",

    # reds
    "Light Gray Red": "#d7abab",
    "Light Muted Red": "#c86464",
    "Bright Red": "#de1212",

    "Gray Red": "#8b6868",
    "Muted Red": "#8e4444",
    "Deep Red": "#890f0f",

    "Dark Gray Red": "#362e2e",
    "Dark Muted Red": "#432222",
    "Dark Red": "#360707",

    # oranges
    "Light Gray Orange": "#d9bfae",
    "Light Muted Orange": "#c88a64",
    "Bright Orange": "#e27311",

    "Gray Orange": "#8b7768",
    "Muted Orange": "#8e7244",
    "Deep Orange": "#895e0f",

    "Dark Gray Orange": "#36322e",
    "Dark Muted Orange": "#433222",
    "Dark Orange": "#361d07",

    # Amber-Oranges
    "Light Gray Amber-Orange": "#d6c7ac",
    "Light Muted Amber-Orange": "#c8a764",
    "Bright Amber-Orange": "#e49b14",

    "Gray Amber-Orange": "#8b8068",
    "Muted Amber-Orange": "#8e7744",
    "Deep Amber-Orange": "#89680f",

    "Dark Gray Amber-Orange": "#36342e",
    "Dark Muted Amber-Orange": "#433722",
    "Dark Amber-Orange": "#362607",

    # yellows
    "Light Gray Yellow": "#d6d2ac",
    "Light Muted Yellow": "#c8be64",
    "Bright Yellow": "#e4d914",

    "Gray Yellow": "#8b8768",
    "Muted Yellow": "#8e8744",
    "Deep Yellow": "#89830f",

    "Dark Gray Yellow": "#36362e",
    "Dark Muted Yellow": "#433e22",
    "Dark Yellow": "#363307",

    # chartreuse-greens
    "Light Gray Chartreuse-Green": "#c9d6a9",
    "Light Muted Chartreuse-Green": "#aac864",
    "Bright Chartreuse-Green": "#a9e414",

    "Gray Chartreuse-Green": "#7f8b68",
    "Muted Chartreuse-Green": "#728e44",
    "Deep Chartreuse-Green": "#5c890f",

    "Dark Gray Chartreuse-Green": "#33362e",
    "Dark Muted Chartreuse-Green": "#374322",
    "Dark Chartreuse-Green": "#263607",

    # green-yellows
    "Light Gray Green-Yellow": "#bcd6a9",
    "Light Muted Green-Yellow": "#89c864",
    "Bright Green-Yellow": "#5de414",

    "Gray Green-Yellow": "#728b68",
    "Muted Green-Yellow": "#628e44",
    "Deep Green-Yellow": "#36890f",

    "Dark Gray Green-Yellow": "#31362e",
    "Dark Muted Green-Yellow": "#2e4322",
    "Dark Green-Yellow": "#173607",

    # greens
    "Light Gray Green": "#a9d6ab",
    "Light Muted Green": "#64c866",
    "Bright Green": "#14e41b",

    "Gray Green": "#698b68",
    "Muted Green": "#448e45",
    "Deep Green": "#0f8911",

    "Dark Gray Green": "#2e362f",
    "Dark Muted Green": "#224323",
    "Dark Green": "#073609",

    # teals
    "Light Gray Teal": "#acd4d0",
    "Light Muted Teal": "#64c8bc",
    "Bright Teal": "#14e4c5",

    "Gray Teal": "#688b84",
    "Muted Teal": "#448e85",
    "Deep Teal": "#0f897f",

    "Dark Gray Teal": "#2e3636",
    "Dark Muted Teal": "#224341",
    "Dark Teal": "#073630",
    
    # teals
    "Light Gray Teal": "#a4d1cd",
    "Light Muted Teal": "#64c8bc",
    "Bright Teal": "#14e4c5",

    "Gray Teal": "#688b84",
    "Muted Teal": "#448e85",
    "Deep Teal": "#0f897f",

    "Dark Gray Teal": "#2e3636",
    "Dark Muted Teal": "#224341",
    "Dark Teal": "#073630",

    # cyans
    "Light Gray Cyan": "#abd4d8",
    "Light Muted Cyan": "#64bec8",
    "Bright Cyan": "#14e4e4",

    "Gray Cyan": "#68898b",
    "Muted Cyan": "#448c8e",
    "Deep Cyan": "#0f8589",

    "Dark Gray Cyan": "#2e3636",
    "Dark Muted Cyan": "#224143",
    "Dark Cyan": "#073636",

    # turquoises
    "Light Gray Turquoise": "#b0c4da",
    "Light Muted Turquoise": "#649ec8",
    "Bright Turquoise": "#14a6e4",

    "Gray Turquoise": "#687b8b",
    "Muted Turquoise": "#44748e",
    "Deep Turquoise": "#0f6889",

    "Dark Gray Turquoise": "#2e3236",
    "Dark Muted Turquoise": "#223743",
    "Dark Turquoise": "#072536",

    # blues
    "Light Gray Blue": "#b5bade",
    "Light Muted Blue": "#6471c8",
    "Bright Blue": "#1445e4",

    "Gray Blue": "#68708b",
    "Muted Blue": "#44538e",
    "Deep Blue": "#0f2b89",

    "Dark Gray Blue": "#2e2f36",
    "Dark Muted Blue": "#222a43",
    "Dark Blue": "#070f36",

    # purples
    "Light Gray Purple": "#bca7d4",
    "Light Muted Purple": "#9864c8",
    "Bright Purple": "#7214e4",

    "Gray Purple": "#79688b",
    "Muted Purple": "#6d448e",
    "Deep Purple": "#4e0f89",

    "Dark Gray Purple": "#322e36",
    "Dark Muted Purple": "#322243",
    "Dark Purple": "#1c0736",

    # magentas
    "Light Gray Magenta": "#d8b4dc",
    "Light Muted Magenta": "#c364c8",
    "Bright Magenta": "#cc14e4",

    "Gray Magenta": "#89688b",
    "Muted Magenta": "#8e448a",
    "Deep Magenta": "#890f87",

    "Dark Gray Magenta": "#362e36",
    "Dark Muted Magenta": "#432243",
    "Dark Magenta": "#360735",

    # pinks
    "Light Gray Pink": "#daabc6",
    "Light Muted Pink": "#c864a3",
    "Bright Pink": "#e2119c",

    "Gray Pink": "#8b687e",
    "Muted Pink": "#8e4478",
    "Deep Pink": "#890f64",

    "Dark Gray Pink": "#362e33",
    "Dark Muted Pink": "#432235",
    "Dark Pink": "#360725",

    # roses
    "Light Gray Rose": "#daa8be",
    "Light Muted Rose": "#c8648f",
    "Bright Rose": "#e21157",

    "Gray Rose": "#8b6878",
    "Muted Rose": "#8e4467",
    "Deep Rose": "#890f48",

    "Dark Gray Rose": "#362e32",
    "Dark Muted Rose": "#432233",
    "Dark Rose": "#360722",
}

alt_basic_colors = {
    # Neutrals
    "Black": "#000000",
    "White": "#FFFFFF",
    "Gray": "#808080",
    "LightGray": "#D3D3D3",
    "DarkGray": "#505050",
    "Silver": "#C0C0C0",
    "Beige": "#F5F5DC",
    "Brown": "#A52A2A",
    "DarkBrown": "#5C2E00",
    
    # Grayish variants for desaturated hues
    "GreyRed": "#B76D6D",
    "GreyOrange": "#C29E7F",
    "GreyYellow": "#C2C291",
    "GreyGreen": "#789878",
    "GreyBlue": "#66758C",
    "GreyPurple": "#8F7D9D",
    "GreyPink": "#D8A7A7",

    # Reds
    "Red": "#FF0000",
    "DarkRed": "#8B0000",
    "LightRed": "#FF6666",
    "Rose": "#FF007F",
    "Maroon": "#800000",

    # Bridging colors between red & orange
    "Coral": "#FF7F50",
    "Tomato": "#FF6347",
    "Salmon": "#FA8072",
    "LightSalmon": "#FFA07A",
    "Peach": "#FFDAB9",

    # Oranges
    "Orange": "#FFA500",
    "RedOrange": "#FF4500",
    "LightOrange": "#FFB347",
    "DarkOrange": "#CC5500",

    # Pinks
    "Pink": "#FFC0CB",
    "HotPink": "#FF69B4",
    "LightPink": "#FFB6C1",
    "DeepPink": "#FF1493",

    # Bridging colors between pink & yellow
    "PeachPuff": "#FFDAB9",
    "LightGold": "#FFEC8B",
    "ButterYellow": "#F2C14B",
    "GoldenRod": "#DAA520",

    # Yellows
    "Yellow": "#FFFF00",
    "LightYellow": "#FFFFE0",
    "Gold": "#FFD700",

    # Bridging colors between green & yellow
    "LimeGreen": "#99CC33",  
    "OliveGreen": "#708238",  
    "Avocado": "#78A725",
    "MossGreen": "#8A9A5B",
    "EnergiticGreen": "#7FFF00",

    # Greens
    "Green": "#008000",
    "DarkGreen": "#006400",
    "LightGreen": "#90EE90",
    "Lime": "#00FF00",
    "Mint": "#AAF0D1",
    "Olive": "#808000",

     # Bridging colors between green & blue
    "SeaGreen": "#2E8B57",
    "Turquoise": "#40E0D0",
    "Teal": "#008080",
    "MediumTurquoise": "#48D1CC",
    "Aquamarine": "#7FFFD4",

    # Blues
    "Blue": "#0000FF",
    "DarkBlue": "#00008B",
    "LightBlue": "#ADD8E6",
    "SkyBlue": "#87CEEB",
    "Navy": "#000080",

    # Bridging colors between blue & purple
    "SlateBlue": "#6A5ACD",
    "MediumBlue": "#0000CD",
    "RoyalBlue": "#4169E1",
    "Periwinkle": "#CCCCFF",

    # Cyans
    "Cyan": "#00FFFF",
    "Teal": "#008080",
    "LightCyan": "#E0FFFF",

    # Purples
    "Purple": "#800080",
    "Lavender": "#E6E6FA",
    "Violet": "#8F00FF",
    "Indigo": "#4B0082",
}

basic_colors_hsl = {name: rgb_to_hsl(hex_to_rgb(hex_code)) for name, hex_code in basic_colors.items()}

def get_basic_color_name(hex_color):
    target_hsl = rgb_to_hsl(hex_to_rgb(hex_color))
    closest_name = None
    min_distance = float('inf')
    for name, ref_hsl in basic_colors_hsl.items():
        dist = hsl_distance(target_hsl, ref_hsl)
        if dist < min_distance:
            min_distance = dist
            closest_name = name
    return closest_name

# Read and clean CSV
with open("base_colors.csv", newline='', encoding="utf-8") as infile, \
     open("cleaned_colors.csv", "w", newline='', encoding="utf-8") as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(["name", "hex", "basic name"])
    
    for row in reader:
        if len(row) >= 2:
            name, hex_code = row[0], row[1].strip().lower()
            if hex_code.startswith("#") and len(hex_code) == 7:
                basic = get_basic_color_name(hex_code)
                writer.writerow([name, hex_code, basic])
