import unittest
from unittest.mock import patch
import main


class my_input:
    def __init__(self, array):
        self.counter = -1
        self.array = array

    def __call__(self, *args, **kwargs):
        self.counter += 1
        if self.counter >= len(self.array):
            raise "Unexpected amount of input calls"
        else:
            return self.array[self.counter]

def my_input_decor(array):
    def my_input_creator():
        return my_input(array)
    return patch('main.input', new_callable=my_input_creator)

class TestCheckDocumentExastance(unittest.TestCase):
    def setUp(self):
        main.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        main.directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

    def test_check_document_existance(self):
        self.assertEqual(main.check_document_existance('10006'), True)

    @patch('main.input', return_value='10006')
    def test_get_doc_owner_name(self, mocked_input):
        self.assertEqual(main.get_doc_owner_name(), 'Аристарх Павлов')

    def test_show_document_info(self):
        self.assertEqual(main.show_document_info(main.documents[0]), 'passport "2207 876234" "Василий Гупкин"')

    @patch('main.input', return_value='10006' )
    def test_get_doc_shelf(self, mocked_input):
        self.assertEqual(main.get_doc_shelf(), '2')

    @my_input_decor(['749375', 'passport', 'Иванов Иван Иванович', '3', '749375'])
    def test_add_document_info(self, mocked_input):
        # действие, которое проверяем
        result = main.add_new_doc()
        self.assertEqual(result, '3')
        # проверка
        self.assertEqual(main.get_doc_shelf(), '3')

    @patch('main.input', return_value='10006')
    def test_delete_doc(self, mocked_input):
        # действие, которое проверяем
        main.delete_doc()
        documents_number = []
        for document in main.documents:
            documents_number.append(document['number'])
        # проверка
        self.assertNotIn('10006', documents_number)


if __name__ == '__main__':
    unittest.main()
