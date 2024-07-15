from typing import List, Dict


def product_data(name: str = "Iphone 14 Pro Max", quantity: int = 10, price: float = 8500.0, status: bool = True) -> Dict:
    """
    Retorna um dicionário de dados de produto para testes.

    :param name: Nome do produto
    :param quantity: Quantidade do produto
    :param price: Preço do produto
    :param status: Status de disponibilidade do produto
    :return: Dicionário com dados do produto
    """
    return {
        "name": name,
        "quantity": quantity,
        "price": price,
        "status": status,
    }


def products_data() -> List[Dict]:
    """
    Retorna uma lista de dicionários de dados de produtos para testes.

    :return: Lista de dicionários com dados de produtos
    """
    return [
        {"name": "Iphone 11 Pro Max", "quantity": 20, "price": 4500.0, "status": True},
        {"name": "Iphone 12 Pro Max", "quantity": 15, "price": 5500.0, "status": True},
        {"name": "Iphone 13 Pro Max", "quantity": 5, "price": 6500.0, "status": True},
        {"name": "Iphone 15 Pro Max", "quantity": 3, "price": 10500.0, "status": False},
    ]
