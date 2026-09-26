# whatsapp-customer-data-extractor
A Python automation tool to extract customer data from WhatsApp Web using Playwright.

## Features
- Extract customer name
- Extract phone number
- Extract timestamp
- Generate Excel report

## Setup

Install dependencies:

```bash
pip install -r requirements.txt

Install Playwright:
python -m playwright install

Run
python whatsapp_export.py

Scan WhatsApp Web QR code when browser opens.
After completion, an Excel file will be generated.

Output
clean_whatsapp_data.xlsx

Contains:
- Name
- Phone Number
- Timestamp
- WhatsApp Link
