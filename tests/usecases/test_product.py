from typing import List
from uuid import UUID

import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


@pytest.mark.asyncio
async def test_usecases_create_should_return_success(product_in):
    """
    Teste para verificar se a criação de um produto retorna com sucesso.
    """
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"
    assert result.price == product_in.price
    assert result.description == product_in.description


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_inserted):
    """
    Teste para verificar se a obtenção de um produto pelo ID retorna com sucesso.
    """
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.id == product_inserted.id
    assert result.name == "Iphone 14 Pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_not_found():
    """
    Teste para verificar se a obtenção de um produto com ID inválido lança uma exceção de não encontrado.
    """
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert err.value.message == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"


@pytest.mark.usefixtures("products_inserted")
@pytest.mark.asyncio
async def test_usecases_query_should_return_success():
    """
    Teste para verificar se a consulta de produtos retorna uma lista de produtos com sucesso.
    """
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1
    assert all(isinstance(product, ProductOut) for product in result)


@pytest.mark.asyncio
async def test_usecases_update_should_return_success(product_up, product_inserted):
    """
    Teste para verificar se a atualização de um produto retorna com sucesso.
    """
    product_up.price = "7.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
    assert result.price == "7.500"
    assert result.name == product_up.name


@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(product_inserted):
    """
    Teste para verificar se a exclusão de um produto retorna com sucesso.
    """
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


@pytest.mark.asyncio
async def test_usecases_delete_should_not_found():
    """
    Teste para verificar se a exclusão de um produto com ID inválido lança uma exceção de não encontrado.
    """
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert err.value.message == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
