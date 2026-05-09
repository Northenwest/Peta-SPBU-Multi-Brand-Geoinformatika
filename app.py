import streamlit as st
import folium
from folium import plugins
import json
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SPBU Bekasi — Dashboard Spasial",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0D0F14; }
[data-testid="stSidebar"] { background: #12151C; border-right: 1px solid #1E2230; }
[data-testid="stSidebar"] .stMarkdown p { color: #8A8FA8; font-size: 12px; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #FFD166 0%, #FF6B6B 50%, #A855F7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 4px;
}
.hero-sub {
    color: #5A5F72;
    font-size: 13px;
    font-weight: 300;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-card {
    background: #12151C;
    border: 1px solid #1E2230;
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.pertamina::before { background: #E8001D; }
.metric-card.shell::before { background: #F5A623; }
.metric-card.vivo::before { background: #1A5EBF; }
.metric-card.bp::before { background: #009B4E; }
.metric-card.total::before { background: linear-gradient(90deg,#FFD166,#FF6B6B); }
.metric-card.nearby::before { background: linear-gradient(90deg,#A855F7,#6B9FE4); }
.metric-num {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #F0F0F5;
    line-height: 1;
}
.metric-lbl {
    font-size: 11px;
    color: #5A5F72;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}
.metric-icon { font-size: 22px; margin-bottom: 6px; }

.brand-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.pill-Pertamina { background: rgba(232,0,29,.15); color: #FF4D5E; border: 1px solid rgba(232,0,29,.3); }
.pill-Shell     { background: rgba(245,166,35,.15); color: #F5A623; border: 1px solid rgba(245,166,35,.3); }
.pill-VIVO      { background: rgba(26,94,191,.15); color: #6B9FE4; border: 1px solid rgba(26,94,191,.3); }
.pill-BP        { background: rgba(0,155,78,.15); color: #4ADE80; border: 1px solid rgba(0,155,78,.3); }

.section-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #3A3F52;
    font-weight: 500;
    margin-bottom: 8px;
    border-bottom: 1px solid #1E2230;
    padding-bottom: 6px;
}

.info-banner {
    background: linear-gradient(135deg, rgba(255,209,102,.08), rgba(168,85,247,.08));
    border: 1px solid rgba(255,209,102,.15);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 12px;
    color: #8A8FA8;
    margin-bottom: 16px;
}

.nearby-banner {
    background: linear-gradient(135deg, rgba(168,85,247,.1), rgba(107,159,228,.1));
    border: 1px solid rgba(168,85,247,.25);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 12px;
    color: #C0A8F0;
    margin-bottom: 12px;
}

.detail-card {
    background: #12151C;
    border: 1px solid #1E2230;
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 8px;
}
.detail-name {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #F0F0F5;
    margin-bottom: 6px;
}
.detail-row {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    margin: 5px 0;
    font-size: 12px;
    color: #8A8FA8;
}
.badge-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.badge { padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 500; }
.badge-atm    { background: rgba(245,166,35,.15); color: #F5A623; }
.badge-toilet { background: rgba(26,94,191,.15);  color: #6B9FE4; }
.badge-247    { background: rgba(0,155,78,.15);   color: #4ADE80; }
.badge-fuel   { background: rgba(255,255,255,.06); color: #8A8FA8; }
.badge-dist   { background: rgba(168,85,247,.15); color: #C084FC; }

.nearby-card {
    background: #12151C;
    border: 1px solid #2A1F45;
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.nearby-rank {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    color: #A855F7;
    font-weight: 700;
    margin-bottom: 4px;
}
.nearby-name {
    font-size: 13px;
    font-weight: 600;
    color: #F0F0F5;
    margin-bottom: 3px;
}
.nearby-dist { font-size: 12px; color: #C084FC; font-weight: 600; }
.nearby-addr { font-size: 11px; color: #5A5F72; }

[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.js-plotly-plot .plotly { background: transparent !important; }

.filter-header {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3A3F52;
    font-weight: 600;
    margin: 14px 0 6px;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── HELPER: Haversine Distance ────────────────────────────────────────────────
def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_and_process():
    with open("SPBU.geojson", "r") as f:
        raw = json.load(f)

    records = []
    for feat in raw["features"]:
        p = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        lat, lng = coords[1], coords[0]

        # Address assembly — fallback to coordinates if no address
        parts = [
            str(p.get("addr:street", "") or ""),
            str(p.get("addr:housenumber", "") or ""),
            str(p.get("addr:subdistrict", "") or ""),
            str(p.get("addr:district", "") or ""),
            str(p.get("addr:city", "") or ""),
            str(p.get("addr:province", "") or ""),
        ]
        address = ", ".join(x for x in parts if x.strip())
        if not address:
            address = f"Koordinat: {lat:.6f}, {lng:.6f}"
        address_display = address  # keep original for display

        # Coordinate string for display
        coord_str = f"{lat:.6f}, {lng:.6f}"

        # Postcode
        postcode = p.get("addr:postcode", "")

        # Fuel types
        fuel_map = {
            "fuel:octane_88":   "Pertalite (88)",
            "fuel:octane_90":   "Oktan 90",
            "fuel:octane_91":   "Oktan 91",
            "fuel:octane_92":   "Pertamax/V-Power (92)",
            "fuel:octane_95":   "Pertamax Turbo (95)",
            "fuel:octane_98":   "Pertamax Racing (98)",
            "fuel:octane_100":  "Oktan 100",
            "fuel:diesel":      "Solar/Diesel",
            "fuel:diesel_1":    "Dexlite",
            "fuel:GTL_diesel":  "Pertamina Dex",
            "fuel:HGV_diesel":  "Solar HGV",
            "fuel:biodiesel":   "Biodiesel",
            "fuel:lpg":         "LPG",
            "fuel:cng":         "CNG",
            "fuel:electricity": "EV Charging",
        }
        fuels = [label for key, label in fuel_map.items() if p.get(key) == "yes"]

        # Payment methods
        payments = []
        if p.get("payment:cash") == "yes":          payments.append("Tunai")
        if p.get("payment:credit_cards") == "yes":  payments.append("Kartu Kredit")
        if p.get("payment:debit_cards") == "yes":   payments.append("Kartu Debit")
        if p.get("payment:qris") == "yes":          payments.append("QRIS")
        if p.get("payment:mastercard") == "yes" and "Kartu Kredit" not in payments: payments.append("Mastercard")
        if p.get("payment:visa") == "yes" and "Kartu Kredit" not in payments:       payments.append("Visa")

        brand = p.get("brand", "Unknown")
        name  = p.get("name") or brand

        # EV charging flag
        has_ev = p.get("fuel:electricity") == "yes"
        has_air = p.get("compressed_air") == "yes"

        records.append({
            "id":          feat.get("id", p.get("@id", "")),
            "name":        name,
            "brand":       brand,
            "operator":    p.get("operator", "-"),
            "address":     address_display,
            "coord_str":   coord_str,
            "postcode":    postcode,
            "district":    p.get("addr:district", "") or p.get("addr:city", ""),
            "city":        p.get("addr:city", ""),
            "province":    p.get("addr:province", ""),
            "hours":       p.get("opening_hours", "-"),
            "phone":       p.get("phone", ""),
            "atm":         p.get("atm") == "yes",
            "toilets":     p.get("toilets") == "yes",
            "is_247":      p.get("opening_hours", "") == "24/7",
            "has_ev":      has_ev,
            "has_air":     has_air,
            "self_service": p.get("self_service", ""),
            "fuels":       fuels,
            "payments":    payments,
            "lat":         lat,
            "lng":         lng,
            "ref":         p.get("ref", ""),
            "has_address": bool(p.get("addr:street", "")),
        })

    return pd.DataFrame(records)

df_all = load_and_process()

BRAND_COLORS = {
    "Pertamina": "#E8001D",
    "Shell":     "#F5A623",
    "VIVO":      "#1A5EBF",
    "BP":        "#009B4E",
    "Unknown":   "#555566",
}
BRAND_ICONS = {
    "Pertamina": "⛽",
    "Shell":     "🐚",
    "VIVO":      "🔵",
    "BP":        "🟢",
}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:20px">⛽ SPBU Bekasi</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Analisis Spasial Multi-Brand</div>', unsafe_allow_html=True)
    st.markdown("---")

    # ── LOKASI USER (NEAREST SPBU) ──
    st.markdown('<div class="filter-header">📍 Lokasi Saya (Cari SPBU Terdekat)</div>', unsafe_allow_html=True)
    user_lat = st.number_input("Latitude:", value=None, placeholder="-6.2500", format="%.6f", label_visibility="visible")
    user_lng = st.number_input("Longitude:", value=None, placeholder="107.0000", format="%.6f", label_visibility="visible")

    n_nearest = st.slider("Tampilkan N SPBU terdekat:", min_value=3, max_value=20, value=5)
    radius_km  = st.slider("Radius pencarian (km):", min_value=1, max_value=30, value=10)

    user_loc_active = user_lat is not None and user_lng is not None

    st.markdown("""
    <div style="font-size:10px;color:#3A3F52;margin-top:4px;line-height:1.5">
    💡 Cara cari koordinat: buka Google Maps → klik kanan lokasi Anda → salin koordinat
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="filter-header">🏷 Filter Brand</div>', unsafe_allow_html=True)
    brands_available = sorted(df_all["brand"].unique())
    selected_brands = st.multiselect(
        "Pilih brand:",
        options=brands_available,
        default=brands_available,
        label_visibility="collapsed",
    )

    st.markdown('<div class="filter-header">🔍 Fasilitas</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        filter_atm     = st.checkbox("🏧 ATM")
        filter_toilet  = st.checkbox("🚻 Toilet")
        filter_ev      = st.checkbox("⚡ EV Charging")
    with col_b:
        filter_247     = st.checkbox("🌙 Buka 24/7")
        filter_phone   = st.checkbox("📞 Telepon")

    st.markdown('<div class="filter-header">📍 Cari Nama / Alamat</div>', unsafe_allow_html=True)
    search_q = st.text_input("Cari:", placeholder="contoh: Ahmad Yani…", label_visibility="collapsed")

    st.markdown('<div class="filter-header">🗺 Tampilan Peta</div>', unsafe_allow_html=True)
    map_style = st.selectbox(
        "Basemap:",
        ["OpenStreetMap (Default)", "CartoDB Positron", "Esri Satellite", "CartoDB Dark Matter"],
        label_visibility="collapsed",
    )
    show_heatmap  = st.checkbox("🔥 Heatmap", value=False)
    show_clusters = st.checkbox("🔵 Clustering", value=False)
    show_fullscreen = st.checkbox("⛶ Fullscreen", value=True)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:10px;color:#3A3F52;line-height:1.6">
    📡 Data: OpenStreetMap (ODbL)<br>
    📅 Diperbarui: Mei 2026<br>
    🏙 Wilayah: Kota & Kab. Bekasi<br>
    🔢 Total: {len(df_all)} lokasi SPBU
    </div>
    """, unsafe_allow_html=True)


# ── FILTERING ─────────────────────────────────────────────────────────────────
df = df_all[df_all["brand"].isin(selected_brands)].copy()
if filter_atm:    df = df[df["atm"]]
if filter_toilet: df = df[df["toilets"]]
if filter_247:    df = df[df["is_247"]]
if filter_phone:  df = df[df["phone"] != ""]
if filter_ev:     df = df[df["has_ev"]]
if search_q.strip():
    q = search_q.strip().lower()
    df = df[df["name"].str.lower().str.contains(q) | df["address"].str.lower().str.contains(q)]

# Compute distances if user location provided
if user_loc_active:
    df["distance_km"] = df.apply(
        lambda r: haversine(user_lat, user_lng, r["lat"], r["lng"]), axis=1
    )
    df_within_radius = df[df["distance_km"] <= radius_km].sort_values("distance_km")
    df_nearest = df_within_radius.head(n_nearest)
else:
    df["distance_km"] = None
    df_nearest = pd.DataFrame()


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">📍 Peta SPBU Multi-Brand Bekasi</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Dashboard Analisis Spasial Bahan Bakar Wilayah Bekasi · Jeremy</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# ── STAT CARDS ────────────────────────────────────────────────────────────────
total = len(df)
brand_counts = df["brand"].value_counts()

cols_cards = st.columns(8)
def metric_card(col, css_class, icon, num, label):
    col.markdown(f"""
    <div class="metric-card {css_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-num">{num}</div>
        <div class="metric-lbl">{label}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(cols_cards[0], "total",     "⛽", total,                          "Total SPBU")
metric_card(cols_cards[1], "pertamina", "🔴", brand_counts.get("Pertamina", 0), "Pertamina")
metric_card(cols_cards[2], "shell",     "🟡", brand_counts.get("Shell", 0),     "Shell")
metric_card(cols_cards[3], "vivo",      "🔵", brand_counts.get("VIVO", 0),      "VIVO")
metric_card(cols_cards[4], "bp",        "🟢", brand_counts.get("BP", 0),        "BP")
metric_card(cols_cards[5], "total",     "🏧", int(df["atm"].sum()),             "Ada ATM")
metric_card(cols_cards[6], "total",     "🌙", int(df["is_247"].sum()),          "Buka 24/7")
metric_card(cols_cards[7], "total",     "⚡", int(df["has_ev"].sum()),          "EV Charging")

st.markdown("<br>", unsafe_allow_html=True)


# ── MAP + DETAIL PANEL ────────────────────────────────────────────────────────
map_col, detail_col = st.columns([3, 1])

with map_col:
    tile_map = {
        "OpenStreetMap (Default)": ("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                                     "© OpenStreetMap contributors"),
        "CartoDB Dark Matter":     ("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                                    "© OpenStreetMap © CartoDB"),
        "CartoDB Positron":        ("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                                    "© OpenStreetMap © CartoDB"),
        "Esri Satellite":          ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                                    "© Esri © OpenStreetMap"),
    }
    tile_url, tile_attr = tile_map[map_style]

    # Center on user if given, else center on Bekasi
    map_center = [user_lat, user_lng] if user_loc_active else [-6.25, 107.00]
    map_zoom = 13 if user_loc_active else 11

    m = folium.Map(
        location=map_center,
        zoom_start=map_zoom,
        tiles=tile_url,
        attr=tile_attr,
    )

    if show_fullscreen:
        plugins.Fullscreen(position="topright").add_to(m)
    plugins.MiniMap(toggle_display=True, position="bottomright").add_to(m)

    if show_heatmap and len(df) > 0:
        heat_data = [[row["lat"], row["lng"]] for _, row in df.iterrows()]
        plugins.HeatMap(heat_data, radius=20, blur=15, max_zoom=13, name="Heatmap").add_to(m)

    if show_clusters:
        marker_layer = plugins.MarkerCluster(name="SPBU Cluster")
    else:
        marker_layer = folium.FeatureGroup(name="SPBU")
    marker_layer.add_to(m)

    # Nearest SPBU group (highlighted)
    nearest_ids = set(df_nearest["id"].tolist()) if user_loc_active and len(df_nearest) > 0 else set()

    for _, row in df.iterrows():
        brand  = row["brand"]
        color  = BRAND_COLORS.get(brand, "#888")
        is_near = row["id"] in nearest_ids

        fuel_html = "".join(
            f'<span style="display:inline-block;background:rgba(255,255,255,.08);border-radius:4px;padding:2px 7px;font-size:10px;margin:2px;color:#aaa">{f}</span>'
            for f in row["fuels"]
        ) or '<span style="color:#555;font-size:11px">Tidak ada data</span>'
        pay_html = ", ".join(row["payments"]) or "-"

        badges = []
        if row["atm"]:     badges.append('<span style="background:rgba(245,166,35,.2);color:#F5A623;padding:2px 7px;border-radius:5px;font-size:10px">🏧 ATM</span>')
        if row["toilets"]: badges.append('<span style="background:rgba(26,94,191,.2);color:#6B9FE4;padding:2px 7px;border-radius:5px;font-size:10px">🚻 Toilet</span>')
        if row["is_247"]:  badges.append('<span style="background:rgba(0,155,78,.2);color:#4ADE80;padding:2px 7px;border-radius:5px;font-size:10px">🌙 24/7</span>')
        if row["has_ev"]:  badges.append('<span style="background:rgba(168,85,247,.2);color:#C084FC;padding:2px 7px;border-radius:5px;font-size:10px">⚡ EV</span>')
        badges_html = " ".join(badges)

        # Distance line in popup
        dist_html = ""
        if row.get("distance_km") is not None:
            dist_html = f'<tr><td style="color:#5A5F72;padding:3px 0">📏 Jarak</td><td style="color:#C084FC;text-align:right;font-weight:600">{row["distance_km"]:.2f} km</td></tr>'

        # Show coord if no real address
        addr_label = row["address"]
        coord_note = "" if row["has_address"] else f'<div style="font-size:10px;color:#3A3F52;margin-top:2px">🗺 {row["coord_str"]}</div>'

        # Pre-compute optional rows to avoid inline ternary in f-string
        phone_tr    = f"<tr><td style='color:#5A5F72;padding:3px 0'>📞 Telepon</td><td style='color:#C0C0D0;text-align:right'>{row['phone']}</td></tr>" if row['phone'] else ""
        operator_tr = f"<tr><td style='color:#5A5F72;padding:3px 0'>🏢 Operator</td><td style='color:#C0C0D0;text-align:right'>{row['operator']}</td></tr>" if row['operator'] != '-' else ""
        ref_tr      = f"<tr><td style='color:#5A5F72;padding:3px 0'>🔢 Ref</td><td style='color:#C0C0D0;text-align:right'>{row['ref']}</td></tr>" if row['ref'] else ""
        dist_header = f'<div style="font-size:10px;color:rgba(255,255,255,.5);margin-top:2px">📏 {row["distance_km"]:.2f} km dari lokasi Anda</div>' if row.get("distance_km") is not None else ""

        popup_html = f"""
        <div style="font-family:'DM Sans',Arial,sans-serif;width:270px;background:#12151C;color:#E0E0E8;border-radius:10px;overflow:hidden">
          <div style="background:{color};padding:10px 14px">
            <div style="font-weight:700;font-size:14px;color:#fff">{row['name']}</div>
            <div style="font-size:11px;color:rgba(255,255,255,.7);margin-top:2px">{brand}</div>
            {dist_header}
          </div>
          <div style="padding:12px 14px">
            <div style="font-size:11px;color:#7A7D8A;margin-bottom:4px">📍 {addr_label}</div>
            {coord_note}
            <table style="width:100%;font-size:11px;border-collapse:collapse;margin-top:8px">
              <tr><td style="color:#5A5F72;padding:3px 0">🕐 Jam Buka</td><td style="color:#C0C0D0;text-align:right">{row['hours']}</td></tr>
              <tr><td style="color:#5A5F72;padding:3px 0">💳 Pembayaran</td><td style="color:#C0C0D0;text-align:right">{pay_html}</td></tr>
              {phone_tr}
              {operator_tr}
              {ref_tr}
              {dist_html}
            </table>
            <div style="margin-top:8px">
              <div style="font-size:10px;color:#3A3F52;text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px">Bahan Bakar</div>
              {fuel_html}
            </div>
            {f'<div style="margin-top:8px;display:flex;gap:4px;flex-wrap:wrap">{badges_html}</div>' if badges else ""}
          </div>
        </div>
        """

        # Highlighted marker for nearest SPBU
        if is_near:
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=11,
                color="#A855F7",
                weight=3,
                fill=True,
                fill_color=color,
                fill_opacity=0.95,
                popup=folium.Popup(popup_html, max_width=290),
                tooltip=folium.Tooltip(f"<b>{row['name']}</b><br><span style='color:{color}'>{brand}</span><br><span style='color:#C084FC'>📏 {row['distance_km']:.2f} km</span>"),
            ).add_to(marker_layer)
        else:
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=7,
                color="#000",
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=290),
                tooltip=folium.Tooltip(f"<b>{row['name']}</b><br><span style='color:{color}'>{brand}</span>"),
            ).add_to(marker_layer)

    # User location marker
    if user_loc_active:
        folium.Marker(
            location=[user_lat, user_lng],
            tooltip="📍 Lokasi Anda",
            popup=folium.Popup(f"<b>Lokasi Anda</b><br>{user_lat:.6f}, {user_lng:.6f}", max_width=200),
            icon=folium.Icon(color="purple", icon="user", prefix="fa"),
        ).add_to(m)

        if radius_km > 0:
            folium.Circle(
                location=[user_lat, user_lng],
                radius=radius_km * 1000,
                color="#A855F7",
                weight=1.5,
                fill=True,
                fill_color="#A855F7",
                fill_opacity=0.05,
                dash_array="6",
                tooltip=f"Radius {radius_km} km",
            ).add_to(m)

    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Legend
    legend_items = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin:5px 0">'
        f'<div style="width:12px;height:12px;border-radius:50%;background:{BRAND_COLORS[b]};flex-shrink:0"></div>'
        f'<span style="font-size:11px">{b} ({brand_counts.get(b,0)})</span></div>'
        for b in ["Pertamina","Shell","VIVO","BP"] if b in brand_counts
    )
    nearby_legend_item = "<div style='margin-top:6px;display:flex;align-items:center;gap:6px'><div style='width:12px;height:12px;border-radius:50%;border:2px solid #A855F7;flex-shrink:0'></div><span style='font-size:11px'>SPBU Terdekat</span></div>" if user_loc_active else ""

    legend_html = f"""
    <div style="position:fixed;bottom:30px;left:20px;z-index:9999;
                background:rgba(12,13,20,.92);backdrop-filter:blur(8px);
                border:1px solid rgba(255,255,255,.1);border-radius:12px;
                padding:12px 16px;font-family:'DM Sans',Arial,sans-serif;color:#ddd;
                box-shadow:0 4px 20px rgba(0,0,0,.5)">
      <div style="font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:#5A5F72;margin-bottom:8px">⛽ Brand SPBU</div>
      {legend_items}
      {nearby_legend_item}
      <div style="border-top:1px solid rgba(255,255,255,.08);margin-top:8px;padding-top:6px;font-size:10px;color:#3A3F52">
        Tampil: {total} dari {len(df_all)} SPBU
      </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    map_data = st_folium(m, width="100%", height=520, returned_objects=["last_object_clicked"])


# ── DETAIL PANEL ──────────────────────────────────────────────────────────────
with detail_col:
    # Nearest SPBU section
    if user_loc_active:
        n_in_radius = len(df_within_radius) if "df_within_radius" in dir() else 0
        st.markdown(f"""
        <div class="nearby-banner">
            📍 <b>{n_in_radius} SPBU</b> dalam radius {radius_km} km dari lokasi Anda
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label">🎯 SPBU Terdekat</div>', unsafe_allow_html=True)
        if len(df_nearest) > 0:
            for rank, (_, r) in enumerate(df_nearest.iterrows(), 1):
                bcolor = BRAND_COLORS.get(r["brand"], "#888")
                addr_short = r["address"] if r["has_address"] else r["coord_str"]
                hours_short = r["hours"] if r["hours"] != "-" else "Tidak diketahui"
                badges_near = []
                if r["atm"]:    badges_near.append("🏧 ATM")
                if r["toilets"]:badges_near.append("🚻 Toilet")
                if r["is_247"]: badges_near.append("🌙 24/7")
                if r["has_ev"]: badges_near.append("⚡ EV")
                badges_near_html = "<div style='margin-top:5px;font-size:10px;color:#6B9FE4'>" + " · ".join(badges_near) + "</div>" if badges_near else ""
                st.markdown(f"""
                <div class="nearby-card" style="border-left: 3px solid {bcolor}">
                  <div class="nearby-rank">#{rank} Terdekat</div>
                  <div class="nearby-name">{r['name']}</div>
                  <div class="nearby-dist">📏 {r['distance_km']:.2f} km</div>
                  <div class="nearby-addr">📍 {addr_short[:60]}{'...' if len(addr_short)>60 else ''}</div>
                  <div class="nearby-addr">🕐 {hours_short}</div>
                  {badges_near_html}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-banner">
                Tidak ada SPBU dalam radius yang ditentukan. Coba perbesar radius.
            </div>
            """, unsafe_allow_html=True)
    else:
        # Donut chart if no user location
        st.markdown('<div class="section-label">📊 Distribusi Brand</div>', unsafe_allow_html=True)
        brand_df_chart = df["brand"].value_counts().reset_index()
        brand_df_chart.columns = ["brand", "count"]
        fig_donut = go.Figure(go.Pie(
            labels=brand_df_chart["brand"],
            values=brand_df_chart["count"],
            hole=0.62,
            marker=dict(
                colors=[BRAND_COLORS.get(b, "#888") for b in brand_df_chart["brand"]],
                line=dict(color="#0D0F14", width=2),
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value} SPBU (%{percent})<extra></extra>",
        ))
        fig_donut.add_annotation(
            text=f"<b>{total}</b><br><span style='font-size:10px'>SPBU</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="#F0F0F5"),
            align="center",
        )
        fig_donut.update_layout(
            showlegend=True,
            legend=dict(font=dict(color="#8A8FA8", size=10), orientation="h", y=-0.1),
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=220,
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # Facility mini stats
    st.markdown('<div class="section-label" style="margin-top:10px">⚡ Statistik Fasilitas</div>', unsafe_allow_html=True)
    fa_col1, fa_col2 = st.columns(2)
    fa_col1.metric("🏧 ATM", int(df["atm"].sum()))
    fa_col2.metric("🚻 Toilet", int(df["toilets"].sum()))
    fa_col3, fa_col4 = st.columns(2)
    fa_col3.metric("🌙 24/7", int(df["is_247"].sum()))
    fa_col4.metric("⚡ EV", int(df["has_ev"].sum()))

# ── CHARTS ROW ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">📈 Analisis Data SPBU</div>', unsafe_allow_html=True)

ch1, ch2, ch3, ch4 = st.columns(4)

brand_df = df["brand"].value_counts().reset_index()
brand_df.columns = ["brand", "count"]

with ch1:
    fig_bar = px.bar(
        brand_df, x="brand", y="count",
        color="brand",
        color_discrete_map=BRAND_COLORS,
        labels={"brand": "", "count": "Jumlah"},
        title="Jumlah SPBU per Brand",
        text="count",
    )
    fig_bar.update_traces(textposition="outside", textfont_color="#F0F0F5")
    fig_bar.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8A8FA8", size=11),
        title_font=dict(color="#F0F0F5", size=13),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#1E2230", zeroline=False),
        margin=dict(t=40, b=0, l=0, r=0),
        height=260,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with ch2:
    hours_df = df["hours"].replace("", "Tidak Diketahui").replace("-", "Tidak Diketahui").value_counts().reset_index()
    hours_df.columns = ["hours", "count"]
    hours_df_top = hours_df.head(7)
    fig_hours = px.bar(
        hours_df_top, x="count", y="hours", orientation="h",
        color="count",
        color_continuous_scale=["#1E2230", "#FFD166"],
        labels={"hours": "", "count": "Jumlah"},
        title="Pola Jam Operasional",
    )
    fig_hours.update_layout(
        showlegend=False, coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8A8FA8", size=10),
        title_font=dict(color="#F0F0F5", size=13),
        xaxis=dict(showgrid=True, gridcolor="#1E2230"),
        yaxis=dict(showgrid=False),
        margin=dict(t=40, b=0, l=0, r=0),
        height=260,
    )
    st.plotly_chart(fig_hours, use_container_width=True, config={"displayModeBar": False})

with ch3:
    fac_data = []
    for brand in brands_available:
        sub = df[df["brand"] == brand]
        if len(sub) == 0: continue
        fac_data.append({
            "Brand":  brand,
            "ATM":    int(sub["atm"].sum()),
            "Toilet": int(sub["toilets"].sum()),
            "24/7":   int(sub["is_247"].sum()),
            "EV":     int(sub["has_ev"].sum()),
        })
    fac_df = pd.DataFrame(fac_data)
    if len(fac_df):
        fac_melted = fac_df.melt(id_vars="Brand", value_vars=["ATM","Toilet","24/7","EV"], var_name="Fasilitas", value_name="Jumlah")
        fig_fac = px.bar(
            fac_melted, x="Brand", y="Jumlah", color="Fasilitas",
            barmode="group",
            color_discrete_map={"ATM":"#F5A623","Toilet":"#6B9FE4","24/7":"#4ADE80","EV":"#A855F7"},
            title="Fasilitas per Brand",
        )
        fig_fac.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8A8FA8", size=11),
            title_font=dict(color="#F0F0F5", size=13),
            legend=dict(font=dict(color="#8A8FA8", size=10), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#1E2230", zeroline=False),
            margin=dict(t=40, b=0, l=0, r=0),
            height=260,
        )
        st.plotly_chart(fig_fac, use_container_width=True, config={"displayModeBar": False})

with ch4:
    # Fuel type coverage across all SPBU
    fuel_map_display = {
        "fuel:octane_88": "Pertalite (88)",
        "fuel:octane_90": "Oktan 90",
        "fuel:octane_92": "Pertamax (92)",
        "fuel:octane_95": "Pertamax Turbo",
        "fuel:octane_98": "Pertamax Racing",
        "fuel:diesel":    "Solar/Diesel",
        "fuel:electricity":"EV Charging",
        "fuel:lpg":       "LPG",
    }
    # Count from raw geojson
    with open("SPBU.geojson", "r") as f:
        raw_geojson = json.load(f)

    fuel_counts = {}
    for key, label in fuel_map_display.items():
        count = sum(1 for feat in raw_geojson["features"]
                    if feat["properties"].get(key) == "yes"
                    and feat["properties"].get("brand", "Unknown") in selected_brands)
        if count > 0:
            fuel_counts[label] = count

    if fuel_counts:
        fuel_df = pd.DataFrame({"Jenis BBM": list(fuel_counts.keys()), "Jumlah": list(fuel_counts.values())})
        fuel_df = fuel_df.sort_values("Jumlah", ascending=True)
        fig_fuel = px.bar(
            fuel_df, x="Jumlah", y="Jenis BBM", orientation="h",
            color="Jumlah",
            color_continuous_scale=["#E8001D", "#FFD166"],
            title="Ketersediaan Jenis BBM",
        )
        fig_fuel.update_layout(
            showlegend=False, coloraxis_showscale=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8A8FA8", size=10),
            title_font=dict(color="#F0F0F5", size=13),
            xaxis=dict(showgrid=True, gridcolor="#1E2230"),
            yaxis=dict(showgrid=False),
            margin=dict(t=40, b=0, l=0, r=0),
            height=260,
        )
        st.plotly_chart(fig_fuel, use_container_width=True, config={"displayModeBar": False})


# ── DATA TABLE ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if user_loc_active and len(df_nearest) > 0:
    with st.expander(f"🎯 Tabel SPBU Terdekat dari Lokasi Anda — {len(df_within_radius)} dalam radius {radius_km} km", expanded=True):
        near_table = df_within_radius[[
            "name", "brand", "address", "coord_str", "distance_km", "hours", "phone", "atm", "toilets", "is_247", "has_ev"
        ]].copy()
        near_table.columns = [
            "Nama SPBU", "Brand", "Alamat", "Koordinat", "Jarak (km)", "Jam Operasional", "Telepon", "ATM", "Toilet", "24/7", "EV"
        ]
        near_table["ATM"]   = near_table["ATM"].map({True:"✅",False:"—"})
        near_table["Toilet"]= near_table["Toilet"].map({True:"✅",False:"—"})
        near_table["24/7"]  = near_table["24/7"].map({True:"✅",False:"—"})
        near_table["EV"]    = near_table["EV"].map({True:"✅",False:"—"})
        near_table["Jarak (km)"] = near_table["Jarak (km)"].round(2)
        st.dataframe(near_table, use_container_width=True, height=300)
        csv_near = near_table.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV Terdekat", data=csv_near, file_name="spbu_terdekat.csv", mime="text/csv")

with st.expander(f"📋 Tabel Atribut Lengkap — {total} SPBU Terfilter", expanded=False):
    table_df = df[[
        "name", "brand", "address", "coord_str", "postcode", "district", "hours",
        "phone", "atm", "toilets", "is_247", "has_ev", "operator", "ref"
    ]].copy()
    table_df.columns = [
        "Nama SPBU", "Brand", "Alamat", "Koordinat", "Kodepos", "Kecamatan",
        "Jam Operasional", "Telepon", "ATM", "Toilet", "Buka 24/7", "EV Charging", "Operator", "Ref"
    ]
    table_df["ATM"]         = table_df["ATM"].map({True:"✅",False:"—"})
    table_df["Toilet"]      = table_df["Toilet"].map({True:"✅",False:"—"})
    table_df["Buka 24/7"]   = table_df["Buka 24/7"].map({True:"✅",False:"—"})
    table_df["EV Charging"] = table_df["EV Charging"].map({True:"✅",False:"—"})

    st.dataframe(table_df, use_container_width=True, height=350)
    csv = table_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV Lengkap", data=csv, file_name="spbu_bekasi_data.csv", mime="text/csv")


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px 0 10px;font-size:11px;color:#2A2D3A">
    Data bersumber dari OpenStreetMap · Lisensi ODbL · Dashboard dibuat untuk keperluan akademik
</div>
""", unsafe_allow_html=True)