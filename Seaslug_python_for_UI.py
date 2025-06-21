
import math
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation
from scipy.stats import t
import streamlit as st
import numpy as np
import tempfile
import os
from PIL import Image

#import PIL
#!pip install pillow

def temp_health_penalty(temp):
    if 3 <= temp <= 5:
        return 0.1
    return abs(temp - 4)**2 * 0.05

def salinity_health_penalty(salinity):
    sigma = 1.5
    return 1 - math.exp(-((salinity - 34)**2) / (2 * sigma**2))

def depth_health_penalty(depth):
    if 50 <= depth <= 200:
        return 0.1
    return abs(depth - 125) / 100

def hunt(df=4, scale=1.0, success_chance=0.8):

    if random.random() > success_chance:
        return 0  # Failed hunt = no gain
    
    # Sample from a t-distribution (heavy tails, centered around 0)
    gain = t.rvs(df=df) * scale
    
    # Clamp to non-negative values (or optionally allow negative = exhaustion)
    return max(0, round(gain, 2))


def daily_health_penalty(temp, salinity, depth):
    """
    Calculates total daily health penalty based on environmental conditions.
    """
    temp_penalty = temp_health_penalty(temp)
    sal_penalty = salinity_health_penalty(salinity)
    depth_penalty = depth_health_penalty(depth)
    #print(temp_penalty,sal_penalty,depth_penalty)

    return temp_penalty + sal_penalty + depth_penalty


def daily_energy_change(temp, salinity, depth):
    change = 10.0

    # Temperature effect on energy (cold = sluggish, warm = overactive = energy loss)
    if 3.5 <= temp <= 4.5:
        change += 0.3  # Slight energy gain in optimal temp
    elif temp < 2.5 or temp > 5.5:
        change -= abs(temp - 4) * 1.5  # Strong energy penalty

    # Salinity: stable salinity helps conserve energy
    if 33.5 <= salinity <= 34.5:
        change += 0.2
    else:
        change -= ((salinity - 34) ** 2) * 0.1

    # Depth: going too deep costs energy, even if it's safe for health
    if depth < 75 or depth > 175:
        change -= abs(depth - 125) / 80  # penalty increases away from optimal
    else:
        change += 0.1  # gain in sweet spot

    return round(change, 2)


class SeaSlug:
    def __init__(self):
        self.age = 0
        self.health = 100.0
        self.energy = 100.0
        self.reproductive_success = 0
        self.alive = True
    def step(self, temp, salinity, depth):
        if not self.alive:
            return
        
        self.health = min(100, self.health + hunt())
        penalty = daily_health_penalty(temp, salinity, depth) + (max(self.age-50,0) ** 2)/100
        self.health -= penalty
        change = daily_energy_change(temp, salinity, depth) - (max(self.age-40,0) ** 2) /100 
        self.energy += change
        self.energy = min(100, self.energy + hunt())

        #resting
        if self.energy > 90 and self.health < 30:
            self.energy -= 10
            self.health += 5


        # Reproduction logic placeholder
        if self.energy > 80 and self.health > 80 and self.age > 30:
            self.reproductive_success += self.energy * self.health /10000
            self.energy -= 20

        self.age += 1

        if self.age > 100 or self.health <= 0 or self.energy <= 0:
            self.alive = False


def simulate_population(temp, salinity, depth, n=1000):
    slugs = [SeaSlug() for _ in range(n)]

    for day in range(365 * 10):  # Simulate up to 10 years
        for slug in slugs:
            if slug.alive:
                slug.step(temp=temp, salinity=salinity, depth=depth)

    # Collect only slugs that actually lived (avoid division by zero)
    lifespans = [slug.age for slug in slugs]
    energies = [slug.energy for slug in slugs]
    repro_rates = [slug.reproductive_success for slug in slugs]

    avg_lifespan = sum(lifespans) / len(lifespans)
    avg_energy = sum(energies) / len(energies)
    avg_reproduction = sum(repro_rates) / len(repro_rates)

    return {
        "lifespans": lifespans,
        "energies": energies,
        "repro_rates": repro_rates,
        "avg_lifespan": avg_lifespan,
        "avg_energy": avg_energy,
        "avg_reproduction": avg_reproduction
    }

def simulate_one_slug(temp, salinity, depth):
    slug = SeaSlug()
    history = []

    for day in range(365):  # Simulate for 1 year
        if not slug.alive:
            break
        slug.step(temp=temp, salinity=salinity, depth=depth)
        history.append({
            "day": day,
            "health": slug.health,
            "energy": slug.energy,
            "reproductuion rate": slug.reproductive_success
        })

    return history



def create_slug_animation(history):
    fig, ax = plt.subplots()
    blob = plt.Circle((0.5, 0.5), 0.1, color='green')
    ax.add_patch(blob)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    day_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')
    energy_text = ax.text(0.95, 0.95, '', transform=ax.transAxes, fontsize=12,
                          verticalalignment='top', horizontalalignment='right')
    repro_text = ax.text(0.95, 0.90, '', transform=ax.transAxes, fontsize=12,
                         verticalalignment='top', horizontalalignment='right')

    def update(frame):
        health = history[frame]["health"]
        energy = history[frame]["energy"]
        reproduction = history[frame]["reproductuion rate"]  # keep your key consistent!
        if health > 70:
            color = "green"
        elif health > 30:
            color = "orange"
        elif health > 0:
            color = "red"
        else:
            color = "black"
            anim.event_source.stop()  # Stop animation when slug dies

        blob.set_color(color)
        day_text.set_text(f"Day: {history[frame]['day']}")
        energy_text.set_text(f"Energy: {energy:.1f}")
        repro_text.set_text(f"Repro: {reproduction:.1f}")
        return (blob, day_text)

    anim = FuncAnimation(fig, update, frames=len(history), interval=300)

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
    anim.save(tmpfile.name, writer='pillow')
    plt.close(fig)
    return tmpfile.name


# Sidebar Inputs
st.title("Sea Slug Simulator")

st.sidebar.header("Environment Parameters")
temperature = st.sidebar.slider("Temperature (°C)", 0.0, 10.0, 4.0)
salinity = st.sidebar.slider("Salinity (PSU)", 30.0, 40.0, 34.0)
depth = st.sidebar.slider("Depth (m)", 0, 300, 125)

# Mode selection
mode = st.radio("Choose Simulation Mode", ["Single Slug (Animation)", "1000 Slugs (Stats)"])

if st.button("Run Simulation", key="run_sim_button"):
    if mode == "Single Slug (Animation)":
        st.write("Running animation...")
        history = simulate_one_slug(temperature, salinity, depth)
        gif_path = create_slug_animation(history)
        st.image(gif_path, caption="Sea Slug Health Over Time")
    else:
        st.write("Simulating 1000 slugs...")
        results = simulate_population(temperature, salinity, depth, n=1000)
        
        st.write(f"**Average lifespan:** {results['avg_lifespan']:.2f} days")
        st.write(f"**Average energy:** {results['avg_energy']:.2f}")
        st.write(f"**Average reproductive success:** {results['avg_reproduction']:.2f}")
        
        # Plot histogram
        fig, ax = plt.subplots()
        ax.hist(results["lifespans"], bins=30, color="skyblue", edgecolor="black")
        ax.set_title("Lifespan Distribution")
        ax.set_xlabel("Lifespan (days)")
        ax.set_ylabel("Number of Slugs")
        st.pyplot(fig)