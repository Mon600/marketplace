from fastapi import APIRouter, UploadFile, File, HTTPException

from api.depends.service_depend import announcement_service
from api.depends.user_depends import current_user_access
from schemas.announcement_schemas import SAnnouncement


router = APIRouter(prefix="/announcements", tags=["Объявления"])


@router.post("/new-announcement")
async def new_announcement(
                           service: announcement_service,
                           user: current_user_access,
                           announcement: SAnnouncement,):
    await service.new_announcement(announcement, user_id=int(user.sub))
    return {"ok": True, "detail": "Announcement successfully created"}



@router.get("/announcement/{announcement_id}")
async def get_announcement(service: announcement_service, announcement_id: int, user: current_user_access):
    result = await service.get_announcement(announcement_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return result


@router.put("/announcement/{announcement_id}")
async def update_announcement(service: announcement_service,
                              announcement_id: int,
                              announcement: SAnnouncement,
                              user: current_user_access):
    try:
        result = await service.update_announcement(announcement_id, announcement, user_id=int(user.sub))
        if result:
            return {"ok": True, "detail": "Announcement successfully updated"}
        else:
            return {"ok": False, "detail": "Something went wrong."}
    except:
        raise HTTPException(status_code=400, detail='Incorrect file type.')
