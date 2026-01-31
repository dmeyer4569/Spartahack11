import type { PantryItem } from './types/item'

interface CardProps {
  item: PantryItem;
}

function Card({item}: CardProps) {
  return (
    <div className="rounded-xl bg-white border border-gray-100 overflow-hidden">
      <div className="h-48 w-full overflow-hidden">
        <img 
          src={item.image}
          alt={item.name}
          className="h-full w-full object-cover"
        />
      </div>

      <div className="p-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-gray-800">
            {item.name}
          </h3>
          
          <span className="text-sm font-medium text-red-500">
            Expires: {item.expirationDate}
          </span>
        </div>
      </div>
    </div>
  )
}

export default Card
