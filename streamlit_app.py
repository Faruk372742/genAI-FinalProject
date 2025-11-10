import streamlit as st
from streamlit_searchbox import st_searchbox
from openai import OpenAI
import json

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    
if not api_key:
    st.error("⚠️ OpenAI API key not found! Please set it in secrets.toml or as an environment variable.")
    st.stop()

client = OpenAI(api_key=api_key)

# Comprehensive list of countries with their flag emojis
COUNTRIES = [
    ("🇦🇫", "Afghanistan"), ("🇦🇱", "Albania"), ("🇩🇿", "Algeria"), ("🇦🇩", "Andorra"),
    ("🇦🇴", "Angola"), ("🇦🇬", "Antigua and Barbuda"), ("🇦🇷", "Argentina"), ("🇦🇲", "Armenia"),
    ("🇦🇺", "Australia"), ("🇦🇹", "Austria"), ("🇦🇿", "Azerbaijan"), ("🇧🇸", "Bahamas"),
    ("🇧🇭", "Bahrain"), ("🇧🇩", "Bangladesh"), ("🇧🇧", "Barbados"), ("🇧🇾", "Belarus"),
    ("🇧🇪", "Belgium"), ("🇧🇿", "Belize"), ("🇧🇯", "Benin"), ("🇧🇹", "Bhutan"),
    ("🇧🇴", "Bolivia"), ("🇧🇦", "Bosnia and Herzegovina"), ("🇧🇼", "Botswana"), ("🇧🇷", "Brazil"),
    ("🇧🇳", "Brunei"), ("🇧🇬", "Bulgaria"), ("🇧🇫", "Burkina Faso"), ("🇧🇮", "Burundi"),
    ("🇰🇭", "Cambodia"), ("🇨🇲", "Cameroon"), ("🇨🇦", "Canada"), ("🇨🇻", "Cape Verde"),
    ("🇨🇫", "Central African Republic"), ("🇹🇩", "Chad"), ("🇨🇱", "Chile"), ("🇨🇳", "China"),
    ("🇨🇴", "Colombia"), ("🇰🇲", "Comoros"), ("🇨🇬", "Congo"), ("🇨🇷", "Costa Rica"),
    ("🇭🇷", "Croatia"), ("🇨🇺", "Cuba"), ("🇨🇾", "Cyprus"), ("🇨🇿", "Czech Republic"),
    ("🇩🇰", "Denmark"), ("🇩🇯", "Djibouti"), ("🇩🇲", "Dominica"), ("🇩🇴", "Dominican Republic"),
    ("🇪🇨", "Ecuador"), ("🇪🇬", "Egypt"), ("🇸🇻", "El Salvador"), ("🇬🇶", "Equatorial Guinea"),
    ("🇪🇷", "Eritrea"), ("🇪🇪", "Estonia"), ("🇪🇹", "Ethiopia"), ("🇫🇯", "Fiji"),
    ("🇫🇮", "Finland"), ("🇫🇷", "France"), ("🇬🇦", "Gabon"), ("🇬🇲", "Gambia"),
    ("🇬🇪", "Georgia"), ("🇩🇪", "Germany"), ("🇬🇭", "Ghana"), ("🇬🇷", "Greece"),
    ("🇬🇩", "Grenada"), ("🇬🇹", "Guatemala"), ("🇬🇳", "Guinea"), ("🇬🇼", "Guinea-Bissau"),
    ("🇬🇾", "Guyana"), ("🇭🇹", "Haiti"), ("🇭🇳", "Honduras"), ("🇭🇺", "Hungary"),
    ("🇮🇸", "Iceland"), ("🇮🇳", "India"), ("🇮🇩", "Indonesia"), ("🇮🇷", "Iran"),
    ("🇮🇶", "Iraq"), ("🇮🇪", "Ireland"), ("🇮🇱", "Israel"), ("🇮🇹", "Italy"),
    ("🇯🇲", "Jamaica"), ("🇯🇵", "Japan"), ("🇯🇴", "Jordan"), ("🇰🇿", "Kazakhstan"),
    ("🇰🇪", "Kenya"), ("🇰🇮", "Kiribati"), ("🇰🇵", "North Korea"), ("🇰🇷", "South Korea"),
    ("🇰🇼", "Kuwait"), ("🇰🇬", "Kyrgyzstan"), ("🇱🇦", "Laos"), ("🇱🇻", "Latvia"),
    ("🇱🇧", "Lebanon"), ("🇱🇸", "Lesotho"), ("🇱🇷", "Liberia"), ("🇱🇾", "Libya"),
    ("🇱🇮", "Liechtenstein"), ("🇱🇹", "Lithuania"), ("🇱🇺", "Luxembourg"), ("🇲🇰", "North Macedonia"),
    ("🇲🇬", "Madagascar"), ("🇲🇼", "Malawi"), ("🇲🇾", "Malaysia"), ("🇲🇻", "Maldives"),
    ("🇲🇱", "Mali"), ("🇲🇹", "Malta"), ("🇲🇭", "Marshall Islands"), ("🇲🇷", "Mauritania"),
    ("🇲🇺", "Mauritius"), ("🇲🇽", "Mexico"), ("🇫🇲", "Micronesia"), ("🇲🇩", "Moldova"),
    ("🇲🇨", "Monaco"), ("🇲🇳", "Mongolia"), ("🇲🇪", "Montenegro"), ("🇲🇦", "Morocco"),
    ("🇲🇿", "Mozambique"), ("🇲🇲", "Myanmar"), ("🇳🇦", "Namibia"), ("🇳🇷", "Nauru"),
    ("🇳🇵", "Nepal"), ("🇳🇱", "Netherlands"), ("🇳🇿", "New Zealand"), ("🇳🇮", "Nicaragua"),
    ("🇳🇪", "Niger"), ("🇳🇬", "Nigeria"), ("🇳🇴", "Norway"), ("🇴🇲", "Oman"),
    ("🇵🇰", "Pakistan"), ("🇵🇼", "Palau"), ("🇵🇸", "Palestine"), ("🇵🇦", "Panama"),
    ("🇵🇬", "Papua New Guinea"), ("🇵🇾", "Paraguay"), ("🇵🇪", "Peru"), ("🇵🇭", "Philippines"),
    ("🇵🇱", "Poland"), ("🇵🇹", "Portugal"), ("🇶🇦", "Qatar"), ("🇷🇴", "Romania"),
    ("🇷🇺", "Russia"), ("🇷🇼", "Rwanda"), ("🇰🇳", "Saint Kitts and Nevis"), ("🇱🇨", "Saint Lucia"),
    ("🇻🇨", "Saint Vincent and the Grenadines"), ("🇼🇸", "Samoa"), ("🇸🇲", "San Marino"),
    ("🇸🇹", "Sao Tome and Principe"), ("🇸🇦", "Saudi Arabia"), ("🇸🇳", "Senegal"),
    ("🇷🇸", "Serbia"), ("🇸🇨", "Seychelles"), ("🇸🇱", "Sierra Leone"), ("🇸🇬", "Singapore"),
    ("🇸🇰", "Slovakia"), ("🇸🇮", "Slovenia"), ("🇸🇧", "Solomon Islands"), ("🇸🇴", "Somalia"),
    ("🇿🇦", "South Africa"), ("🇸🇸", "South Sudan"), ("🇪🇸", "Spain"), ("🇱🇰", "Sri Lanka"),
    ("🇸🇩", "Sudan"), ("🇸🇷", "Suriname"), ("🇸🇿", "Swaziland"), ("🇸🇪", "Sweden"),
    ("🇨🇭", "Switzerland"), ("🇸🇾", "Syria"), ("🇹🇼", "Taiwan"), ("🇹🇯", "Tajikistan"),
    ("🇹🇿", "Tanzania"), ("🇹🇭", "Thailand"), ("🇹🇱", "Timor-Leste"), ("🇹🇬", "Togo"),
    ("🇹🇴", "Tonga"), ("🇹🇹", "Trinidad and Tobago"), ("🇹🇳", "Tunisia"), ("🇹🇷", "Turkey"),
    ("🇹🇲", "Turkmenistan"), ("🇹🇻", "Tuvalu"), ("🇺🇬", "Uganda"), ("🇺🇦", "Ukraine"),
    ("🇦🇪", "United Arab Emirates"), ("🇬🇧", "United Kingdom"), ("🇺🇸", "United States"),
    ("🇺🇾", "Uruguay"), ("🇺🇿", "Uzbekistan"), ("🇻🇺", "Vanuatu"), ("🇻🇦", "Vatican City"),
    ("🇻🇪", "Venezuela"), ("🇻🇳", "Vietnam"), ("🇾🇪", "Yemen"), ("🇿🇲", "Zambia"),
    ("🇿🇼", "Zimbabwe")
]

