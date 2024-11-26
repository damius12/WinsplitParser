import os
import tempfile
import unittest

import docx
from docx import Document

from src.create_word import create_word


class TestCreateWord(unittest.TestCase):
    def test_create_word_integration(self):
        # Create a temporary PNG file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_image:
            tmp_image.write(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x18\x05\x00\x00\x00\x00IEND\xaeB`\x82"
            )
            image_path = tmp_image.name

        event_title = "Test Event"
        results_text = "Sample results text."

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "results.docx")
            create_word(event_title, results_text, image_path, output_path)

            self.assertTrue(os.path.exists(output_path))

            doc = Document(output_path)
            doc_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            self.assertIn(event_title, doc_text)
            self.assertIn(results_text, doc_text)

            images = [shape for shape in doc.inline_shapes]
            self.assertTrue(len(images) > 0)

        # Clean up
        os.remove(image_path)


if __name__ == "__main__":
    unittest.main()
