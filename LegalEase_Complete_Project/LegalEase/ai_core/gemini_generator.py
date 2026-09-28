from __future__ import annotations

from dataclasses import dataclass

from config import Settings


SYSTEM_INSTRUCTION = """You are LegalEase, a legal-document drafting assistant.
Create a professional first draft from the user's supplied facts.
Never invent names, addresses, dates, amounts, obligations, governing law, or facts that the user did not provide.
If information is missing, use a clearly marked placeholder such as [INSERT AMOUNT] rather than making it up.
Do not claim the document is legally valid, attorney-reviewed, or jurisdiction-compliant.
Use clear formal language and a structure appropriate for the requested document type.
Return plain text only. Do not use Markdown tables, code fences, or commentary outside the document.
"""


@dataclass
class GenerationResult:
    text: str
    mode: str
    model: str


class GeminiDocumentGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._client = None

        if settings.gemini_api_key:
            from google import genai

            self._client = genai.Client(api_key=settings.gemini_api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str = "",
        language: str = "English",
    ) -> GenerationResult:
        if self._client is None:
            if self.settings.demo_mode:
                return GenerationResult(
                    text=self._demo_document(
                        document_type, parties, terms, dates, jurisdiction, language
                    ),
                    mode="demo",
                    model="local-demo",
                )
            raise RuntimeError("GEMINI_API_KEY is not configured and DEMO_MODE is disabled.")

        prompt = self._build_prompt(
            document_type, parties, terms, dates, jurisdiction, language
        )

        response = self._client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": self.settings.temperature,
                "max_output_tokens": self.settings.max_output_tokens,
            },
        )

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return GenerationResult(text=text, mode="gemini", model=self.settings.gemini_model)

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str,
        language: str,
    ) -> str:
        return f"""Draft a {document_type} using exactly the information below.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{dates}

JURISDICTION (optional):
{jurisdiction or '[NOT PROVIDED]'}

LANGUAGE:
{language}

Required document structure:
1. Document title
2. Effective date
3. Parties
4. Recitals/background only if supported by the supplied facts
5. Definitions if genuinely needed
6. Main clauses suitable for this document type
7. The supplied terms, preserved accurately
8. Termination/expiry if the supplied terms support it
9. Governing law/dispute provisions only if the user supplied jurisdiction or an explicit instruction
10. Signature blocks with placeholders where information is missing
11. A short 'Drafting Notice' stating that the document should be reviewed for applicable law before use

Do not fabricate missing facts. Keep the draft internally consistent.
"""

    @staticmethod
    def _demo_document(
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str,
        language: str,
    ) -> str:
        term_items = [item.strip() for item in terms.split(";") if item.strip()]
        bullets = "\n".join(f"{i}. {item}" for i, item in enumerate(term_items, 1))
        if not bullets:
            bullets = "1. [INSERT AGREED TERMS]"

        jurisdiction_clause = (
            f"\nGOVERNING LAW\nThis draft is intended to be reviewed under the laws of {jurisdiction}."
            if jurisdiction
            else "\nGOVERNING LAW\n[INSERT GOVERNING LAW / JURISDICTION IF REQUIRED]"
        )

        return f"""{document_type.upper()}

EFFECTIVE DATE
{dates or '[INSERT EFFECTIVE DATE]'}

BETWEEN
{parties or '[INSERT PARTIES AND ROLES]'}

PURPOSE
This draft records the agreement described by the parties for the requested {document_type}.

TERMS AND CONDITIONS
{bullets}

ADDITIONAL PROVISIONS
The parties should insert any required provisions concerning notices, amendments, assignment, confidentiality, liability, termination, dispute resolution, and signatures where applicable.
{jurisdiction_clause}

SIGNATURES

Party 1: ______________________________
Name: [INSERT NAME]
Date: _________________________________

Party 2: ______________________________
Name: [INSERT NAME]
Date: _________________________________

DRAFTING NOTICE
This is an AI-assisted draft and is not a substitute for advice from a qualified legal professional. Review the document for the applicable law and facts before signing or relying on it.
""".strip()
