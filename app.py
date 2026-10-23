from __future__ import annotations
import csv, re
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / 'data'
REGISTRATION_FILE = DATA_DIR / 'registrations.csv'
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title='AnalytixFest 2K27 | When Data Meets the Upside Down', page_icon='🌀', layout='wide')

st.markdown(r'''<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Cinzel+Decorative:wght@700;900&family=Outfit:wght@300;400;500;600;700;800&family=Special+Elite&family=VT323&display=swap');
:root{--bg:#050507;--red:#E50914;--crimson:#FF1E27;--blue:#55C8FF;--violet:#7626A8;--text:#E2E8F0;--muted:#9BA3AF}
html,body,[class*="css"]{font-family:'Outfit',sans-serif}
.stApp{color:var(--text);background:radial-gradient(ellipse at 15% 0%,rgba(118,38,168,.18),transparent 35%),radial-gradient(ellipse at 85% 12%,rgba(229,9,20,.15),transparent 33%),linear-gradient(180deg,#050507 0%,#10151C 48%,#090608 100%)}
[data-testid="stHeader"]{background:rgba(5,5,7,.7)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#08080C,#111019 60%,#090608);border-right:1px solid rgba(255,30,39,.35)}
[data-testid="stSidebar"] *{color:#E2E8F0}
.block-container{padding-top:1.5rem;max-width:1250px}
.hero{padding:3rem 1.5rem;text-align:center;border-radius:22px;border:1px solid rgba(255,30,39,.5);background:linear-gradient(120deg,rgba(5,5,7,.92),rgba(20,10,18,.8));box-shadow:0 0 38px rgba(229,9,20,.14),inset 0 0 40px rgba(118,38,168,.08);position:relative;overflow:hidden}
.eyebrow{color:var(--blue);text-transform:uppercase;letter-spacing:.24em;font-size:.76rem}
.hero-title{font-family:'Cinzel Decorative','Creepster',serif;text-transform:uppercase;font-size:clamp(2.2rem,6vw,5.5rem);line-height:1.08;letter-spacing:.06em;color:#fff;text-shadow:0 0 8px #FF1E27,0 0 25px rgba(229,9,20,.75);margin:.8rem 0}
.hero-tag{font-family:'Special Elite',monospace;font-size:clamp(1rem,2vw,1.35rem);color:#FFB9BC}
.section-title{font-family:'Cinzel Decorative',serif;color:#fff;font-size:clamp(1.45rem,3vw,2.2rem);text-shadow:0 0 13px rgba(229,9,20,.55);border-bottom:1px solid rgba(255,30,39,.4);padding-bottom:.55rem;margin:1.2rem 0}
.panel{border:1px solid rgba(85,200,255,.22);border-left:3px solid var(--red);border-radius:14px;padding:1.15rem 1.25rem;background:rgba(10,12,18,.78);margin-bottom:.8rem}
.event-name{font-family:'Cinzel Decorative',serif;font-weight:700;color:#fff;font-size:1.1rem}.event-code{font-family:'VT323',monospace;letter-spacing:.12em;color:var(--blue);font-size:1.1rem}.muted{color:var(--muted)}
.metric-box{padding:1rem;border-radius:12px;background:rgba(15,17,25,.8);border:1px solid rgba(255,30,39,.3);text-align:center}.metric-num{font-family:'VT323',monospace;color:#FF424A;font-size:2rem}.metric-label{color:#CBD5E1;font-size:.82rem;text-transform:uppercase;letter-spacing:.08em}
.stButton>button,.stDownloadButton>button{background:linear-gradient(90deg,#9D0610,#E50914);color:white;border:1px solid #FF424A;border-radius:8px;font-weight:700}.stButton>button:hover,.stDownloadButton>button:hover{box-shadow:0 0 18px rgba(229,9,20,.45);color:white}
a{color:#75D4FF!important}hr{border-color:rgba(255,30,39,.25)}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>''', unsafe_allow_html=True)

