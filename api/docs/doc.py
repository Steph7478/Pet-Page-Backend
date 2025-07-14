from drf_yasg.utils import swagger_auto_schema
from .params import generate_query_params_from_model

def document_api(serializer=None, model=None, summary=None, request_body=False, security=None, responses=None, manual_parameters=None, methods=None):
    """
    Gera um decorator `swagger_auto_schema` com base no serializer e model fornecidos.
    - `serializer`: serializer para resposta e/ou request_body
    - `model`: model para gerar query params (opcional)
    - `summary`: texto para operation_summary
    - `request_body`: se True, inclui o serializer no corpo da requisição
    - `security`: lista para configurar o esquema de autenticação (ex: [{"RefreshCookieAuth" or "AccessCookieAuth": []}])
    - `responses`: dict para customizar respostas (ex: {200: serializer, 400: "Bad request"})
    - `manual_parameters`: lista adicional de parâmetros manuais para incluir (ex: cookie auth)
    """
    def decorator(func):
        resp = responses
        if resp is None:
            if serializer:
                if request_body:
                    resp = {200: serializer}
                else:
                    resp = {200: serializer(many=True)}
            else:
                resp = {200: "Success"}

        params_model = generate_query_params_from_model(model) if model else []
        manual_params = params_model + (manual_parameters if manual_parameters else [])

        return swagger_auto_schema(
            request_body=serializer if request_body else None,
            responses=resp,
            manual_parameters=manual_params,
            operation_summary=summary,
            security=security or [],
            methods=methods
        )(func)
    return decorator
