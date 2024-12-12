import pandas as pd
import os

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
                <img src="https://vocabulary.uncefact.org/images/unlogo.png" alt="UN Logo">
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

# Generate Home Page
with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write(header_template.format(title="UN/LOCODE Directory"))
    f.write("<h2>Welcome to the UN/LOCODE Directory</h2>")
    f.write("<ul>")
    f.write('<li><a href="countries.html">Country Codes</a></li>')
    f.write('<li><a href="subdivisions.html">Subdivision Codes</a></li>')
    f.write('<li><a href="unlocode-directory.html">UNLOCODE Directory</a></li>')
    f.write("</ul>")
    f.write(footer_template)

# Generate Country Codes Page
with open(os.path.join(output_dir, "countries.html"), "w") as f:
    f.write(header_template.format(title="Country Codes"))
    f.write("<h2>Country Codes</h2>")
    f.write(country_df.to_html(index=False, classes="unlocode-table"))
    f.write(footer_template)

# Generate Subdivision Codes Page
with open(os.path.join(output_dir, "subdivisions.html"), "w") as f:
    f.write(header_template.format(title="Subdivision Codes"))
    f.write("<h2>Subdivision Codes</h2>")
    f.write(subdivision_df.to_html(index=False, classes="unlocode-table"))
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
            cf.write(country_data.to_html(index=False, classes="unlocode-table"))
            cf.write(footer_template)

    f.write("</ul>")
    f.write(footer_template)