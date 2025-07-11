import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Load and clean the dataset
df = pd.read_csv("eCommercePK.csv")

# Convert date and sales columns
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', dayfirst=True)
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
df = df.dropna(subset=['order_date', 'sales'])

# Basic analysis
total_orders = len(df)
total_sales = df['sales'].sum()
top_cities = df.groupby('city')['sales'].sum().sort_values(ascending=False).head(5)
top_categories = df['category'].value_counts().head(5)

# Save a chart (Top 5 Cities by Sales)
plt.figure(figsize=(6,4))
top_cities.plot(kind='bar', color='skyblue')
plt.title("Top 5 Cities by Sales")
plt.ylabel("Total Sales (Rs)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_cities_chart.png")
plt.close()

# Prepare PDF
pdf_path = "ecommerce_report_enhanced.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Title
elements.append(Paragraph("eCommerce Dataset Report - 2025", styles['Title']))
elements.append(Spacer(1, 12))

# Summary Table
summary_data = [
    ['Metric', 'Value'],
    ['Total Orders', total_orders],
    ['Total Sales (Rs.)', f"{total_sales:,.2f}"]
]
summary_table = Table(summary_data)
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('FONTSIZE', (0,0), (-1,-1), 10),
]))
elements.append(summary_table)
elements.append(Spacer(1, 20))

# Top Cities
elements.append(Paragraph("Top 5 Cities by Sales", styles['Heading2']))
for city, sales in top_cities.items():
    elements.append(Paragraph(f"{city}: Rs. {sales:,.2f}", styles['Normal']))
elements.append(Spacer(1, 20))

# Top Categories
elements.append(Paragraph("Top 5 Categories by Number of Orders", styles['Heading2']))
for category, count in top_categories.items():
    elements.append(Paragraph(f"{category}: {count} orders", styles['Normal']))
elements.append(Spacer(1, 20))

# Add Chart Image
elements.append(Paragraph("Chart: Top 5 Cities by Sales", styles['Heading2']))
elements.append(Image("top_cities_chart.png", width=400, height=250))

# Save PDF
doc.build(elements)
print("PDF report generated:", pdf_path)
