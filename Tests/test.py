import unittest
from main import CsvParserGui
from new_customer_supplier import db

class TestCsvParserGui(unittest.TestCase):

    def setUp(self):
        self.excel_to_parse = r"C:/Users/phoeb/Documents/Work/Company software solutions/Excels Run/excel for unit testing.xlsx"
        self.csvParser = CsvParserGui()

    def test_get_entered_file_path(self):
        self.assertEqual(self.csvParser.get_entered_file_path(), self.excel_to_parse, 'The path is wrong.')

    def test_fill_file_path_box(self):
        self.assertEqual(self.csvParser.fill_file_path_box(), self.excel_to_parse, 'The path is wrong.')

    def test_clear(self):
        self.csvParser.clear()
        self.assertIsNone(self.csvParser.get_entered_file_path(), 'The clear function did not work.')


class TestAccountsDatabase(unittest.TestCase):

    def setUp(self):
        self.start = CsvParserGui()
        self.database = db
        self.db = r"C:\Users\phoeb\PycharmProjects\CSV-Parser\Tests\accounts_formatter.db"

    def test_database_created(self):
        self.assertIsNotNone(self.db, 'The database was not created.')

    def test_get_table(self):
        table = [(1, "cust a"), (2, "cust b")]
        self.assertEqual(self.database.get_table("customer"), table, 'The customer table was not fetched.')

    def test_customer_table_created(self):
        table = "customer"
        self.assertIsNotNone(self.database.get_table(table), 'The customer table was not created.')

    def test_supplier_table_created(self):
        table = "supplier"
        self.assertIsNotNone(self.database.get_table(table), 'The supplier table was not created.')

    def test_get_customer(self):
        customer = "cust a"
        self.assertIn(customer, self.database.get_customer(1), 'Get customer failed.')

    def test_get_supplier(self):
        supplier = "supplier a"
        self.assertIn(supplier, self.database.get_supplier(1), 'Get supplier failed.')

    def test_add_customer(self):
        customer = (3, "cust c")
        self.database.add_customer(customer)
        self.assertIsNotNone(self.database.get_customer(3), 'Add customer failed')

    def test_add_supplier(self):
        supplier = (2, "supplier b")
        self.database.add_supplier(supplier)
        self.assertIsNotNone(self.database.get_supplier(3), 'Add supplier failed.')

    def test_delete_customer(self):
        customer = (2, "cust b")
        self.database.delete_customer(customer)
        self.assertIsNone(self.database.get_customer(2), 'Delete customer failed')

    def test_delete_supplier(self):
        supplier = (1, "supplier a")
        self.database.delete_supplier(supplier)
        self.assertIsNone(self.database.get_supplier(1), 'Delete supplier failed.')


if __name__ == '__main__':
    unittest.main()
