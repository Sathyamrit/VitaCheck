export interface SymptomPayload {
  age: number;
  gender: 'male' | 'female' | 'other';
  rawInput: string;
  structuredSymptoms?: string;
}

export interface AnalysisResult {
  deficiency: string;
  confidence: number;
  physicalSigns: string;
  recommendations: string;
  recipes: Recipe;
}

export interface Recipe {
  id: string;
  title: string;
  nutrients: string;
  image: string;
}

// Structure of user inputs and the expected analysis results from the AI