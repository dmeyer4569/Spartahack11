export interface PantryItem {
  id: number; // Unique identifier from your DB
  name: string;
  location: string;
  image: string; // URL
  expirationDate: string;  
}
