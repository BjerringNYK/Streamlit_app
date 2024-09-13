import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

# Cache the data loading function using st.cache_data
@st.cache
def load_data():
    data = pd.read_csv('data_cleaned.csv')
    return data

# Load the data
data = load_data()

# Sidebar for selecting sections
st.sidebar.title("Explore Financial Insights")
option = st.sidebar.radio(
    "Select an analysis section:",
    ("Home", 'Description of Variables', "Regional-Based Analysis", "Income-Based Analysis", "Gender-Based Analysis")
)            

# Add a summary of Findex at the bottom of the sidebar
st.sidebar.markdown("### What is Findex?")
st.sidebar.write("""
The Global Findex database provides comprehensive data on how adults worldwide save, borrow, make payments, and manage risk. 
Launched with support from the Bill & Melinda Gates Foundation, the database is updated every three years and is the world’s most 
detailed dataset on how adults use formal and informal financial services. It offers insights into the financial behaviors and 
access to financial systems globally.

For more information, visit the [Global Findex website](https://www.worldbank.org/en/publication/globalfindex).
""")

# Main section logic
if option == "Home":
    # First display the Plotly globe with the title
    # Create the globe visualization
    economy_data = data['economy'].value_counts(normalize=True) * 100
    economy_df = economy_data.reset_index()
    economy_df.columns = ['economy', 'percentage']

    # Round the percentage to 2 decimal places for display
    economy_df['percentage'] = economy_df['percentage'].round(2)

    # Create a choropleth map using Plotly with a green color scheme
    fig = px.choropleth(
        economy_df,
        locations='economy',
        locationmode='country names',
        color='percentage',
        hover_name='economy',
        hover_data={'percentage': ':.2f'},  # Format hover data to 2 decimal places
        color_continuous_scale='Greens',
    )

    # Update hover text to add the percentage sign
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "percentage=%{z:.2f}%<extra></extra>",
        hovertext=economy_df['economy']
    )

    # Add the title to the Plotly chart itself, making it bold and larger
    fig.update_layout(
        title=dict(
            text="FINDEX 2021 Data Visualizer",  # Title text
            font=dict(size=49, color='black', family="Raleway, sans-serif"),  # Stylish font and bigger size
            x=0.5,  # Center the title
            xanchor='center',
            y=0.95,  # Adjust positioning
            yanchor='top',
            pad=dict(t=20),  # Add padding to reduce space
        ),
        geo=dict(
            showframe=True,  # Show a frame around the map
            framecolor="black",  # Frame color
            showcoastlines=True,  # Keep coastlines visible
            coastlinecolor="Black",  # Set coastlines color to black
            projection_type='orthographic',  # Change projection to orthographic for a globe effect
            projection_scale=0.85,  # Zoom out more by reducing the scale
            center=dict(lat=10, lon=0),  # Center the globe around the equator
            lataxis_range=[-85, 85],  # Strictly limit the vertical dragging
            lonaxis_range=[-180, 180],  # Strictly limit the horizontal dragging
            oceancolor='lightblue',  # Set the color of the oceans
            showocean=True,  # Ensure oceans are displayed
        ),
        coloraxis_colorbar=dict(
            title="Participation (%)",
            len=0.5,
            thickness=15,
            tickvals=[0.5, 1, 1.5, 2],
            ticks="outside",
        ),
        width=1000,
        height=800,
        margin={"r":50,"t":50,"l":0,"b":0}
    )

    # Display the Plotly chart first
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Now display the Financial Inclusion and Behaviour description
    st.markdown("""
    This application leverages the Global Findex 2021 dataset with over 140,000 participants to explore financial inclusion and behavior across various economies worldwide.
    
    Key features of this application include:
    - **Quick Visualization**: Instantly visualize the percentage of respondents from each country who participate in various financial services.
    - **Regional Analysis**: Explore financial trends and behaviors by country and region, identifying disparities in access to financial systems.
    - **Income-Based Analysis**: Analyze financial behaviors like savings, borrowing, and digital payments across different income levels.
    - **Gender-Based Analysis**: Compare financial inclusion patterns between genders, looking into variables such as account ownership, borrowing, and savings behavior.
""")

