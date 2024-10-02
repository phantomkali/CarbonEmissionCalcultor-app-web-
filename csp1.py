import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import mysql.connector

# Function to calculate carbon footprint
def calculate_footprint(transportation, waste, diet, electricity, water, air_travel, heating_cooling):
    # Emission factors (in kg CO2 per unit)
    emission_factors = {
        "car": 0.18,  # per km
        "bus": 0.082,  # per km
        "bike": 0.001,  # per km
        "waste": 0.45,  # per kg
        "diet_meat": 3.3,  # per day
        "diet_vegetarian": 1.7,  # per day
        "diet_vegan": 1.5,  # per day
        "electricity": 0.82,  # per kWh
        "water": 0.001,  # per liter (average emission factor)
        "air_travel": 0.254,  # per km
        "heating_cooling": 0.21  # per kWh
    }

    transportation_emission = (
        transportation['car'] * emission_factors['car'] +
        transportation['bus'] * emission_factors['bus'] +
        transportation['bike'] * emission_factors['bike']
    )

    waste_emission = waste * emission_factors['waste']
    diet_emission = emission_factors[f"diet_{diet}"]
    electricity_emission = electricity * emission_factors['electricity']
    water_emission = water * emission_factors['water']
    air_travel_emission = air_travel / 52 * emission_factors['air_travel']
    heating_cooling_emission = heating_cooling / 4 * emission_factors['heating_cooling']

    total_emission = (
        transportation_emission +
        waste_emission +
        diet_emission +
        electricity_emission +
        water_emission +
        air_travel_emission +
        heating_cooling_emission
    )

    return total_emission, transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission

# Function for the Carbon Footprint Calculator Page
def calculator_page():
    st.title("Carbon Footprint Calculator")
    
    # User inputs
    car_km = st.slider("Car kilometers driven per week:", min_value=0, max_value=10000, value=0)
    bus_km = st.slider("Bus kilometers taken per week:", min_value=0, max_value=10000, value=0)
    bike_km = st.slider("Bike kilometers ridden per week:", min_value=0, max_value=10000, value=0)
    waste_kg = st.slider("Waste produced per week (kg):", min_value=0, max_value=10000, value=0)
    diet = st.selectbox("Diet Type:", ["meat", "vegetarian", "vegan"])
    electricity_kwh = st.slider("Electricity usage per week (kWh):", min_value=0, max_value=10000, value=0)
    water_liters = st.slider("Water usage per week (liters):", min_value=0, max_value=10000, value=0)
    air_travel_km = st.slider("Air travel distance per year (km):", min_value=0, max_value=100000, value=0)
    heating_cooling_kwh = st.slider("Heating/Cooling usage per week (kWh):", min_value=0, max_value=10000, value=0)

    # Calculate button
    if st.button("Calculate Carbon Footprint"):
        with st.spinner("Calculating your carbon footprint..."):
            transportation_data = {
                'car': car_km,
                'bus': bus_km,
                'bike': bike_km
            }
            
            carbon_footprint, transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission = calculate_footprint(
                transportation_data, waste_kg, diet, electricity_kwh / 4, water_liters, air_travel_km / 52, heating_cooling_kwh / 4
            )
            
            st.success(f"Your estimated weekly carbon footprint is {carbon_footprint:.2f} kg CO2e")

            # Save to MySQL
            save_to_mysql(
                carbon_footprint,
                transportation_emission,
                waste_emission,
                diet,
                electricity_emission,
                water_emission,
                air_travel_emission,
                heating_cooling_emission
            )

            # Emissions data for bar chart
            emission_types = ['Transportation', 'Waste', 'Diet', 'Electricity', 'Water', 'Air Travel', 'Heating/Cooling']
            emission_values = [transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission]

            # Bar chart for emissions
            fig, ax = plt.subplots()
            ax.bar(emission_types, emission_values, color='skyblue')
            ax.set_ylabel('Emission (kg CO2e)')
            ax.set_title('Emissions Breakdown')
            
            # Emissions data for heat map
            emission_types = ['Transportation', 'Waste', 'Diet', 'Electricity', 'Water', 'Air Travel', 'Heating/Cooling']
            emission_values = np.array([[transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission]])

            # Create a heat map for emissions
            plt.figure(figsize=(10, 1))
            sns.heatmap(emission_values, annot=True, fmt=".2f", cmap='YlGnBu', cbar_kws={'label': 'Emission (kg CO2e)'}, yticklabels=["Your Emissions"])
            plt.xticks(ticks=np.arange(len(emission_types)) + 0.5, labels=emission_types)
            plt.title('Emissions Breakdown Heat Map')
            plt.xlabel('Emission Types')

            st.pyplot(plt)

