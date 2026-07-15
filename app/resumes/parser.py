import fitz


class ResumeParser:

    def parse(self, path: str):

        doc = fitz.open(path)

        text = ""

        for page in doc:
            text += page.get_text()

        return text