elif option == "Description of Variables":
    st.markdown("<h2 style='text-align: center;'>Descripton of Variables</h2>", unsafe_allow_html=True)
    st.markdown("""
- **economy**: The name of the country or economy.
- **economycode**: ISO 3-digit code representing each economy.
- **regionwb**: World Bank region classification (e.g., Sub-Saharan Africa, East Asia, etc.).
- **pop_adult**: The population of adults (aged 15+) in the economy.
- **wpid_random**: A unique identifier for each respondent in the dataset.
- **wgt**: Survey weight for each respondent, used to make the sample representative of the population.
- **female**: Gender of the respondent (1 if female, 2 if male).
- **age**: Age of the respondent.
- **educ**: Respondent’s education level from level 1 to 3.
- **inc_q**: Income quintile of the respondent’s household.
- **emp_in**: Employment status of the respondent.
- **account**: Whether the respondent has an account at a financial institution or with a mobile money service provider.
- **account_fin**: Whether the respondent has an account at a formal financial institution.
- **fin2**: Has a debit card.
- **fin14_1**: Whether the respondent used mobile money.
- **fin14a**: Made bill payments online using the Internet.
- **fin14a1**: Sent money to a relative or friend online using the Internet.
- **fin14b**: Bought something online using the Internet.
- **fin16**: Saved for old age.
- **fin17a**: Saved using an account at a financial institution.
- **fin20**: Borrowed for medical purposes.
- **fin22a**: Borrowed from a financial institution.
- **fin22b**: Borrowed from family or friends.
- **fin24**: Main source of emergency funds in 30 days.
- **fin30**: Paid a utility bill.
- **fin32**: Received wage payments.
- **fin37**: Received a government transfer.
- **fin38**: Received a government pension.
- **fin44a**: Financially worried: old age.
- **fin44b**: Financially worried: medical cost.
- **fin44c**: Financially worried: bills.
- **fin44d**: Financially worried: education.
- **saved**: Saved money in the past 12 months.
- **borrowed**: Borrowed money in the past 12 months.
- **receive_wages**: Received a wage payment and method.
- **receive_transfers**: Received government transfers or aid payments and method.
- **receive_pension**: Received government pension payments and method.
- **pay_utilities**: Paid utility bills and method.
- **mobileowner**: Whether the respondent owns a mobile phone.
- **internetaccess**: Whether the respondent has access to the internet.
- **anydigpayment**: Whether the respondent made any digital payment.
- **year**: The year of the data collection.
""")
    

    # Main section logic for each page
if option == "Regional-Based Analysis":
    st.markdown("<h2 style='text-align: center;'>Regional Analysis</h2>", unsafe_allow_html=True)
    st.write("This section allows you to explore financial trends and behaviors, including savings, borrowing, and digital payments, across various regions. You can compare how access to financial systems differs between regions and examine disparities in financial inclusion globally.")

    
    # List of regions from your dataset (assuming 'regionwb' column holds this data)
    regions = data['regionwb'].unique()

    # Multiselect for region selection
    selected_regions = st.multiselect("Select regions to compare", options=regions, default=regions[0])

    # Filter data based on selected regions
    regional_data = data[data['regionwb'].isin(selected_regions)]
    
    # Allow user to choose which variable they want to analyze
    variable_to_compare = st.selectbox("Select variable to analyze:", options=[
        'account', 'saved', 'borrowed', 'fin14a', 'fin44a', 'mobileowner', 'internetaccess', 'anydigpayment'
    ])
    

    # Summarize the data for the selected regions and variable
    summary = regional_data.groupby('regionwb')[variable_to_compare].mean().reset_index()
    summary.columns = ['regionwb', f'Average {variable_to_compare}']
    
    # Create an interactive Plotly bar chart to compare the regions
    fig = px.bar(summary, x='regionwb', y=f'Average {variable_to_compare}', 
                 title=f"Comparison of {variable_to_compare} Across Selected Regions",
                 labels={'regionwb': 'Region', f'Average {variable_to_compare}': f'Average {variable_to_compare}'},
                 color='regionwb')

    # Update layout for better aesthetics
    fig.update_layout(
        xaxis_title="Region",
        yaxis_title=f"Average {variable_to_compare}",
        showlegend=False,
        width=800,
        height=500,
        margin={"r":0,"t":50,"l":0,"b":50},
    )

    # Show the chart in Streamlit
    st.plotly_chart(fig)


