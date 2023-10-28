import pandas as pd
from sentence_transformers import SentenceTransformer, util


# model config with main functions

class Model:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
        self.standards_groups = pd.read_csv('standarts.csv')['Группа продукции'].unique()
        self.standarts_groups_file = pd.read_csv('standarts.csv')

    def get_products_group_embeddings(self):
        # Получаем эмбеддинги для групп продуктов
        passage_embedding = self.model.encode(self.standards_groups)
        return passage_embedding

    def get_equipment_list(self, most_similar):
        equipments = pd.read_csv('dataset_Equipment.csv')
        standarts = self.standarts_groups_file[self.standarts_groups_file['Группа продукции']
                                               == most_similar]['Обозначение и наименование стандарта'].unique()
        equipment_list = []
        for standard in standarts:
            for gost_name in equipments['gost'].unique():
                if standard.__contains__(gost_name):
                    eqt = equipments[equipments['gost'] == gost_name]['Equipment'].values
                    if eqt[0].__contains__('Оборудование не реглам'):
                        print('шляпа')
                    else:
                        equipment_list.append(eqt)

        return equipment_list

    def get_most_similar_value(self, product_name):
        # find similar product group by product name
        product_name_embedding = self.model.encode(product_name)  # получаем эмбеддинг наименования продукта
        similarities = util.dot_score(product_name_embedding, self.get_products_group_embeddings())[0]
        most_similar = pd.DataFrame({'similarity_score': similarities, 'standarts_groups': self.standards_groups}). \
                           sort_values(['similarity_score'], ascending=False)['standarts_groups'][:1].values[0]

        return most_similar

    def get_recommendation(self, query):
        most_similar_value = self.get_most_similar_value(product_name=query)
        return self.get_equipment_list(most_similar=most_similar_value)
