export interface NutritionTargets {
  nutrients: string[];
  foodTypes: string[];
}

const NUTRIENT_KEYWORDS = [
  'iron',
  'vitamin d',
  'vitamin c',
  'vitamin b12',
  'folate',
  'magnesium',
  'zinc',
  'calcium',
  'potassium',
  'omega-3',
  'protein',
];

const FOOD_TYPE_KEYWORDS = [
  'leafy greens',
  'citrus fruits',
  'whole grains',
  'legumes',
  'nuts and seeds',
  'fatty fish',
  'lean protein',
  'fermented foods',
  'dairy',
  'eggs',
  'berries',
];

const toUnique = (values: string[]) => Array.from(new Set(values.map(v => v.toLowerCase())));

export function extractNutritionTargetsFromDiagnosis(diagnosisText: string): NutritionTargets {
  const source = diagnosisText.toLowerCase();

  const nutrients = toUnique(
    NUTRIENT_KEYWORDS.filter(keyword => source.includes(keyword))
  );

  const foodTypes = toUnique(
    FOOD_TYPE_KEYWORDS.filter(keyword => source.includes(keyword))
  );

  return { nutrients, foodTypes };
}
