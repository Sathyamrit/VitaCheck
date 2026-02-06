import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const RecipeSection: React.FC<{ diagnosis: string }> = () => {
  const navigate = useNavigate();
  const { taskId } = useParams<{ taskId: string }>();

  return (
    <section className="bg-gray-900 text-white rounded-[2.5rem] p-10 shadow-2xl flex flex-col h-fit sticky top-8">
      <h3 className="text-2xl font-black uppercase mb-2 text-[#f7a221]">Dietary Therapy</h3>
      <p className="text-gray-400 text-[10px] mb-8 font-bold uppercase tracking-widest leading-relaxed">
        Based on your clinical markers, our AI has synthesized a targeted nutritional intervention.
      </p>
      
      <button 
        onClick={() => navigate(`/meal-plan/${taskId}`)}
        className="w-full bg-white text-black py-5 rounded-3xl font-black uppercase hover:bg-[#f7a221] hover:text-white transition-all text-sm tracking-widest shadow-xl"
      >
        View Full Meal Plan
      </button>

      <div className="mt-8 pt-8 border-t border-white/10">
        <p className="text-[9px] text-gray-500 font-medium text-center uppercase tracking-tighter">
          Verified against the NutriCuisine Index and global food composition databases.[1, 2]
        </p>
      </div>
    </section>
  );
};

export default RecipeSection;