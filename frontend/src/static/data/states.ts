import { InventoryStatus } from "../types/Status";

export const states = {
  [InventoryStatus.BROKEN]: {
    text: "сломано",
    color: "#FF8284",
  },
  [InventoryStatus.USED]: {
    text: "используется",
    color: "#82BCFF",
  },
  [InventoryStatus.NEW]: {
    text: "новое",
    color: " #82FFBA",
  },
};
