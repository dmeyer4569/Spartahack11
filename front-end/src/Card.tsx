import type { PantryItem } from './types/item'

interface CardProps {
  item: PantryItem;
}

function Card({item}: CardProps) {
  return (
    <div className="group rounded-2xl bg-white shadow-sm border border-gray-100 overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
      <div className="h-48 w-full overflow-hidden relative">
        <img 
          src={item.image}
          alt={item.name}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-100"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
      </div>

      <div className="p-5">
          <h3 className="text-lg font-bold text-gray-900 capitalize mb-1">
            {item.name}
          </h3>
        
          <div className="flex items-center justify-between mt-4">
            <span className="text-xs font-semibold text-gray-400 uppercase">Expires</span>
            <span className="text-sm font-bold text-red-500 bg-red-50 px-3 py-1 rounded-full">
              {item.expirationDate}
            </span>
        </div>
      </div>
    </div>
  )
}

export default Card
