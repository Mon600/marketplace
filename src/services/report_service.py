from redis.asyncio import Redis

from db.repositories.report_repository import ReportRepository
from schemas.announcement_schemas import Pagination
from schemas.report_schemas import SReportExtended, SReport


class ReportService:
    def __init__(self, repository: ReportRepository,):
        self.repository = repository

    async def send_report(self, report: SReport, user_id: int):
        try:
            report_dict = report.model_dump()
            report_dict['user_id'] = user_id
            report_schema = SReportExtended.model_validate(report_dict)
            await self.repository.add_report(report_schema)
            return True
        except Exception as e:
            raise e

    async def get_reports(self, pagintation: Pagination):
        try:
            pagination_dict = pagintation.model_dump()
            limit = pagination_dict['limit']
            offset = pagination_dict['offset']
            res = await self.repository.get_reports(limit, offset)
            return res
        except Exception as e:
            raise e

    async def allow_report(self, report_id: int):
        res =  await self.repository.allow_report(report_id)
        return res

    async def deny_report(self, report_id: int):
        res = await self.repository.deny_report(report_id)
        return res

    async def get_reviewed(self, pagintation: Pagination):
        pagination_dict = pagintation.model_dump()
        limit = pagination_dict['limit']
        offset = pagination_dict['offset']
        res = await self.repository.get_reviewed(limit, offset)
        return res
