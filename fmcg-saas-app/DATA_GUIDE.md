# Data Preparation Guide

## Quick Start

The app includes sample data in the `data/` folder. To get started immediately:

1. Go to "Upload Data" page
2. Upload `data/sales_orders_complete.csv`
3. The app will auto-map columns
4. Click "Process & Continue"

## Data Requirements

### Minimum Required Columns

Your CSV/Excel file must have these columns (names can vary, app will auto-detect):

| Column | Variations | Example | Required |
|--------|-----------|---------|----------|
| Order ID | order_id, orderid, invoice_id, id | SO000001 | Yes |
| Order Date | order_date, date, invoice_date | 2025-01-15 | Yes |
| Product ID | product_id, sku, product, item_code | SKU0082 | Yes |
| Region | region, warehouse, location, city | North | Yes |
| Quantity | quantity, qty, units, volume | 97 | Yes |
| Unit Price | unit_price, price, rate | 640.86 | Yes |
| Total Amount | total_amount, amount, revenue | 62203.42 | Yes |

### Optional Columns

| Column | Variations | Example | Purpose |
|--------|-----------|---------|---------|
| Customer ID | customer_id, customer, client_id | CUST0362 | Customer analysis |
| Discount % | discount_percent, discount, disc_pct | 10 | Margin analysis |
| Sales Rep | sales_rep, rep_id, employee | EMP0070 | Performance tracking |
| Channel | channel, sales_channel | Wholesale | Channel analysis |

## Data Format Examples

### Example 1: Basic Sales Data

```csv
OrderID,OrderDate,ProductID,Region,Quantity,UnitPrice,TotalAmount
SO001,2025-01-15,SKU001,North,100,50.00,5000.00
SO002,2025-01-16,SKU002,South,50,75.50,3775.00
SO003,2025-01-16,SKU001,East,75,50.00,3750.00
```

### Example 2: Complete Sales Data

```csv
OrderID,OrderDate,CustomerID,ProductID,Region,Quantity,UnitPrice,DiscountPercent,TotalAmount,Channel
SO001,2025-01-15,CUST001,SKU001,North,100,50.00,5,4750.00,Wholesale
SO002,2025-01-16,CUST002,SKU002,South,50,75.50,0,3775.00,Retail
```

## Data Quality Tips

### 1. Date Format
- **Recommended**: YYYY-MM-DD (2025-01-15)
- **Also works**: DD/MM/YYYY, MM/DD/YYYY, DD-MM-YYYY
- **Avoid**: Text dates like "Jan 15, 2025"

### 2. Numeric Fields
- Remove currency symbols: ~~$5,000~~ → 5000
- Remove commas: ~~1,234~~ → 1234
- Use decimal points: 50.00 (not 50,00)

### 3. Product IDs
- Use consistent format: SKU001, SKU002 (not SKU1, SKU-002)
- Avoid special characters: ~~SKU#001~~ → SKU001
- Keep it short: SKU001 (not PRODUCT-SKU-001-VARIANT-A)

### 4. Regions
- Use consistent names: "North" (not "north", "NORTH", "Northern")
- Avoid abbreviations: "North Region" (not "N", "NR")
- Keep it simple: "Mumbai" (not "Mumbai, Maharashtra, India")

