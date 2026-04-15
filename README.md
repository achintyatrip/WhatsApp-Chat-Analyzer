WhatsApp Analytics | Enterprise Edition|
A modern, offline, enterprise-grade WhatsApp chat analytics tool built with Python.
Designed for deep insights, clean UI, and powerful NLP-based analysis — all running locally without any cloud dependency.

Features

1. Core Analytics
   a. Total messages, words, media, links
   b. Active users & participation stats
   c. Daily averages & peak activity hours

2. Advanced NLP Insights
   a. Emotion detection (joy, anger, sadness, etc.)
   b. Topic classification (work, tech, relationships, etc.)
   c. Conflict & toxicity detection
   d. Politeness & laughter analysis

3. Visualizations
   a. Monthly timelines
   b. Activity heatmaps (day × hour)
   c. Hourly & weekday activity graphs
   d. Message type distribution (text/media/links)

4. User-Level Intelligence
   a. Response time analysis
   b. Conversation starters tracking
   c. Double-texting behavior
   d. Night owl 🌙 vs early bird 🌅 detection

5. Smart Insights (Trophies System)
   Automatically assigns roles like:
     a. 🏛️ Architect (long messages)
     b. 🗣️ Orator (most words)
     c. 😂 Humorist
     d. 🤝 Diplomat
     e. ⚡ Fastest responder

6. Export & Reporting
   a. Export plots as PNG
   b. Generate professional PDF reports   

7. Modern UI
   a. Clean SaaS-style interface using Tkinter
   b. Theme & font customization
   c. Scrollable dashboards & KPI cards

Tech Stack
  a. Python
  b. Tkinter (GUI)
  c. Pandas & NumPy (data processing)
  d. Matplotlib & Seaborn (visualization)
  e. Regex-based NLP engine
  f. Optional: wordcloud

Installation
  1. Clone the repository
     git clone https://github.com/your-username/whatsapp-analytics-enterprise.git
     cd whatsapp-analytics-enterprise

  2. Install dependencies
     pip install pandas numpy matplotlib seaborn emoji wordcloud

 Usage
   1. Export your WhatsApp chat as .txt
   2. Run the app:
      python main.py
   3. Load your chat file
   4. Explore dashboards, insights & reports   
