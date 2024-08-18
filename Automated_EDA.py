from random import choice
from pandas.core.dtypes.missing import notnull
import streamlit as st 
from annotated_text import annotated_text
st.set_page_config(layout="wide",page_icon="📊",page_title="Automated EDA")
import pandas as pd 
import numpy as np 
from scipy import stats
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
# import seaborn as sns 
import base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
     .stApp {
  background-image: url("data:image/png;base64,%s");
  background-size: cover;
  text-color:Green;
  
}
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



def main():
	"""Semi Automated ML App with Streamlit """
	st.header("Exploratory Data Analysis")
	set_background('.streamlit//EDA Bg image.jpg')

	
	# Code to remove the settings and the footer ->made with streamlit from the application
	hide_menu_style="""<style>
	#MainMenu{visibility: hidden;}
	footer{visibility: hidden;}
	</style>"""
	st.markdown(hide_menu_style,unsafe_allow_html=True)

	activities = ["About","Overview","Numerical Analysis","Categorical Analysis","Visualization"]
	

	
	choice = st.sidebar.radio("Analytics",activities)
	

	
	if choice=='About':
		st.subheader("This app can be used to perform Exploratory Data Analysis on any set of data. \n ")
		st.subheader("Drag and drop any dataset and select the options from the sidebar to draw important insights from dataset.")	
	elif choice == 'Overview':
		st.subheader("Exploratory Data Analysis")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt","xlsx"])
		
		
		
		if data is not None:
			df = pd.read_csv(data)
			
			st.dataframe(df.head())
			
			st.subheader(" Overview ")
			
			if st.checkbox("Show Shape"):
				st.write(df.shape)
				

			if st.checkbox("Show Columns"):
				st.write("#")
				all_columns = df.columns.to_list()
				st.write(all_columns)
				st.write("#")

			if st.checkbox("Describe dataset Stastically"):
				st.write("#")
				st.write(df.describe())
				st.write("#")

			if st.checkbox("Show Selected Columns"):
				selected_columns = st.multiselect("Select Columns",all_columns)
				new_df = df[selected_columns]
				st.dataframe(new_df)

			if st.checkbox("Number of Numerical feature"):
				num_fea=[features for features in df.columns if df[features].dtype!='O']
				st.write("Total number of Numerical features are ",len(num_fea))

			if st.checkbox("Number of Categorical feature"):
				cat_fea=[features for features in df.columns if df[features].dtype=='O']
				st.write("Total number of Categorical features are ",len(cat_fea))

			if st.checkbox("Number of missing cells "):
				st.write('Total number of missing cells are ',df.isna().sum().sum())
				st.write('Percentage of missing cells is ',np.round((df.isna().sum().sum())*100/(len(df)*len(df.columns)),3),'%')
				st.write(df.isna().sum())
	elif choice=='Numerical Analysis':
		st.subheader("Numerical Data Analysis")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt","xlsx"])
	
		if data is not None:
			df = pd.read_csv(data)
			
			st.dataframe(df.head())
			
			st.subheader(" Numerical feature Analysis ")
			
			# if st.checkbox("Show Shape"):
			# 	st.write(df.shape)
			num_fea=[features for features in df.columns if df[features].dtype!='O']
			for feature in num_fea:
				st.subheader(feature)
				mi=df[feature].min()
				ma=df[feature].max()
				st.write("Maximum",ma)
				st.write("Minimum",mi)
				st.write("Range",np.round(ma-mi,3))
				m=np.mean(df[feature])
				st.write("Mean of ",feature," is ",np.round(m,3))
				me=np.median(df[feature])
				if(np.isnan(me)):
					st.write("Median of ",feature," is affected by null values")
				else:
				    st.write("Median of" ,feature," is ",np.round(me,3))
				st.write("Standard Deviation",np.round(np.std(df[feature]),3))
				st.write("Variance",np.round(np.var(df[feature]),3))
				st.write("Number of zeros",len(df[feature])-np.count_nonzero(df[feature]))                                                         				
				st.write("Percentage of zeros",np.round((len(df[feature])-np.count_nonzero(df[feature]))*100/len(df[feature]),3),"%")                                                         				
				st.write("Number of Unique Entries",len(df[feature].unique()))
				st.write("Percentage of Unique Entries",np.round(len(df[feature].unique())*100/len(df[feature]),3),"%")
				if(df[feature].isna().sum()>=1):
					# st.markdown("Null Values present")
					st.write(annotated_text( "There are some ",  ("missing/nan values", "", "#faa"),  " present "))
	
				st.write("Null values",(df[feature].isna().sum()))
				st.write("Null values",np.round((df[feature].isna().sum())*100/len(df[feature]),3),"%")				
	elif choice=='Categorical Analysis':
		
		# Categorical Analysis  -> word cloud,value_counts,null values
		st.subheader("Categorical Data Analysis")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt","xlsx"])
	
		if data is not None:
			df = pd.read_csv(data)
			
			st.dataframe(df.head())
			
			st.subheader(" Categorical feature Analysis ")
			cat_fea=[features for features in df.columns if df[features].dtype=='O']
			for feature in cat_fea:
				if(feature=='Name'):
					if st.checkbox('Name'):
						st.write(df[feature])
					continue
				if(feature=='name'):
					if st.checkbox('Name'):
						st.write(df[feature])
					continue

				st.subheader(feature)
				st.write("Different categories present in ",feature,"are :",df[feature].unique())
				st.write("Value Counts of ",feature,"are ",df[feature].value_counts())
				if(df[feature].isna().sum()>=1):
					# st.markdown("Null Values present")
					st.write(annotated_text( "There are some ",  ("missing/nan values", "", "#faa"),  " present "))
	else :
		st.subheader("Data Visualizations")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt","xlsx"])
	
		if data is not None:
			df = pd.read_csv(data)
			
			st.dataframe(df.head())
			
			st.subheader("Data Visualizations")
			all_columns_names = df.columns.tolist()
			type_of_plot = st.selectbox("Select Type of Plot",["Area","Bar","Line","Hist"])
			selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)
			if st.button("Generate Plot"):
				st.success("Customized Plot of {} for {}".format(type_of_plot,selected_columns_names))
				if type_of_plot == 'Area':
					cust_data = df[selected_columns_names]
					st.area_chart(cust_data)

				elif type_of_plot == 'Bar':
					cust_data = df[selected_columns_names]
					st.bar_chart(cust_data)

				elif type_of_plot == 'Line':
					cust_data = df[selected_columns_names]
					st.line_chart(cust_data)

if __name__ == '__main__':
	main()