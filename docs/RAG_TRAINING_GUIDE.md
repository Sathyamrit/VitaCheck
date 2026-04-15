# RAG Training & Knowledge Base Management Guide

Complete guide to training VitaCheck RAG with custom data and managing your knowledge base.

---

## Overview

Your RAG system has **three ways** to manage the knowledge base:

1. **Local Training Script** - For quick iteration and testing
2. **Management Script** - For clearing, resetting, and exporting data
3. **Web Dashboard** - For production use with web interface

---

## Part 1: Local Training Script (`train_rag.py`)

### Quick Start

```bash
# Train from CSV
cd server
python train_rag.py sample_nutrients.csv

# Train from JSON
python train_rag.py nutrients.json --format json
```

### CSV Format

Your CSV should have these columns:

```
name,category,deficiency_symptoms,rda_male,rda_female,optimal_range,bioavailability,supplementation_notes,food_sources,drug_nutrient_interactions,absorption_factors
```

**Example row:**
```csv
Vitamin B12,Vitamin,"fatigue,weakness,brain fog",2.4 mcg,2.4 mcg,200-900 pmol/L,50-98% from animal products,Take sublingual form,Beef liver;Salmon;Eggs,"Metformin reduces B12 absorption","{""intrinsic_factor"": ""required""}"
```

**Column Details:**

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| name | string | Vitamin B12 | Unique identifier |
| category | string | Vitamin, Mineral | Used for filtering |
| deficiency_symptoms | string | fatigue;weakness;numbness | Semicolon or comma separated |
| rda_male | string | 2.4 mcg | Recommended Daily Allowance |
| rda_female | string | 2.4 mcg | Can be different from male |
| optimal_range | string | 200-900 pmol/L | Optimal blood levels |
| bioavailability | string | 50-98% from animal products | % absorption rate |
| supplementation_notes | string | Take sublingual form | Usage tips |
| food_sources | string | Beef liver;Salmon;Eggs | Semicolon separated |
| drug_nutrient_interactions | string | Metformin reduces B12 absorption | Comma or semicolon separated |
| absorption_factors | string | {"intrinsic_factor": "required"} | JSON format OK |

### JSON Format

```json
[
  {
    "name": "Vitamin B12",
    "category": "Vitamin",
    "deficiency_symptoms": ["fatigue", "weakness", "brain fog"],
    "rda_male": "2.4 mcg",
    "rda_female": "2.4 mcg",
    "optimal_range": "200-900 pmol/L",
    "bioavailability": "50-98% from animal products",
    "supplementation_notes": "Take sublingual form",
    "food_sources": [
      {"food": "beef liver", "amount": "100g", "content": "68 mcg"}
    ],
    "drug_nutrient_interactions": ["Metformin reduces B12 absorption"],
    "absorption_factors": {"intrinsic_factor": "required"}
  }
]
```

### Usage Examples

**Train with CSV (append to existing):**
```bash
python train_rag.py nutrients.csv --format csv
```

**Train with JSON with custom column mapping:**
```bash
python train_rag.py nutrients.csv --format csv --mapping '{"items": "name", "category": "type"}'
```

### Output Example

```
======================================================================
VITACHECK RAG TRAINING
======================================================================

[INFO] Loading CSV: sample_nutrients.csv
[INFO] Found 10 rows
[OK] Row 1: Vitamin B1 (Thiamine)
[OK] Row 2: Vitamin B3 (Niacin)
[OK] Row 3: Folate (Vitamin B9)
...
[OK] CSV loaded: 10 nutrients

[INFO] Adding 10 nutrients to vector store...
[INFO] Generating embeddings...
Batches: 100%|████████████| 1/1 [00:02<00:00, 2.51it/s]
[OK] 10 nutrients added to vector store

======================================================================
TRAINING REPORT
======================================================================
Total Added: 10
Total Updated: 0
Total Errors: 0

Items Added:
  • Vitamin B1 (Thiamine) (Vitamin)
  • Vitamin B3 (Niacin) (Vitamin)
  • Folate (Vitamin B9) (Vitamin)
  • Vitamin B5 (Pantothenic Acid) (Vitamin)
  • Zinc (Mineral)
  • Copper (Mineral)
  • Selenium (Mineral)
  • Vitamin C (Vitamin)
  • Vitamin E (Vitamin)
  • Chromium (Mineral)

[OK] Training complete!
```

