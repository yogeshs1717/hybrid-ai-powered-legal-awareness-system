#!/usr/bin/env python3
"""Builds both LegalLens Interview Viva Notes and Improvements Changelog in PDF and Markdown format."""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

DOCS_DIR = Path("/home/shnl/Documents")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y' and running headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColorRGB(0.35, 0.42, 0.52) # Slate-500
        
        doc_title = getattr(self, '_doc_title', 'LegalLens — Interview & Viva Notes')
        
        # Running header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 842 - 36, doc_title)
            self.drawRightString(595 - 54, 842 - 36, "Republic of India Law Awareness Engine")
            self.setStrokeColorRGB(0.82, 0.86, 0.90)
            self.setLineWidth(0.5)
            self.line(54, 842 - 42, 595 - 54, 842 - 42)

        # Running footer
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — MAJOR PROJECT DEFENSE & TECHNICAL AUDIT")
        self.drawRightString(595 - 54, 36, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColorRGB(0.82, 0.86, 0.90)
        self.setLineWidth(0.5)
        self.line(54, 46, 595 - 54, 46)
        self.restoreState()


def get_styles():
    base = getSampleStyleSheet()
    s = {}
    s['Title'] = ParagraphStyle(
        'DocTitle', parent=base['Title'], fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=colors.HexColor('#0f172a'), alignment=0, spaceAfter=4
    )
    s['SubTitle'] = ParagraphStyle(
        'DocSubTitle', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=colors.HexColor('#0284c7'), spaceAfter=8
    )
    s['Meta'] = ParagraphStyle(
        'MetaBox', parent=base['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=11,
        textColor=colors.HexColor('#475569'), spaceAfter=10
    )
    s['SecHeading'] = ParagraphStyle(
        'SecHeading', parent=base['Heading1'], fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=colors.HexColor('#0f172a'), spaceBefore=12, spaceAfter=5, keepWithNext=True
    )
    s['SubSecHeading'] = ParagraphStyle(
        'SubSecHeading', parent=base['Heading2'], fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=colors.HexColor('#1e293b'), spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    s['SubSubSecHeading'] = ParagraphStyle(
        'SubSubSecHeading', parent=base['Heading3'], fontName='Helvetica-Bold', fontSize=8.5, leading=12,
        textColor=colors.HexColor('#334155'), spaceBefore=5, spaceAfter=2, keepWithNext=True
    )
    s['Body'] = ParagraphStyle(
        'Body', parent=base['Normal'], fontName='Helvetica', fontSize=8, leading=11,
        textColor=colors.HexColor('#334155'), spaceAfter=4
    )
    s['BodyBold'] = ParagraphStyle(
        'BodyBold', parent=s['Body'], fontName='Helvetica-Bold'
    )
    s['Bullet'] = ParagraphStyle(
        'Bullet', parent=s['Body'], leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )
    s['Preformatted'] = ParagraphStyle(
        'Preformatted', parent=base['Code'], fontName='Courier', fontSize=6.5, leading=8.5,
        textColor=colors.HexColor('#0f172a'), backColor=colors.HexColor('#f8fafc'),
        borderColor=colors.HexColor('#e2e8f0'), borderWidth=0.5, borderPadding=5,
        spaceBefore=3, spaceAfter=5
    )
    s['TableHead'] = ParagraphStyle(
        'TableHead', parent=base['Normal'], fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=colors.HexColor('#0f172a')
    )
    s['TableCell'] = ParagraphStyle(
        'TableCell', parent=base['Normal'], fontName='Helvetica', fontSize=7, leading=9,
        textColor=colors.HexColor('#334155')
    )
    s['TableCellBold'] = ParagraphStyle(
        'TableCellBold', parent=s['TableCell'], fontName='Helvetica-Bold', textColor=colors.HexColor('#0f172a')
    )
    s['QuoteBox'] = ParagraphStyle(
        'QuoteBox', parent=s['Body'], fontName='Helvetica-Oblique', textColor=colors.HexColor('#0369a1'),
        backColor=colors.HexColor('#f0f9ff'), borderColor=colors.HexColor('#0284c7'),
        borderWidth=1, borderPadding=6, spaceBefore=4, spaceAfter=6
    )
    return s

print("NumberedCanvas and styles initialized.")