TECH_EVENTS = [
{'name':'The Cerebro Code','subtitle':'Bug Flayer','description':'Competitive coding and algorithmic bug hunt. Repair code fragments, solve algorithmic challenges, and demonstrate efficient solutions.','team':'1–2 participants','time':'10:00 AM–1:00 PM (source schedule; verify)','venue':'CS Lab 1 & 2, PG Block','rounds':['Hawkins Signal Debug — fix 15 code fragments (45 min).','Suzie, Do You Copy? — algorithms, graph traversal and dynamic programming (60 min).'],'rules':'Languages listed: Python, C++, Java and C. Plagiarism or unauthorized AI copilots may lead to disqualification.'},
{'name':'Hawkins Lab Dossier','subtitle':'Paper Presentation','description':'Research paper and conceptual presentation on emerging data and computing topics.','team':'1–2 authors','time':'10:00 AM–1:00 PM (source schedule; verify)','venue':'Classroom 304, 3rd Floor, Admin Block','rounds':['Submit an abstract of up to 300 words in IEEE format before the event.','Source says 8-minute talk + 3-minute Q&A; another field says 10 minutes per team. Confirm.'],'rules':'Topics include Big Data Analytics, Generative AI, LLMs, Quantum Data Computing and Ethical AI. Original work only; source states plagiarism over 15% leads to rejection.'},
{'name':'The Hellfire Query','subtitle':'Database Forensics & Dashboard Analytics','description':'Use SQL reasoning and analytical reporting to investigate a database challenge.','team':'Individual or team of 2','time':'10:00 AM–1:00 PM (source schedule; verify)','venue':'CS Lab 3, PG Block — room conflict to resolve','rounds':['Joins, subqueries and grouping rollups (45 min).','Dashboard or report (30 min).'],'rules':'PostgreSQL/MySQL are listed; Tableau or Power BI are optional. Evaluation includes query correctness, index awareness and execution-cost optimization.'},
{'name':'Web of Vecna','subtitle':'AI Prompt & Web Design','description':'Combine creative prompting with a themed interactive web design challenge.','team':'1–2 participants','time':'10:00 AM–1:00 PM (source schedule; verify)','venue':'CS Lab 3, PG Block — room conflict to resolve','rounds':['AI Prompt Challenge — generate themed images (60 min).','Web Design Challenge — create an interactive dashboard (60 min).'],'rules':'Source lists prompt engineering tools, image-generation tools and web technologies. Check permitted tools with the organizers.'}
]
NONTECH_EVENTS = [
{'name':'The Hellfire Boardroom','subtitle':'Corporate Walk','description':'A professional persona showcase judged on confidence, body language, articulation, grooming and presence of mind.','team':'Individual or team of 2','time':'Event data: 11:00 AM–12:30 PM; timeline: 1:45–3:45 PM. Verify.','venue':'Seminar Hall I / Classroom 304 — verify','rounds':['Executive Stride (30 min).','Boardroom Interrogation (45 min).'],'rules':'Formal business attire is specified in the source.'},
{'name':'The Hawkins AV Archive','subtitle':'Multimedia Storytelling','description':'Create an original short-form video or storyboard and explain the creative choices.','team':'1–3 participants','time':'Event data: 11:30 AM–1:00 PM; timeline: 1:45–3:45 PM. Verify.','venue':'Digital Media Studio / CS Lab 3 — verify','rounds':['Prior submission and screening.','Live defense: source lists both 3 minutes and 5 minutes per team; confirm.'],'rules':'Video length 60–90 seconds or storyboard up to 10 slides. Original content only.'},
{'name':'The Palace Arcade Draft','subtitle':'Franchise Auction','description':'Build a balanced team or asset portfolio under a fixed virtual budget.','team':'2–3 participants','time':'Event data: 2:00–4:00 PM; timeline: 1:45–3:45 PM. Verify.','venue':'Multipurpose Auditorium','rounds':['Purse Allocation Brief (30 min prep).','Live Bidding Wars (90 min).'],'rules':'Over-bidding may cause asset forfeiture. Judging includes budget optimization, squad balance and tactical selection.'},
{'name':'Surfer Boy Pitch','subtitle':'Ad-Zap','description':'Pitch a futuristic data product through a persuasive, funny, retro-inspired advertisement.','team':'3–4 participants','time':'1:45–3:45 PM (timeline; verify)','venue':'Multipurpose Auditorium','rounds':['Jingle Formulation (30 min prep).','Live Commercial Broadcast (5 min per team).'],'rules':'Create a comedic or persuasive 1980s-style advertisement for a futuristic data product.'},
{'name':'Dungeons & Data','subtitle':'Mystery Treasure Hunt','description':'Follow campus clues and solve code- and QR-style puzzles in a mystery hunt.','team':'3–4 participants','time':'Event data: 2:30–4:30 PM; timeline: 1:45–3:45 PM. Verify.','venue':'College Quadrangle / Campus Open Playfield — verify','rounds':['Starcourt Mall Clue.','Russian Underground Hunt.'],'rules':'Follow organizer instructions and campus safety rules. Exact route and clue rules are not confirmed in the source.'}
]
TIMELINE = [
('08:30–09:30 AM','Hawkins Security Clearance & Registration Verification','Multipurpose Auditorium Foyer','Inauguration'),('09:30–10:30 AM','Grand Inauguration: Opening the Dimensional Rift','Multipurpose Auditorium','Inauguration'),('10:45 AM–04:30 PM','Vecna’s Paradox — The Grand Ideathon','Old Auditorium Lab','Flagship'),('10:00 AM–01:00 PM','The Cerebro Code (Bug Flayer)','CS Lab 1 & 2, PG Block','Technical'),('10:00 AM–01:00 PM','Hawkins Lab Dossier (Paper Presentation)','Classroom 304, 3rd Floor, Admin Block','Technical'),('10:00 AM–01:00 PM','Web of Vecna (AI Prompt & Web Design)','CS Lab 3, PG Block','Technical'),('01:00–01:45 PM','Surfer Boy Feast (Lunch Break)','Dining Hall & Quadrangle','Break'),('10:00 AM–01:00 PM','The Hellfire Query','CS Lab 3, PG Block','Technical'),('01:45–03:45 PM','Surfer Boy Pitch (Ad-Zap)','Multipurpose Auditorium','Non-technical'),('01:45–03:45 PM','Dungeons & Data (Mystery Treasure Hunt)','Campus Open Playfield','Non-technical'),('01:45–03:45 PM','The Hellfire Boardroom (Corporate Walk)','Classroom 304, 3rd Floor, Admin Block','Non-technical'),('01:45–03:45 PM','The Hawkins AV Archive (Multimedia Storytelling)','CS Lab 3, PG Block','Non-technical'),('01:45–03:45 PM','The Palace Arcade Draft (Franchise Auction)','Multipurpose Auditorium','Non-technical'),('04:45–05:45 PM','Valedictory Ceremony & Vecna Grand Prize Distribution','Multipurpose Auditorium','Valedictory')]
COORDINATORS = [('Dr. J. Princy Merlin','Principal, Bishop Heber College — Patron listing'),('Dr. R. Jemima Priyadarsini','Head & Associate Professor, PG Department of Data Science'),('Dr. A. Selin Vironicka','Association Incharge & Assistant Professor'),('Dr. C. Linda Hepsibha','Organizing Secretary'),('Thirumalai Rajan S','President'),('Balaji G','Secretary'),('Amala Binisha C','Treasurer'),('Kevin Lazarus B','Technical Head — +91 9043558840'),('Abisheik Ruban C','Hospitality Head'),('Rithika M & Rajavignesh P','Event Coordinators'),('Ajay Raam E A','Photography & Media Head')]

