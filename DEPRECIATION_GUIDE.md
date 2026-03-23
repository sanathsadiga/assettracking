# Asset Depreciation System - Documentation

## 📊 Overview

The Asset Tracking System now includes an **automatic depreciation calculation system** that:

- ✅ Calculates asset depreciation based on purchase date and rate
- ✅ Automatically reflects depreciation in real-time
- ✅ Supports custom depreciation rates per asset
- ✅ Uses compound annual depreciation formula
- ✅ Displays current value on all asset pages
- ✅ Provides depreciation update management command

---

## 🎯 Features

### 1. **Financial Fields on Asset Creation**

When creating a new asset, you can now set:

- **Purchase Date**: When the asset was purchased
- **Purchase Cost (₹)**: Original purchase price
- **Annual Depreciation Rate (%)**: How much value the asset loses each year

### 2. **Automatic Depreciation Calculation**

The system calculates depreciation using the compound depreciation formula:

```
Current Value = Purchase Cost × (1 - Depreciation Rate)^Years
```

**Example:**
- Purchase Date: 23-03-2026
- Purchase Cost: ₹100
- Depreciation Rate: 5% per year
- Today: 23-03-2026 → Current Value: ₹100 (0 years)
- Today: 23-03-2027 → Current Value: ₹95 (1 year, 5% depreciation)
- Today: 23-03-2028 → Current Value: ₹90.25 (2 years, compound)

### 3. **Real-Time Display**

Current values are displayed in:
- Asset List View (new "Current Value" column)
- Asset Detail View (Financial Information section)
- API responses

### 4. **Depreciation History**

The system logs all depreciation updates in the Activity Log.

---

## 🔧 Usage

### Adding an Asset with Depreciation

1. Navigate to **Dashboard → Add Asset**
2. Fill in basic information (Name, Category, Location, etc.)
3. Scroll to **Financial Information** section
4. Enter:
   - **Purchase Date**: Select the date of purchase
   - **Purchase Cost**: Enter the original cost
   - **Depreciation Rate**: Enter annual rate (e.g., 5 for 5%)
5. Click **Create Asset**

### Real-Time Updates

The depreciation value is **automatically calculated** whenever:
- You view an asset
- The asset list is loaded
- You run the depreciation update command
- The asset is saved/updated

**No manual updates needed!** The calculation happens automatically based on the current date.

---

## 📋 Depreciation Calculation Details

### Formula Used

**Compound Annual Depreciation:**
```
V(t) = P × (1 - r)^t

Where:
- V(t) = Value at time t
- P = Purchase cost
- r = Annual depreciation rate (as decimal)
- t = Years elapsed since purchase
```

### Example Scenarios

#### Scenario 1: Asset Created Today

| Asset | Purchase Date | Cost | Rate | Current Value |
|-------|---------------|------|------|----------------|
| Laptop | 23-03-2026 | ₹100,000 | 10% | ₹100,000 |

*(0 years elapsed)*

#### Scenario 2: Asset Created 1 Year Ago

| Asset | Purchase Date | Cost | Rate | Current Value |
|-------|---------------|------|------|----------------|
| Laptop | 23-03-2025 | ₹100,000 | 10% | ₹90,000 |

*(1 year elapsed, 10% depreciation)*

#### Scenario 3: Asset Created 2 Years Ago

| Asset | Purchase Date | Cost | Rate | Current Value |
|-------|---------------|------|------|----------------|
| Laptop | 23-03-2024 | ₹100,000 | 10% | ₹81,000 |

*(2 years elapsed, compound depreciation: 100k × 0.9 × 0.9)*

---

## 🛠️ Management Command

### Update Depreciation Values

You can manually update all asset depreciation values using:

```bash
python manage.py update_depreciation
```

**With verbose output:**
```bash
python manage.py update_depreciation --verbose
```

**Output example:**
```
Starting depreciation update for 15 assets...
✓ ASSET0001 (HP Laptop): ₹100000.00 → ₹95000.00
✓ ASSET0002 (Dell Desktop): ₹80000.00 → ₹72000.00
...
✅ Depreciation update complete!
Updated: 8/15 assets
```

### Scheduling Automatic Updates

To run this command automatically **daily**, add a cron job:

