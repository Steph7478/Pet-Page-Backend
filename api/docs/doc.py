from drf_yasg.utils import swagger_auto_schema
from .params import generate_query_params_from_model

def document_api(serializer, model=None, summary=None, request_body=False):
    """
    Gera um decorator `swagger_auto_schema` com base no serializer e model fornecidos.
    - `serializer`: o serializer de resposta (e request se `request_body=True`)
    - `model`: a model (opcional, só necessária se quiser gerar parâmetros de query)
    - `summary`: string para `operation_summary`
    - `request_body`: se True, inclui o serializer como corpo da requisição
    """
    def decorator(func):
        return swagger_auto_schema(
            request_body=serializer if request_body else None,
            responses={200: serializer(many=True) if not request_body else serializer},
            manual_parameters=generate_query_params_from_model(model) if model else [],
            operation_summary=summary,
        )(func)
    return decorator
