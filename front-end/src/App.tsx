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
          name: "this city", 
          image: url, 
          date: "2026-01-31"
        });
      }

      if (!hasLoaded) {
        setItems(newItems);
      }
    }
    
    fetchImage();

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

  return (
    <>
      <CardOrganizer items={items} priorityExpiration={priorityExpiration} />
    </>
  )
}

export default App
