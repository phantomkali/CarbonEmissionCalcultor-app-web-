__Carbon Emission Calculator App__
This is a Streamlit-based Carbon Emission Calculator developed for my conceptual project in my third semester. The application helps users calculate their weekly carbon footprint based on various factors like transportation, diet, electricity usage, water consumption, and more. The results are stored in a MySQL database, and the app provides visualizations to compare emissions with other users.

__Features__
Carbon Footprint Calculation: The app calculates your weekly carbon emissions using various inputs such as transportation methods, diet, electricity usage, and air travel.
Emissions Breakdown: It displays a breakdown of your emissions across categories like transportation, waste, diet, electricity, water, air travel, and heating/cooling.
Comparison with Other Users: The app allows you to compare your carbon footprint with other users and see how it ranks.
FAQ Section: Includes common questions about carbon footprints and tips on how to reduce emissions.
MySQL Integration: Stores user emission data in a MySQL database for comparison and future reference.
Visualizations: Uses Matplotlib and Seaborn to provide bar charts and heatmaps of emissions data.

__How to Run__

Prerequisites
Python 3.7+
MySQL Server
Streamlit
Required Python packages listed in requirements.txt

__Set up the MySQL database:__

Create a database named cf_calculation.
Run the following SQL to create the table:-
CREATE TABLE carbon_footprint (
  id INT AUTO_INCREMENT PRIMARY KEY,
  total_emission FLOAT,
  transportation FLOAT,
  waste FLOAT,
  diet VARCHAR(50),
  electricity FLOAT,
  water FLOAT,
  air_travel FLOAT,
  heating_cooling FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

__Images Used__
image1: Displays carbon emission sources.
image2: Shows the impact of carbon emissions.
Ensure these images are in the same directory as the csp1.py file or provide the correct path to the images.

__Usage__
Navigate to the Calculator section to input your weekly carbon emission factors.
View a breakdown of your carbon emissions and compare them with the average user in the Compare section.
Read more about carbon emissions in the FAQ section.

__Contact__
For any issues or contributions, feel free to contact me.


