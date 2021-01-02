import yaml
from copy import deepcopy
from taiwanese.back.utils.gapi_connection import get_doc_service


class GDoc(object):
    def __init__(self, config_path):
        with open(config_path, 'r') as stream:
            self.__config = yaml.safe_load(stream)

        self.__service = self.get_service()

    def get_service(self):
        cred_path = self.config["credentials"]["google"]
        return get_doc_service(cred_path)

    @property
    def config(self):
        return deepcopy(self.__config)

    @property
    def service(self):
        return self.__service

    @staticmethod
    def read_paragraph_element(element):
        """Returns the text in the given ParagraphElement.

            Args:
                element: a ParagraphElement from a Google Doc.
        """
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    def read_strucutural_elements(self, elements):
        """Recurses through a list of Structural Elements to read a document's text where text may be
            in nested elements.

            Args:
                elements: a list of Structural Elements.
        """
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += self.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += self.read_strucutural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += self.read_strucutural_elements(toc.get('content'))
        return text

    def load_doc(self, doc_id):
        """Uses the Docs API to print out the text of a document."""

        doc = self.service.documents().get(documentId=doc_id).execute()
        doc_content = doc.get('body').get('content')
        print(self.read_strucutural_elements(doc_content))
