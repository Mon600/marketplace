from fastapi import APIRouter, UploadFile, File, HTTPException

from api.depends.service_depend import file_service
from api.depends.user_depends import current_user_access

router = APIRouter(tags=["Файлы"], prefix="/files")


@router.post("/")
async def post_file(service: file_service, announcement_id: int, user: current_user_access, file: list[UploadFile] = File()):
    if len(file) > 10 or len(file) == 0:
        raise HTTPException(status_code=400, detail='You can upload from 1 to 10 files.')
    try:
        result = await service.save_uploaded_files(file, announcement_id, int(user.sub),)

        if result:
            return {'ok': True, 'detail': 'Files uploaded successfully!'}
        else:
            return {'ok': False, 'detail': 'Something went wrong!'}
    except:
        raise HTTPException(status_code=400, detail='Incorrect file format.')

@router.put('/')
async def post_file(service: file_service,
                    announcement_id: int,
                    user: current_user_access,
                    file: list[UploadFile] = File()):
    if len(file) > 10 or len(file) == 0:
        raise HTTPException(status_code=400, detail='You can upload from 1 to 10 files.')
    try:
        await service.update_files(file, announcement_id, int(user.sub))
        return {'ok': True, 'detail': 'Files updated successfully!'}
    except:
        return {'ok': False, 'detail': 'Something went wrong!'}


@router.delete('/')
async def delete_files(service: file_service,user: current_user_access, announcement_id: int, files_id: list[int]):
    try:
        res = await service.delete_files(files_id, announcement_id, int(user.sub))
        if res:
            return {'ok': True, 'detail': 'Files deleted successfully!'}
        else:
            return {'ok': False, 'detail': 'Something went wrong!'}
    except Exception as e:
        print(e)

