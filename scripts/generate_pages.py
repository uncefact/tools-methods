import pandas as pd
import os
import unicodedata

# Paths to CSV files
source_dir = "source-files/UNLOCODE"
unlocode_file = os.path.join(source_dir, "2024-1 UNLOCODE CodeList.csv")
subdivision_file = os.path.join(source_dir, "2024-1 SubdivisionCodes.csv")
country_file = os.path.join(source_dir, "country_codes.csv")

# Output directory for generated HTML
output_dir = "docs"
os.makedirs(output_dir, exist_ok=True)

# Load data
unlocode_df = pd.read_csv(unlocode_file)
subdivision_df = pd.read_csv(subdivision_file)
country_df = pd.read_csv(country_file)

# Template Header and Footer
header_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://vocabulary.uncefact.org/css/style.css">
    <link rel="stylesheet" href="https://vocabulary.uncefact.org/css/un-style.css">
</head>
<body>
<header>
    <div id="header">
        <div class="logo">
            <a href="https://www.unece.org">
                <img src="https://vocabulary.uncefact.org/images/logo.png" alt="UN Logo">
            </a>
        </div>
        <h1>United Nations Code for Trade and Transport Locations (UN/LOCODE)</h1>
    </div>
</header>
<main>
"""

footer_template = """
</main>
<footer>
    <div id="footer">
        <p>&copy; United Nations Economic Commission for Europe (UNECE)</p>
    </div>
