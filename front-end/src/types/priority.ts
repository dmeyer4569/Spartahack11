export const enum Priority {
  Low,
  Medium,
  High,
  Max
}

export interface ExpiryInfo {
  deadline: Date;
  label: string;
  colorClass: string;
}

export type PriorityExpiration = Record<Priority, ExpiryInfo>;