---

## Part 2: Management Script (`manage_rag_kb.py`)

Control your knowledge base: list, clear, reset, export, delete.

### Commands

#### 1. List All Items

```bash
python manage_rag_kb.py list
```

**Output:**
```
[OK] Found 15 items in knowledge base:
======================================================================
1. Vitamin B12 (Cobalamin) (Vitamin)
2. Iron (Mineral)
3. Vitamin D (Vitamin)
4. Magnesium (Mineral)
5. Zinc (Mineral)
6. Vitamin B1 (Thiamine) (Vitamin)
...
```

#### 2. Show Statistics

```bash
python manage_rag_kb.py stats
```

**Output:**
```
[OK] KB STATISTICS:
======================================================================
Total Items: 15
Categories:
  • Vitamin: 8
  • Mineral: 7
```

#### 3. Delete Specific Item

```bash
python manage_rag_kb.py delete-item vitamin_b12_cobalamin
```

#### 4. Delete All Items in Category

```bash
python manage_rag_kb.py delete-category Vitamin
```

⚠️ **Warning:** This will delete ALL vitamins from your KB!

#### 5. Clear All Data

```bash
python manage_rag_kb.py clear
```

**Interactive confirmation:**
```
[WARNING] This will DELETE ALL data from ChromaDB!
Type 'yes' to confirm: yes
[INFO] Clearing all items from vector store...
[OK] Deleted 15 items
```

**Skip confirmation with `--confirm` flag:**
```bash
python manage_rag_kb.py clear --confirm
```

#### 6. Reset to Default Micronutrients

```bash
python manage_rag_kb.py reset
```

**What it does:**
- Clears all existing data
- Reloads the 5 default micronutrients (B12, Iron, Vitamin D, Magnesium, Zinc)
- Perfect to start fresh

```bash
python manage_rag_kb.py reset --confirm
```

#### 7. Export KB to JSON

```bash
python manage_rag_kb.py export kb_backup.json
```

**Creates:**
```json
{
  "metadata": [
    {"name": "Vitamin B12", "category": "Vitamin"},
    {"name": "Iron", "category": "Mineral"},
    ...
  ],
  "documents": [...],
  "count": 15
}
```

#### 8. Delete Entire ChromaDB Collection

```bash
python manage_rag_kb.py delete-collection
```

⚠️ **DANGER:** Deletes the entire ChromaDB storage. This is a full reset.

---

## Part 3: Web Dashboard

### Setup

1. **Install in React app** (already done):
   ```
   client/src/components/RAGDashboard/RAGDashboard.tsx
   client/src/components/RAGDashboard/RAGDashboard.css
   ```

2. **Import in your app:**
   ```tsx
   import RAGDashboard from './components/RAGDashboard/RAGDashboard';

   export default function App() {
     return <RAGDashboard />;
   }
   ```

3. **Add to your router** (if using React Router):
   ```tsx
   <Route path="/rag-dashboard" element={<RAGDashboard />} />
   ```

### Features

- 📂 **File Upload** - Drag & drop or click to upload CSV/JSON
- 📊 **Live Statistics** - Real-time KB stats and categories
- 🔄 **Training Progress** - Visual progress bar during training
- 🗑️ **Management** - Clear, reset, export KB with confirmation
- 📋 **Current Items** - View all items in knowledge base
- ⬇️ **Sample Download** - Download template CSV for reference

### Usage

