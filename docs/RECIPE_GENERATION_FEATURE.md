# Recipe Generation Feature Implementation

## Overview
Added a complete recipe generation workflow that connects the diagnostic results from DeepSeek RAG to personalized recipe generation via Groq API.

## User Flow

### 1. **Diagnostic Dashboard** (`DiagnosticDashboard.tsx`)
- User completes symptom assessment
- AI analyzes and streams diagnosis with identified nutrients
- **NEW**: After diagnosis completes, two buttons appear:
  - 🍳 **"Generate Personalized Recipes"** (orange/primary)
  - ↻ "Start New Session" (gray/secondary)

### 2. **Recipe Generation** (New)
When user clicks "Generate Personalized Recipes":
- Diagnosis data, extracted nutrients, and symptoms are passed to MealPlan page
- User can select dietary preferences (Vegetarian, Vegan, Keto, etc.)
- User can specify allergies/restrictions
- Groq API generates 3 recipes optimized for the identified deficiencies

### 3. **Meal Plan Display** (`MealPlan.tsx`)
- Shows recipe cards with:
  - Recipe name
  - Key nutrients provided (highlighted in orange)
  - Prep time
  - Rationale (why this recipe targets the deficiencies)
  - Instructions (expandable)
  - Servings information

## Technical Implementation

### Frontend Components

#### 1. **New Hook: `useRecipeGeneration.ts`**
```typescript
export function useRecipeGeneration() {
  const generateRecipes = async (
    diagnosisText: string,
    nutrients: string[] = [],
    preferences: { dietType, allergies, cookingTime } = {}
  ) => Recipe[]
}
```

**Features:**
- Extracts nutrients from diagnosis text if not explicitly provided
- Calls backend `/generate-recipes` endpoint
- Returns array of Recipe objects with full details
- Error handling for failed generations

**Recipe Type:**
```typescript
interface Recipe {
  name: string;
  ingredients: string[];
  instructions: string[];
  prep_time: string;
  cooking_time: string;
  servings: number;
  nutrients_provided: string[];
  rationale: string;
}
```

#### 2. **Updated: `DiagnosticDashboard.tsx`**
**New imports:**
```typescript
import { useNavigate } from 'react-router-dom';
```

**New function:**
```typescript
const handleGenerateRecipe = () => {
  navigate('/meal-plan', {
    state: {
      diagnosis,           // Full diagnosis text
      extracted,           // Symptoms, medications, allergies
      symptoms,            // Array of identified symptoms
      medications,         // User medications
      allergies,           // User allergies
    },
  });
};
```

**New UI:**
- Added "Generate Personalized Recipes" button (orange) above "Start New Session"
- Visible only when `status === 'completed'`
- Button uses navigation state to pass diagnosis data to MealPlan

#### 3. **Updated: `MealPlan.tsx`**
**New imports:**
```typescript
import { useLocation } from 'react-router-dom';
import { useRecipeGeneration } from '../hooks/useRecipeGeneration';
```

**Data sources (priority order):**
1. Navigation state from DiagnosticDashboard (preferred)
2. TaskId from URL params (fallback for legacy flow)

**New function:**
```typescript
const handleStartGeneration = async () => {
  const generatedRecipes = await generateRecipes(
    diagnosisData.diagnosis,
    diagnosisData.extracted?.symptoms || [],
    preferences
  );
  setRecipesData(generatedRecipes);
};
```

**Enhanced recipe display:**
- Shows `nutrients_provided` array as tags (orange background)
- Displays `rationale` explaining why recipe targets deficiencies
- Shows cooking time in addition to prep time

### Backend Endpoint

#### **`POST /generate-recipes`** (New)

**Request:**
```json
{
  "diagnosis": "Patient has symptoms of iron and B12 deficiency...",
  "nutrients": ["iron", "vitamin b12", "folate"],
  "preferences": {
    "dietType": "Vegetarian",
    "allergies": "gluten",
    "cookingTime": "30 mins"
  }
}
```

**Response:**
```json
{
  "recipes": [
    {
      "name": "Spinach & Lentil Soup",
      "ingredients": ["2 cups spinach", "1 cup lentils", ...],
      "instructions": ["Heat oil", "Add lentils", ...],
      "prep_time": "15 mins",
      "cooking_time": "25 mins",
      "servings": 2,
      "nutrients_provided": ["iron", "folate", "magnesium"],
      "rationale": "Rich in plant-based iron paired with vitamin C from tomatoes for enhanced absorption..."
    },
    {...},
    {...}
  ]
}
```

