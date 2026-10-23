# AnalytixFest 2K27 — Streamlit Starter

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`
4. Run `streamlit run app.py`

## Included pages
- Cinematic home / hero
- About and participant checklist
- Vecna's Paradox flagship ideathon
- Four technical events
- Five non-technical events
- Source timeline with category filter and CSV download
- Organizing committee
- Demo registration form
- Contact page

## Before deployment
The supplied content document flags unresolved conflicts in event date, timetable, venues, coordinator contacts, fee inclusions and registration endpoint. The app preserves source details and marks conflicts rather than inventing corrections. Obtain committee approval before publishing.

The registration form writes personal data to `data/registrations.csv` on the machine running Streamlit. This is a demo, not a production registration/payment system. Do not deploy publicly without a secure database, access controls, privacy notice and approved submission/payment flow.

The visual styling uses CSS and Google Fonts. Internet access is required for Google Fonts. No Stranger Things character imagery, logos, footage or music are bundled; use authorized assets or original genre-inspired visuals.
