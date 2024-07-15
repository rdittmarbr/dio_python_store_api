import pytest
import asyncio
from uuid import UUID
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data, products_data
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """
    Cria um novo loop de evento para a sessão de testes.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    """
    Fornece um cliente MongoDB para a sessão de testes.
    """
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    """
    Limpa as coleções do banco de dados após cada teste.
    """
    yield
    collection_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collection_names:
        if collection_name.startswith("system"):
            continue
        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
async def client() -> AsyncClient:
    """
    Fornece um cliente HTTP assíncrono para a sessão de testes.
    """
    from store.main import app

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def products_url() -> str:
    """
    URL base para os endpoints de produtos.
    """
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    """
    Fornece um UUID fixo para testes de produto.
    """
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in(product_id: UUID) -> ProductIn:
    """
    Cria um schema ProductIn para testes de criação de produto.
    """
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_up(product_id: UUID) -> ProductUpdate:
    """
    Cria um schema ProductUpdate para testes de atualização de produto.
    """
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(product_in: ProductIn):
    """
    Insere um produto no banco de dados antes de executar o teste.
    """
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in() -> list[ProductIn]:
    """
    Cria uma lista de schemas ProductIn para testes de criação de múltiplos produtos.
    """
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in: list[ProductIn]):
    """
    Insere múltiplos produtos no banco de dados antes de executar o teste.
    """
    return [await product_usecase.create(body=product_in) for product_in in products_in]
