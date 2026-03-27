/**
 * Recipe Generation Hook
 * Uses Groq API to generate recipes based on nutrients and food types from diagnosis
 */

import { useState, useCallback } from 'react';

export interface Recipe {
  name: string;
  ingredients: string[];
  instructions: string[];
  prep_time: string;
  servings: number;
  nutrients_provided: string[];
  rationale: string;
}

export interface DiagnosisNutrients {
  nutrients: string[];
  food_types: string[];
  deficiencies: string[];
  [key: string]: any;
}

export function useRecipeGeneration() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateRecipes = useCallback(async (
    diagnosisText: string,
    nutrients: string[] = [],
    preferences: {
      dietType?: string;
      allergies?: string;
      cookingTime?: string;
    } = {}
  ) => {
    setLoading(true);
    setError(null);

    try {
      // Extract nutrients from diagnosis if not explicitly provided
      let targetNutrients = nutrients;
      if (targetNutrients.length === 0) {
        // Try to extract nutrients mentioned in diagnosis
        const nutrientPatterns = /vitamin|mineral|iron|calcium|magnesium|zinc|folate|b12|vitamin d|vitamin c|potassium/gi;
        const matches = diagnosisText.match(nutrientPatterns);
        targetNutrients = Array.from(new Set(matches?.map(m => m.toLowerCase()) || []));
      }

      const prompt = `You are a culinary nutritionist. Generate 3 personalized recipes based on the following:

DIAGNOSIS: ${diagnosisText.substring(0, 500)}

TARGET NUTRIENTS TO INCLUDE:
${targetNutrients.join(', ') || 'balanced micronutrients'}

DIETARY PREFERENCES:
- Diet Type: ${preferences.dietType || 'Standard'}
- Allergies/Restrictions: ${preferences.allergies || 'None'}
- Preferred Cooking Time: ${preferences.cookingTime || '30-45 minutes'}

For each recipe, provide JSON format:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "ingredients": ["ingredient 1", "ingredient 2"],
      "instructions": ["step 1", "step 2"],
      "prep_time": "20 mins",
      "cooking_time": "25 mins",
      "servings": 2,
      "nutrients_provided": ["nutrient 1", "nutrient 2"],
      "rationale": "Why this recipe helps with the diagnosed deficiencies"
    }
  ]
}

IMPORTANT: Return ONLY valid JSON, no markdown blocks or additional text.`;

      // Call Groq API directly (or use backend endpoint if available)
      const response = await fetch('http://localhost:8000/generate-recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          diagnosis: diagnosisText,
          nutrients: targetNutrients,
          preferences,
        }),
      });

      if (!response.ok) {
        throw new Error(`Recipe generation failed: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.recipes && Array.isArray(data.recipes)) {
        setRecipes(data.recipes);
        return data.recipes;
      } else {
        throw new Error('Invalid recipe format received');
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to generate recipes';
      setError(errorMsg);
      console.error('Recipe generation error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    recipes,
    loading,
    error,
    generateRecipes,
  };
}
