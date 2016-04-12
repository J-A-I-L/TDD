#!/usr/bin/python3
'''Unit tests for foo.py'''
__author__ = 'J.A.I.L.'

import unittest
import sqlite3
import os
import re

class TestCase(unittest.TestCase):
    '''
    A class that extends unittest.TestCase by adding an assert that allows multiple
    lines comparison for unordered lines.
    '''    
    @staticmethod
    def strip_multiline_string(multiline_string, sort=False):
        list_of_lines = [line.strip() for line in multiline_string.splitlines()]
        if sort:
            list_of_lines.sort()
        striped_and_sorted_multiline_string = '\n'.join(list_of_lines)
        return striped_and_sorted_multiline_string
    
    def assertShuffledMultilineEqual(self, first, second, msg=None):
        ''' Assert that two multi-line strings have equal lines, even in different line positions.'''
        self.assertIsInstance(first, str, 'First argument is not a string')
        self.assertIsInstance(second, str, 'Second argument is not a string')

        stripped_and_sorted_first = TestCase.strip_multiline_string(first, sort=True)
        stripped_and_sorted_second = TestCase.strip_multiline_string(second, sort=True)
        #self.maxDiff = None
        self.assertMultiLineEqual(stripped_and_sorted_first, stripped_and_sorted_second, msg)

class BioinformaticsTest(TestCase):
    '''
    A class that performs unit tests for the Bioinformatics course.
    '''    
    def setUp(self):
        ''' 
        Before running the tests, execute a method that prepares the module. 
        E.G: You may want to initialize/declare constants in this method. 
        '''
        module_to_test.main()

def convert_from_camel_case_to_separated_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return s2

def convert_from_separated_underscore_to_camel_case(name):
    s1 = ''.join(x.capitalize() or '_' for x in name.split('_'))
    return s1

def database_retrieval():
    '''
    Retrieves information from the database.
    Fetches data from a D.B. Columns: 'name_of_method_to_test', 'input_data', 
    'expected_data', 'perform_test' (boolean), ...
    If the database doesn't exist, it creates is, adds the tables, and prompts 
    the user a message telling it must be populated with data.
    Output:
        A list of tuples (rows) with the values of 'name_of_method_to_test', 
        'data_input', 'expected_output'.
    '''
    table_attributes = {'database_filename': name_of_module_to_test + '.sqlite3',
                        'table_name': 'Test', 
                        'method_column': 'name_of_method_to_test', 
                        'input_column': 'data_input', 
                        'output_column': 'expected_output', 
                        'is_test_performed_column': 'perform_test',
                        'comment_column': 'comment'}
    connection = sqlite3.connect(table_attributes['database_filename'])
    try:
        cursor = connection.cursor()
        
        # Check if the table exists
        cursor.execute('''
            SELECT COUNT(*) 
            FROM sqlite_master
            WHERE type='table' 
              AND name = ? ''',
            (table_attributes['table_name'], ))
        if int(cursor.fetchone()[0]) != 1:
            cursor.execute('''
                CREATE TABLE {table_name} 
                    ({method_column} TEXT, 
                    {input_column} TEXT, 
                    {output_column} TEXT, 
                    {is_test_performed_column} INTEGER DEFAULT 1 /* Pity there's no BOOLEAN in SQLite */,
                    {comment_column}) '''
                .format(**table_attributes))
                        
            raise sqlite3.ProgrammingError('''
    The database didn't exist. Creating a new database...
    Database file '{database_filename}' has been created.
    Fill the table '{table_name}' with data and execute this program again to 
    run the tests:
        In the '{method_column}' column you should type the name of the method 
        to test. This method must accept one single parameter of type string. 
        E.G:
            frequent_words
        In '{input_column}' the string that will be passed to the method when 
        called. It can have multiple lines, E.G:
            ACGTTGCATGTCGCATGATGCATGAGAGCT
            4
        In '{output_column}' the string that the method should return if it is 
        correct. E.G:
            CATG GCAT  '''
                .format(**table_attributes))
        
        else:
            cursor.execute('''
                SELECT {method_column}, {input_column}, {output_column}, {comment_column}
                FROM {table_name}
                WHERE {is_test_performed_column} = 1  '''
                .format(**table_attributes))
            result = cursor.fetchall()
    finally:
        connection.close()
    
    return result

def add_test(test_class_to_add_the_method, module_to_test, name_of_method_to_test, data_input, expected_output, comment):
    '''
    Adds a test method dynamically using reflection.
    '''
    try:
        '''  Imports dynamically the function to be tested '''
        method_to_test = getattr(module_to_test, name_of_method_to_test)
    except AttributeError:
        # print('Method not implemented:', name_of_method_to_test, file=sys.stderr)
        method_to_test = None

    # Make sure the chosen name doesn't already exist.
    i = 0
    name_of_new_method_test = 'test_' + name_of_method_to_test + '_' + str(i)
    while name_of_new_method_test in dir(test_class_to_add_the_method):
        i += 1
        name_of_new_method_test = 'test_' + name_of_method_to_test + '_' + str(i)
        
    # Add the new method to the class.
    @unittest.skipIf(method_to_test is None, 'Method not implemented yet.')
    def method_test_template(self):
        '''
        A template for a test method.
        This doc comment will be replaced when the method is created dynamically.
        '''
        
        ''' Arrange '''
        # data_input and expected_output are declared as  add_test() method parameters.
        
        ''' Act '''
        result = method_to_test(data_input)
        
        ''' Assert '''
        self.assertShuffledMultilineEqual(expected_output, result)

    method_test_template.__name__ = name_of_new_method_test
    method_test_template.__doc__ = 'Test for method ' + '\'' +  name_of_new_method_test + '\''
    method_test_template.__doc__ += comment if comment is not None else ''
    
    setattr(test_class_to_add_the_method, method_test_template.__name__, method_test_template)
                
if __name__ == '__main__':    
    ''' Create a class that extends BioinformaticsTest '''
    this_file_path_and_name = os.path.split(__file__)
    name_of_module_to_test = this_file_path_and_name[1][len('test_'):-len('.py')]
    name_of_new_test_class = convert_from_separated_underscore_to_camel_case(name_of_module_to_test) + 'Test'
    new_test_class = type(name_of_new_test_class, (BioinformaticsTest, ), dict())


    '''  Imports dynamically the file module with functions to be tested. '''
    ''' Remember the file to be testes must be in the same directory as this one. '''
    module_to_test = __import__(name_of_module_to_test)

    for name_of_method_to_test, data_input, expected_output, comment in database_retrieval():
        ''' Creates dynamically the test method in the class '''
        add_test(new_test_class, module_to_test, name_of_method_to_test, data_input, expected_output, comment)
    
    unittest.main(verbosity=2)
    
