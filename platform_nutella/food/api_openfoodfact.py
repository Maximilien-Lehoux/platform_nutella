import json
import requests

# API_TO_PRODUCT_FIELDS = {
    # 'product_name_fr': 'name',
    # 'url': 'url',
    # 'nutrition_grade_fr': 'nutriscore',
    # 'category': 'category'
    # }

NUMBER_PRODUCTS = 100

# payload_products_generic_name = {
                    # 'search_terms': 'coquillette',
                    # 'page_size': NUMBER_PRODUCTS,
                    # 'json': 'true',
                    # }

# payload_substitutes = {
                    # 'action': 'process',
                    # 'tagtype_0': 'categories',
                    # 'tag_contains_0': 'contains',
                    # 'tag_0': 'Pâtes alimentaire',
                    # 'page_size': NUMBER_PRODUCTS,
                    # 'json': 'true',
                    # }


URL_GENERAL = 'https://fr.openfoodfacts.org/cgi/search.pl'
info1 = "product_name_fr"
info2 = "image_front_thumb_url"
info3 = "nutrition_grade_fr"
info4 = "url"


class DataApi:
    """the request to the API which contains the parameters"""
    def __init__(self, product):
        self.url = URL_GENERAL

        self.payload_products_generic_name = {
            'search_terms': product,
            'page_size': NUMBER_PRODUCTS,
            'json': 'true',
        }

    def get_categories_name_food(self):
        response = requests.get(self.url, params=self.payload_products_generic_name)
        if 'json' in response.headers.get('Content-Type'):
            data = response.json()["products"][0]["categories"]
        else:
            print('response content is not in json format.')
            data = 'spam'
        return data

    def get_data_products_category(self, category_product):
        payload_substitutes = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category_product,
            'page_size': NUMBER_PRODUCTS,
            'json': 'true',
        }
        response = requests.get(self.url, params=payload_substitutes).json()
        data = response["products"]
        with open("file_json.json", "w") as file:
            json.dump(data, file, sort_keys=True, indent=4)
        return data

    def select_key_test(self, key1=info1, key2=info2, key3=info3, key4=info4):
        """The different keys are sorted and placed in lists"""
        list_general = []
        categories = self.get_categories_name_food()
        category = self.get_category_selected(categories)

        data = self.get_data_products_category(category)
        for item in data:
            product_list = [item.get(key1), item.get(key2), item.get(key3),
                            item.get(key4)]
            if '' not in product_list and None not in product_list:
                list_general.append(product_list)
        return list_general

    def get_category_selected(self, categories):
        categories_list = categories.split(",")
        category = categories_list[0]
        return category


# 'product_name_fr', 'generic_name_fr', 'url', 'image_front_thumb_url', 'nutrition_grade_fr'


example_data_api = DataApi("cassoulet")
data_categories = example_data_api.select_key_test()
# category = example_data_api.get_category_selected(data_categories)

print(data_categories)


# data_products_category = example_data_api.select_key_test()




# print(data_products_category)





# 'image_front_thumb_url'
# 'selected_images': {'front': {'display': {'fr'