def search_countries(searchterm: str):
    """Search function that filters countries based on input"""
    # Always return all countries formatted with flags
    all_countries = [f"{flag} {name}" for flag, name in COUNTRIES]
    
    if not searchterm:
        # Return first 50 countries if no search term
        return all_countries[:20]
    
    # Filter countries that match the search term
    filtered = [
        country 
        for country in all_countries
        if searchterm.lower() in country.lower()
    ]
    return filtered if filtered else all_countries[:20]

# Streamlit app
st.title("Event Finder 🔍")

# Create searchbox
default_options = [f"{flag} {name}" for flag, name in COUNTRIES[:20]]
selected_country = st_searchbox(
    search_countries,
    key="country_searchbox",
    placeholder="Search for a country...",
    label="🌍 Select your country:",
    clear_on_submit=False,
    default_options=default_options
)

# Display selected country
if selected_country:
    st.success(f"✅ You selected: **{selected_country}**")
    
    # Extract just the country name (without flag)
    country_name = selected_country.split(" ", 1)[1] if " " in selected_country else selected_country



if selected_country != None and st.button("Find Important Events", type="primary"):
    with st.spinner(f"Searching for today's important events in {selected_country}..."):
        try:
            # Make API request with web search
            response = client.chat.completions.create(
                model="gpt-4o-mini-search-preview",
                web_search_options={},
                messages=[
                    {
                        "role": "user",
                        "content": f"""Find the 3 most today's important events in {selected_country}. 
                        For each event, provide:
                        1. A clear title
                        2. A detailed description (2-3 sentences, max 30 words)
                        
                        IMPORTANT: Write ALL descriptions in the official language of {selected_country}.
                        
                        Return the response as a JSON array with this structure:
                        [
                            {{
                                "title": "Event title in official language",
                                "description": "Detailed description in official language"
                            }}
                        ]
                        
                        Return ONLY the JSON array, no other text."""
                    }
                ],
            )
            
            # Extract the response content
            result = response.choices[0].message.content
            
            # Parse JSON response
            try:
    # Remove markdown code blocks
                cleaned_result = result.strip()
                
                # Remove ```json and ``` markers
                if cleaned_result.startswith("```json"):
                    cleaned_result = cleaned_result[7:]  # Remove ```json
                elif cleaned_result.startswith("```"):
                    cleaned_result = cleaned_result[3:]   # Remove ```
                
                if cleaned_result.endswith("```"):
                    cleaned_result = cleaned_result[:-3]  # Remove trailing ```
                
                cleaned_result = cleaned_result.strip()  # Remove any extra whitespace
                
                # Now parse the JSON
                events = json.loads(cleaned_result)
                
                st.success(f"✅ Found important events in {selected_country}")
                st.divider()
                
                # Display events
                for i, event in enumerate(events, 1):
                    with st.container():
                        st.subheader(f"📌 Event {i}")
                        st.markdown(f"**{event['title']}**")
                        st.write(event['description'])
                        
                        if i < len(events):
                            st.divider()
                            
            except json.JSONDecodeError as e:
                st.error(f"JSON Parse Error: {str(e)}")
                st.warning("Could not parse structured response. Showing raw results:")
                st.code(result)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Make sure your OpenAI API key is set in Streamlit secrets and has access to GPT-4o with web search.")
