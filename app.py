import os
import random
from PIL import Image
import streamlit as st
from pdf2image import convert_from_path
import pandas as pd
import glob

st.set_page_config(
    page_title="DataLabs labeling Tool",
    page_icon='✅',
    layout="wide",
    initial_sidebar_state="expanded",
)

def show():
    st.write(
        """
        ## 🕵️ Welcome to DataLabs Labeling Tool : Spoofing Data Labelling Tool
        
        This is one for all Computer Vision : Label some images and all of your 
        annotations are preserved in `st.session_state`!
        """
    )
    selected_box = st.sidebar.selectbox('Choose one of the following', ('Welcome to DataLabs Labeling Tools', 'Image Classification labeling', 'Face Matching Data labeling') )
    
    if selected_box == 'Welcome':
        pass 
    if selected_box == 'Image Classification labeling':
        ImageClassification_Label()
    if selected_box == 'Face Matching Data labeling':
        st.write("`Work In Progress.....`!")
        
def ImageClassification_Label():

    #script_path = os.path.dirname(__file__)
    #rel_path = "images"
    abs_file_path = column_name_1 = st.text_input(label='Path Of your Data', key='first')

    #files = os.listdir(abs_file_path)
    column_name_1 = st.text_input(label='Column Name 1', key='second')
    column_name_2 = st.text_input(label='Column Name 2', key='third')
    csv_path = st.text_input(label='Path to CSV ', key='fourth')
    
    
    if not csv_path:
        #st.write('Submitted Sucessfully')
        #st.session_state.input = submit_button

        st.stop()    

    df = pd.read_csv(csv_path)
    files_d = list(zip(df[column_name_1].astype(str), df[column_name_2].astype(str)))

    #st.progress(len(st.session_state.annotations)) 

    if "annotations" not in st.session_state:
        st.session_state.annotations = pd.DataFrame()
        st.session_state.files = files_d
        st.session_state.current_image = files_d[0]

    def annotate(label):
        st.session_state.annotations = st.session_state.annotations.append(
            {"APP NO": st.session_state.current_image[0], "ITEM":st.session_state.current_image[1], "Label":label}, 
            ignore_index=True)
        
        if st.session_state.files:
            st.session_state.current_image = random.choice(st.session_state.files)
            st.session_state.files.remove(st.session_state.current_image)

    image_path = glob.glob(os.path.join(abs_file_path , st.session_state.current_image[0], st.session_state.current_image[1] , "*.pdf") )[0]

    st.write("")
    col1, col3 = st.columns(2)
    file = convert_from_path(image_path)
    file[0].save('page_0.jpg', 'JPEG')
    col1.image('page_0.jpg', use_column_width=True)
    #col2.image(image_path, use_column_width=True)
    with col3:
        if st.session_state.files:
            st.write(
                "Annotated:",
                len(st.session_state.annotations),
                "– Remaining:",
                len(st.session_state.files),
            )
            st.button("Spoof Detected! 🐶", on_click=annotate, args=("Spoof",))
            st.button("Real! 🐱", on_click=annotate, args=("Real",))
        else:
            st.success(
                f"🎈 Done! All {len(st.session_state.annotations)} images annotated."
            )

        st.write("### Annotations")
        st.write(st.session_state.annotations)
        st.session_state.annotations.to_csv("annotation.csv")
        


if __name__ == "__main__":
    show()