#### macOS/Linux

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * cd /path/to/asset-tracking-system && source venv/bin/activate && python manage.py update_depreciation
```

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 2:00 AM
4. Set action: `python manage.py update_depreciation`
5. Set working directory: `C:\path\to\asset-tracking-system`

---

## 📱 API Integration

### Asset List API

The depreciation value is included in API responses:

```json
{
  "id": 1,
  "asset_id": "ASSET0001",
  "name": "HP Laptop",
  "purchase_date": "2025-03-23",
  "purchase_cost": "100000.00",
  "depreciation_rate": "10.00",
  "current_value": "81000.00",
  "status": "in_use"
}
```

---

## 💾 Database Schema

### New Fields in Asset Model

```python
purchase_date = models.DateField()
purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2)
current_value = models.DecimalField(max_digits=12, decimal_places=2)
```

### Fields Description

| Field | Type | Description |
|-------|------|-------------|
| purchase_date | Date | Date of purchase |
| purchase_cost | Decimal | Original purchase cost |
| depreciation_rate | Decimal | Annual depreciation % |
| current_value | Decimal | Calculated current value |

---

## 🎓 Examples

### Example 1: Office Laptop

**Input:**
- Purchase Date: 01-01-2024
- Cost: ₹80,000
- Depreciation Rate: 20% per year

**Calculations:**
| Date | Years | Formula | Value |
|------|-------|---------|-------|
| 01-01-2024 | 0 | 80,000 × (0.8)^0 | ₹80,000 |
| 01-01-2025 | 1 | 80,000 × (0.8)^1 | ₹64,000 |
| 01-01-2026 | 2 | 80,000 × (0.8)^2 | ₹51,200 |
| 01-01-2027 | 3 | 80,000 × (0.8)^3 | ₹40,960 |

### Example 2: Office Printer

**Input:**
- Purchase Date: 15-06-2023
- Cost: ₹50,000
- Depreciation Rate: 15% per year

**Current (23-03-2026):**
- Years elapsed: ~2.8 years
- Current Value: ₹50,000 × (0.85)^2.8 ≈ ₹32,800

---

## ⚠️ Important Notes

1. **Depreciation is Calculated Dynamically**
   - Not stored as a fixed value
   - Changes every day based on elapsed time
   - Always reflects current date

2. **Rounding**
   - Values rounded to 2 decimal places
   - Suitable for financial reporting

3. **Negative Rates Not Supported**
   - Only depreciation (0-100%)
   - Appreciation not supported

4. **Historical Data**
   - Logs show all depreciation updates
   - Track value changes over time

5. **Reporting**
   - Use current_value for financial reports
   - Use activity logs for audit trails

---

## 🔄 Workflow

1. **Asset Creation**
   ```
   Admin adds asset with:
   - Purchase Date: 23-03-2026
   - Cost: ₹100,000
   - Rate: 5%
   ↓
   System calculates:
   - Current Value: ₹100,000 (day 0)
   ```

2. **Real-Time Viewing**
   ```
   User views asset on 23-03-2027:
   ↓
   System recalculates:
   - Current Value: ₹95,000 (1 year later)
   ↓
   Displays in:
   - Asset Detail page
   - Asset List page
   - API response
   ```

3. **Periodic Updates**
   ```
   Admin runs: python manage.py update_depreciation
   ↓
   System updates all assets
   ↓
   Creates audit log entries
   ```

---

## 🎯 Use Cases

### Financial Reporting
- Get accurate asset values for balance sheets
- Track depreciation for tax purposes
- Monitor asset portfolio value

### Budget Planning
- Know when assets will reach end-of-life value
- Plan replacement budgets based on depreciation
- Forecast future asset values

### Compliance & Auditing
- Maintain depreciation history
- Track all value changes in logs
- Generate audit trails

---

## 📊 Viewing Depreciation

### On Asset List
- New column shows "Current Value"
- Easy comparison of asset values
- Quick depreciation overview

### On Asset Detail
- Full "Financial Information" section
- Shows:
  - Purchase Date
  - Purchase Cost
  - Depreciation Rate
  - Current Value (calculated)
  - Depreciation amount

### In Activity Log
- All depreciation updates logged
- Shows old → new value
- Timestamp of each update
- System-generated entries

---

## 🔐 Access Control

- **All Users**: Can view current values
- **Admins**: Can set depreciation rates when creating/editing assets
- **System**: Automatically updates values

---

## 🐛 Troubleshooting

### Issue: Current Value Shows as "-"

**Cause**: Asset doesn't have purchase_date and purchase_cost set

**Solution**: Edit asset and add financial information

### Issue: Values Not Updating

**Cause**: Cache issue or page not refreshed

**Solution**: 
1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R)
3. Run: `python manage.py update_depreciation`

### Issue: Incorrect Depreciation Calculation

**Cause**: Wrong depreciation rate or purchase date

**Solution**:
1. Check asset details
2. Verify depreciation rate (should be 0-100)
3. Verify purchase date is correct

---

## 📝 Notes for Developers

### Method: `calculate_depreciation()`

Located in Asset model, calculates the depreciated value:

```python
def calculate_depreciation(self):
    """Calculate current value based on depreciation from purchase date"""
    # Uses compound depreciation formula
    # Returns Decimal value rounded to 2 places
```

### When Called

- During asset save (if financial data present)
- In management command
- In API serializers (optional)

### Performance

- Calculation is fast (mathematical operation)
- Not I/O intensive
- Can be called frequently without issues

---

## 🚀 Future Enhancements

Potential improvements:

1. **Multiple Depreciation Methods**
   - Straight-line depreciation
   - Declining balance
   - Units of production

2. **Depreciation Schedules**
   - Different rates per month/quarter
   - Non-linear depreciation

3. **Reports & Analytics**
   - Depreciation trends
   - Portfolio value over time
   - Depreciation projections

4. **Alerts**
   - When asset reaches minimum value
   - Depreciation milestones
   - Renewal recommendations

---

## 📚 Related Commands

```bash
# View all assets with financial info
python manage.py shell
>>> Asset.objects.filter(purchase_cost__isnull=False).count()

# Batch update depreciation
python manage.py update_depreciation --verbose

# Export asset values
python manage.py shell
>>> from tracker.models import Asset
>>> assets = Asset.objects.filter(purchase_cost__isnull=False)
>>> for a in assets: print(f"{a.asset_id}: ₹{a.current_value}")
```

---

## 📞 Support

For issues or questions about depreciation:

1. Check Activity Log on asset detail page
2. Run depreciation update command with `--verbose`
3. Review database values directly
4. Check migrations are applied

---

**Happy Asset Tracking with Depreciation! 📊**

*Last Updated: 23 March 2026*
