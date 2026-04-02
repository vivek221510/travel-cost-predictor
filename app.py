import streamlit as st
import pickle
import pandas as pd

model=pickle.load(open("model.pkl","rb"))

st.title("✈️ Travel Cost Predictor")
st.markdown("Estimate your trip cost based on travel details")\
#inputs
distance_map = {
    ("Hyderabad", "Bangalore"): 570,
    ("Hyderabad", "Chennai"): 630,
    ("Hyderabad", "Mumbai"): 710,
    ("Hyderabad", "Goa"): 660,
    ("Hyderabad", "Delhi"): 1550,

    ("Bangalore", "Chennai"): 350,
    ("Bangalore", "Mumbai"): 980,
    ("Bangalore", "Goa"): 560,

    ("Mumbai", "Goa"): 590,
    ("Mumbai", "Delhi"): 1400,
}

def get_distance(source, destination):
    if source == destination:
        return 0
    elif (source, destination) in distance_map:
        return distance_map[(source, destination)]
    elif (destination, source) in distance_map:
        return distance_map[(destination, source)]
    else:
        return 800 


cities = ["Hyderabad","Bangalore","Chennai","Mumbai","Delhi","Goa","Jaipur","Kolkata","Pune","Kochi"]

source= st.selectbox("Select Source",cities)
destination=st.selectbox("Select Destination",cities)

days = st.number_input("Number of Days",min_value=1,max_value=10,value=3)
people= st.number_input("number of people",min_value=1,max_value=5,value=2)

transport = st.selectbox("Transport",["bus","train","flight"])
hotel=st.selectbox("hotel type",["2-star","3-star","4-star"])


if source == destination:
    st.error("Source and Destination cannot be the same")
    
st.write("### selected inputs")
st.write({
    "Source": source,
    "Destination": destination,
    "Days": days,
    "People": people,
    "Transport": transport,
    "Hotel": hotel,
})

st.title("Travel cost predictor")

st.write("App is running successfully!")

#prediction
if st.button("Predict Cost"):

    if source == destination:
        distance_km = 0
    else:
        distance_km = 2*get_distance(source, destination)

    input_data = pd.DataFrame([{
        "source": source,
        "destination": destination,
        "distance_km": distance_km,
        "days": days,
        "people": people,
        "transport": transport,
        "hotel_type": hotel,
        
    }])

    input_data = pd.get_dummies(input_data)
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    prediction = model.predict(input_data)[0]

    st.markdown(f"💰 Estimated Cost: ₹{int(prediction)}")
    
    st.divider()
    
    cost_per_person = prediction / people
    if cost_per_person < 3000:
        st.success("💰 Budget Trip")
    elif cost_per_person < 7000:
        st.info("💸 Moderate Trip")
    else:
        st.warning("💎 Expensive Trip")
        st.write("💡 Tip: Using bus or reducing days can lower cost")
    st.write(f"👤 Cost per person: ₹{int(cost_per_person)}")
    
    if cost_per_person>3000:
        st.subheader("Why this cost?")

    if days > 2:
        st.write("📅 More days → higher stay & food cost")

    if people > 2:
        st.write("👨‍👩‍👧 More people → cost increases")

    if transport == "flight":
        st.write("🚨 Major cost driver: Flight travel")

    if hotel == "4-star":
        st.write("🚨 Major cost driver: Premium hotel")