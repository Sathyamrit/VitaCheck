# RAG Training - Complete Option C Implementation

## ✅ What You Have

### 1. Local Training Script - `train_rag.py`
**For:** Development, rapid iteration, testing

```bash
# Train with CSV
python train_rag.py nutrients.csv

# Train with JSON
python train_rag.py nutrients.json --format json

# With custom column mapping
python train_rag.py data.csv --mapping '{"my_column": "name"}'
```

**Supports:**
- ✅ CSV import
- ✅ JSON import
- ✅ Custom column mapping
- ✅ Batch training
- ✅ Progress reporting
- ✅ Error handling

---

### 2. Management Script - `manage_rag_kb.py`
**For:** Clearing, resetting, backing up, exporting

```bash
# List all items
python manage_rag_kb.py list

# Show statistics
python manage_rag_kb.py stats

# Delete specific item
python manage_rag_kb.py delete-item vitamin_b12

# Delete category
python manage_rag_kb.py delete-category Vitamin

# Clear all data
python manage_rag_kb.py clear --confirm

# Reset to defaults
python manage_rag_kb.py reset --confirm

# Export to JSON
python manage_rag_kb.py export backup.json

# Delete entire collection
python manage_rag_kb.py delete-collection --confirm
```

**Supports:**
- ✅ List items by category
- ✅ View KB statistics
- ✅ Delete individual items
- ✅ Delete by category
- ✅ Clear all data
- ✅ Reset to defaults
- ✅ Export entire KB
- ✅ Delete collection

---

### 3. Web Dashboard - `RAGDashboard.tsx`
**For:** Production use, non-technical users, visual management

**Features:**
- 📤 Drag & drop file upload
- 📊 Real-time KB statistics
- 🔄 Training progress visualization
- 📥 Sample CSV download
- 🗑️ Clear/Reset with confirmation
- 📋 View all KB items
- 📥 Export KB

**Location:** `client/src/components/RAGDashboard/`

**Setup:**
```tsx
import RAGDashboard from './components/RAGDashboard/RAGDashboard';

// In your app
<RAGDashboard />
```

---

## 📊 Comparison Table

| Feature | Local Script | Management Script | Dashboard |
|---------|-------------|-------------------|-----------|
| Train CSV | ✅ | ❌ | ✅ |
| Train JSON | ✅ | ❌ | ✅ |
| List items | ❌ | ✅ | ✅ |
| Stats | ❌ | ✅ | ✅ |
| Delete items | ❌ | ✅ | ✅ |
| Clear all | ❌ | ✅ | ✅ |
| Reset defaults | ❌ | ✅ | ✅ |
| Export KB | ❌ | ✅ | ✅ |
| Web interface | ❌ | ❌ | ✅ |
| No dependencies | ✅ | ✅ | ❌ (API needed) |
| Batch processing | ✅ | ❌ | ❌ |

---

## 🚀 Quick Start Workflow

### Development (Use Local Script)

```bash
# Step 1: Train with your data
cd server
python train_rag.py my_nutrients.csv

# Step 2: Check what was added
python manage_rag_kb.py list

# Step 3: Show statistics
python manage_rag_kb.py stats

# Step 4: If not happy, clear and retry
python manage_rag_kb.py clear --confirm
python train_rag.py different_data.csv

# Step 5: Backup when satisfied
python manage_rag_kb.py export kb_final.json
```

### Production (Use Dashboard)

**For end users, use the web dashboard:**

1. Navigate to `/rag-dashboard`
2. Click "Download Sample CSV" to see the format
3. Prepare your CSV file
4. Upload using the upload area
5. Click "Start Training"
6. Watch progress
7. Verify in stats

---

## 📝 Data Format

### CSV Format

Required columns:
```
name,category,deficiency_symptoms,rda_male,rda_female,optimal_range,bioavailability,supplementation_notes,food_sources,drug_nutrient_interactions,absorption_factors
```

Example:
```csv
Vitamin B12,Vitamin,fatigue;weakness;brain fog,2.4 mcg,2.4 mcg,200-900 pmol/L,50-98% from animal products,Take sublingual form,Beef liver;Salmon;Eggs,Metformin reduces B12 absorption,"{""intrinsic_factor"": ""required""}"
```

### JSON Format

```json
[
  {
    "name": "Vitamin B12",
    "category": "Vitamin",
    "deficiency_symptoms": ["fatigue", "weakness"],
    "rda_male": "2.4 mcg",
    "rda_female": "2.4 mcg",
    "optimal_range": "200-900 pmol/L",
    "bioavailability": "50-98% from animal products",
    "supplementation_notes": "Take sublingual form",
    "food_sources": [{"food": "Beef liver", "amount": "100g", "content": "68 mcg"}],
    "drug_nutrient_interactions": ["Metformin reduces B12 absorption"],
    "absorption_factors": {"intrinsic_factor": "required"}
  }
]
```