elif option == "Income-Based Analysis":
    st.markdown("<h2 style='text-align: center;'>Income-Based Analysis</h2>", unsafe_allow_html=True)
    st.write("This section allows you to analyze financial behaviors such as savings, borrowing, and digital payments across different income levels.")

    # Select Income Quintile
    income_quintile = st.selectbox("Select Income Quintile:", data['inc_q'].unique())

    # Filter the data based on the selected income quintile
    filtered_data_income = data[data['inc_q'] == income_quintile]
    
    # Multi-select for financial indicators
    selected_indicators_income = st.multiselect(
        "Select Financial Indicators to Analyze:",
        ['account', 'saved', 'borrowed', 'anydigpayment'],
        default=['account']  # Default is financial account ownership
    )

    st.markdown(f"### Analysis for Income Quintile {income_quintile}")

    # Initialize a dictionary to store the summary for income analysis
    income_summary_dict = {}

    # Loop through selected indicators and create a chart for each
    for indicator in selected_indicators_income:
        # Normalize and calculate the percentage for the selected indicator
        income_indicator_chart = filtered_data_income[indicator].value_counts(normalize=True).mul(100).reset_index()
        income_indicator_chart.columns = [indicator, 'Percentage']
        
        # Get the percentage of people with the selected financial indicator
        has_indicator_income = income_indicator_chart[income_indicator_chart[indicator] == 1]['Percentage'].values[0] if 1 in income_indicator_chart[indicator].values else 0
        income_summary_dict[indicator] = has_indicator_income

        # Create a bar chart for each selected indicator
        fig_income = px.bar(
            income_indicator_chart,
            x=indicator,
            y='Percentage',
            title=f"{indicator.capitalize()} for Income Quintile {income_quintile}",
            labels={indicator: indicator.replace('_', ' ').capitalize()},
            color=indicator,
            color_continuous_scale='Blues'
        )

        st.plotly_chart(fig_income)

    # Print out the summary text at the bottom for income analysis
    st.markdown("### Summary")
    for indicator, percentage in income_summary_dict.items():
        st.write(f"**{percentage:.1f}% of respondents in Income Quintile {income_quintile} have {indicator.replace('_', ' ')}**.")
    
    

elif option == "Gender-Based Analysis":
    st.markdown("<h2 style='text-align: center;'>Gender-Based Analysis</h2>", unsafe_allow_html=True)
    st.write("Here can analyze financial behaviors such as savings, borrowing, and digital payments for selected gender and age groups.")
    
    # Gender selection
    gender = st.radio("Select Gender:", ("Female", "Male"))
    
    # Age group selection (assuming 'age_group' column is already in the dataset)
    age_group = st.selectbox("Select Age Group:", data['age_group'].unique())
    
    # Convert gender to appropriate coding (assuming female=1, male=2 in the dataset)
    gender_code = 1 if gender == "Female" else 2
    
    # Filter the data based on gender and age group
    filtered_data = data[(data['female'] == gender_code) & (data['age_group'] == age_group)]
    
    # Multi-select for financial indicators
    selected_indicators = st.multiselect(
        "Select Financial Indicators to Analyze:",
        ['account', 'saved', 'borrowed', 'anydigpayment'],
        default=['account']  # Default is financial account ownership
    )
    
    st.markdown(f"### Analysis for {gender}s in {age_group} Age Group")
    
    # Initialize a dictionary to store the summary
    summary_dict = {}
    
    # Loop through selected indicators and create a chart for each
    for indicator in selected_indicators:
        # Normalize and calculate the percentage for the selected indicator
        indicator_chart = filtered_data[indicator].value_counts(normalize=True).mul(100).reset_index()
        indicator_chart.columns = [indicator, 'Percentage']
        
        # Get the percentage of people with the selected financial indicator
        has_indicator = indicator_chart[indicator_chart[indicator] == 1]['Percentage'].values[0] if 1 in indicator_chart[indicator].values else 0
        summary_dict[indicator] = has_indicator
        
        # Create a bar chart for each selected indicator
        fig = px.bar(
            indicator_chart,
            x=indicator,
            y='Percentage',
            title=f"{indicator.capitalize()} for {gender}s in {age_group} Age Group",
            labels={indicator: indicator.replace('_', ' ').capitalize()},
            color=indicator,
            color_continuous_scale='Viridis'
        )
        
        st.plotly_chart(fig)

    # Print out the summary text at the bottom
    st.markdown("### Summary")
    for indicator, percentage in summary_dict.items():
        st.write(f"**{percentage:.1f}% of {gender}s in the {age_group} age group have {indicator.replace('_', ' ')}**.")
    
    
