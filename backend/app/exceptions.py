from fastapi import status, HTTPException

InventoryAlreadyExisted = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Инвентарь уже существует")
InventoryNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Инвентарь не найден")

InvalidToken = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен или его нет")

UserNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не найден")

NotEnoughInventory = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Недостаточно инвентаря данного типа")

UserAlreadyHasThisInventory = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                            detail="У этого пользователя уже есть этот инвентарь")