---

## ❓ FAQ

### Q: Which should I use?

**A:** 
- **Development/Testing?** → Use `train_rag.py` (fastest)
- **Managing data?** → Use `manage_rag_kb.py` (most control)
- **Real users?** → Use Dashboard (most user-friendly)

### Q: Can I clear ChromaDB and start fresh?

**A:** Yes!

**Option 1 (Keep defaults):**
```bash
python manage_rag_kb.py reset --confirm
```

**Option 2 (Complete wipe):**
```bash
python manage_rag_kb.py clear --confirm
```

**Option 3 (Nuclear):**
```bash
python manage_rag_kb.py delete-collection --confirm
```

### Q: What if training fails?

**A:**
1. Run: `python manage_rag_kb.py stats` to check current state
2. Export backup: `python manage_rag_kb.py export backup.json`
3. Clear and retry: `python manage_rag_kb.py clear --confirm`
4. Check CSV format is correct (see Data Format section)

### Q: Can I see what's trained?

**A:** Yes, list everything:
```bash
python manage_rag_kb.py list
```

### Q: How do I update just one nutrient?

**A:**
```bash
# Delete it
python manage_rag_kb.py delete-item vitamin_b12_cobalamin

# Re-train with updated data
python train_rag.py updated_nutrients.csv
```

### Q: Can I mix different datasets?

**A:** Yes! Keep training over and over:
```bash
python train_rag.py vitamins.csv
python train_rag.py minerals.csv
python train_rag.py supplements.csv
# All added together!
```

---

## 📂 File Structure

```
server/
├── train_rag.py              # ← Training script
├── manage_rag_kb.py          # ← Management script
├── sample_nutrients.csv       # ← Example data
├── RAG_TRAINING_GUIDE.md     # ← Full documentation
├── micronutrient_kb.py       # (existing)
├── vector_store.py           # (existing)
└── rag_pipeline.py           # (existing)

client/src/components/
├── RAGDashboard/
│   ├── RAGDashboard.tsx      # ← React component
│   └── RAGDashboard.css      # ← Styles
```

---

## 🎯 Usage Scenarios

### Scenario: Add 50 New Nutrients

```bash
# 1. Prepare nutrients.csv with 50 rows
# 2. Train
python train_rag.py nutrients.csv

# 3. Verify
python manage_rag_kb.py stats
python manage_rag_kb.py list | head -20
```

### Scenario: Switch to Completely Different Data

```bash
# 1. Backup current data
python manage_rag_kb.py export backup.json

# 2. Clear everything
python manage_rag_kb.py clear --confirm

# 3. Train with new dataset
python train_rag.py new_dataset.csv

# 4. Verify
python manage_rag_kb.py stats
```

### Scenario: Daily Updates

```bash
# Every day, just append new data
for file in daily_updates/*.csv; do
    python train_rag.py "$file"
done

# Check growth
python manage_rag_kb.py stats
```

### Scenario: Weekly Backups

```bash
# Every Friday
python manage_rag_kb.py export kb_backup_$(date +%Y%m%d).json
```

---

## 🔧 Troubleshooting

### Problem: "File not found"
```bash
# Make sure you're in the right directory
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
python train_rag.py sample_nutrients.csv
```

### Problem: "JSON decode error"
```bash
# Your CSV might have bad JSON in columns
# Try with simpler format first:
python train_rag.py simple_nutrients.csv
```

### Problem: Trained but not appearing
```bash
# Verify it was added
python manage_rag_kb.py list

# Check stats
python manage_rag_kb.py stats

# Check the vector store directly
python -c "
from vector_store import vector_store
print(f'Items in store: {vector_store.collection.count()}')
"
```

### Problem: "ChromaDB locked"
```bash
# Kill any hanging processes
taskkill /F /IM python.exe 2>$null || true

# Wait a moment
# Retry
```

---

## 📞 Support

**Questions about:**
- **Training?** → See `RAG_TRAINING_GUIDE.md`
- **Management?** → Run `python manage_rag_kb.py --help`
- **Format?** → Check `sample_nutrients.csv`
- **Dashboard?** → Check `RAGDashboard.tsx` code

---

## ✨ Summary

**You now have:**
1. ✅ `train_rag.py` - Add data (CSV/JSON)
2. ✅ `manage_rag_kb.py` - Manage/clear/export
3. ✅ `RAGDashboard.tsx` - Web interface
4. ✅ `sample_nutrients.csv` - Example data
5. ✅ `RAG_TRAINING_GUIDE.md` - Full documentation

**Start training!** 🚀

```bash
python train_rag.py sample_nutrients.csv
```
