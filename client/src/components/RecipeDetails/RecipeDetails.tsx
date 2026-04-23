import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const RecipeDetails: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { recipe } = location.state || {};

  if (!recipe) return <div className="p-20 text-center">Recipe not found.</div>;

  // Helpers to generate external links
  const query = encodeURIComponent(`${recipe.name} recipe`);
  const youtubeLink = `https://www.youtube.com/results?search_query=${query}`;
  const googleLink = `https://www.google.com/search?q=${query}`;

  return (
    <div className="max-w-4xl mx-auto py-16 px-6">
      <button onClick={() => navigate(-1)} className="mb-8 font-black uppercase text-xs tracking-widest text-gray-400">
        ← Back to Meal Plan
      </button>

      <div className="bg-white rounded-[3rem] p-12 shadow-2xl border border-gray-100">
        <h1 className="text-5xl font-black uppercase tracking-tighter mb-6">{recipe.name}</h1>
        
        <div className="flex flex-wrap gap-4 mb-8">
          <a href={youtubeLink} target="_blank" rel="noreferrer" 
             className="bg-red-600 text-white px-6 py-3 rounded-full text-xs font-black uppercase flex items-center gap-2 hover:bg-red-700 transition-all">
             Watch on YouTube
          </a>
          <a href={googleLink} target="_blank" rel="noreferrer" 
             className="bg-blue-600 text-white px-6 py-3 rounded-full text-xs font-black uppercase flex items-center gap-2 hover:bg-blue-700 transition-all">
             Search Web Recipes
          </a>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="md:col-span-1">
            <h3 className="font-black uppercase text-[#f7a221] text-sm mb-4">Ingredients</h3>
            <ul className="space-y-3 text-gray-700 font-medium">
              {recipe.ingredients?.map((ing: string, i: number) => (
                <li key={i} className="border-b border-gray-100 pb-2">{ing}</li>
              ))}
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-black uppercase text-[#f7a221] text-sm mb-4">Preparation Steps</h3>
            <ol className="space-y-6">
              {recipe.instructions?.map((step: string, i: number) => (
                <li key={i} className="flex gap-4">
                  <span className="font-black text-2xl text-gray-200">{i + 1}</span>
                  <p className="text-gray-700 leading-relaxed">{step}</p>
                </li>
              ))}
            </ol>
            
            <div className="mt-12 p-8 bg-gray-50 rounded-3xl border border-gray-100">
              <h4 className="font-black uppercase text-xs mb-2">Nutritional Rationale</h4>
              <p className="text-sm text-gray-500 italic">{recipe.rationale}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetails;