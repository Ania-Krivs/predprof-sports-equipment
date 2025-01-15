from fastapi import status, HTTPException

InventoryAlreadyExisted = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="Инвентарь уже существует")
