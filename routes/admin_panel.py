from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from models.models import RepairRequest, RequestStatus
from routes.auth import get_current_user, require_admin
from settings import get_db
from tg_bot import send_msg

router = APIRouter()

"""a) Перегляд всіх заявок, та тільки тих що мають статус «Нова» (фільтр) (/admin/repairs?new=1)
b) Прийняття заявки (/admin/repair/{repair_id}/self/get)
c) Перегляд всіх заявок що взяв на опрацювання (/admin/self/repairs)
d) Зміна статуса заявки (закриття, взяття на опрацювання і тд)
(/admin/repair/{repair_id}/change/status)
e) Створення повідомлень (коментарів)(/admin/repair/{repair_id}/change/comment)"""


class StatusUpdateRequest(BaseModel):
    status: RequestStatus


@router.get("/user/admin/me")
async def only_for_admin(current_user: User = Depends(require_admin)):
    return {"is admin": current_user}


# Зміна статусу заявки та відправлення повідомлення у телеграм


@router.patch("/requests/{request_id}/status")
async def update_request_status(

    request_id: int,
    body: StatusUpdateRequest,
    current_user_admin=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Изменение статуса заявки (только для админов).
    После успешного изменения — отправляет сообщение в Telegram пользователю (если он привязан).
    """

    new_status = body.status

    req = await db.scalar(select(RepairRequest).filter_by(id=request_id))
    if req is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не знайдена")

    # Обновляємо статус
    req.status = new_status
    db.add(req)
    await db.commit()
    await db.refresh(req)

    # Формуємо текст повідомлення
    message_text = (
        f"Статус вашої заявки #{req.id} було змінено на: {new_status.value}.\n"
        f"Деталі: {req.description}\n"
        f"Для деталей відкрийте ваш особистий кабінет."
    )

    # Відправляємо повідомлення у телеграм
    try:
        await send_msg(req.user_id, message_text)
        message_sent = True
    except Exception as e:
        print(f"Помилка при відправці повідомлення у телеграм: {e}")
        message_sent = False
    return {"request_id": req.id, "status": req.status, "message_sent": message_sent}