1. **Visit `/rag-dashboard` in your app**
2. **Click "Download Sample CSV"** to understand the format
3. **Prepare your CSV with nutrient data**
4. **Upload and click "Start Training"**
5. **Monitor the progress bar**
6. **Check updated statistics**

---

## Workflow Comparison

### Development Phase (Use Local Script)

```bash
# Fast iteration
python train_rag.py new_nutrients.csv
python manage_rag_kb.py stats
python manage_rag_kb.py clear --confirm
python train_rag.py refined_data.csv
```

**✅ Pros:**
- Fast
- No browser needed
- Easy to script/automate
- Great for testing

**❌ Cons:**
- Command line only
- Not user-friendly
- Hard to distribute

### Production Phase (Use Dashboard)

**✅ Pros:**
- Web-based interface
- Non-technical users can use it
- Real-time feedback
- Visual management
- Professional appearance

**❌ Cons:**
- More complex backend integration needed
- Requires API endpoints

---

## Practical Scenarios

### Scenario 1: Add 10 New Nutrients

```bash
# Prepare your data in CSV format
# Then train:
python train_rag.py new_nutrients.csv

# Check what was added
python manage_rag_kb.py stats
```

### Scenario 2: Switch to Completely Different Dataset

```bash
# Reset to defaults
python manage_rag_kb.py reset --confirm

# Train with new data
python train_rag.py different_dataset.csv

# Verify
python manage_rag_kb.py list
```

### Scenario 3: Backup Before Major Changes

```bash
# Export current KB
python manage_rag_kb.py export kb_backup_march27.json

# Now safe to do risky operations
python manage_rag_kb.py clear --confirm
python train_rag.py experimental_data.csv

# If something goes wrong, you have the backup
```

### Scenario 4: Regular Training Workflow

```bash
# Monday: Add new research findings
python train_rag.py new_findings_2024.csv

# Wednesday: Add supplement interactions
python train_rag.py supplement_interactions.csv

# Friday: Check stats
python manage_rag_kb.py stats

# Export weekly backup
python manage_rag_kb.py export kb_backup_week_12.json
```

---

## Advanced: Data Validation

Before training, validate your CSV:

```bash
python -c "
import pandas as pd
df = pd.read_csv('nutrients.csv')
print(f'Rows: {len(df)}')
print(f'Columns: {list(df.columns)}')
print('Sample:')
print(df.head())
"
```

### Required Columns Checklist

- [ ] `name` - Unique nutrient name
- [ ] `category` - Vitamin or Mineral
- [ ] `deficiency_symptoms` - Comma/semicolon separated
- [ ] `rda_male` - Male RDA with units
- [ ] `rda_female` - Female RDA with units
- [ ] `food_sources` - Food items with semicolons
- [ ] `drug_nutrient_interactions` - Drug interactions
- [ ] `bioavailability` - % or description

### Common Issues

**Issue:** "JSON decode error in absorption_factors"
- Fix: Ensure JSON is properly formatted or use semicolon-separated list

**Issue:** Too many errors in training
- Fix: Check column names match exactly (case-sensitive)

**Issue:** Data not appearing after training
- Fix: Run `python manage_rag_kb.py list` to verify it was added
- Check: Is ChromaDB collection initialized? Run `python manage_rag_kb.py stats`

---

## Next Steps

1. **Prepare your nutrient dataset** in CSV format
2. **Test with `sample_nutrients.csv`** first
3. **Use local script for development**
4. **Deploy dashboard for production**
5. **Regular backups** with `export` command

---

## API Endpoints (For Future Dashboard Integration)

Coming soon - These will be added to `streaming_api.py`:

- `POST /rag/train` - Upload and train CSV/JSON
- `GET /rag/items` - List all KB items
- `GET /rag/stats` - Get KB statistics  
- `POST /rag/clear` - Clear all data
- `POST /rag/reset` - Reset to defaults
- `GET /rag/export` - Export KB as JSON
- `DELETE /rag/item/:id` - Delete specific item

---

**Happy training! 🚀**
