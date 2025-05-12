import os
from os.path import exists

from django.http import HttpResponse
from dotenv import load_dotenv

from core import exceptions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

compotence_conf = os.path.join(BASE_DIR, 'magic_urn.conf')

if exists(compotence_conf):
    load_dotenv(compotence_conf)


def generate_report_to_download(name: str, params: dict):
    try:
        command = (
            f"java -jar {os.environ.get('SOURCE_LOCAL')}/generate-report-1.0-SNAPSHOT-jar-with-dependencies.jar"  # /home/samuel/PycharmProjects/api
            f" {os.environ.get('SOURCE_LOCAL')}/VotosPorEventoVotacao.jrxml"  # /home/<seu user>/PycharmProjects/api
            f" {os.environ.get('SOURCE_LOCAL')}"  # /home/<seu user>/PycharmProjects/api
            f" VotosPorEventoVotacao1.pdf"
            f" {os.environ.get('DB_HOST')}"
            f" magic_urn"
            f" 5432"
            f" postgres"
            f" 123456 "
            f"'idEventVoting|{params['event_vote']}'")

        os.system(command)
        pdf_path = f"{os.environ.get('SOURCE_LOCAL')}/VotosPorEventoVotacao1.pdf"

        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="resume.pdf"'
            os.remove(pdf_path)
            return response

        # return response
    except Exception:
        raise exceptions.ReportServerUnavailableException


def generate_report_to_plate_user_download(name: str, params: dict):
    try:
        command = (
            f"java -jar /usr/app/reports/generate-report-1.0-SNAPSHOT-jar-with-dependencies.jar"  # /home/<seu user>/PycharmProjects/api
            f" /usr/app/reports/VotosPorEventoVotacaoPorChapa.jrxml"  # /home/<seu user>/PycharmProjects/api
            f" /usr/app/reports"  # /home/<seu user>/PycharmProjects/api
            f" VotosPorEventoVotacaoPorChapa.pdf"
            f" {os.environ.get('DB_HOST')}"
            f" magic_urn"
            f" 5432"
            f" postgres"
            f" 123456 "
            f" 'idEventVoting|{params['event_vote']}','idPlate|{params['plate']}'")

        os.system(command)
        pdf_path = f"/usr/app/reports/VotosPorEventoVotacaoPorChapa.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="resume.pdf"'
            os.remove(pdf_path)
            return response

        # return response
    except Exception:
        raise exceptions.ReportServerUnavailableException


def generate_report_to_resume_download(name: str, params: dict):
    try:
        command = (
            f"java -jar {os.environ.get('SOURCE_LOCAL')}/generate-report-1.0-SNAPSHOT-jar-with-dependencies.jar"  # /home/<seu user>/PycharmProjects/api
            f" {os.environ.get('SOURCE_LOCAL')}/VotosPorEventoVotacaoProvisoria.jrxml"  # /home/<seu user>/PycharmProjects/api
            f" {os.environ.get('SOURCE_LOCAL')}"  # /home/<seu user>/PycharmProjects/api
            f" VotosPorEventoVotacaoProvisoria.pdf"
            f" {os.environ.get('DB_HOST')}"
            f" magic_urn"
            f" 5432"
            f" postgres"
            f" 123456 "
            f"'idEventVoting|{params['event_vote']}'")

        os.system(command)
        pdf_path = f"{os.environ.get('SOURCE_LOCAL')}/VotosPorEventoVotacaoProvisoria.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="resume.pdf"'
            os.remove(pdf_path)
            return response

        # return response
    except Exception:
        raise exceptions.ReportServerUnavailableException
