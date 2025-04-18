from fastapi import APIRouter, UploadFile, File, HTTPException

from api.depends.service_depend import announcement_service, file_service
from api.depends.user_depends import current_user_access
from schemas.announcement_schemas import SAnnouncement, SAnnouncementGet, Pagination, PaginationDep, FiltersDep

router = APIRouter(prefix="/announcements", tags=["Объявления"])


@router.post("/new-announcement")
async def new_announcement(
                           a_service: announcement_service,
                           f_service: file_service,
                           user: current_user_access,
                           announcement: SAnnouncement,
                           file: list[UploadFile] = File(None,min_length=0, max_length=10)):
    announcement_id = await a_service.new_announcement(announcement, user_id=int(user.sub))
    if not file is None:
        await f_service.add_files(file, announcement_id, user_id=int(user.sub))
    return {"ok": True, "detail": "Announcement successfully created"}



@router.get("/announcement/{announcement_id}")
async def get_announcement(service: announcement_service,
                           announcement_id: int) -> SAnnouncementGet:
    result = await service.get_announcement(announcement_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return result


@router.get("/user/{user_id}")
async def get_announcements(service: announcement_service, user_id: int) -> list[SAnnouncementGet]:
    result = await service.get_user_announcements(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Announcements not found")
    return result


@router.get('/feed')
async def get_feed(service: announcement_service,
                   user: current_user_access,
                   pagination: PaginationDep,
                   filters: FiltersDep) -> list[SAnnouncementGet]:
    result = await service.get_feed(int(user.sub), pagination, filters)
    if result is None:
        raise HTTPException(status_code=404, detail="Announcements not found")
    return result


@router.put("/announcement/{announcement_id}")
async def update_announcement(a_service: announcement_service,
                              f_service: file_service,
                              announcement_id: int,
                              announcement: SAnnouncement,
                              user: current_user_access,
                              file: list[UploadFile] = File(None, min_length=0, max_length=10)
                              ):
    try:
        user_id = int(user.sub)
        result = await a_service.update_announcement(announcement_id, announcement, user_id)
        if not file is None:
            await f_service.update_files(file, announcement_id, user_id)
        if result:
            return {"ok": True, "detail": "Announcement successfully updated"}
        else:
            return {"ok": False, "detail": "Something went wrong."}
    except:
        raise HTTPException(status_code=400, detail='Incorrect file type.')


@router.delete("/announcement/{announcement_id}")
async def delete_announcemet(a_service: announcement_service,
                             f_service: file_service,
                             announcement_id: int,
                             user: current_user_access):
    user_id = int(user.sub)
    await a_service.delete_announcement(announcement_id, user_id)
    await f_service.delete_files(announcement_id, user_id)
    return {"ok": True, "detail": "Announcement successfully deleted"}
