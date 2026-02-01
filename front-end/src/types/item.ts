export interface PantryItem {
  id: number; // Unique identifier from your DB
  name: string;
  expire: string;  
  quantity: number;
  img_path: string; // URL
  location_id: number;
}
