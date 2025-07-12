# 🐌 Sea Lemon Simulator

A marine biology-inspired simulation tool that models the life of a **Doris pseudoargus** (commonly known as the **sea lemon**). This project was designed as an educational and creative hackathon project, blending ecology, probability, and data visualization with Python and Streamlit.

---

## 🎯 Purpose

This project explores how environmental variables affect the **health, behavior, reproduction, and survival** of sea lemons over a simulated year. It offers two modes:

- **Single Sea Lemon (Animation)**: Visualizes one slug’s journey over time.
- **1000 Sea Lemons (Stats)**: Simulates a population and analyzes lifespan, energy, and cause of death distribution.

---

## 🧠 Educational Goals

- Introduce ecological modeling and simulation
- Show how parameters like **temperature, salinity, depth, and pollution** affect species
- Teach basic concepts of randomness, distributions, and animation
- Serve as a fun learning tool for students interested in marine biology or data science

---

## 🖥 Features

- Interactive Streamlit UI
- Realistic sea slug behavior simulation
- Environmental sliders: Temperature, Salinity, Depth
- Pollution levels (with real death risks)
- Visual animation (health-color coded blob)
- Statistical output: lifespan, energy, reproduction
- Cause-of-death pie chart for population simulations

---

## 🚀 How to Run

### 🔧 Requirements

Make sure you have Python 3.8+ installed. Install required packages:

```bash
pip install streamlit matplotlib numpy pillow scipy
```

### ▶️ Run the App

Use the uploaded version on streamlit:
https://sealsimulation-b3pcyvp7h8cybzf5lv6j7v.streamlit.app/

OR

```bash
streamlit run Seaslug_python_for_UI.py
```

Then open the local URL (usually `http://localhost:8501`) in your browser.

---

## 📊 Variables Explained

| Parameter     | Description                                                  |
|---------------|--------------------------------------------------------------|
| Temperature   | Ideal: 10–15°C. Too cold or too hot reduces health/energy.   |
| Salinity      | Ideal: 30–40 PSU (euhaline). Brackish water causes penalties.|
| Depth         | Ideal: 10–50m. Too deep or too shallow affects survival.     |
| Pollution     | Added death risk on every 10th day based on selected level.  |

---

## 📂 File Structure

- `Seaslug_python_for_UI.py`: Main simulation + UI logic
- `README.md`: Project overview and usage instructions

---

## 🧪 Scientific Background

The model is inspired by the ecology of *Doris pseudoargus*, a nudibranch found in NE Atlantic waters. Assumptions like energy gains, predation risk, and salinity tolerance are simplified but rooted in marine biology literature.

---

## 🧑‍🔬 Credits

Created as a personal hackathon project to explore biology and simulation together with my sister Terezia Bogyo an aspiring Marine Biologist.
