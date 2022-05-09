import os
from dataclasses import dataclass
import datetime
import allure


@dataclass
class DATA:
    PATH = os.path.abspath('xml_responses/xml_response.xml')
    URL_GUIDE_CURRENCY_CODES = f'https://www.cbr.ru/scripts/XML_val.asp?d=0'
    URL_FOR_CURRENT_CURRENCY_QUOTES = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=' \
                                      f'{datetime.datetime.now().strftime("%d/%m/%Y")}'
    URL_FOR_CURRENT_CURRENCY_QUOTES_ENGLISH_VERSION = f'http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=' \
                                                      f'{datetime.datetime.now().strftime("%d/%m/%Y")}'
    FILE_XML_RESPONSE = 'xml_response.xml'
    FILE_XML_GUIDE_CURRENCY_CODES = "guide_currency_codes.xml"
    ENGLISH_LANGUAGE_IS_NOT_USED = r'[a-zA-Z]'
    RUSSIAN_LANGUAGE_IS_NOT_USED = r'[а-яА-Я]'


class TestAPICurrencyQuotes:
    def test_is_xml_valid(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES, DATA.FILE_XML_RESPONSE)
        with allure.step('Check is xml valid'):
            api_service.is_xml_valid(), "XML don't valid"

    def test_all_fields_in_document_exists(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES, DATA.FILE_XML_RESPONSE)
        with allure.step('Check the format corresponds to the declared one. All the fields described in the document.'):
            assert api_service.check_all_attributes(), "One or more fields in xml aren't exist"

    def test_valid_numbers(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES, DATA.FILE_XML_RESPONSE)
        with allure.step('Check are numbers valid'):
            api_service.check_are_numbers_valid(), 'One or more numbers are invalid'

    def test_valid_currency_id_codes(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES, DATA.FILE_XML_RESPONSE)
        api_service.create_file_with_xml_response(DATA.URL_GUIDE_CURRENCY_CODES, DATA.FILE_XML_GUIDE_CURRENCY_CODES)
        with allure.step('Checking that currency codes are real'):
            api_service.check_are_currency_id_codes_valid(), 'One or more currency codes are invalid'

    def test_russian_letters_are_valid(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES, DATA.FILE_XML_RESPONSE)
        with allure.step('Check that in russian version of website not used english letters'):
            api_service.check_not_used_letters_specified_language(DATA.ENGLISH_LANGUAGE_IS_NOT_USED), \
                'One or more names have not russian letters'

    def test_english_letters_are_valid(self, api_service):
        api_service.create_file_with_xml_response(DATA.URL_FOR_CURRENT_CURRENCY_QUOTES_ENGLISH_VERSION,
                                                  DATA.FILE_XML_RESPONSE)
        with allure.step('Check that in english version of website not used russian letters'):
            api_service.check_not_used_letters_specified_language(DATA.RUSSIAN_LANGUAGE_IS_NOT_USED), \
                'One or more names have not english letters'
