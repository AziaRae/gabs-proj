# pyright: strict

from copy import deepcopy
from typing import cast


class Item:
    def __init__(self, name: str, price: float, category: str) -> None:
        self._price: float = price
        self._category: str = category
        self._name: str = name

    @property
    def price(self) -> float:
        return self._price

    @property
    def category(self) -> str:
        return self._category

    @property
    def name(self) -> str:
        return self._name


class Model:
    def __init__(self, budget: float) -> None:
        self._items: list[Item] = []
        self._budget: float = budget
        self._keep_going: bool = True
        self._total_cost: float = 0
        self._remaining_money: float = self._budget
        self._sorting_descending: bool = True

    @property
    def keep_going(self):
        return self._keep_going

    def stop(self):
        self._keep_going = False

    @property
    def budget(self) -> float:
        return self._budget

    @property
    def total_cost(self):
        return self._total_cost

    @property
    def remaining(self):
        return abs(self._remaining_money)

    @property
    def items(self) -> list[Item]:
        return deepcopy(self._items)

    def convert_input_to_item(self, name: str, price: float, category: str) -> Item:
        item: Item = Item(name.lower(), price, category.lower())
        return item

    def add_item_to_cart(self, item: Item) -> None:
        self._items.append(item)

    def remove_item_from_cart(self, index: int) -> None:
        self._total_cost -= self._items[index].price
        self._items.pop(index)

    def increment_cost(self, item: Item) -> None:
        self._total_cost += item.price

    def calculate_remaining_money(self) -> None:
        self._remaining_money = self._budget - self._total_cost

    def sort_ascending_price(self):
        items: list[Item] = sorted(
            [item for item in self._items], key=lambda item: item.price, reverse=False
        )
        self._items = deepcopy(items)

    def sort_descending_price(self):
        items: list[Item] = sorted(
            [item for item in self._items], key=lambda item: item.price, reverse=True
        )
        self._items = deepcopy(items)

    def sort_by_category(self):
        items: list[Item] = sorted(
            [item for item in self._items], key=lambda item: item.category
        )
        self._items = deepcopy(items)

    def sort_items(self):
        match self._sorting_descending:
            case True:
                self.sort_descending_price()

            case False:
                self.sort_ascending_price()

    def toggle_descending_sort(self):
        self._sorting_descending = True

    def toggle_ascending_sort(self):
        self._sorting_descending = False

    def over_budget(self):
        return self._remaining_money < 0

    def suggest_item_to_remove(self) -> tuple[Item, ...]:
        items: list[Item] = self._items
        num_items: int = len(self._items)
        target_deduction: float = self.remaining

        potential_items_to_remove: dict[tuple[Item, ...], float] = {}

        for mask in range(1 << num_items):
            potential_items: tuple[Item, ...] = tuple(
                items[i] for i in range(num_items) if mask & (1 << i)
            )
            total_deduction = sum(item.price for item in potential_items)

            if total_deduction >= target_deduction:
                potential_items_to_remove[potential_items] = total_deduction

        items_to_remove: tuple[Item, ...] = tuple()

        min: float = 1 << 128

        for potential in potential_items_to_remove:
            to_deduct: float = potential_items_to_remove[potential]

            if to_deduct < min:
                min = to_deduct
                items_to_remove = potential

        return items_to_remove

    def index_of_suggested_items_to_remove(
        self, items_to_remove: tuple[Item, ...]
    ) -> tuple[int, ...]:
        items: list[Item | None] = cast(list[Item | None], list(self._items))
        og_len: int = len(items)
        items.reverse()

        item_indices: tuple[int, ...] = tuple()

        for item in items_to_remove:
            index = items.index(item)
            item_indices += ((og_len - index - 1),)
            items[index] = None

        return item_indices
