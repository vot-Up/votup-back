
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

AUTH_SCHEMAS = {
    'login': extend_schema(
        tags=['Authentication'],
        summary='Fazer login no sistema',
        description='Autentica um usuário e retorna tokens de acesso e refresh.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string', 'format': 'password'}
                },
                'required': ['email', 'password']
            }
        },
        examples=[
            OpenApiExample(
                'Login Example',
                value={
                    'email': 'admin@gmail.com',
                    'password': 'TwIu7an43@v1'
                }
            )
        ],
        responses={
            200: {
                'description': 'Login realizado com sucesso',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'token': {
                                    'type': 'object',
                                    'properties': {
                                        'access': {'type': 'string'},
                                        'refresh': {'type': 'string'}
                                    }
                                },
                                'user': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer'},
                                        'name': {'type': 'string'},
                                        'email': {'type': 'string'}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            405: {'description': 'Credenciais inválidas'}
        }
    )
}

# Schemas para usuários
USER_SCHEMAS = {
    'reset_password': extend_schema(
        tags=['Users'],
        summary='Resetar senha do usuário',
        description='Permite resetar a senha de um usuário usando email e celular.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'cellphone': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'},
                    'new_password': {'type': 'string', 'format': 'password'}
                },
                'required': ['cellphone', 'email', 'new_password']
            }
        },
        responses={
            200: {'description': 'Senha alterada com sucesso'},
            400: {'description': 'Dados inválidos ou usuário não encontrado'}
        }
    )
}

# Schemas para eleitores
VOTER_SCHEMAS = {
    'list': extend_schema(
        tags=['Voters'],
        summary='Listar eleitores',
        description='Lista todos os eleitores cadastrados no sistema.',
        parameters=[
            OpenApiParameter('name', OpenApiTypes.STR, description='Filtrar por nome'),
            OpenApiParameter('cellphone', OpenApiTypes.STR, description='Filtrar por celular'),
            OpenApiParameter('active', OpenApiTypes.BOOL, description='Filtrar por status ativo'),
            OpenApiParameter('expand', OpenApiTypes.STR, description='Expandir campos relacionados'),
        ]
    ),
    'can_vote': extend_schema(
        tags=['Voting Process'],
        summary='Verificar se eleitor pode votar',
        description='Verifica se um eleitor pode votar com base no número de celular.',
        parameters=[
            OpenApiParameter('cellphone', OpenApiTypes.STR, description='Número do celular', required=True)
        ],
        responses={
            200: {
                'description': 'Eleitor pode votar',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'cellphone': {'type': 'string'},
                                'has_voted': {'type': 'boolean'}
                            }
                        }
                    }
                }
            },
            400: {'description': 'Eleitor já votou ou dados inválidos'}
        }
    )
}

# Schemas para votação
VOTING_SCHEMAS = {
    'voting': extend_schema(
        tags=['Voting Process'],
        summary='Iniciar processo de votação',
        description='Inicia o processo de votação para um eleitor.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'cellphone': {'type': 'string'}
                },
                'required': ['cellphone']
            }
        },
        responses={
            200: {'description': 'Processo de votação iniciado'},
            400: {'description': 'Eleitor não pode votar ou votação não disponível'}
        }
    ),
    'ranking': extend_schema(
        tags=['Reports'],
        summary='Ranking de votação',
        description='Retorna o ranking das chapas por votação.',
        responses={
            200: {
                'description': 'Ranking das chapas',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'plate__id': {'type': 'integer'},
                                    'plate__name': {'type': 'string'},
                                    'total': {'type': 'integer'}
                                }
                            }
                        }
                    }
                }
            }
        }
    ),
    'active_vote': extend_schema(
        tags=['Voting Events'],
        summary='Ativar votação',
        description='Ativa uma votação específica.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'vote_id': {'type': 'integer'}
                },
                'required': ['vote_id']
            }
        },
        responses={
            200: {'description': 'Votação ativada com sucesso'},
            400: {'description': 'Erro ao ativar votação'}
        }
    ),
    'close_vote': extend_schema(
        tags=['Voting Events'],
        summary='Fechar votação',
        description='Fecha uma votação específica.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'vote_id': {'type': 'integer'}
                },
                'required': ['vote_id']
            }
        },
        responses={
            200: {'description': 'Votação fechada com sucesso'},
            400: {'description': 'Erro ao fechar votação'}
        }
    )
}

# Schemas para relatórios
REPORT_SCHEMAS = {
    'resume_report': extend_schema(
        tags=['Reports'],
        summary='Gerar relatório de resumo',
        description='Gera um relatório em PDF com o resumo da votação.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'event_vote': {'type': 'integer'}
                },
                'required': ['event_vote']
            }
        },
        responses={
            200: {
                'description': 'Relatório PDF gerado',
                'content': {'application/pdf': {'schema': {'type': 'string', 'format': 'binary'}}}
            },
            400: {'description': 'Erro ao gerar relatório'}
        }
    ),
    'get_voting_user_plate_quantity_pdf': extend_schema(
        tags=['Reports'],
        summary='Relatório PDF de votação por chapa',
        description='Gera um relatório PDF com a quantidade de votos por chapa.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'event_vote': {'type': 'integer'}
                },
                'required': ['event_vote']
            }
        },
        responses={
            200: {
                'description': 'Relatório PDF gerado',
                'content': {'application/pdf': {'schema': {'type': 'string', 'format': 'binary'}}}
            }
        }
    )
}