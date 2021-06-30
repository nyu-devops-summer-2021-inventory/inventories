# TODO: License header
"""Factory for constructing fake InventoryItemm objects during testing"""

from random import randrange

import factory
from factory.fuzzy import FuzzyChoice

from service.models import InventoryItem, Condition


class InventoryItemFactory(factory.Factory):
    """Creates fake items to use when testing the inventory service"""

    class Meta:
        model = InventoryItem

    id = factory.Sequence(lambda n: n)
    # This isn't exactly a SKU, but it's pretty close, link to docs below:
    # https://faker.readthedocs.io/en/master/providers/faker.providers.barcode.html  # noqa E503
    sku = factory.Faker("ean8")
    # I.e. pick a random number between 0 and 50
    count = randrange(0, 51)
    condition = FuzzyChoice(
        choices=[Condition.New, Condition.Used, Condition.OpenBox]
    )
    restock_level = randrange(5, 21)
    # I.e. make sure our restock amount is some multiple larger than our 
    # restock level
    restock_amount = restock_level * randrange(2, 6)
    in_stock = FuzzyChoice(choices=[True, False])