### 5. Missing Data
- Leave cells empty (don't use "N/A", "NULL", "-")
- The app will handle missing data automatically
- Required fields must have values

## Common Data Issues & Fixes

### Issue 1: Dates Not Recognized

**Problem**: Dates showing as text or errors

**Fix**:
```python
# In Excel: Format cells as Date (YYYY-MM-DD)
# In CSV: Ensure format is 2025-01-15
```

### Issue 2: Numbers as Text

**Problem**: Calculations not working

**Fix**:
```python
# Remove currency symbols: $5,000 → 5000
# Remove commas: 1,234 → 1234
# In Excel: Format cells as Number
```

### Issue 3: Inconsistent Product Names

**Problem**: Same product with different names

**Fix**:
```python
# Before: "Coca Cola", "Coca-Cola", "CocaCola"
# After: "COCA_COLA" (consistent format)
```

### Issue 4: Multiple Regions Format

**Problem**: "Mumbai, Maharashtra" vs "Mumbai"

**Fix**:
```python
# Choose one format and stick to it
# Recommended: Use city name only
```

## Data Preprocessing Script

If you need to clean your data, use this Python script:

```python
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# 1. Standardize dates
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

# 2. Clean numeric columns
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')

# 3. Remove currency symbols
df['TotalAmount'] = df['TotalAmount'].str.replace('$', '').str.replace(',', '')
df['TotalAmount'] = pd.to_numeric(df['TotalAmount'], errors='coerce')

# 4. Standardize text fields
df['Region'] = df['Region'].str.strip().str.title()
df['ProductID'] = df['ProductID'].str.strip().str.upper()

# 5. Remove duplicates
df = df.drop_duplicates(subset=['OrderID'])

# 6. Remove rows with missing required fields
df = df.dropna(subset=['OrderDate', 'ProductID', 'Quantity'])

# 7. Calculate TotalAmount if missing
if 'TotalAmount' not in df.columns or df['TotalAmount'].isna().any():
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Save cleaned data
df.to_csv('cleaned_data.csv', index=False)
print(f"Cleaned data saved! {len(df)} rows processed.")
```

## Sample Data Included

The app includes these sample datasets:

### 1. sales_orders_complete.csv
- 1000+ orders
- Multiple products and regions
- Complete with all fields
- **Use this to test the app**

### 2. inventory.csv
- Current stock levels
- Reorder points
- Safety stock

### 3. warehouses.csv
- Warehouse locations
- Capacity information

### 4. suppliers.csv
- Supplier details
- Lead times

## Exporting from Common Systems

### From Excel
1. Open your Excel file
2. File → Save As
3. Choose "CSV (Comma delimited) (*.csv)"
4. Upload to the app

### From ERP Systems (SAP, Oracle)
1. Export sales order report
2. Include: Order ID, Date, Product, Quantity, Price
3. Save as CSV
4. Upload to the app

### From Google Sheets
1. File → Download → Comma-separated values (.csv)
2. Upload to the app

### From Database (SQL)
```sql
SELECT 
    order_id,
    order_date,
    product_id,
    customer_id,
    region,
    quantity,
    unit_price,
    discount_percent,
    total_amount
FROM sales_orders
WHERE order_date >= '2024-01-01'
ORDER BY order_date DESC;
```

Export results as CSV and upload.

## Data Size Limits

- **Streamlit Cloud**: Up to 200MB per file
- **Local**: No limit (depends on your RAM)
- **Recommended**: 10,000 - 100,000 rows for best performance
- **Minimum**: 30 days of data for accurate forecasting

## Multiple Files

You can upload multiple files:
1. Upload first file → Map columns → Process
2. Upload second file → Map columns → Process
3. The app will merge them automatically
4. Duplicates are removed based on Order ID

## Need Help?

If your data doesn't match the format:
1. Check the auto-mapping on upload page
2. Manually map columns if needed
3. Use the preprocessing script above
4. Contact support with a sample (5-10 rows)

## Best Practices

✅ **Do**:
- Use consistent date formats
- Keep product IDs simple
- Remove special characters
- Test with sample data first
- Keep backups of original data

❌ **Don't**:
- Mix date formats in same column
- Use merged cells in Excel
- Include summary rows
- Use formulas in CSV files
- Upload files with macros

## Validation Checklist

Before uploading, verify:
- [ ] Dates are in YYYY-MM-DD format
- [ ] Numbers don't have currency symbols
- [ ] No empty required columns
- [ ] Product IDs are consistent
- [ ] Region names are standardized
- [ ] File is CSV or XLSX format
- [ ] File size is under 200MB
- [ ] At least 30 days of data included

## Example Workflow

1. **Export** data from your system
2. **Clean** using the preprocessing script
3. **Validate** using the checklist
4. **Upload** to the app
5. **Map** columns (auto or manual)
6. **Process** and start analyzing!

---

**Ready to upload?** Go to the "Upload Data" page in the app and try with `data/sales_orders_complete.csv` first!
