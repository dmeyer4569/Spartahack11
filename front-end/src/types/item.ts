export interface PantryItem {
  id: number; // Unique identifier from your DB
  name: string;
  locationId: id;
  image: string; // URL
  expirationDate: string;  
}
