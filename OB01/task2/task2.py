import datetime

class Store:

    def __init__(self, name, address):
        self.name = name 
        self.address = address
        self.items = {}

    def add_item(self, item_name, item_price):
        """Добавляет товар в ассортимент"""
        if item_name not in self.items:
            self.items[item_name] = item_price

    def remove_item(self, item_name):
        """Удаляет товар из ассортимента"""
        if item_name in self.items:
            del self.items[item_name]

    def get_price(self, item_name):
        """Получает цену товара по его назнаванию"""
        print(f"Цена на {item_name} - {self.items.get(item_name)}\n")

    def update_price(self, item_name, item_price):
        """Обновляет цену товара"""
        if item_name in self.items:
            self.items[item_name] = item_price

    def display_info(self):
        print(f"Название: {self.name}")
        print(f"Адрес: {self.address}")
        if len(self.items) > 0:
            print("Товары:")

            for key, value in self.items.items():
                print(f"\t{key} - {value}")
        print("")

def main():

    # Создать не менее трех различных магазинов с разными названиями, 
    # адресами и добавь в каждый из них несколько товаров.

    store1 = Store(name="Фруктовый рай", address="ул. Садовая, 15")  
    store1.add_item(item_name="яблоки", item_price=0.5)
    store1.add_item(item_name="бананы", item_price=0.75)
    store1.add_item(item_name="апельсины", item_price=0.9)

    store2 = Store(name="ТехноМир", address="пр. Науки, 42")  
    store2.add_item(item_name="смартфон", item_price=15000)
    store2.add_item(item_name="ноутбук", item_price=45000)
    store2.add_item(item_name="наушники", item_price=3000)

    store3 = Store(name="Книжный уголок", address="ул. Литературная, 7") 
    store3.add_item(item_name="роман '1984'", item_price=500)
    store3.add_item(item_name="энциклопедия по истории", item_price=1200)
    store3.add_item(item_name="детская книга", item_price=300) 

    store1.display_info()
    store2.display_info()
    store3.display_info()

    # Протестировать методы
    # добавить товар
    store1.add_item(item_name="манго", item_price=0.8)

    # обновить цену
    store1.update_price(item_name="яблоки", item_price=0.6)

    # убрать товар
    store1.remove_item(item_name="бананы")

    # запросить цену
    store1.get_price(item_name="апельсины")
    
    store1.display_info()


if __name__ == "__main__":
    main()