def save_to_mysql(total_emission, transportation_emission, waste_emission, diet, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission):
    try:
        # Establish MySQL connection
        conn = mysql.connector.connect(
            host="localhost",  # Change to your actual host
            user="root",  # Change to your MySQL user
            password="niru",  # Change to your MySQL password
            database="cf_calculation"  # Ensure this is your correct database
        )
        
        # Check if connection was successful
        if conn.is_connected():
            st.write("MySQL connection successful.")
        
        cursor = conn.cursor()

        # Prepare the SQL query with parameters
        insert_query = """
            INSERT INTO carbon_footprint 
            (total_emission, transportation, waste, diet, electricity, water, air_travel, heating_cooling)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Ensure diet is a string and others are floats
        st.write("SQL query to execute:")
        st.write(insert_query)
        st.write("Values being inserted into MySQL:")
        st.write(f"Total Emission: {total_emission}")
        st.write(f"Transportation Emission: {transportation_emission}")
        st.write(f"Waste Emission: {waste_emission}")
        st.write(f"Diet: {diet}")
        st.write(f"Electricity Emission: {electricity_emission}")
        st.write(f"Water Emission: {water_emission}")
        st.write(f"Air Travel Emission: {air_travel_emission}")
        st.write(f"Heating/Cooling Emission: {heating_cooling_emission}")

        # Execute the SQL query
        cursor.execute(insert_query, (
            total_emission, transportation_emission, waste_emission, diet,  # Diet is passed as a string
            electricity_emission, water_emission, air_travel_emission, heating_cooling_emission
        ))

        # Commit the transaction to persist changes
        conn.commit()

        st.success("Data successfully saved to MySQL!")
        
    except mysql.connector.Error as err:
        # Display any MySQL error that occurs
        st.error(f"Error inserting data into MySQL: {err}")
    
    finally:
        # Ensure the connection is properly closed
        if conn.is_connected():
            cursor.close()
            conn.close()
            st.write("MySQL connection closed.")

# Function for the FAQ Page
def faq_page():
    st.title("Frequently Asked Questions (FAQ)")

    st.subheader("1. What is a carbon footprint?")
    st.write("A carbon footprint is the total amount of greenhouse gases, particularly carbon dioxide (CO2), "
             "that are emitted directly or indirectly by an individual, organization, event, or product over a specified period. "
             "It is usually expressed in equivalent tons of CO2 (CO2e).")

    st.subheader("2. Why is it important to reduce carbon emissions?")
    st.write("Reducing carbon emissions is crucial for combating climate change, which is causing extreme weather, "
             "rising sea levels, and loss of biodiversity. By lowering emissions, we can help mitigate these effects "
             "and work towards a more sustainable future for our planet.")

    st.subheader("3. How do I measure my water usage?")
    st.write("To measure your water usage, you can look at your water bill, which typically includes the amount of water you’ve used in cubic meters or liters. "
             "You can also install a water meter to track usage. Reducing water consumption, such as fixing leaks and using water-efficient appliances, can significantly lower your footprint.")

    st.subheader("4. What are the most effective ways to reduce my carbon footprint?")
    st.write("Here are some of the most effective ways to reduce your carbon footprint: "
             "- Use public transport, bike, or walk instead of driving. "
             "- Adopt a plant-based diet. "
             "- Reduce waste through recycling and composting. "
             "- Use energy-efficient appliances and switch to renewable energy if possible.")

    # External Resources Section
    st.subheader("5. External Resources for Further Learning")
    st.write("Here are some great resources to learn more about carbon emissions and sustainability:")
    
    st.write("- [Environmental Protection Agency (EPA)](https://www.epa.gov): Comprehensive information on climate change and emissions.")
    st.write("- [Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch): Authoritative climate reports and research.")
    st.write("- [Carbon Footprint Calculator by WWF](https://footprint.wwf.org.uk): A great tool to measure and understand your footprint.")
    st.write("- [Sustainability Explained YouTube Channel](https://www.youtube.com/sustainability): Informative videos on sustainability topics.")
    st.write("- [The Green Podcast](https://www.thegreenpodcast.com): A podcast about sustainability and reducing emissions.")


# Function for the Home Page
def home_page():
    st.title("Welcome to the Carbon Footprint App!")
    st.subheader("What are Carbon Emissions?")
    st.write("Carbon emissions refer to the release of carbon, particularly carbon dioxide (CO2), into the atmosphere. "
             "These emissions primarily come from the burning of fossil fuels for energy, such as coal, oil, and natural gas, "
             "as well as from other human activities like deforestation and industrial processes. High levels of carbon emissions "
             "contribute to climate change and global warming.")
    
    # Provide image paths or URLs correctly
    st.image("C:/Users/keerthan/Desktop/csp/1000_F_422341753_pER5lO7WERP5ZYDq6Gfuq9d1GaqpBg5q-1190024145.jpg", caption="Carbon Emissions Sources", use_column_width=True)  
    st.image("C:/Users/keerthan/Desktop/csp/carbon-footprint-infographic2-scaled-26216501.jpg", caption="Impact of Carbon Emissions", use_column_width=True) 
    
    st.write("Understanding carbon emissions is crucial for reducing our environmental impact and combating climate change. "
             "By using this app, you can calculate your carbon footprint and learn how to reduce your emissions.")
# Main Function to run the Streamlit 
def compare_users():
    try:
        # Establish MySQL connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="niru",
            database="cf_calculation"
        )
        cursor = conn.cursor()

        # Get the total carbon footprint for the user from the 'carbon_footprint' table
        cursor.execute("SELECT total_emission FROM carbon_footprint ORDER BY created_at DESC LIMIT 1")
        user_emission = cursor.fetchone()

        if user_emission:
            user_emission_value = user_emission[0]
            st.write(f"Your latest carbon footprint: **{user_emission_value:.2f} kg CO2e**")
        else:
            st.write("No emissions data found for you.")
            return  # Exit if no user data is found

        # Get the average carbon footprint for all users
        cursor.execute("SELECT AVG(total_emission) FROM carbon_footprint")
        average_emission = cursor.fetchone()[0]

        st.write(f"Average carbon footprint: **{average_emission:.2f} kg CO2e**")

        # Get the carbon footprint of all users for comparison
        cursor.execute("SELECT total_emission FROM carbon_footprint ORDER BY total_emission DESC")
        results = cursor.fetchall()

        st.subheader("Comparison of Carbon Footprints")

        if results:
            # Create a list of emissions from the results
            emissions = [emission[0] for emission in results]
            st.write("Here is a comparison of carbon footprints (sorted by highest emission):")
            for i, emission in enumerate(emissions, 1):
                st.write(f"{i}. User - {emission:.2f} kg CO2e")

            # Add the user's emission to the list for comparison
            emissions.append(user_emission_value)
            labels = [f"User {i+1}" for i in range(len(emissions)-1)] + ["current"]

            # Create a bar chart to compare emissions
            plt.figure(figsize=(10, 5))
            plt.bar(labels, emissions, color='skyblue')
            plt.ylabel('Emission (kg CO2e)')
            plt.title('Carbon Footprint Comparison')
            plt.axhline(y=average_emission, color='r', linestyle='--', label='Average Emission')
            plt.legend()

            st.pyplot(plt)

            # Display how the user compares to the average
            if user_emission_value > average_emission:
                st.write("Your carbon footprint is **above** the average.")
            else:
                st.write("Your carbon footprint is **below** the average.")
        else:
            st.write("No carbon footprint data available for comparison.")

    except mysql.connector.Error as err:
        st.error(f"Error retrieving data from MySQL: {err}")

    finally:
        # Ensure the connection is properly closed
        if conn.is_connected():
            cursor.close()
            conn.close()



# Main function to handle navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Calculator", "FAQ", "Compare"])
    if page == "Home":
        home_page()
    elif page == "Calculator":
        calculator_page()
    elif page == "FAQ":
        faq_page()
    elif page == "Compare":
        compare_users()

if __name__ == "__main__":
    main()
