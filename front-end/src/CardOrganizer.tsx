// My components
import CardSection from './CardSection'

// My types
import type { PriorityExpiration } from './types/priority'
import      { Priority }           from './types/priority'
import type { PantryItem } from './types/item'
import type { Location } from './type/location'

interface CardOrganizerProps {
  items: PantryItem[];
  priorityExpiration: PriorityExpiration; 
  locations: Location[];
}

export default function CardOrganizer({items, priorityExpiration, locations}: CardOrganizerProps) {
  const groupedItems = items.reduce((acc, item) => {
    const date = item.expire;
    if (date <= priorityExpiration[Priority.Max].deadline) {
      acc.max.push(item);
    } else if (date <= priorityExpiration[Priority.High].deadline) {
      acc.high.push(item);
    } else if (date <= priorityExpiration[Priority.Medium].deadline) {
      acc.medium.push(item);
    } else {
      acc.low.push(item);
    }
    return acc;
  }, {
    max: [] as PantryItem[],
    high: [] as PantryItem[],
    medium: [] as PantryItem[],
    low: [] as PantryItem[],
  });


  return (
    <>
      <CardSection key={0} items={groupedItems.max} locations={locations} expiryInfo={priorityExpiration[Priority.Max]} />
      <CardSection key={1} items={groupedItems.high} locations={locations} expiryInfo={priorityExpiration[Priority.High]} />
      <CardSection key={2} items={groupedItems.medium} locations={locations} expiryInfo={priorityExpiration[Priority.Medium]} />
      <CardSection key={3} items={groupedItems.low} locations={locations} expiryInfo={priorityExpiration[Priority.Low]} />
    </>
  )
}
