// My components
import CardSection from './CardSection'

// My types
import type { PriorityExpiration } from './types/priority'
import      { Priority }           from './types/priority'
import type { PantryItem } from './types/item'

interface CardOrganizerProps {
  items: PantryItem[];
  priorityExpiration: PriorityExpiration; 
}

export default function CardOrganizer({items, priorityExpiration}: CardOrganizerProps) {
  const groupedItems = items.reduce((acc, item) => {
    const date = item.expirationDate;
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
      <CardSection key={0} items={groupedItems.max} expiryInfo={priorityExpiration[Priority.Max]} />
      <CardSection key={1} items={groupedItems.high} expiryInfo={priorityExpiration[Priority.High]} />
      <CardSection key={2} items={groupedItems.medium} expiryInfo={priorityExpiration[Priority.Medium]} />
      <CardSection key={3} items={groupedItems.low} expiryInfo={priorityExpiration[Priority.Low]} />
    </>
  )
}
