import { GoogleGenerativeAI } from "@google/generative-ai";
import ReactMarkdown from 'react-markdown';

import { useState } from "react";

const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY);

interface GeminiRecipeProps {
  items: PantryItem[]; 
}


export default function GeminiRecipe({items}: GeminiRecipeProps) {
  const [recipeText, setRecipeText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
 

  const getRecipeSuggestion = async (items: PantryItem[]) => {
    const sortedIngredients = [...items].sort((a, b) =>
      new Date(a.expirationDate).getTime() - new Date(b.expirationDate).getTime()
    );

    const ingredientList = sortedIngredients
      .map(item => `- ${item.name} (Expires: ${item.expirationDate})`)
      .join("\n");

    const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });

    const prompt = `
      I have the following ingredients in my pantry, listed in order of expiration.
      Please suggest a recipe that prioritizes using the items at the top of the list
      to prevent food waste.

      Ingredients:
      ${ingredientList}

      Provide the recipe name, a brief description, and instructions.
    `;

    const result = await model.generateContent(prompt);

    return result.response.text();  
  }

  const handleClick = async () => {
    setIsLoading(true);
    try {
      const geminiText = await getRecipeSuggestion(items);
      setRecipeText(geminiText);
    } catch (error) {
      console.error("Gmeini failed:", error);
      setRecipeText("Sorry, I couldn't cook that up right now.");
    } finally {
      setIsLoading(false);
    }
  }
  
  return (
    <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-1 shadow-xl">
      <div className="bg-white rounded-[22px] p-6 h-full">
        <div className="flex items-center gap-4 mb-8">
          <div className="bg-blue-100 p-2 text-2xl rounded-lg text-blue-600"> ✨ </div>
          <h2 className="font-black text-3xl text-slate-800 tracking-tight">Recipe Generator</h2>
        </div>

        <p className="text-slate-500 text-sm mb-6">
          Need ideas? I'll scan your expiring items and suggest a meal.
        </p>
        <button 
          onClick={handleClick} 
          disabled={isLoading}
          className="w-full py-4 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition-all disabled:opacity-50 flex items-center justify-center gap-2 mb-6"
        >
          {isLoading ? <span className="animate-pulse">Chef is cooking...</span> : "Suggest a Recipe"}
        </button>
        
        {recipeText && (
          <div className="mt-4 border-t border-slate-100 pt-6 prose prose-sm prose-blue max-h-[500px] overflow-y-auto">
            <ReactMarkdown>{recipeText}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}
