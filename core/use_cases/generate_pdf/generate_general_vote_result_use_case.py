from core.ports.pdf.pdf_generator_port import ReportRepositoryPort
from core.use_cases.generate_pdf.generate_general_vote_result_pdf_service import GenerateGeneralVoteResultPdfService


class GenerateGeneralVoteResultUseCase:
    def __init__(self, report_repository: ReportRepositoryPort):
        self.report_repository = report_repository

    def execute(self, event_vote_id: int) -> bytes:
        rows = self.report_repository.get_general_vote_result(event_vote_id)
        service = GenerateGeneralVoteResultPdfService(rows)
        return service.generate()
