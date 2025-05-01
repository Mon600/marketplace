from sqlalchemy import select, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models.models import ReportModel, AnnouncementsModel, ReportsStatus
from schemas.report_schemas import SReportExtended


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_report(self, report: SReportExtended):
        try:
            report_dict = report.model_dump()
            new_report = ReportModel(**report_dict)
            self.session.add(new_report)
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False

    async def get_reports(self, limit: int, offset: int):
        try:
            query = (select(ReportModel)
                     .where(ReportModel.status == 'unseen')
                     .limit(limit)
                     .offset(offset)
                     .order_by(ReportModel.created_at.desc())
                     .options(joinedload(ReportModel.announcement_rel).joinedload(AnnouncementsModel.user_rel),
                              joinedload(ReportModel.user_rel)))
            result = await self.session.execute(query)
            return result.scalars().all()
        except:
            await self.session.rollback()
            return None

    async def allow_report(self, report_id: int):
        try:
            query = (select(ReportModel)
                     .where(ReportModel.id == report_id)
                     .options(joinedload(ReportModel.announcement_rel)
                              .joinedload(AnnouncementsModel.reports_rel)))
            result = await self.session.execute(query)
            report = result.scalars().first()
            report.status = ReportsStatus.allowed
            if report and report.status == ReportsStatus.unseen:
                report.status = ReportsStatus.allowed
                report.announcement_rel.status = False
                for report in report.announcement_rel.reports_rel:
                    if report.status == ReportsStatus.unseen:
                        report.status = ReportsStatus.allowed
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return None


    async def deny_report(self, report_id: int):
        try:
            query = (update(ReportModel)
                     .where(ReportModel.id == report_id).values(status='denied'))
            await self.session.execute(query)
            await self.session.commit()
            return True
        except:
            await self.session.rollback()
            return False

    async def get_reviewed(self, limit: int, offset: int):
        try:
            query = (select(ReportModel)
                     .where(
                or_(
                    ReportModel.status == "allowed",
                    ReportModel.status == "denied"
                )
            )
                .options(joinedload(ReportModel.announcement_rel).joinedload(AnnouncementsModel.user_rel),
                         joinedload(ReportModel.user_rel))
                .limit(limit)
                .offset(offset))

            res = await self.session.execute(query)
            result = res.scalars().all()
            return result
        except:
            await self.session.rollback()
            return False

