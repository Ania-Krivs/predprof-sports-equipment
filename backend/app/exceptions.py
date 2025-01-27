from fastapi import status, HTTPException

InventoryAlreadyExisted = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Инвентарь уже существует")
InventoryNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Инвентарь не найден")
