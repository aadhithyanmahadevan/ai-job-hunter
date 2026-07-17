from pathlib import Path
import docx
import fitz


class ResumeParser:

    def extract_text(self, filepath: str) -> str:

        extension = Path(filepath).suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf(filepath)

        if extension == ".docx":
            return self._extract_docx(filepath)

        raise Exception("Unsupported file format")

    def _extract_pdf(self, filepath):

        text = ""

        pdf = fitz.open(filepath)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text

    def _extract_docx(self, filepath):

        doc = docx.Document(filepath)

        return "\n".join(p.text for p in doc.paragraphs)
