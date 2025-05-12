from fpdf import FPDF
from django.db.models import F, Case, When, Value, CharField, Subquery, OuterRef, Count
from core import models
from core.models import VotingUser, Plate, Voter, PlateUser, Candidate


class BaseBehavior:
    def run(self):
        raise NotImplementedError('You must subclass and implement the trace rule validation')


class PDFWithFooter(FPDF):
    def footer(self):
        # Get the page size
        page_width = self.w
        page_height = self.h

        # Set the position of the footer at 15mm from the bottom
        self.set_y(page_height - 15)

        # Set font for the footer
        self.set_font("Arial", size=10)

        # Page number
        self.cell(0, 10, "FPF Labs", align="C")


class VotingBehaviorPdfVoter(BaseBehavior):
    def __init__(self, header_text):
        self.header_text = header_text

    def get_header(self):
        header = models.EventVoting.objects.get(pk=self.header_text, active=True)
        return header

    def get_body(self):
        queryset = models.VotingUser.objects.filter(
            voter__active=True,
            plate__active=True
        ).annotate(
            voting_name=F('voter__name'),
            plate_name=F('plate__name'),
            presidente=Subquery(
                models.Candidate.objects.filter(
                    id=Subquery(
                        models.PlateUser.objects.filter(
                            type='P',
                            plate__voting_user_plate=OuterRef('pk')  # Using OuterRef for voting_user.id
                        ).values('candidate')[:1]
                    )
                ).values('name')[:1]
            )
        ).order_by()
        results = queryset.values('voting_name', 'plate_name', 'presidente', 'vice')
        return results

    def run(self):
        pdf = PDFWithFooter()
        pdf.add_page()

        # Set font and size for header
        pdf.set_font("Arial", style="B", size=12)

        # Header
        pdf.cell(200, 10, txt=self.get_header().description, ln=True, align="C")

        # Set font and size for body
        pdf.set_font("Arial", size=12)

        for content in self.get_body():
            pdf.multi_cell(0, 10, txt=content['plate_name'], align="C")
            pdf.multi_cell(0, 10, txt=content['voting_name'], align="C")

        # Set font and size for footer
        pdf.set_font("Arial", size=10)

        # Footer
        pdf_content = pdf.output(dest='S').encode('latin1')
        return pdf_content


class VoterInPlate(BaseBehavior):
    def __init__(self, plate):
        self.plate = plate

    def get_header(self):
        header = models.Plate.objects.get(pk=self.plate)
        return header

    def get_body(self):
        result = models.Voter.objects.filter(votinguser__plate=self.plate).values()
        return result

    def _make_pdf(self):
        pdf = PDFWithFooter()
        pdf.add_page()

        # Set font and size for header
        pdf.set_font("Arial", style="B", size=24)

        # Header
        pdf.cell(0, 10, txt=self.get_header().name, ln=True, align="C")

        # Set font and size for body
        pdf.set_font("Arial", size=16)



        pdf.ln(10)
        pdf.cell(0, 10, "Eleitor", align="C",  border=1)
        pdf.ln(10)

        for content in self.get_body():
            pdf.cell(0, 10, content['name'], border=1, align="C")
            pdf.ln()

        # Set font and size for footer
        pdf.set_font("Arial", size=12)
        # Footer
        pdf_content = pdf.output(dest='S').encode('latin1')
        return pdf_content

    def run(self):
        return self._make_pdf()


class VoterInPlateResume(BaseBehavior):
    def __init__(self, plate):
        self.plate = plate

    def get_header(self):
        header = models.Plate.objects.get(pk=self.plate)
        return header

    def get_body(self):
        result = models.Voter.objects.filter(votinguser__plate=self.plate).values()
        return result

    def _make_pdf(self):
        pdf = PDFWithFooter()
        pdf.add_page()

        # Set font and size for header
        pdf.set_font("Arial", style="B", size=12)

        # Header
        pdf.cell(200, 10, txt=self.get_header().name, ln=True, align="C")

        # Set font and size for body
        pdf.set_font("Arial", size=12)

        pdf.cell(0, 10, txt="Eleitor", align="C")

        for content in self.get_body():
            pdf.cell(0, 10, txt=content['name'], align="C")

        # Set font and size for footer
        pdf.set_font("Arial", size=10)

        # Footer
        pdf_content = pdf.output(dest='S').encode('latin1')
        return pdf_content

    def run(self):
        return self._make_pdf()


class ResumeVoterProvisory(BaseBehavior):
    def __init__(self, event_vote):
        self.event_vote = event_vote

    def get_header(self):
        header = models.EventVoting.objects.get(pk=self.event_vote)
        return header

    def get_body(self):
        result = models.ResumeVote.objects.all().values('plate__name', 'quantity')
        return result

    def _make_pdf(self):
        pdf = PDFWithFooter()
        pdf.add_page()

        # Set font and size for header
        pdf.set_font("Arial", style="B", size=24)

        # Header
        pdf.cell(0, 10, txt=self.get_header().description, ln=True, align="C")

        # Set font and size for body
        pdf.set_font("Arial", size=12)

        pdf.ln(10)

        cell_width = 95  # Adjust the cell width as needed

        pdf.cell(cell_width, 10, "Chapa", border=1, align="C")
        pdf.cell(cell_width, 10, "Quantidade de votos", border=1, align="C")

        pdf.ln(10)

        for content in self.get_body():
            pdf.cell(cell_width, 10, content.get('plate__name'), border=1, align="C")
            pdf.cell(cell_width, 10, str(content.get('quantity')), border=1, align="C")
            pdf.ln()

        # Set font and size for footer
        pdf.set_font("Arial", size=10)

        # Footer
        pdf_content = pdf.output(dest='S').encode('latin1')
        return pdf_content

    def run(self):
        return self._make_pdf()


class VotingUserBehavior(BaseBehavior):
    def __init__(self, event_vote):
        self.event_vote = event_vote

    def get_header(self):
        header = models.EventVoting.objects.get(pk=self.event_vote)
        return header

    def get_body(self):
        result = models.VotingUser.objects.all().values('plate__id', 'plate__name').annotate(
            total=Count('*')
        ).filter(voting_id=self.get_header().id, voter__isnull=False, ).order_by('-total')
        return result

    def _make_pdf(self):
        pdf = PDFWithFooter()
        pdf.add_page()

        # Set font and size for header
        pdf.set_font("Arial", style="B", size=24)

        # Header
        pdf.cell(0, 10, txt=self.get_header().description, ln=True, align="C")

        # Set font and size for body
        pdf.set_font("Arial", size=12)

        cell_width = 95  # Adjust the cell width as needed

        pdf.ln(10)
        pdf.cell(95, 10, "Chapa", border=1, align="C")
        pdf.cell(95, 10, "Quantidade de votos", border=1, align="C")

        pdf.ln(10)

        for content in self.get_body():
            pdf.cell(cell_width, 10, content.get('plate__name'), border=1, align="C")
            pdf.cell(cell_width, 10, str(content.get('total')), border=1, align="C")
            pdf.ln()

        # pdf.set_y(-1)
        # pdf.set_font("Arial", size=10)
        # pdf.cell(0, 10, txt="Fpf Labs", ln=True, align="C")
        # Footer
        pdf_content = pdf.output(dest='S').encode('latin1')
        return pdf_content

    def run(self):
        return self._make_pdf()