def section(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle: st.caption(subtitle)

def event_card(e):
    st.markdown(f'''<div class="panel"><div class="event-code">{e['subtitle'].upper()}</div><div class="event-name">{e['name']}</div><p>{e['description']}</p><p><b>Team:</b> {e['team']}<br><b>Time:</b> {e['time']}<br><b>Venue:</b> {e['venue']}</p></div>''', unsafe_allow_html=True)
    with st.expander(f"View rounds and guidelines — {e['name']}"):
        st.markdown('**Rounds**')
        for r in e['rounds']: st.write('• ' + r)
        st.markdown('**Guidelines**'); st.write(e['rules'])

def save_registration(record):
    exists = REGISTRATION_FILE.exists()
    with REGISTRATION_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(record.keys()))
        if not exists: writer.writeheader()
        writer.writerow(record)

with st.sidebar:
    st.markdown('<div class="eyebrow">Hawkins National Laboratory</div>', unsafe_allow_html=True)
    st.markdown('## 🌀 AF2K27')
    st.caption('When Data Meets the Upside Down')
    page = st.radio('NAVIGATE THE RIFT',['HOME','ABOUT','FLAGSHIP','TECHNICAL EVENTS','NON-TECHNICAL EVENTS','TIMELINE','COORDINATORS','REGISTRATION','CONTACT'])
    st.markdown('---')
    st.markdown('**SYSTEM STATUS**')
    st.markdown('<span class="event-code">SYS_TICK: 1986 // SIGNAL ACTIVE</span>', unsafe_allow_html=True)
    st.caption('Event date and schedule need committee confirmation.')

