import streamlit as st
from  BusinessCard import load_dataset, extract_data, show_dataset

st.set_page_config(page_title='Businesscard Extraction', layout="wide")
st.title(":yellow[Business Card Data Extraction]")


data_extraction, database_side = st.tabs(["Data upload and view", "Database_side"])


with data_extraction:
    file_name = "bala"
    st.markdown("![Alt Text](https://cdn.dribbble.com/users/393235/screenshots/1643374/media/b32f920793005f554f22129c96627c56.gif)")

    st.subheader(":red[Choose Image.png to Extract Data]")
#----------------------------------------------------------------------------------------------------------------------------------------

    imported = st.file_uploader("Choose Image File")
#----------------------------------------------------------------------------------------------------------------------------------------
if imported  is not None:
   with open(f'{file_name}.png', 'wb') as f:
       f.write(imported.getvalue())

# ---------------------------------------------------------------------------------------------------------------------------------------
st.subheader("Choose Image and view Data")
if st.button("Extract data from image"):
    extractfile = extract_data(f'{file_name}.png')
    st.image(extractfile)

#----------------------------------------------------------------------------------------------------------------------------------------------
st.subheader("Upload extracted file to database")
if st.button("Upload_data"):
    load_dataset(f'{file_name}.png')
    st.success('Data uploaded to Database successfully!')
#------------------------------------------------------------------------------------------------------------------------------------------------
df = show_dataset()
with database_side:
    st.markdown("![Alt Text](https://cdn.dribbble.com/users/2037413/screenshots/4144417/ar_businesscard.gif)")

#-----------------------------------------------------------------------------------------------------------------------------------------------
st.title(":red[All Data in this dataase]")
st.button("show data")
st.dataframe(df)

#------------------------------------------------------------------------------------------------------------------------------------------
st.subheader(":violet[See the data by column]")
column = str(st.radio("choose the column", ('Name', 'Designation', 'Company_name', 'Address', 'Contact_number', 'Email_id', 'Web_link', 'Image')))
value =str(st.selectbox("Select the column", df[column]))
if st.button("pick data"):
    st.dataframe(df[df[column] == value])

#--------------------------------------------------------------------------------------------------------------------



