import { useState, useEffect } from 'react'
import './App.css'

// My component imports
import CardOrganizer from './CardOrganizer'
import GeminiRecipe  from './GeminiRecipe'

// My type imports
import type { PantryItem } from './types/item'
import type { PriorityExpiration } from './types/priority'
import      { Priority } from './types/priority'

// My helpers
import { getDaysUntil } from './utils/date'


function App() {
  const [items, setItems] = useState([]);
  const [locations, setLocations] = useState([]);
  const [selectedLocations, setSelectedLocations] = useState([]);

  const foods = ["apple", "banana", "butter", "chocolate", "milk", "strawberries"];

  useEffect(() => {
    let hasLoaded = false;

    const fetchImage = async () => {
      const newItems: PantryItems[] = [];

      const response = await fetch(`http://localhost:8000/api/items`, {
        method: 'GET'
      });

      const data = await response.json();

      if (!hasLoaded) {
        setItems(data);
      }
    }

    const getLocations = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/locations`, {
          method: 'GET'
        });
        const data = await response.json();
        setLocations(data);
        setSelectedLocations(data.map((location) => { return location.id; }));
      } catch (error) {
        console.error("Failed to fetch locations", error);
      }
    }
    
    fetchImage();
    getLocations();

    return () => {
      hasLoaded = true;
    };
  }, []);

  console.log(items);

  const priorityExpiration: PriorityExpiration = {
    [Priority.Max]: {
      deadline: getDaysUntil(0),
      label: "Expired",
      colorClass: "bg-black"
    },
    [Priority.High]: {
      deadline: getDaysUntil(2),
      label: "Expiring Soon!",
      colorClass: "bg-red-500",
    },
    [Priority.Medium]: {
      deadline: getDaysUntil(7),
      label: "Expires in less than a Week",
      colorClass: "bg-orange-500",
    },
    [Priority.Low]: {
      deadline: getDaysUntil(1000),
      label: "Shelf Stable",
      colorClass: "bg-green-500",
    }
  };

  const handleToggle = (locationId: int) => {
    if (selectedLocations.includes(locationId)) {
      setSelectedLocations(selectedLocations.filter(id => id !== locationId));
    } else {
      setSelectedLocations([...selectedLocations, locationId]);
    }
  };

  const filteredItems = items.filter(item => selectedLocations.includes(item.location_id));

  return (
    <div className="min-h-screen bg-gray-50 text-slate-900">
      <div className="max-w-7xl mx-auto py-12 px-4">
        <header className="mb-12 border-b border-slate-200 pb-8">
          <h1 className="text-5xl font-black text-gray-900">Pantry <span className="text-blue-600">Tracker</span></h1>
          <p className="text-gray-500 mt-3 text-lg">Manage your inventory and expiration dates.</p>
        </header>
        <main className="grid grid-cols-1 lg:grid-cols-5 gap-12 items-start">
          <div className="className lg:col-span-3 space-y-12">
            <section className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
              <label className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 block">
                Storage Location
              </label>
              <div className="flex flex-wrap gap-3">
                {locations.map((loc) => (
                  <button
                    key={loc.id}
                    onClick={() => handleToggle(loc.id)}
                    className={`px-5 py-2.5 rounded-xl font-medium transition-all ${
                      selectedLocations.includes(loc.id)
                      ? "bg-blue-600 text-white border-blue-600 shadow-lg"
                      : "bg-gray-800 text-slate-200 hover:bg-slate-600"
                    }`}
                  >
                    {loc.location}
                  </button>
                ))}
              </div>
            </section>
            <CardOrganizer items={filteredItems} priorityExpiration={priorityExpiration} locations={locations} />
          </div>

          <aside className="lg:sticky lg:col-span-2 lg:top-2">
            <GeminiRecipe 
              items={filteredItems
                      .filter(item => item.expire > priorityExpiration[Priority.Max].deadline) 
                      .slice(0, 5)
                    }
            />
          </aside>
        </main>
      </div>
    </div>
  )
}

export default App
