# Marina Mental

**Marina Mental** is a desktop application designed to promote emotional awareness and mindfulness through real-time emotion recognition, guided breathing exercises, and emotion trend visualization.  
The system integrates computer vision, affective computing, and relaxation techniques into a unified, user-friendly interface.

---

## Overview

Marina Mental captures facial expressions using a webcam, detects emotional states with the **DeepFace** library, and presents affirmations that encourage self-reflection and emotional regulation.  
Detected emotions are logged automatically and can be analyzed through interactive visualizations.  
Built-in breathing exercises further support mindfulness by guiding users through controlled breathing cycles.

---

## Features

- **Real-Time Emotion Detection** – Uses OpenCV and DeepFace to detect and classify emotions; logs results with timestamps and confidence values.  
- **Affirmation Feedback** – Displays context-specific affirmations based on the user’s detected emotional state.  
- **Guided Breathing Exercises** – Includes 4-7-8 Breathing, Box Breathing, and Diaphragmatic Breathing, with synchronized circle animation and textual prompts (“Inhale”, “Hold”, “Exhale”).  
- **Emotion Data Visualization** – Generates interactive charts showing emotion frequency, intensity trends, and distribution.
- **Structured Logging** – Saves emotional data securely in `stats.json` via the `LogEmotion` module.

---

## Installation and Execution

`pip install -r requirements.txt`

`python main.py`


All logged data are stored in stats.json and can be revisited or visualized.

## Purpose

This project explores how affective computing and mindfulness practices can enhance mental well-being.
By combining real-time emotion recognition with mindfulness exercises, Marina Mental provides a supportive environment for emotional self-awareness and stress management.

## Authors and Acknowledgment

Developed as part of the MarinaHacks 5.0 Hackathon under the title Marina Mental.
Created for academic and research purposes using open-source technologies.

Alena Funkner 

Alexis Ramirez

Alex Pulido 

Sarah Beatriz
