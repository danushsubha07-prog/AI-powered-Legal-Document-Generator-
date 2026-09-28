from utils.document_formatters import format_docx, format_pdf, format_txt


def test_txt_export():
    data = format_txt("TEST DOCUMENT\n\nHello")
    assert data.startswith(b"TEST DOCUMENT")


def test_docx_export():
    data = format_docx("TEST DOCUMENT\nHello", "Test Agreement", "A, B", "Payment within 30 days")
    assert data[:2] == b"PK"


def test_pdf_export():
    data = format_pdf("TEST DOCUMENT\nHello", "Test Agreement", "A, B", "Payment within 30 days")
    assert data.startswith(b"%PDF")
