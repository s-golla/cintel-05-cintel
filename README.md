# cintel-05-cintel: Arctic Climate Dashboard

## Overview
This project is a modern PyShiny Express dashboard for live monitoring of Arctic temperature and humidity. It features interactive charts, value boxes, and a sidebar with resources, designed for scientific and educational use.

## Features
- Real-time simulation of Arctic climate data (temperature & humidity)
- Modern UI with value boxes and cards
- Interactive Plotly charts (trend lines, histograms)
- Sidebar with colored icons and resource links
- Data table of recent readings

## Technologies Used
- Python 3.13+
- PyShiny Express
- pandas
- plotly
- shinywidgets
- Font Awesome icons (faicons)

## Setup Instructions
1. Clone this repository:
   ```sh
   git clone https://github.com/s-golla/cintel-05-cintel.git
   ```
2. Create and activate a Python virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the dashboard:
   ```sh
   shiny run .\dashboard\app.py
   ```

## Usage
- The dashboard simulates new readings every 10 seconds.
- View live temperature, humidity, and last update time in value boxes.
- Explore recent data in the table and interactive charts.
- Access resources from the sidebar for further learning.

## Resources
- [GitHub Repository](https://github.com/s-golla/cintel-05-cintel)
- [PyShiny Documentation](https://shiny.posit.co/py/)
- [PyShiny Express Blog](https://shiny.posit.co/blog/posts/shiny-express/)
