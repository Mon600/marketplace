from fastapi import APIRouter, HTTPException

from api.depends.service_depend import report_service
from api.depends.user_depends import current_user_access, StatusDep
from schemas.announcement_schemas import PaginationDep
from schemas.report_schemas import SReport
router = APIRouter(tags=["Жалобы"], prefix='/report')

@router.post('/send/', summary='Отправить репорт')
async def send_report(report: SReport, user: current_user_access, service: report_service):
    try:
        await service.send_report(report, int(user.sub))
        return {"ok": True, 'detail': 'Report sent'}
    except:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get('/get', summary='Получить репорты')
async def get_reports(pagination: PaginationDep, user: current_user_access, service: report_service, status: StatusDep):
     try:
        result = await service.get_reports(pagination)
        if not result:
            raise HTTPException(status_code=404, detail='Reports not found')
        return result
     except:
         raise HTTPException(status_code=500, detail="Something went wrong")


@router.put('/{report_id}/allow/', summary="Рассмотреть репорт(положительно)")
async def allow_report(report_id: int, user: current_user_access, service: report_service, status: StatusDep):
    res = await service.allow_report(report_id)
    if res:
        return {"ok": True, "detail": "Report approved, advertisement was removed"}
    else:
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.put('/{report_id}/deny/', summary="Рассмотреть репорт(Отрицательно)")
async def deny_report(report_id: int, user: current_user_access, service: report_service, status: StatusDep):
    res = await service.deny_report(report_id)
    if res:
        return {"ok": True, "detail": "Report denied"}
    # else:
    #     raise HTTPException(status_code=500, detail="Something went wrong")



@router.get('/get-reviewed', summary='Получить рассмотренные репорты')
async def get_reviewed(user: current_user_access, service: report_service, status: StatusDep, pagination: PaginationDep):
    # try:
    res = await service.get_reviewed(pagination)
    # if res:
    return res
    # else:
    #     raise HTTPException(status_code=404, detail='Reports not found')
    # except:
    #     raise HTTPException(status_code=500, detail="Something went wrong")