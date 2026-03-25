# pyright: strict

from model import Model, Item
from view import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self._model = model
        self._view = view



    def run(self):
        model = self._model
        view = self._view

        while model.keep_going:
            if model.over_budget():
                view.display_over_budget_warning(model.remaining)
                view.display_cart(model.items)
                suggested_items_to_remove = model.suggest_item_to_remove()
                view.suggest_items_to_remove(
                    suggested_items_to_remove,
                    model.index_of_suggested_items_to_remove(suggested_items_to_remove),
                )
                model.remove_item_from_cart(view.get_target_option(model.items))
                model.calculate_remaining_money()
                continue
            model.sort_items()
            model.sort_by_category()
            view.display_budget(model.budget)
            view.display_total_cost(model.total_cost)
            view.display_remaining(model.remaining)
            view.display_cart(model.items)

            action: str = view.prompt_action()

            match action:
                case "A":
                    inputs: tuple[str, float, str] = view.collect_inputs()
                    item: Item = model.convert_input_to_item(*inputs)
                    model.add_item_to_cart(item)
                    model.increment_cost(item)
                    model.calculate_remaining_money()

                case "B":
                    view.display_cart(model.items)
                    model.remove_item_from_cart(view.get_target_option(model.items))
                    model.calculate_remaining_money()

                case "C":
                    model.toggle_ascending_sort()

                case "D":
                    model.toggle_descending_sort()

                case "E":
                    model.stop()

                case _:
                    print(f"Failed!! Invalid Input!!")
                    continue
