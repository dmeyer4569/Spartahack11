import { useState, useEffect } from 'react'
import './App.css'
import Card from './Card'
import type { PantryItem } from './types/item'

function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    let hasLoaded = false;

    const fetchImage = async () => {
      const newItems: PantryItems[] = [];

      const response = await fetch(`https://picsum.photos/id/237/200/300`, {
        method: 'GET'
      });

      let unique = Date.now();
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
     
      for (let i = 0; i < 10; i++) {
        newItems.push({
          id: unique + i, 
          name: "dog", 
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

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
        {items.length > 0 
          ? items.map(item => <Card key={item.id} item={item} />)
          : <p> loading items </p>
        }
      </div>
    </>
  )
}

export default App
