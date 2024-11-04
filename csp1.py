import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from PIL import Image
from google.cloud import firestore
# Firebase config
firebaseConfig = {
    'apiKey': "AIzaSyD2Z0OxoF5hXgJUbTkuBQATmc0AId3Z6z8",
    'authDomain': "carbon-emision.firebaseapp.com",
    'projectId': "carbon-emision",
    'storageBucket': "carbon-emision.appspot.com",
    'messagingSenderId': "868155278267",
    'appId': "1:868155278267:web:1e982da0e66e04d35f7a9e",
    'measurementId': "G-PB2M44MM3L",
    'databaseURL': "https://carbon-emision-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize Firebase Admin SDK for Firestore
cred = credentials.Certificate("C:/Users/keerthan/Desktop/csp/carbon-emision-firebase-adminsdk-dd3iv-58e22e1d81.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def faq_page():
    # Page Title
    st.title("🌍 Frequently Asked Questions (FAQ)")

    # Introduction Section
    st.write(
        """
        Welcome to the FAQ section! Here, you'll find answers to common questions about our carbon footprint calculator, 
        understanding your impact on the environment, and tips to reduce your carbon footprint. We’re here to help you 
        make informed choices for a more sustainable future.
        """
    )

    # FAQ Content - More Detailed and Aesthetic
    faq_data = {
        "How is my carbon footprint calculated?": (
            "We estimate your carbon output based on various factors you provide, such as transportation habits, "
            "energy consumption, dietary choices, and waste generation. Each category has a unique emissions factor, "
            "reflecting average carbon dioxide equivalent (CO2e) emissions. We use trusted data sources and scientific "
            "studies to ensure our calculations are as accurate as possible."
        ),
        "What is CO2e?": (
            "CO2e stands for Carbon Dioxide Equivalent, a universal measurement used to compare emissions from different "
            "greenhouse gases. For instance, methane and nitrous oxide have a much higher global warming potential than CO2, "
            "so CO2e allows us to standardize and express their impact on a comparable scale."
        ),
        "How can I reduce my footprint?": (
            "There are several ways to lower your carbon footprint. Start by minimizing waste, optimizing your transportation "
            "choices (e.g., carpooling, biking, or using public transit), and managing your energy use at home. You can also consider "
            "adjusting your diet to include more plant-based meals, which generally have a smaller carbon footprint compared to meat-based diets."
        ),
        "Why should I care about my carbon footprint?": (
            "Understanding and managing your carbon footprint is one of the most effective ways to help mitigate climate change. "
            "Your individual actions, while they may seem small, collectively contribute to a larger impact. By reducing your emissions, "
            "you contribute to a healthier planet and a more sustainable future for all."
        ),
        "What data sources do you use?": (
            "We gather data from reputable sources, such as governmental and environmental agencies, scientific research papers, "
            "and industry-standard emissions factors. This helps us keep our calculations transparent, reliable, and up-to-date."
        )
    }

    # Display FAQ with aesthetics
    for question, answer in faq_data.items():
        st.markdown(f"### ❓ {question}")
        st.markdown(f"<p style='color: gray; font-size: 1.1em; line-height: 1.6;'>{answer}</p>", unsafe_allow_html=True)
        st.divider()  # Adds a divider line for better readability

    # Additional Resources Section
    st.write("### 📚 Additional Resources")
    st.write(
        """
        - [United Nations: Climate Change](https://www.un.org/en/climatechange) - Learn about global climate action initiatives.
        - [Carbon Footprint Calculator Tips](https://www.carbonfootprint.com) - Practical tips to reduce your footprint.
        - [Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch) - Access scientific reports on climate change impact.
        """
    )

    # Closing Section
    st.write(
        """
        We’re constantly updating our FAQ and resources to help answer your questions. If you have more questions or suggestions, 
        feel free to reach out!
        """
    )


# Function for User Comparison Page with enhanced aesthetics
def compare_users():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>📊 Community Carbon Footprint Comparison</h1>", unsafe_allow_html=True)
    st.write(
        "<div style='text-align: center; font-size: 18px; color: #555;'>"
        "See how your carbon footprint compares to other users in our community."
        "</div>",
        unsafe_allow_html=True
    )

    try:
        # Retrieve all user footprints
        docs = db.collection('carbon_footprint').get()
        user_data = []
        for doc in docs:
            data = doc.to_dict()
            user_data.append((data['user_id'], data['total_emission']))

        # Sort data for clear comparison
        user_data.sort(key=lambda x: x[1], reverse=True)  # Sorted in descending order
        users, emissions = zip(*user_data)

        # Customize plot
        fig2, ax = plt.subplots(figsize=(10, len(users) * 0.5))
        sns.barplot(y=users, x=emissions, hue=users, palette="magma", ax=ax, legend=False, edgecolor="0.5")


        # Adding labels and styles
        ax.set_xlabel("Total Carbon Emission (kg CO2e)", fontsize=14, color="#333")
        ax.set_ylabel("User", fontsize=14, color="#333")
        ax.set_title("Community Carbon Footprint Comparison", fontsize=18, color="#FF5733", pad=20)

        # Customize ticks and layout for readability
        plt.xticks(fontsize=12, color="#333")
        plt.yticks(fontsize=12, color="#333")

        # Add value labels for each bar
        for i, (emission, user) in enumerate(zip(emissions, users)):
            ax.text(emission + 10, i, f"{emission:.1f} kg", va='center', ha='left', color="black", fontsize=10, fontweight="bold")
        
        # Reduce whitespace around the plot
        plt.tight_layout()

        # Display plot
        st.pyplot(fig2)

    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Additional guidance for users
    st.markdown(
        "<div style='text-align: center; font-size: 16px; color: #FF5733;'>"
        "Want to reduce your footprint? Check out our FAQ for tips!"
        "</div>",
        unsafe_allow_html=True
    )

 
      

   

# Hashing function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function for user signup
def signup(username, password):
    try:
        user = auth.create_user_with_email_and_password(username, password)
        st.success(f"User {username} signed up successfully.")
        return True
    except Exception as e:
        st.error(f"Error during signup: {e}")
        return False

# Function for user login
def login(username, password):
    try:
        user = auth.sign_in_with_email_and_password(username, password)
        st.success(f"User {username} logged in successfully.")
        return user
    except Exception as e:
        st.error(f"Error during login: {e}")
        return None

# Function to calculate carbon footprint
def calculate_footprint(transportation, waste, diet, electricity, water, air_travel, heating_cooling):
    emission_factors = {
        "car": 0.18,
        "bus": 0.082,
        "bike": 0.001,
        "waste": 0.45,
        "diet_meat": 3.3,
        "diet_vegetarian": 1.7,
        "diet_vegan": 1.5,
        "electricity": 0.82,
        "water": 0.001,
        "air_travel": 0.254,
        "heating_cooling": 0.21
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

# Function to save data to Firestore
def save_to_firestore(user, total_emission, transportation_emission, waste_emission, diet, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission):
    try:
        data = {
            'user_id': user['localId'],
            'total_emission': total_emission,
            'transportation': transportation_emission,
            'waste': waste_emission,
            'diet': diet,
            'electricity': electricity_emission,
            'water': water_emission,
            'air_travel': air_travel_emission,
            'heating_cooling': heating_cooling_emission
        }
        db.collection('carbon_footprint').add(data)
        st.success("Data saved successfully.")
    except Exception as e:
        st.error(f"Error saving data to Firestore: {e}")


# Function for the Carbon Footprint Calculator Page 
def calculator_page(user):
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌍 Carbon Footprint Calculator 🌱</h1>", unsafe_allow_html=True)
    st.write(
        "<div style='text-align: center; font-size: 18px; color: #555;'>"
        "Estimate your weekly carbon emissions and see where you can make a difference!"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Custom styling for sliders and input fields
    st.markdown("""
        <style>
        .stSlider label, .stSelectbox label {
            color: #2C3E50;
            font-weight: bold;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px 20px;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("Transportation")
    car_km = st.slider("🚗 Car kilometers driven per week:", min_value=0, max_value=1000, step=10)
    bus_km = st.slider("🚌 Bus kilometers taken per week:", min_value=0, max_value=1000, step=10)
    bike_km = st.slider("🚲 Bike kilometers ridden per week:", min_value=0, max_value=1000, step=10)
    
    st.subheader("Waste & Consumption")
    waste_kg = st.slider("🗑️ Waste produced per week (kg):", min_value=0, max_value=100, step=1)
    diet = st.selectbox("🍽️ Diet Type:", ["meat", "vegetarian", "vegan"])

    st.subheader("Energy Usage")
    electricity_kwh = st.slider("⚡ Electricity usage per week (kWh):", min_value=0, max_value=1000, step=10)
    water_liters = st.slider("💧 Water usage per week (liters):", min_value=0, max_value=10000, step=50)
    air_travel_km = st.slider("✈️ Air travel distance per year (km):", min_value=0, max_value=50000, step=100)
    heating_cooling_kwh = st.slider("🔥 Heating/Cooling usage per week (kWh):", min_value=0, max_value=1000, step=10)

    if st.button("Calculate Carbon Footprint"):
        with st.spinner("Calculating your carbon footprint..."):
            transportation_data = {'car': car_km, 'bus': bus_km, 'bike': bike_km}
            
            # Calculate emissions
            carbon_footprint, transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission = calculate_footprint(
                transportation_data, waste_kg, diet, electricity_kwh, water_liters, air_travel_km, heating_cooling_kwh
            )

            # Display total footprint
            st.success(f"🌎 Your estimated weekly carbon footprint is **{carbon_footprint:.2f} kg CO2e**.")
            st.write(
                "<div style='font-size: 16px; color: #4CAF50;'>"
                "Try reducing your carbon footprint by making small changes!"
                "</div>",
                unsafe_allow_html=True
            )

            # Save to Firestore
            save_to_firestore(
                user,
                carbon_footprint,
                transportation_emission,
                waste_emission,
                diet,
                electricity_emission,
                water_emission,
                air_travel_emission,
                heating_cooling_emission
            )

            # Emissions data for the bar chart
            emission_types = ['Transportation', 'Waste', 'Diet', 'Electricity', 'Water', 'Air Travel', 'Heating/Cooling']
            emission_values = [transportation_emission, waste_emission, diet_emission, electricity_emission, water_emission, air_travel_emission, heating_cooling_emission]

            # Bar chart for emissions
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=emission_types, y=emission_values, hue=emission_types, palette="coolwarm", ax=ax, legend=False)
            ax.set_title("Breakdown of Carbon Footprint", fontsize=18, color="#333")
            ax.set_xlabel("Emissions Source", fontsize=14, color="#333")
            ax.set_ylabel("Emissions (kg CO2e)", fontsize=14, color="#333")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

            # Encourage further action
            st.markdown(
                "<div style='text-align: center; font-size: 18px; margin-top: 20px;'>"
                "<a href='https://www.carbonfootprint.com/' target='_blank' style='color: #4CAF50;'>"
                "Learn more about reducing your carbon footprint</a>"
                "</div>",
                unsafe_allow_html=True
            )



def main():
    # Set the page title with an icon
    st.markdown("<h1 style='text-align: center; color: #2E8B57;'>🌍 Carbon Footprint Tracker 🌍</h1>", unsafe_allow_html=True)

    # Check if the user is logged in
    if 'user' not in st.session_state:
        # Login/Signup section
        st.sidebar.markdown("<h2 style='text-align: center; color: #2E8B57;'>🚪 Welcome! Please Login or Sign Up</h2>", unsafe_allow_html=True)

        # Sidebar menu for login and signup options
        menu_options = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Select an option", menu_options)

        # Signup option
        if choice == "Sign Up":
            st.sidebar.markdown("<h3 style='color: #2E8B57;'>Create an Account</h3>", unsafe_allow_html=True)
            username = st.sidebar.text_input("Email")
            password = st.sidebar.text_input("Password", type='password')

            if st.sidebar.button("Sign Up"):
                if signup(username, password):
                    st.sidebar.success("🎉 Signup successful! You can now log in.")
                else:
                    st.sidebar.error("❌ Signup failed. Please try again.")

        # Login option
        elif choice == "Login":
            st.sidebar.markdown("<h3 style='color: #2E8B57;'>Log In</h3>", unsafe_allow_html=True)
            username = st.sidebar.text_input("Email")
            password = st.sidebar.text_input("Password", type='password')

            if st.sidebar.button("Login"):
                user = login(username, password)
                if user:
                    st.session_state.user = user  # Store user session
                    st.sidebar.success("✅ Login successful!")
                else:
                    st.sidebar.error("❌ Invalid username or password.")
    else:
        # User is logged in
        st.markdown(f"<h3 style='text-align: center;'>Hello, {st.session_state.user['email']}! 🌱</h3>", unsafe_allow_html=True)

        # Top bar for page navigation with icons
        st.markdown("<h2 style='text-align: center; color: #2E8B57;'>🌱 Navigate 🌱</h2>", unsafe_allow_html=True)
        page_options = ["🌐 Calculator", "📚 FAQ", "📊 Compare Users"]
        page_choice = st.selectbox("Select a Page", page_options, label_visibility="collapsed")

        # Display selected page's content
        if page_choice == "🌐 Calculator":
            st.markdown("<h2 style='text-align: center;'>🔍 Carbon Footprint Calculator 🔍</h2>", unsafe_allow_html=True)
            calculator_page(st.session_state.user)
        elif page_choice == "📚 FAQ":
            st.markdown("<h2 style='text-align: center;'>📖 Frequently Asked Questions 📖</h2>", unsafe_allow_html=True)
            faq_page()
        elif page_choice == "📊 Compare Users":
            st.markdown("<h2 style='text-align: center;'>🔍 Compare User Emissions 🔍</h2>", unsafe_allow_html=True)
            compare_users()


if __name__ == "__main__":
    main()
