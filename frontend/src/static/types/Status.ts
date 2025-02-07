export enum Status {
  AWAITING,
  ACCEPTED,
  CANCELLED,
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
}

export const inventoryStatusNames = {
  [InventoryStatus.BROKEN]: 'Сломанный',
  [InventoryStatus.USED]: 'Использованный',
  [InventoryStatus.NEW]: 'Новый',
}