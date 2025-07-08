import streamlit as st
import requests
from datetime import date

# Leer API Key desde secrets o variable
API_KEY = st.secrets["api"]["key"] if "api" in st.secrets else "TU_API_KEY"
BASE_URL = "https://api.football-data.org/v4"
headers = {"X-Auth-Token": API_KEY}

def get_matches_today(competition_code="PD"):
    today = date.today().isoformat()
    url = f"{BASE_URL}/competitions/{competition_code}/matches"
    params = {"dateFrom": today, "dateTo": today}
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("matches", [])

def get_team_corner_stats(team_id):
    avg_corners_for = 4.5 + (team_id % 3)
    avg_corners_against = 3.8 + (team_id % 2)
    return avg_corners_for, avg_corners_against

def estimar_linea_corners(avg_for_home, avg_against_away, avg_for_away, avg_against_home):
    est_local = (avg_for_home + avg_against_away) / 2
    est_visit = (avg_for_away + avg_against_home) / 2
    total_estimado = est_local + est_visit
    return round(total_estimado * 2) / 2

st.title("📊 Estimador de Línea de Córners – Previa del Partido")

matches = get_matches_today("PD")

if not matches:
    st.info("No hay partidos hoy.")
else:
    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        home_id = match["homeTeam"]["id"]
        away_id = match["awayTeam"]["id"]

        st.markdown(f"### ⚽ {home} vs {away}")

        avg_for_home, avg_against_home = get_team_corner_stats(home_id)
        avg_for_away, avg_against_away = get_team_corner_stats(away_id)

        linea_estimada = estimar_linea_corners(
            avg_for_home, avg_against_away, avg_for_away, avg_against_home
        )

        st.write(f"🟢 {home} – Córners a favor: {avg_for_home:.2f}, en contra: {avg_against_home:.2f}")
        st.write(f"🔵 {away} – Córners a favor: {avg_for_away:.2f}, en contra: {avg_against_away:.2f}")
        st.markdown(f"### 🎯 Línea estimada: **{linea_estimada} córners**")
        st.divider()