if page == 'HOME':
    st.markdown('''<div class="hero"><div class="eyebrow">PG Department of Data Science presents</div><div class="hero-title">AnalytixFest<br>2K27</div><div class="hero-tag">WHEN DATA MEETS THE UPSIDE DOWN</div><p style="max-width:760px;margin:1.2rem auto;color:#d8dce5">A Stranger Things-inspired celebration of data science, intelligent systems, creative problem-solving, research, and collaborative competition.</p><div class="eyebrow">National Level Data Science Symposium</div><p style="margin-top:1rem;color:#ffb9bc">Bishop Heber College (Autonomous) · Tiruchirappalli, Tamil Nadu</p></div>''', unsafe_allow_html=True)
    st.write(''); cols=st.columns(4)
    for col,num,label in zip(cols,['01','04','05','₹250*'],['Flagship Ideathon','Technical Events','Non-technical Events','Listed Fee']):
        with col: st.markdown(f'<div class="metric-box"><div class="metric-num">{num}</div><div class="metric-label">{label}</div></div>',unsafe_allow_html=True)
    st.caption('*Fee from the supplied source; reconfirm with organizers.')
    section('Enter the Upside Down','Explore the events, challenge your skills, and follow the signal.')
    a,b=st.columns(2)
    with a: st.markdown('<div class="panel"><div class="event-code">OPERATION UPSIDE DOWN</div><div class="event-name">Vecna’s Paradox</div><p>Context-aware intent reasoning ideathon focused on decision history, strategic intent, and adaptive AI coaching.</p></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="panel"><div class="event-code">HAWKINS CHALLENGE ARCHIVE</div><div class="event-name">Nine Event Realms</div><p>Four technical and five non-technical challenges across coding, research, storytelling, ad-zap, auction strategy and mystery puzzles.</p></div>',unsafe_allow_html=True)
    st.warning('SOURCE CHECK REQUIRED: The exact event date, final timetable, room allocations, registration destination and fee inclusions are not consistently confirmed in the supplied content.')
    st.info('The registration form is a demo and saves locally to CSV; it does not process payments or submit to an official endpoint.')
