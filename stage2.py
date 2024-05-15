from abc import ABC, abstractmethod

# Базовий клас для стратегій розрахунку витрат
class CostCalculationStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, components_cost, additional_param=None):
        pass

# Схема 1: Сума вартості компонентів
class SumComponentsCost(CostCalculationStrategy):
    def calculate_cost(self, components_cost, additional_param=None):
        return sum(components_cost)

# Схема 2: Сума вартості компонентів + відсоток націнки
class SumComponentsCostPlusMarkup(CostCalculationStrategy):
    def calculate_cost(self, components_cost, markup_percentage):
        return sum(components_cost) * (1 + markup_percentage / 100)

# Схема 3: Сума складових вартості - вартість утримання за день
class SumComponentsCostMinusHoldingCost(CostCalculationStrategy):
    def calculate_cost(self, components_cost, holding_cost_per_day, storage_days):
        return sum(components_cost) - (holding_cost_per_day * storage_days)

# Клас продукту
class Product:
    def __init__(self, name, components_cost, calculation_strategy, additional_param=None):
        self.name = name
        self.components_cost = components_cost
        self.calculation_strategy = calculation_strategy
        self.additional_param = additional_param

    def calculate_cost(self):
        if isinstance(self.calculation_strategy, SumComponentsCostMinusHoldingCost):
            return self.calculation_strategy.calculate_cost(self.components_cost, self.additional_param['holding_cost_per_day'], self.additional_param['storage_days'])
        return self.calculation_strategy.calculate_cost(self.components_cost, self.additional_param)
    
    def __str__(self):
        cost = self.calculate_cost()
        output = f'Продукт: {self.name}, Вартість: {cost}'
        return output

# Клас контейнер для продуктів
class ProductContainer:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_name):
        self.products = [product for product in self.products if product.name != product_name]

    def __iter__(self):
        return iter(self.products)

    def calculate_all_costs(self):
        for product in self.products:
            print(product)

# Основна програма
container = ProductContainer()

# Додавання продуктів з різними стратегіями розрахунку вартості
product1 = Product("Product 1", [10, 20, 30], SumComponentsCost())
product2 = Product("Product 2", [15, 25, 35], SumComponentsCostPlusMarkup(), 10)
product3 = Product("Product 3", [20, 30, 40], SumComponentsCostPlusMarkup(), 20)
product4 = Product("Product 4", [25, 35, 45], SumComponentsCostMinusHoldingCost(), {'holding_cost_per_day': 2, 'storage_days': 5})
product5 = Product("Product 5", [30, 40, 50], SumComponentsCostMinusHoldingCost(), {'holding_cost_per_day': 3, 'storage_days': 10})

container.add_product(product1)
container.add_product(product2)
container.add_product(product3)
container.add_product(product4)
container.add_product(product5)

container.calculate_all_costs()
