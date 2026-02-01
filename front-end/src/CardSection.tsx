// My imports
import Card from './Card'

// My types
import type { ExpiryInfo } from './types/priority'
import type { Location } from './types/location'

interface CardSectionProps {
  items: PantryItem[];
  expiryInfo: ExpiryInfo;
  locations: Location[];
}

export default function CardSection({items, expiryInfo, locations}: CardSectionProps) {
  return (
    <section>
      <div className="flex items-center gap-4 mb-6 border-b border-gray-200 pb-4"> 
        <div className={`w-3 h-3 rounded-full ${expiryInfo.colorClass}`} />
        <h2 className="text-xl font-bold text-gray-800 uppercase tracking-wide">
          {expiryInfo.label}
        </h2>
        <span className="ml-auto text-sm text-gray-400 font-medium">{items.length} Items</span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {items.length > 0 
          ? items.map(item => {
              const loc = locations.find(l => l.id === item.location_id)?.location; 

              return (
                <Card key={item.id} item={item} locationName={loc}/>
              )
            })
          : <div className="col-span-full py-10 text-center bg-gray-100 rounded-xl text-gray-400 italic">No items in this category</div>
        }
      </div>
    </section>
  );
}
