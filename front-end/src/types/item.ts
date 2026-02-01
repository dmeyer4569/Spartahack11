export interface PantryItem {
  id: number; // Unique identifier from your DB
  name: string;
  quantity: number;
  locationId: id;
  image: string; // URL
  expirationDate: string;  
}
