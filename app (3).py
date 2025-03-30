import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import os
import streamlit as st
from datetime import date  

GOOGLE_GENAI_API_KEY = "AIzaSyDxq34Z3EtWUEA8uSfgOAigJgwOAQQ0yCc"
genai.configure(api_key=GOOGLE_GENAI_API_KEY)

# Streamlit UI
st.title("🚀 AI-Powered Travel Planner ✈️  ")
st.write("Enter your travel details to get estimated traveling cost details for various travel modes including 🚖 cab, 🚆 train, 🚌 bus, and ✈️ flight.")

# User inputs
source = st.text_input("📍 Source:")
destination = st.text_input("📍 Destination:")
budget = st.number_input("💰 Budget (in your currency):", min_value=0, step=100)
start_date = st.date_input("📅 Start Date:", min_value=date.today())
end_date = st.date_input("📅 End Date:", min_value=start_date)
travel_time = st.selectbox("⏰ Preferred Time to Travel:", 
                           ["🌅 Morning", "🌞 Afternoon", "🌆 Evening", "🌙 Night", "Anytime"])
num_travelers = st.number_input("👥 Number of Travelers:", min_value=1, step=1)
preferred_mode = st.multiselect("🚗 Preferred Mode of Transport:", ["🏍️ Bike", "🚖 Cab", "🚌 Bus", "🚆 Train", "✈️ Flight", "Any"])

if st.button("🛫Get Travel options"):
    if source and destination:
            with st.spinner("🔄 Fetching travel options..."):
              st.warning("⚡ Processing your request, please wait...")

            #  AI Chat Prompt
            chat_template = ChatPromptTemplate(messages=[
                ("system", """You are an AI-powered travel assistant that provides users with optimal travel recommendations.  
                Your goal is to generate a structured response with the best available travel options.  

                For each travel mode, provide: 
                - 🚗 Transport Mode: e.g., Cab, Train, Flight  
                - 📍 Total Distance: Between source & destination  
                - ⏳ Estimated Travel Time: Time taken for the journey  
                - 💰 Estimated Cost: Approximate fare range  
                - 🏁 Stops & Transfers: If applicable (e.g., layovers, train changes)  
                - 🍽️ Food Recommendations: If available along the route  

                Always consider the user’s budget, number of travelers, and preferred travel time when providing suggestions.  
                Present the results in a clear, structured format, making it easy to read.  
                """),

                ("human", """
                Find travel options from {source} to {destination} with estimated costs.
                -Budget: {budget} 
                -  Start Date: {start_date}  
                - End Date: {end_date}
                - Preferred Travel Time: {travel_time}  
                - Number of Travelers: {num_travelers}  
                - Preferred Mode(s): {preferred_mode}  
                
                Please recommend the best travel options based on these details.
                """)
            ])

            # Initialize Google GenAI Model
            chat_model = ChatGoogleGenerativeAI(api_key="AIzaSyDxq34Z3EtWUEA8uSfgOAigJgwOAQQ0yCc", model="gemini-2.0-flash-exp")
            parser = StrOutputParser()

            # Chain the model & prompt
            chain = chat_template | chat_model | parser

            # User Input Dictionary
            raw_input = {
                "source": source,
                "destination": destination,
                "budget": budget,
                "start_date": start_date,
                "end_date": end_date,
                "travel_time": travel_time,
                "num_travelers": num_travelers,
                "preferred_mode": ", ".join(preferred_mode)
            }

            # Get AI Response
            response = chain.invoke(raw_input)

            # Display Results
            st.success("✅ Estimated Travel & Cost Options:")
            travel_modes = response.split("\n")
            for mode in travel_modes:
               st.markdown(mode)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")