elif page == 'ABOUT':
    section('About AnalytixFest 2K27','A data science symposium with a retro supernatural mystery atmosphere.')
    st.markdown('<div class="panel"><div class="event-name">PG Department of Data Science</div><p>AnalytixFest 2K27 is described as a National Level Data Science Symposium organized by the PG Department of Data Science at Bishop Heber College (Autonomous), Tiruchirappalli, Tamil Nadu.</p><p>The theme combines an 1980s supernatural-mystery and fictional research-lab atmosphere with data science, intelligent systems, research, creative problem-solving and teamwork.</p></div>',unsafe_allow_html=True)
    section('Visual direction'); st.write('Dark cinematic backgrounds, red neon accents, electric-blue highlights, violet shadows, retro terminal labels, lab dossiers, dimensional-rift imagery and restrained scanline effects.')
    st.write('Palette: #050507 background · #10151C Hawkins night · #090608 Upside Down · #E50914 signal red · #55C8FF electric blue · #7626A8 toxic violet.')
    section('Participant checklist'); st.markdown('- Bring your college ID card.\n- Bring a Bonafide/Permission letter from your HOD or Principal.\n- Formal dress code is stated in the source.\n- Check the final approved schedule, room allocation, event rules and fee inclusions with organizers.')
elif page == 'FLAGSHIP':
    section('Flagship Event','OPERATION UPSIDE DOWN')
    st.markdown('<div class="hero"><div class="eyebrow">The Ultimate Intent-Aware Ideathon</div><div class="hero-title" style="font-size:clamp(1.8rem,4vw,3.4rem)">Vecna’s Paradox</div><div class="hero-tag">Context-Aware Intent Reasoning</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="event-name">Mission Brief</div><p>Build an Intent-Aware Adaptive AI Coach that interprets decisions using accumulated temporal evidence, strategic intent, long-term planning and recurring patterns rather than relying only on static correct/incorrect evaluation.</p><p><b>Team size:</b> 4–5 registered members<br><b>Venue:</b> Old Auditorium Lab<br><b>Schedule:</b> Source conflicts: 10:00 AM–4:00 PM in event data vs 10:45 AM–4:30 PM in timeline. Confirm.</p></div>',unsafe_allow_html=True)
    for title,duration,desc in [('ROUND 01 — Sequential Context Building & Memory Pipeline','90 minutes','Represent decision history using sequential models or temporal-decay memory mechanisms such as LIF/EMA on structured trajectories.'),('ROUND 02 — Dynamic Context Injection & LLM Reasoning','120 minutes','Pass accumulated evidence to an LLM framework to explain intent and recurring strategic mistakes in human-understandable language.'),('ROUND 03 — Strategic Insights Dashboard & Defense','30 minutes','Build a visual UI showing cognitive patterns, planning consistency and conversational feedback for the jury.')]:
        st.markdown(f'<div class="panel"><div class="event-code">{duration}</div><div class="event-name">{title}</div><p>{desc}</p></div>',unsafe_allow_html=True)
    st.write('**Eligibility listed in source:** UG/PG students in Data Science, Computer Science, IT, AI&DS and allied disciplines.')
    st.write('**Preparation:** Bring laptops and required npm/local LLM environments/libraries. Source says challenge parameters are revealed at inauguration; external internet is monitored and pre-built canned solutions may result in disqualification.')
    st.caption('Prize descriptions should be reconfirmed by the organizing committee before advertising.')
elif page == 'TECHNICAL EVENTS':
    section('Technical Events','Four challenges. Debug the signal. Decode the system.')
    for e in TECH_EVENTS: event_card(e)
elif page == 'NON-TECHNICAL EVENTS':
    section('Non-Technical Events','Five creative challenges from the Hawkins archive.')
    for e in NONTECH_EVENTS: event_card(e)
elif page == 'TIMELINE':
    section('Symposium Timeline','Source entries, not a verified final schedule.')
    st.warning('Several entries overlap or conflict with event-detail fields. This page preserves source values rather than guessing corrections.')
    df=pd.DataFrame(TIMELINE,columns=['Time','Event','Venue','Category'])
    cats=st.multiselect('Filter categories',sorted(df.Category.unique()),default=sorted(df.Category.unique()))
    st.dataframe(df[df.Category.isin(cats)],use_container_width=True,hide_index=True)
    st.download_button('Download timeline CSV',df.to_csv(index=False).encode('utf-8'),'analytixfest_timeline_source.csv','text/csv')
