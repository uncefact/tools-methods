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

# Generate Home Page
with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write("<html><body>")
    f.write("<h1>UNLOCODE Directory</h1>")
    f.write("<ul>")
    f.write('<li><a href="countries.html">Country Codes</a></li>')
    f.write('<li><a href="subdivisions.html">Subdivision Codes</a></li>')
    f.write('<li><a href="unlocode-directory.html">UNLOCODE Directory</a></li>')
    f.write("</ul>")
    f.write("</body></html>")

# Generate Country Codes Page
with open(os.path.join(output_dir, "countries.html"), "w") as f:
    f.write("<html><body>")
    f.write("<h1>Country Codes</h1>")
    f.write(country_df.to_html(index=False))
    f.write("</body></html>")

# Generate Subdivision Codes Page
with open(os.path.join(output_dir, "subdivisions.html"), "w") as f:
    f.write("<html><body>")
    f.write("<h1>Subdivision Codes</h1>")
    f.write(subdivision_df.to_html(index=False))
    f.write("</body></html>")

# Generate UNLOCODE Directory Page
unlocode_output_dir = os.path.join(output_dir, "unlocode")
os.makedirs(unlocode_output_dir, exist_ok=True)

with open(os.path.join(output_dir, "unlocode-directory.html"), "w") as f:
    f.write("<html><body>")
    f.write("<h1>UNLOCODE Directory</h1>")
    f.write("<ul>")

    # Ensure 'Country' column is treated as strings
    unlocode_df["Country"] = unlocode_df["Country"].astype(str)

    # Replace NaN or invalid values with an empty string (or any default value)
    unlocode_df["Country"] = unlocode_df["Country"].fillna("")

    # Filter out empty strings or invalid country codes
    country_codes = [code for code in unlocode_df["Country"].unique() if code.strip()]

    # Sort the country codes
    for country_code in sorted(country_codes):
        # Generate pages for each country as before
        print(f"Processing country: {country_code}")
    for country_code in sorted(unlocode_df["Country"].unique()):
        country_file = f"{country_code}.html"
        f.write(f'<li><a href="unlocode/{country_file}">{country_code}</a></li>')

        # Generate a page for each country
        country_data = unlocode_df[unlocode_df["Country"] == country_code]
        with open(os.path.join(unlocode_output_dir, country_file), "w") as cf:
            cf.write("<html><body>")
            cf.write(f"<h1>{country_code} - UNLOCODE</h1>")
            cf.write(country_data.to_html(index=False))
            cf.write("</body></html>")

    f.write("</ul>")
    f.write("</body></html>")