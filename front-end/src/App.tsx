import { useState, useEffect } from 'react'
import './App.css'

// My component imports
import CardOrganizer from './CardOrganizer'

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

  useEffect(() => {
    let hasLoaded = false;

    const fetchImage = async () => {
      const newItems: PantryItems[] = [];

      const response = await fetch(`https://picsum.photos/id/238/200/300`, {
        method: 'GET'
      });

      let unique = Date.now();
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
     
      for (let i = 0; i < 10; i++) {
        newItems.push({
          id: unique + i, 
          name: `this city ${i}`, 
          image: url, 
          expirationDate: "2026-01-31",
          locationId: i % 3
        });
      }

      if (!hasLoaded) {
        setItems(newItems);
      }
    }

    const getLocations = async () => {
      try {
        const response = null/* fetch(location api) */;
        const data = [
          {
            location: "Pantry",
            id: 0
          },
          {
            location: "Fridge",
            id: 1
          },
          {
            location: "Drawer",
            id: 2
          },
        ];

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
      label: "Expires in a Week",
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

    console.log(selectedLocations);
  };

  const filteredItems = items.filter(item => selectedLocations.includes(item.locationId));

  return (
    <div className="min-h-screen bg-gray-50 overflow-x-hidden">
      <div className="py-12 px-4">
        <div className="max-w-6xl mx-auto px-4">
          <header className="max-w-6xl mx-auto mb-12">
            <h1 className="text-4xl font-black text-gray-900">Pantry Tracker</h1>
            <p className="text-gray-500 mt-2">Manage your inventory and expiration dates.</p>
          </header>
          <main className="space-y-16">
            <div className="mb-6">
              <label className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 block">
                Filter by Storage Location
              </label>
              <div className="flex flex-wrap gap-2 mb-8">
                {locations.map((location) => {
                  const isActive = selectedLocations.includes(location.id);
                  return (
                    <button
                      key={location.id}
                      onClick={() => handleToggle(location.id)}
                      className={`px-4 py-2 rounded-xl border transition-all ${
                        isActive
                        ? "bg-blue-600 text-white border-blue-600 shadow-md"
                        : "bg-gray-800 text-gray-100 border-gray-700 hover:bg-gray-700"
                      }`}
                    >
                      {location.location}
                    </button>
                  );
                })}
              </div>
            </div>
            <CardOrganizer items={filteredItems} priorityExpiration={priorityExpiration} locations={locations} />
          </main>
        </div>
      </div>
    </div>
  )
}

export default App