elif page == 'COORDINATORS':
    section('Organizing Committee','Names and roles present in the supplied source extraction.')
    st.caption('Some source contact fields are masked or missing, so they are not reproduced as if available.')
    for name,role in COORDINATORS: st.markdown(f'<div class="panel"><div class="event-name">{name}</div><div class="muted">{role}</div></div>',unsafe_allow_html=True)
elif page == 'REGISTRATION':
    section('Register Lab Clearance Pass','Demo form only — confirm the official endpoint and payment process before launch.')
    st.warning('This starter saves submissions to a local CSV file on the machine running Streamlit. It is not a secure production registration system and does not collect payment.')
    with st.form('registration_form',clear_on_submit=True):
        name=st.text_input('Full name *'); email=st.text_input('Email address *'); phone=st.text_input('Mobile number *',help='10-digit Indian mobile number.'); college=st.text_input('College / institution *'); course=st.text_input('Course and year')
        event=st.selectbox('Primary event of interest',['Vecna’s Paradox']+[e['name'] for e in TECH_EVENTS+NONTECH_EVENTS]); team=st.text_input('Team members (if applicable)',placeholder='Separate names with commas'); consent=st.checkbox('I confirm the details are accurate and understand this is a demo form.'); submitted=st.form_submit_button('SUBMIT DEMO REGISTRATION')
    if submitted:
        errors=[]
        if not name.strip(): errors.append('Enter your full name.')
        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+',email.strip()): errors.append('Enter a valid email address.')
        if not re.fullmatch(r'[6-9]\d{9}',re.sub(r'\s+','',phone)): errors.append('Enter a valid 10-digit Indian mobile number.')
        if not college.strip(): errors.append('Enter your college / institution.')
        if not consent: errors.append('Please confirm the consent checkbox.')
        if errors:
            for err in errors: st.error(err)
        else:
            save_registration({'submitted_at':datetime.now().isoformat(timespec='seconds'),'full_name':name.strip(),'email':email.strip(),'phone':re.sub(r'\s+','',phone),'college':college.strip(),'course':course.strip(),'event':event,'team_members':team.strip()})
            st.success('Demo registration saved locally. This is not an official event confirmation.')
            st.info(f'Local file: {REGISTRATION_FILE.name}. Protect this file because it contains personal data.')
elif page == 'CONTACT':
    section('Contact & Location','Contact details extracted from the supplied content.')
    st.markdown('<div class="panel"><div class="event-name">Bishop Heber College (Autonomous)</div><p>PG Department of Data Science<br>Puthur, Tiruchirappalli – 620 017<br>Tamil Nadu, India</p><p><b>Email:</b> analytixfest2k2x@gmail.com<br><b>Helplines listed in source:</b> +91 9043558840 · +91 7010754100</p></div>',unsafe_allow_html=True)
    st.caption('Verify email, helplines and availability with the organizing committee before public release.')
    with st.form('contact_form'):
        st.text_input('Your name'); st.text_input('Your email'); st.text_area('Message'); st.form_submit_button('PREPARE MESSAGE')
    st.info('This contact form is visual/demo only and does not send email. Connect an approved backend or institutional form endpoint before launch.')

st.markdown('---')
st.markdown('<div style="text-align:center;color:#89919d;font-size:.85rem">ANALYTIXFEST 2K27 · PG DEPARTMENT OF DATA SCIENCE · BISHOP HEBER COLLEGE (AUTONOMOUS)<br><span style="font-family:VT323,monospace;color:#FF424A;letter-spacing:.12em">SIGNAL ACTIVE // VERIFY FINAL EVENT DETAILS BEFORE PUBLICATION</span></div>',unsafe_allow_html=True)
