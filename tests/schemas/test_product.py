from pydantic import ValidationError

import pytest
from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_return_success():
    """
    Teste para verificar se a validação do schema ProductIn ocorre com sucesso.
    """
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 Pro Max"
    assert product.quantity == data['quantity']
    assert product.price == data['price']
    assert product.status == data['status']


def test_schemas_return_raise():
    """
    Teste para verificar se a validação do schema ProductIn lança um erro de validação quando campos obrigatórios estão faltando.
    """
    data = {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8.500}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Iphone 14 Pro Max", "quantity": 10, "price": 8.5},
        "url": "https://errors.pydantic.dev/2.5/v/missing",
    }

    # Verificar se há mais erros (se necessário)
    assert len(err.value.errors()) == 1


def test_schemas_invalid_price():
    """
    Teste para verificar se a validação do schema ProductIn lança um erro de validação quando o preço é inválido.
    """
    data = product_data()
    data['price'] = "invalid_price"

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "value_error",
        "loc": ("price",),
        "msg": "value is not a valid float",
        "input": "invalid_price"
    }


def test_schemas_negative_price():
    """
    Teste para verificar se a validação do schema ProductIn lança um erro de validação quando o preço é negativo.
    """
    data = product_data()
    data['price'] = -1.00

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "value_error.number.not_ge",
        "loc": ("price",),
        "msg": "ensure this value is greater than or equal to 0",
        "input": -1.00
    }


def test_schemas_zero_quantity():
    """
    Teste para verificar se a validação do schema ProductIn aceita quantidade zero.
    """
    data = product_data()
    data['quantity'] = 0
    product = ProductIn.model_validate(data)

    assert product.quantity == 0


def test_schemas_missing_optional_field():
    """
    Teste para verificar se a validação do schema ProductIn aceita a ausência de campos opcionais.
    """
    data = product_data()
    data.pop('description', None)  # Remover campo opcional 'description'
    product = ProductIn.model_validate(data)

    assert product.name == "Iphone 14 Pro Max"
    assert product.quantity == data['quantity']
    assert product.price == data['price']
    assert product.status == data['status']
    assert product.description is None  # Verificar que o campo ausente é None


def test_schemas_invalid_status():
    """
    Teste para verificar se a validação do schema ProductIn lança um erro de validação quando o status é inválido.
    """
    data = product_data()
    data['status'] = "invalid_status"

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "value_error.enum",
        "loc": ("status",),
        "msg": "value is not a valid enumeration member; permitted: 'available', 'unavailable'",
        "input": "invalid_status"
    }
