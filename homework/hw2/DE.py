

# import zipfile

# zip_file_path = "Import_Refusal_2014-present.zip"

# # unzip
# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     zip_ref.extractall()

# print("ZIP file has been successfully extracted in the same directory.")

import pandas as pd

# Task 1: Read the CSV file and create "country_violations_2014-2023.csv"
try:
    df = pd.read_csv('REFUSAL_ENTRY_2014-October2023.csv', encoding='ISO-8859-1')
    print("File read successfully!")

    # Display information about 'REFUSAL_DATE' column
    print(df['REFUSAL_DATE'].head())

    # Convert 'REFUSAL_DATE' to datetime format with specified format
    df['REFUSAL_DATE'] = pd.to_datetime(df['REFUSAL_DATE'], format='%d-%b-%y', errors='coerce')

    # Map the month abbreviations to month names
    df['REFUSAL_DATE'] = df['REFUSAL_DATE'].dt.strftime('%d-%B-%Y')

except UnicodeDecodeError as e:
    print("Error decoding the file. Please check the file encoding.")
    print(e)

    # Additional steps to handle encoding issue
    with open('REFUSAL_ENTRY_2014-October2023.csv', 'rb') as f:
        # Read the first few lines to identify problematic characters
        preview = f.read(1000).decode('ISO-8859-1')

    print("Preview of the file content:")
    print(preview)

# Define a mapping of month abbreviations to month names
month_mapping = {
    'Jan': 'January',
    'Feb': 'February',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December'
}

# Convert 'REFUSAL_DATE' to datetime format with specified format
df['REFUSAL_DATE'] = pd.to_datetime(df['REFUSAL_DATE'], format='%d-%B-%Y', errors='coerce')

# Map the month abbreviations to month names
df['REFUSAL_DATE'] = df['REFUSAL_DATE'].dt.strftime('%d-%B-%Y')

# Task 1: Create "country_violations_2014-2023.csv"
# Group by ['ISO_CNTRY_CODE', 'PROVINCE_STATE', 'CITY_NAME'], count violations, and select relevant columns
country_violations = df.groupby(['ISO_CNTRY_CODE', 'PROVINCE_STATE', 'CITY_NAME']).count().loc[:, ['ENTRY_NUM']]
country_violations.columns = ['VIOLATION_COUNT']

# Save the result to "country_violations_2014-2023.csv"
country_violations.to_csv('country_violations_2014-2023.csv')

# Task 2: Create "country_violations_year_month_2023.csv"
# Extract 'YEAR' and 'MONTH' from 'REFUSAL_DATE'
df['YEAR'] = pd.to_datetime(df['REFUSAL_DATE'], format='%d-%B-%Y', errors='coerce').dt.year
df['MONTH'] = pd.to_datetime(df['REFUSAL_DATE'], format='%d-%B-%Y', errors='coerce').dt.strftime('%B')

# Group by ['YEAR', 'MONTH', 'ISO_CNTRY_CODE', 'PROVINCE_STATE', 'CITY_NAME'], count violations, and select relevant columns
country_violations_year_month = df.groupby(['YEAR', 'MONTH', 'ISO_CNTRY_CODE', 'PROVINCE_STATE', 'CITY_NAME']).count().loc[:, ['ENTRY_NUM']]
country_violations_year_month.columns = ['VIOLATION_COUNT']

# Save the result to "country_violations_year_month_2014-2023.csv"
country_violations_year_month.to_csv('country_violations_year_month_2014-2023.csv')

# Task 3: Find the city, country, province with the most violations in a single month
# Find the row with the maximum violation count
max_violation_row = country_violations_year_month.loc[country_violations_year_month['VIOLATION_COUNT'].idxmax()]

print(max_violation_row)

# Extract relevant information directly from the index
most_violated_city = max_violation_row.name[4]
most_violated_country = max_violation_row.name[2]
most_violated_province = max_violation_row.name[3]
violations_count = max_violation_row['VIOLATION_COUNT']
year = max_violation_row.name[0]
month = max_violation_row.name[1]

# Display the result
print(f"The city, country, and province with the most violations in a single month: {most_violated_city}, {most_violated_country}, {most_violated_province}")
print(f"Month and year: {month}/{year}, Violations count: {violations_count}")


# Task 4: Find the 10 most frequent products in the IRR for 2018
# Filter data for the year 2018
df_2018 = df[df['YEAR'] == 2018]

# Ensure that 'PRDCT_CODE_DESC_TEXT' exists in the DataFrame
if 'PRDCT_CODE_DESC_TEXT' in df_2018.columns:
    # Get the 10 most frequent products
    top_products_2018 = df_2018['PRDCT_CODE_DESC_TEXT'].value_counts().head(10)

    # Display the result
    print("The 10 most frequent products in the IRR for 2018:")
    print(top_products_2018)
else:
    print("Column 'PRDCT_CODE_DESC_TEXT' not found in the DataFrame 'df_2018'.")



# Task 5: Find the company associated with the largest violation in a single month
# Find the row with the maximum violation count in a single month
max_violation_row_monthly_index = country_violations_year_month.groupby(['YEAR', 'MONTH'])['VIOLATION_COUNT'].idxmax()
max_violation_row_monthly = country_violations_year_month.loc[max_violation_row_monthly_index]

# Extract the corresponding indices for the largest violation
indices = [index for index_tuple in max_violation_row_monthly_index for index in index_tuple]
largest_violation_entry_num = df.loc[indices, 'ENTRY_NUM'].values[0]

# Find the company associated with the largest violation
# Flatten the MultiIndex and use it in loc
largest_violation_entry_num_index = tuple(indices)
largest_violation_entry_num = df.loc[largest_violation_entry_num_index, 'ENTRY_NUM'].values[0]

# Find the company associated with the largest violation
largest_violation_company = df.loc[df['ENTRY_NUM'] == largest_violation_entry_num, 'LGL_NAME'].values[0]

# Display the result
print(f"The company associated with the largest violation in a single month: {largest_violation_company}")

