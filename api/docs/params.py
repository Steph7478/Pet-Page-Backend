from drf_yasg import openapi

def generate_query_params_from_model(model):
    """
    Gera uma lista de parâmetros de query para o Swagger com base nos campos do model.
    """
    params = []
    for field in model._meta.fields:
        param_type = openapi.TYPE_STRING

        internal_type = field.get_internal_type()
        if internal_type in ['IntegerField', 'BigIntegerField', 'SmallIntegerField']:
            param_type = openapi.TYPE_INTEGER
        elif internal_type in ['BooleanField', 'NullBooleanField']:
            param_type = openapi.TYPE_BOOLEAN
        elif internal_type in ['FloatField', 'DecimalField']:
            param_type = openapi.TYPE_NUMBER

        params.append(
            openapi.Parameter(
                name=field.name,
                in_=openapi.IN_QUERY,
                description=f"Filtrar por {field.verbose_name or field.name}",
                type=param_type,
                required=False,
            )
        )
    return params

def generate_cookie_auth_param(cookie_name='access_token'):
    """
    Gera parâmetro manual para documentar cookie JWT no header 'Cookie'.
    """
    return openapi.Parameter(
        name='Cookie',
        in_=openapi.IN_HEADER,
        description=f'Cookie JWT de autenticação. Exemplo: {cookie_name}=seu_token_jwt_aqui',
        type=openapi.TYPE_STRING,
        required=True,
    )


