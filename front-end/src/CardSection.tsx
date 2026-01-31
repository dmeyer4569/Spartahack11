// My imports
import Card from './Card'

// My types
import type { ExpiryInfo } from './types/priority'

interface CardSectionProps {
  items: PantryItem[];
  expiryInfo: ExpiryInfo;
}

export default function CardSection({items, expiryInfo}: CardSectionProps) {
  return (
    <>
      <h2> {expiryInfo.label} </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
        {items.length > 0 
          ? items.map(item => <Card key={item.id} item={item} />)
          : <p> loading items </p>
        }
      </div>
    </>
  );
}
