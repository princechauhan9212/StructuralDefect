import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# configure the model

gemini_api_key = os.getenv('Google_API_Key2')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets create sidebar for image upload
st.sidebar.title(':red[Upload the image here:] ')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)

uploaded_image = [Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Image has been uploaded sucessfully')
    st.sidebar.subheader(':blue[uploaded Image ]')
    st.sidebar.image(uploaded_image)


# Lets create the main page 
st.title(':orange[STRUCTURAL DEFECT:-]:blue[AI Assisted structural Defects Identifier]')
st.markdown('#### :green[This application takes the image of the structural defects from the construction sites and prepares the AI Assisted report]')
title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of the person who had  prepared the report ')
desig = st.text_input('Enter the designation of the person')
orgz = st.text_input('Enter the name of the organization:')

if st.button('SUBMIT'):
    with st.spinner('Processing....'):
            prompt=f'''
            <Role> You are an expert structural engineer with  20+ years of experience.
            <Goal> You need to prepare a deatiled report on the structural defect shown in the images.
            <context> The images shared by the user has been attached.
            <format> follow the steps to prepare the report .The title provided by the user is {title}.
            *add name ,designation and organization of a person who has been prepared this report.
            also include the date when the report is prepared. 
            following are the details rpovided by the user:
            name:{name}
            designation:{desig}
            organization :{orgz}
            date :{dt.datetime.now().date()}
            * Identify and classify the defect for eg: crack , 
            * There could be more then one defect in images . Identify all defects seperately.
            * For each defect identified, provide a short description of the defect and its potential impact on the structure.
            * For each defect measure the sevearility as low medium or high. also mentioning if the defect inevitable or avoidable
            * Provide the short term and long term solution for the repair along with an estimated cost in INR and estimate time.
            * What precationary measures can be taken to avoid the 
            
            <Instructions>
            * The report generted should be in word format.
            * use bullet points and tables where ever possible .
            * Make sure the report does not exceeds 3 pages. '''

            response = model.generate_content([prompt,*uploaded_image],
                                            generation_config={'temperature':0.9})


            st.write(response.text)

            if st.download_button(label='click to Download',
                data= response.text,
                file_name='structural_defect_report.text',
                mime='text/plain'):
                st.success('Your file is Downloaded')