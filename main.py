# pyright: strict

from model import Model
from view import View
from controller import Controller


def main():
    budget: float = float(input(f"Input Budget: "))

    model: Model = Model(budget)
    view: View = View()
    controller: Controller = Controller(model, view)

    controller.run()


if __name__ == "__main__":
    main()
