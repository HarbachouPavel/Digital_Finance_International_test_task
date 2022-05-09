import os
import re
import requests
import xml.etree.cElementTree as ET


class APIService:
    @staticmethod
    def get_response_in_xml(url: str):
        """
        Get response for api request in xml format
        :param url: The url to which the request is sent
        """
        response = requests.get(url)
        return response.text

    def create_file_with_xml_response(self, url: str, file_name: str):
        """
        Create xml file in 'xml_responses' folder with text of response
        :param url: The url to which the request is sent
        :param file_name: Name of the file, which will be created
        """
        xml_response_file = open(file_name, 'w+')
        xml_response_file.write(self.get_response_in_xml(url))
        xml_response_file.close()
        os.replace(file_name, f"xml_responses/{file_name}")

    def check_all_attributes(self):
        """
        Check all attributes in exist xml file 'xml_response.xml' on for the same amount.
        """
        tree = ET.parse('xml_responses/xml_response.xml')
        attributes = ('Valute', 'Valute/NumCode', 'Valute/CharCode', 'Valute/Nominal', 'Valute/Name', 'Valute/Value')
        list_of_lens_of_attributes = [len(tree.findall(x)) for x in attributes]
        return len(set(list_of_lens_of_attributes)) == 1

    @staticmethod
    def check_are_numbers_valid():
        """
        Check numbers in text of attributes on valid
        """
        tree = ET.parse('xml_responses/xml_response.xml').getroot()
        for currency in tree.findall('Valute'):
            assert currency.find('NumCode').text.isdigit(), \
                f"NumCode number is invalid, expected int, but {type(currency.find('NumCode').text)}"
            assert currency.find('Nominal').text.isdigit(), \
                f"Nominal number is invalid, expected int, but {type(currency.find('Nominal').text)}"
            value = currency.find('Value').text.replace(',', '.')
            assert float(value), 'Value number is invalid'

    def get_all_valid_currency_id_codes(self):
        """
        Get all valid currency id codes from central bank in list
        """
        tree = ET.parse('xml_responses/guide_currency_codes.xml').getroot()
        all_valid_currency_codes = []
        for currency_code in tree.findall('Item'):
            currency_id = currency_code.get('ID')
            all_valid_currency_codes.append(currency_id)
        return all_valid_currency_codes

    def check_are_currency_id_codes_valid(self):
        """
        Check that currency code exist in list of valid currency codes
        """
        tree = ET.parse('xml_responses/xml_response.xml').getroot()
        for currency_code in tree.findall('Valute'):
            currency_id = currency_code.get('ID')
            assert currency_id in self.get_all_valid_currency_id_codes(), "Currency id isn't valid"

    @staticmethod
    def has_letters_specified_language(text: str, language: str):
        """
        Search in the text letters of specified language
        :param text: The text in which the letters are searched for
        :param language: The language of the letters by which the search is performed in the text
        """
        return bool(re.search(language, text))

    def check_not_used_letters_specified_language(self, language: str):
        """
        Check The absence of letters of certain language in the text
        :param language: The absence of letters of this language is checked in the text
        """
        tree = ET.parse('xml_responses/xml_response.xml').getroot()
        for currency in tree.findall('Valute'):
            name = currency.find('Name').text
            assert not self.has_letters_specified_language(name, language), \
                f"Expected {language} letters, but {currency.find('Name').text}"

    def is_xml_valid(self):
        """
        Check xml file on validity
        """
        tree = ET.parse("xml_responses/xml_response.xml")
        assert tree, 'Parse error, expected successful parsing'
