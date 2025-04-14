import streamlit as st
import pandas as pd
import PyPDF2
import io
import re
import base64

def extract_data_from_text(text):
    """Extract data from text format assuming specific template"""
    try:
        # Split text into lines and remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Create a list to store the data
        data = []
        
        # Process each line
        for line in lines:
            # Skip header or empty lines
            if not line or line.startswith('Name') or line.startswith('---'):
                continue
                
            # Split line by common delimiters (tab, multiple spaces, or |)
            row = re.split(r'\t+|\s{2,}|\|', line)
            if len(row) >= 9:  # Ensure we have all required fields yt5f5ff5ff5hyhyhyy
                data.append(row[:9])  # Take only the first 9 columns
        
        # Create DataFrame with expected columns
        columns = ['Name', 'Gender', 'Age', 'Designation', 'No.of years Experience',
                  'Japanese Ability', 'JLPT Level', 'Skill', 'Project DOJ']
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"Error processing text data: {str(e)}")
        return None

def load_data(uploaded_file=None):
    try:
        if uploaded_file is not None:
            # Check file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file)
            elif file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            else:
                st.error("Please upload an Excel file (.xlsx, .xls) for data processing")
                return None
            
            # Remove 'Unnamed: 0' column if it exists
            if 'Unnamed: 0' in df.columns:
                df = df.drop('Unnamed: 0', axis=1)
                
            # Remove first column if it exists
            if 'No.' in df.columns:
                df = df.drop('No.', axis=1)
            
            # Rename columns
            column_renames = {
                'Unnamed: 2': 'Name',
                'Unnamed: 3': 'Gender',
                'Unnamed: 4': 'Age',
                'Unnamed: 5': 'Designation',
                'Unnamed: 6': 'No.of years Experience',
                'Unnamed: 7': 'Japanese Ability',
                'Unnamed: 8': 'JLPT Level',
                'Unnamed: 9': 'Skill',
                'Unnamed: 10': 'Project DOJ'
            }
            
            # Apply renaming for columns that exist
            df = df.rename(columns={col: new_name for col, new_name in column_renames.items() if col in df.columns})
            
            # Remove empty rows (where Name is empty)
            df = df.dropna(subset=['Name'])
            
            # Convert experience to numeric, removing any non-numeric characters
            df['No.of years Experience'] = pd.to_numeric(
                df['No.of years Experience'].str.replace(r'[^0-9.]', '', regex=True),
                errors='coerce'
            )
            
            # Sort by experience in descending order
            df = df.sort_values(by='No.of years Experience', ascending=False)
            
            # Reorder rows to move last row to first position
            if len(df) > 0:
                df = pd.concat([
                    df.iloc[[-1]],     # Last row becomes first
                    df.iloc[:-1]       # All other rows remain in order
                ]).reset_index(drop=True)
            
            return df
            
        return None
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def main():
    # Set page config
    st.set_page_config(
        page_title="ISSJ HR Hiring Dashboard",
        layout="wide"
    )
    
    # Add custom CSS for better visibility with background
    st.markdown("""
        <style>
        .title-container {
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .employee-button {
            background-color: rgba(30, 136, 229, 0.9) !important;
            color: white !important;
            padding: 15px 15px !important;
            font-size: 14px !important;
            width: 100% !important;
            margin: 5px 0 !important;
            border-radius: 5px !important;
            border: none !important;
            text-align: center !important;
        }
        .employee-button:hover {
            background-color: rgba(25, 118, 210, 1) !important;
        }
        .emp-title {
            color: white;
            font-size: 24px;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .section-title {
            color: white;
            font-size: 20px;
            margin: 20px 0 10px 0;
            font-weight: bold;
        }
        .section-button {
            background-color: rgba(30, 136, 229, 0.9) !important;
            color: white !important;
            padding: 15px 30px !important;
            font-size: 16px !important;
            width: 100% !important;
            margin: 5px 0 !important;
            border-radius: 5px !important;
            border: none !important;
            text-align: center !important;
        }
        .section-button:hover {
            background-color: rgba(25, 118, 210, 1) !important;
        }
        .number-display {
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-top: 5px;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        .stApp {
            background: linear-gradient(135deg, 
                rgba(28, 58, 148, 0.95) 0%, 
                rgba(73, 125, 189, 0.95) 100%);
            background-attachment: fixed;
        }
        .button-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            margin-bottom: 10px;
        }
        .button-title {
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .number-display {
            color: white;
            font-size: 28px;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        .custom-button {
            background-color: rgba(30, 136, 229, 0.9);
            border: none;
            color: white;
            padding: 20px;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: background-color 0.3s;
        }
        .custom-button:hover {
            background-color: rgba(25, 118, 210, 1);
        }
        .quarterly-container {
            margin-top: 30px;
            padding: 20px 0;
        }
        .quarterly-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            backdrop-filter: blur(5px);
        }
        .quarters-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .quarter-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .quarter-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(255, 255, 255, 0.1);
        }
        .quarter-title {
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .quarter-value {
            color: #64B5F6;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(100, 181, 246, 0.3);
        }
        .department-container {
            margin-top: 30px;
            padding: 20px 0;
        }
        .department-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .department-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .department-button {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
        }
        .department-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
            background: linear-gradient(135deg, #45a049, #388e3c);
        }
        .department-button:active {
            transform: translateY(1px);
        }
        .department-name {
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        .department-count {
            color: rgba(255,255,255,0.9);
            font-size: 16px;
            margin-top: 5px;
        }
        .contact-container {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .contact-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .contact-card {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        .contact-image {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .contact-info {
            flex-grow: 1;
        }
        .contact-name {
            color: white;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .contact-role {
            color: #90CAF9;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .contact-details {
            color: #E0E0E0;
            font-size: 14px;
            line-height: 1.5;
        }
        .contact-link {
            color: #90CAF9;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .contact-link:hover {
            color: #64B5F6;
        }
        .upload-section {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            backdrop-filter: blur(5px);
        }
        
        .stFileUploader {
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border: 2px dashed rgba(255, 255, 255, 0.3);
        }
        
        .stFileUploader:hover {
            border-color: #90CAF9;
        }
        
        .upload-text {
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .fields-container {
            margin-top: 20px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .field-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .field-label {
            color: #E0E0E0;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .field-value {
            color: #90CAF9;
            font-size: 18px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create title container with logo
    st.markdown("""
        <div class="title-container">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <h1 style="color: black; margin: 0; font-size: 32px;">ISSJ HR Hiring Dashboard</h1>
                <img src="data:image/png;base64,{}" style="width: 150px;">
            </div>
        </div>
    """.format(get_base64_encoded_image("l.png")), unsafe_allow_html=True)
    
    # Create a container for Employee Management section
    st.markdown("<h1 style='text-align: center; color: white;'>Employee Management</h1>", unsafe_allow_html=True)
    
    # Add CSS for file uploader
    st.markdown("""
        <style>
        /* Existing styles remain... */
        
        .upload-section {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            backdrop-filter: blur(5px);
        }
        
        .stFileUploader {
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border: 2px dashed rgba(255, 255, 255, 0.3);
        }
        
        .stFileUploader:hover {
            border-color: #90CAF9;
        }
        
        .upload-text {
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Four buttons in a row with numbers inside
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <button class="custom-button" onclick="handleClick('total_employees')">
                <div class="button-title">Total Employees</div>
                <div class="number-display">429</div>
            </button>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <button class="custom-button" onclick="handleClick('permanent_employees')">
                <div class="button-title">Permanent Employees</div>
                <div class="number-display">300</div>
            </button>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <button class="custom-button" onclick="handleClick('contract_employees')">
                <div class="button-title">Contract Employees</div>
                <div class="number-display">89</div>
            </button>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <button class="custom-button" onclick="handleClick('interns')">
                <div class="button-title">Interns</div>
                <div class="number-display">40</div>
            </button>
        """, unsafe_allow_html=True)
    
    # Add file uploader section
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown('<div class="upload-text">Upload Employee Documents</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'xlsx'], key="employee_docs")
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        # Add the three fields in a row
        st.markdown("""
            <div class="fields-container">
                <div class="field-box">
                    <div class="field-label">Year of Completion of Graduation</div>
                    <div class="field-value">2020</div>
                </div>
                <div class="field-box">
                    <div class="field-label">No. of Years of Experience</div>
                    <div class="field-value">3.5 Years</div>
                </div>
                <div class="field-box">
                    <div class="field-label">Technology</div>
                    <div class="field-value">Python, Java</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add quarterly new hires section
    st.markdown("""
        <div class="quarterly-container">
            <div class="quarterly-title">New Hires Overview</div>
            <div class="quarters-grid">
                <div class="quarter-box">
                    <div class="quarter-title">Q1 New Hires</div>
                    <div class="quarter-value">32</div>
                </div>
                <div class="quarter-box">
                    <div class="quarter-title">Q2 New Hires</div>
                    <div class="quarter-value">45</div>
                </div>
                <div class="quarter-box">
                    <div class="quarter-title">Q3 New Hires</div>
                    <div class="quarter-value">38</div>
                </div>
                <div class="quarter-box">
                    <div class="quarter-title">Q4 New Hires</div>
                    <div class="quarter-value">41</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add department buttons section
    st.markdown("""
        <div class="department-container">
            <div class="department-title">Departments</div>
            <div class="department-grid">
                <button class="department-button" onclick="handleDepartmentClick('networking')">
                    <div class="department-name">Networking</div>
                    <div class="department-count">45 Employees</div>
                </button>
                <button class="department-button" onclick="handleDepartmentClick('marketing')">
                    <div class="department-name">Marketing</div>
                    <div class="department-count">38 Employees</div>
                </button>
                <button class="department-button" onclick="handleDepartmentClick('it')">
                    <div class="department-name">IT</div>
                    <div class="department-count">72 Employees</div>
                </button>
                <button class="department-button" onclick="handleDepartmentClick('engineering')">
                    <div class="department-name">Engineering</div>
                    <div class="department-count">95 Employees</div>
                </button>
                <button class="department-button" onclick="handleDepartmentClick('hr')">
                    <div class="department-name">HR</div>
                    <div class="department-count">25 Employees</div>
                </button>
                <button class="department-button" onclick="handleDepartmentClick('security')">
                    <div class="department-name">Security</div>
                    <div class="department-count">32 Employees</div>
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add Sales contact section
    st.markdown("""
        <div class="contact-container">
            <div class="contact-title">Sales Contact</div>
            <div class="contact-card">
                <img src="https://raw.githubusercontent.com/your-repo/sales-profile.jpg" 
                     alt="Sales Manager" 
                     class="contact-image">
                <div class="contact-info">
                    <div class="contact-name">Michael Chen</div>
                    <div class="contact-role">Senior Sales Manager</div>
                    <div class="contact-details">
                        Email: <a href="mailto:michael.chen@company.com" class="contact-link">michael.chen@company.com</a><br>
                        Phone: +1 (555) 987-6543<br>
                        Office: Floor 4, Room 405
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Add function to encode image
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if __name__ == "__main__":
    main()
    