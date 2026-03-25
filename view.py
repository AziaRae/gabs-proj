# pyright: strict

from model import Item


class View:
    def collect_inputs(self) -> tuple[str, float, str]:
        name: str = input("\nEnter name of item: ")
        price: float = float(input("Enter price of item: "))
        category: str = input("Enter category: ")

        return (name, price, category)

    def display_cart(self, cart: list[Item]) -> None:
        print(f"\nInside the Cart: ")
        for index, item in enumerate(cart):
            print(
                f"[{index}]: {item.name} for {item.price} pesos under {item.category}"
            )

    def display_budget(self, budget: float):
        print(f"\nBudget: {budget}")

    def display_total_cost(self, total_cost: float):
        print(f"Total Cost: {total_cost}")

    def display_remaining(self, remaining: float):
        print(f"Remaining: {remaining}")

    def get_target_option(self, cart: list[Item]) -> int:
        while True:
            index: int = int(input(f"Enter target food (0 - {len(cart) - 1}): "))

            if not 0 <= index < len(cart):
                print(f"Invalid Index!!!")
                continue

            return index

    def display_over_budget_warning(self, over_budget_size: float):
        print(
            f"\nYou are over budget by {over_budget_size}!! Please remove some items first before proceeding with your shopping spree :)"
        )

    def suggest_items_to_remove(
        self,
        items_to_remove: tuple[Item, ...],
        index_of_item_to_remove: tuple[int, ...],
    ):
        print(f"Here are some suggested items to remove: ")
        for index, item in zip(index_of_item_to_remove, items_to_remove):
            print(f"[{index}] {item.name} costing {item.price} under {item.category}")
