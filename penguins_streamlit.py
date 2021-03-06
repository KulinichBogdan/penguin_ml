import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle 

st.title('Penguin Classifier: A Machine Learning App')
st.write("This app uses 6 inputs to predice the species of penguin using a model bouilt on the Palmer's Penguin's dataset. Use the form below to get started!")

# password_guess = st.text_input('What is the Password?')
# if password_guess != 'streamlit_password':
#    st.stop()

penguin_df = pd.read_csv('penguins.csv')
rf_pickle = open('random_forest_penguin.pickle', 'rb')
map_pickle = open('output_penguin.pickle', 'rb')
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
rf_pickle.close()
map_pickle.close()


# penguin_df = penguin_df.dropna()
with st.form('user_input'):
    island = st.selectbox('Penguin Island', options=['Biscoe', 'Dream', 'Torgerson'])
    sex = st.selectbox('Sex', options=['Female', 'Male'])
    bill_length = st.number_input('Bill Length (mm)', min_value=0)
    bill_depth = st.number_input('Bill Depth (mm)', min_value=0)
    flipper_length = st.number_input('Flipper Length (mm)', min_value=0)
    body_mass = st.number_input('Body Mass (g)', min_value=0)
    st.form_submit_button()

island_biscoe, island_dream, island_torgerson = 0, 0, 0
if island == 'Biscoe':
    island_biscoe = 1
elif island == 'Dream':
    island_dream = 1
elif island == 'Torgerson':
    island_torgerson =1

sex_female, sex_male = 0, 0
if sex == 'Female':
    sex_female = 1
elif sex == 'Male':
    sex_male = 1

# st.write('The user inputs are {}'.format([island, sex, bill_length, bill_depth, flipper_length, body_mass]))

new_prediction = rfc.predict([[bill_length, bill_depth, flipper_length, body_mass, island_biscoe, island_dream, island_torgerson, sex_male, sex_female]])
prediction_species = unique_penguin_mapping[new_prediction] [0]

st.subheader("Prediction You Penguin's Species: ")
st.write('We predict your penguin is of the {} species'.format(prediction_species))
st.write('We used a machine learning (Random Forest) model to preict the species, the features used in this prediction are ranked by relative importance below.')
st.image('feature_importance.png')

st.write('Below are the histograms for each continuous variable separated by penguin species. The vertical line represents your inputted value.')
fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['bill_length_mm'], hue=penguin_df['species'])
plt.axvline(bill_length)
plt.title('Bill Length by Species')
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['bill_depth_mm'], hue=penguin_df['species'])
plt.axvline(bill_depth)
plt.title('Bill Depth by Species')
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df['flipper_length_mm'], hue=penguin_df['species'])
plt.axvline(flipper_length)
plt.title('Flipper Length by Species')
st.pyplot(ax)