</footer>
</body>
</html>
"""

# Clean up the 'Date' column: Ensure proper date format and handle non-numeric values
def clean_date(x):
    try:
        # Attempt to convert to integer if it's a numeric value
        return str(int(float(x))) if pd.notna(x) else ''
    except ValueError:
        # If conversion fails, return empty string
        return ''

unlocode_df['Date'] = unlocode_df['Date'].apply(clean_date)

# Clean up the UNLOCODE DataFrame
unlocode_df = unlocode_df.fillna(' ')  # Replace NaN values with empty space

# Normalize text to handle diacritics and unusual characters
unlocode_df = unlocode_df.applymap(
    lambda x: unicodedata.normalize("NFKC", str(x)) if isinstance(x, str) else x
)

# Drop 'change' column if it exists
unlocode_df = unlocode_df.drop(columns=["change"], errors="ignore")

# Filter out rows where the 'Location' is missing (i.e., they have a Country code but no location)
unlocode_df = unlocode_df[unlocode_df['Location'].notna()]

# Generate Home Page
with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write(header_template.format(title="UNLOCODE Directory"))
    f.write("<h1>UNLOCODE Directory</h1>")
    f.write("<p>The United Nations Code for Trade and Transport Locations is commonly more known as UN/LOCODE. Although managed and maintained by the UNECE, it is the product of a wide collaboration in the framework of the joint trade facilitation effort undertaken within the United Nations.</p>")
    f.write("<p>Initiated within the UNECE Working Party on Trade Facilitation, UN/LOCODE is based on a code structure set up by UN/ECLAC and a list of locations originating in UN/ESCAP, developed in UNCTAD in co-operation with transport organisations like IATA and the ICS and with active contributions from national governments and commercial bodies. Its first issue in 1981 provided codes to represent the names of some 8.000 locations in the world.</p>")
    f.write("<p>Currently, UN/LOCODE includes over 103,034 locations in 249 countries and territories. It is used by most major shipping companies, by freight forwarders and in the manufacturing industry around the world. It is also applied by national governments and in trade related activities, such as statistics where it is used by the European Union, by the UPU for certain postal services, etc </p>")
    # Add the hyperlink for UNECE Recommendation No. 16 at the end
    f.write('<p>If you are interested in the full text of the formal basis for UN/LOCODE, this can be consulted at ')
    f.write(
        '<a href="https://unece.org/trade/uncefact/unlocode/recommendation-16">UNECE Recommendation No. 16</a>.</p>')
    f.write("The cut-off dates of UN/LOCODE releases are 31 March and 30 September.")

    f.write("The 2024-1 release of UN/LOCODE")
    f.write("<ul>")
    f.write('<li><a href="countries.html">Country Codes</a></li>')
    f.write('<li><a href="subdivisions.html">Subdivision Codes</a></li>')
    f.write('<li><a href="unlocode-directory.html">UNLOCODE Directory</a></li>')
    f.write("</ul>")
    f.write(footer_template)

# Generate Country Codes Page
with open(os.path.join(output_dir, "countries.html"), "w") as f:
    f.write(header_template.format(title="Country Codes"))
    f.write("<h1>Country Codes</h1>")
    f.write(country_df.to_html(index=False))
    f.write(footer_template)

# Generate Subdivision Codes Page
with open(os.path.join(output_dir, "subdivisions.html"), "w") as f:
    f.write(header_template.format(title="Subdivision Codes"))
    f.write("<h1>Subdivision Codes</h1>")

    # Check columns of subdivision_df
    print(f"Columns in subdivision_df: {subdivision_df.columns.tolist()}")

    # Clean the data, adjusting to actual column names
    required_columns = ['Country Code', 'Subdivision Code', 'Subdivision Name', 'Subdivision Type']

    # Remove rows where any of the required columns have missing values
    if all(col in subdivision_df.columns for col in required_columns):
        subdivision_df_cleaned = subdivision_df.dropna(subset=required_columns)
        subdivision_df_cleaned = subdivision_df_cleaned.rename(columns={
            'Country Code': 'Country Code',
            'Subdivision Code': 'Sub Division Code',
            'Subdivision Name': 'Sub Division Name',
            'Subdivision Type': 'Sub Division Type'
        })
        f.write(subdivision_df_cleaned.to_html(index=False))
    else:
        f.write("<p>Error: Missing expected columns in the subdivision dataset.</p>")

    f.write(footer_template)

# Generate UNLOCODE Directory Page
unlocode_output_dir = os.path.join(output_dir, "unlocode")
os.makedirs(unlocode_output_dir, exist_ok=True)

with open(os.path.join(output_dir, "unlocode-directory.html"), "w") as f:
    f.write(header_template.format(title="UNLOCODE Directory"))
    f.write("<h2>UNLOCODE Directory</h2>")
    f.write("<ul>")

    # Ensure 'Country' column is treated as strings
    unlocode_df["Country"] = unlocode_df["Country"].astype(str)

    # Replace NaN or invalid values with an empty string
    unlocode_df["Country"] = unlocode_df["Country"].fillna("")

    # Filter out empty strings or invalid country codes
    country_codes = [code for code in unlocode_df["Country"].unique() if code.strip()]

    # Sort the country codes
    for country_code in sorted(country_codes):
        country_file = f"{country_code}.html"
        f.write(f'<li><a href="unlocode/{country_file}">{country_code}</a></li>')

        # Generate a page for each country
        country_data = unlocode_df[unlocode_df["Country"] == country_code]
        with open(os.path.join(unlocode_output_dir, country_file), "w") as cf:
            cf.write(header_template.format(title=f"{country_code} - UNLOCODE"))
            cf.write(f"<h2>{country_code} - UNLOCODE</h2>")
            cf.write(
                '<p><a href="https://uncefact.github.io/tools-methods/unlocode-directory.html">Back to UNLOCODE Directory</a></p>')

            # Convert country code column to a link pointing to the country-specific page
            country_data["Country"] = country_data["Country"].apply(
                lambda code: f'<a href="https://uncefact.github.io/tools-methods/unlocode/{code}.html">{code}</a>'
                if pd.notna(code) else code
            )

        cf.write(country_data.to_html(index=False, escape=False, classes="unlocode-table"))
        cf.write(footer_template)

    f.write("</ul>")
    f.write(footer_template)