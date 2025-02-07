export enum Status {
  AWAITING,
  ACCEPTED,
  CANCELLED,
  RETURNED
}

export enum InventoryStatus {
  BROKEN,
  USED,
  NEW,
}

export const statusNames = {
  [Status.AWAITING]: 'Ожидание',
  [Status.ACCEPTED]: 'Принята',
  [Status.CANCELLED]: 'Отклонена',
  [Status.RETURNED]: 'Возвращена',
}

export const inventoryStatusNames = {
  [InventoryStatus.BROKEN]: 'Сломанный',
  [InventoryStatus.USED]: 'Используется',
  [InventoryStatus.NEW]: 'Новый',
}