**Implementation details:**
- Uses Groq API (`mixtral-8x7b-32768` model)
- Structured prompt ensures valid JSON response
- Fallback JSON parsing handles markdown-wrapped responses
- Error handling with descriptive messages
- <30s timeout

## Data Flow Architecture

```
DiagnosticDashboard
    ↓ (AI completes diagnosis)
    ↓ streamDiagnosis = diagnosis text + extracted data
    ↓
    ├─→ [Display diagnosis]
    ├─→ User clicks "Generate Recipes"
    │
    ↓
    └─→ navigate('/meal-plan', { state: { diagnosis, extracted, ... } })
        ↓
        MealPlan
        ├─→ useLocation().state extracts diagnosis data
        ├─→ User selects dietary preferences
        ├─→ User clicks "Generate Personalized Recipes"
        │
        ↓
        useRecipeGeneration.generateRecipes(diagnosis, nutrients, prefs)
        │
        ↓
        POST /generate-recipes
        │
        ↓
        Backend (Groq API)
        ├─→ Parse diagnosis for nutrients
        ├─→ Build nutrition-focused prompt
        ├─→ Call Groq with mixtral model
        ├─→ Parse JSON response
        │
        ↓
        Return recipes array
        │
        ↓
        MealPlan displays recipes with:
        - Name
        - Nutrients provided (tagged)
        - Rationale
        - Ingredients
        - Instructions
        - Prep/cook times
```

## Route Configuration

**Existing routes should be:**
```tsx
<Route path="/diagnostic-dashboard" element={<DiagnosticDashboard />} />
<Route path="/meal-plan" element={<MealPlan />} />
```

The new flow uses:
1. User navigates to `/diagnostic-dashboard`
2. Completes assessment → diagnoses
3. Clicks "Generate Personalized Recipes"
4. Navigates to `/meal-plan` with state (no URL params needed)
5. Selects dietary preferences
6. Views generated recipes

## Environment Variables

**Required in `.env`:**
```env
GROQ_API_KEY=your_groq_api_key_here
```

The backend already reads this for the extraction phase, and now also uses it for recipe generation.

## Testing the Feature

### 1. **Complete a Diagnosis**
```bash
# Start the backend
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
python streaming_api.py

# Start the frontend
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\client
npm run dev
```

### 2. **Access Diagnostic Dashboard**
- Navigate to `http://localhost:5173/diagnostic-dashboard`
- Complete the questionnaire
- Enter contextual analysis
- Click "Start AI Analysis"

### 3. **Generate Recipes**
- After diagnosis completes, click "Generate Personalized Recipes"
- Select dietary preferences
- Specify any allergies
- Click "Generate Personalized Recipes"
- View the generated recipes with nutrient information

## Error Handling

**Frontend errors:**
- Missing diagnosis data → Shows "No diagnosis data available"
- Failed recipe generation → Displays error message and allows retry
- Network timeout → Handled gracefully with error display

**Backend errors:**
- Groq API failure → Returns error with empty recipes array
- Malformed JSON response → Attempts to extract JSON from markdown
- Network timeout → 30s timeout with error response

## Next Steps / Enhancements

1. **Add recipe detail modal** - Click "View Details" to see full ingredients and instructions
2. **Save favorite recipes** - Users can bookmark recipes to their profile
3. **Shopping list generation** - Generate aggregated shopping list from selected recipes
4. **Nutritional breakdown** - Show macros and micros per serving
5. **Recipe difficulty levels** - Filter by cooking skill required
6. **Seasonal ingredient options** - Suggest seasonal alternatives for ingredients
7. **Batch recipe generation** - Generate more than 3 recipes if needed
8. **Recipe history** - Track which recipes user has tried and their feedback

## Files Modified

1. ✅ `client/src/hooks/useRecipeGeneration.ts` - NEW
2. ✅ `client/src/pages/DiagnosticDashboard.tsx` - Updated
3. ✅ `client/src/pages/MealPlan.tsx` - Updated
4. ✅ `server/streaming_api.py` - Updated with `/generate-recipes` endpoint

## Estimated Performance

- **Recipe generation latency:** 3-5s (Groq API response time)
- **Total time from diagnosis to recipes:** <10s
- **Frontend response:** <100ms (navigation + state passing)
- **Backend parsing:** <500ms (JSON parsing + response formatting)
