from crewai.tools.structured_tool import CrewStructuredTool
from crewai.tools import tool
from pydantic import BaseModel
import requests
import urllib.parse
import os

@tool
def duke_event_api_tool(future_days: int):
    '''
    Calls the Duke Events API

    Parameters:
        future_days (int): future days to look ahead for events

    Returns:
        A Python dictionary of the following format:

        {
        "events": [
            {
            "id": "CAL-8a000483-92c3adf6-0194-dd19428a-000027cfdemobedework@mysite.edu",
            "start_timestamp": "2025-04-25T04:00:00Z",
            "end_timestamp": "2025-04-27T04:00:00Z",
            "summary": "Duke Datathon",
            "description": "Join us at the Duke Health IPEC Building for an exciting weekend focused on \"Data Science in Critical/Acute Care.\" The event kicks off with a symposium on Friday, April 25, followed by a two-day datathon where clinicians and data scientists collaborate to develop data-driven models using de-identified critical care datasets. No prior experience is required, and teams will be formed to blend clinical and data science expertise. Early registration (through Feb. 28) starts at $50 for trainees and $200 for faculty or industry participants. Registration fees increase on March 1. Sponsorship opportunities are also available.",
            "status": "CONFIRMED",
            "sponsor": "AI Health",
            "co_sponsors": [
                "+DataScience (+DS)",
                "Biomedical Engineering (BME)",
                "Biostatistics and Bioinformatics",
                "Center for Computational Thinking",
                "Computer Science",
                "Department of Medicine",
                "DHTS Web Services",
                "Electrical and Computer Engineering (ECE)",
                "Pratt School of Engineering"
            ],
            "location": {
                "address": "311 Trent Drive, Durham, NC 27710"
            },
            "contact": {
                "name": "A. Ian WONG, MD, PhD",
                "email": "a.ian.wong@duke.edu"
            },
            "categories": null,
            "link": "https://calendar.duke.edu/show?fq=id:CAL-8a000483-92c3adf6-0194-dd19428a-000027cfdemobedework@mysite.edu",
            "event_url": "https://sites.duke.edu/datathon2025/",
            "submitted_by": [
                "tmt26"
            ]
            }
        ]
        }
    '''

     # Construct the URL with the future_days parameter
    url = f'https://calendar.duke.edu/events/index.json?&gfu[]=AI%20Health&future_days={future_days}&feed_type=simple'
    
    print(f'Calling the API with {future_days} future days')
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON body from the response
    else:
        raise Exception(f"Error fetching data from API: {response.status_code} - {response.text}")


@tool
def duke_course_api_tool(subject: str):
    '''
    Calls the Duke Course API with a given subject. Valid subject values are

AAAS - African & African Amer Studies
AADS - Asian American and Diaspora St
ACCOUNTG - Accounting
ADF - American Dance Festival
AEROSCI - Aerospace Studies-AFROTC
AIPI - AI for Product Innovation
AMES - Asian & Middle Eastern Studies
AMXTIAN - American Christianity
ANATOMY - Anatomy
ANESTH - Anesthesiology
ARABIC - Arabic
ARTHIST - Art History
ARTS&SCI - Arts and Science IDEAS themes
ARTSVIS - Visual Arts
ASEP - Anesthesiol, Surg & Envtl Phys
ASL - American Sign Language
BA - Business Administration
BALTFIN - Balto-Finnic
BCS - Black Church Studies
BES - BioMed Engineering and Surgery
BIOCHEM - Biochemistry
BIOETHIC - Bioethics and Science Policy
BIOLOGY - Biology
BIOSTAT - Biostatistics
BIOTRAIN - Biomedical Research Training
BME - Biomedical Engineering
BRAINSOC - Brain & Society
BSP - Behavioral Neuro Study Program
CARDULTR - Cardiac Ultrasound
CBB - Computational Bio  Bioinformat
CEE - Civil and Environmental Egr
CELLBIO - Cell Biology
CESC - Civic Engagement&Social Change
CFM - Community & Family Medicine
CHEM - Chemistry
CHEROKEE - Cherokee Language
CHILDPOL - Child Policy
CHINESE - Chinese
CHURHST - Church History
CHURMIN - Church Ministry
CIF - Colloquia/Interfield/Field Edu
CINE - Cinematic Arts
CLP - Clinical Leadership Program
CLST - Classical Studies
CMAC - Cmputnl Media, Arts & Cultures
CMB - Cell and Molecular Biology
COMMFAM - Community and Family Medicine
COMPSCI - Computer Science
CONTDIV - Continuation - Divinity
CONTENV - Continuation-Completion(NSOE)
CONTNUR - Course Continuation - Nursing
CONTPPS - Course Continuation - PPS
CPE - Clinical Pastoral Education
CREOLE - Creole
CRP - Clinical Research Training Prg
CRS - Continuation of Enrollment
CRSP - Clinical Research Study Prog
CTN - Continuation - Graduate School
CULANTH - Cultural Anthropology
CVS - Cardiovascular Study Program
CYBERSEC - Cybersecurity
DANCE - Dance
DECISION - Decision Sciences
DECSCI - Decision Sciences Program
DERMATOL - Dermatology
DESIGNTK - Design & Technology Innovation
DIVINITY - Divinity
DMNISTRY - Doctor of Ministry
DOCST - Documentary Studies
DSCB - Developmental & Stem Cell Bio
EAS - East Asian Studies
ECE - Electrical & Computer Egr
ECON - Economics
ECS - Earth and Climate Sciences
EDUC - Education
EGR - Engineering
EGRCOOP - Engineering Co-op
EGRMGMT - Engineering Management
EHD - Education and Human Developmnt
EMERGMED - Emergency Medicine
ENERGY - Energy
ENGLISH - English
ENR - Enrollment Fee
ENRGYEGR - Energy Engineering
ENRGYENV - Energy & Environment
ENTREPRN - Entrepreneurship & Innovation
ENVIRON - Environment
EOS - Earth & Ocean Sciences
EPH - Epidemiology & Public Health
ETHICS - Study of Ethics
EVANTH - Evolutionary Anthropology
EXP - Study Away
FECON - Financial Economics
FIELDEDU - Field Education
FINANCE - Finance
FINTECH - Financial Technology
FMKT - Financial Markets
FOCUS - Focus
FRENCH - French
FUQINTRD - Interdisciplinary
GAMEDSGN - Game Design and Development
GATE - Global Academic Travel Exp
GENOME - Genome Sciences and Policy
GEOADMIN - Global Education Admn Use Only
GERMAN - German
GGS - Global Gender Studies
GHS - Global Health Study Program
GLHLTH - Global Health
GREEK - Greek
GS - Graduate Studies
GSF - Gender Sexuality & Feminist St
HCVIS - Historical&Cultural Visualiztn
HEBREW - Hebrew
HGP - Human Genetics Study Program
HINDI - Hindi
HISTORY - History
HISTREL - History of Religion
HISTTHEO - Historical Theology
HLTHMGMT - Health Sector Management
HLTHPOL - Health Policy
HLTHSCI - Health Sciences
HOUSECS - House Course
HSP - Hispanic Summer Program
HUNGARN - Hungarian
I&E - Innovation & Entrepreneurship
IAD - INDEPEN. ACADEMIC DEVELOPMENT
ICS - Internatl Comparative Studies
IDS - Interdisciplinary Data Science
IMMUNOL - Immunology
IMPINV - Initiative on Impact Investing
INCC_CHE - Chemistry
INCC_PHS - Public Health Sciences
INCC_PHY - Physics
INCG_CTR - COMM THERAP/RECREATION STUD
INCG_HDF - Human Dev/Fam Studies
INCG_MAS - Master of Applied Arts/Science
INCG_MUP - Musical Performance
INCG_PHY - Physics
INCG_REL - Religious Studies
INCG_SWK - Social Work
INCH_AAD - Afri, Afri-Amer, Diaspora Stds
INCH_AHS - Allied Health Sciences
INCH_ANT - Anthropology
INCH_APL - Applied Sciences
INCH_ARB - Arabic
INCH_ARH - Art History
INCH_ASA - Asian Studies
INCH_AST - American Studies
INCH_ASY - Astronomy
INCH_BIO - Biology
INCH_BME - Biomedical Engineering
INCH_BST - Biostatistics
INCH_BUS - Business
INCH_CHM - Chemistry
INCH_CHN - Chinese
INCH_CHR - Cherokee
INCH_CLR - Classical Archaeology
INCH_CMM - Communication Studies
INCH_CMP - Comparative Literature
INCH_COM - Computer Science
INCH_DRA - Drama
INCH_DTH - Dutch
INCH_ECO - Economics
INCH_EDU - Education
INCH_EME - Earth, Marine and Env Sci
INCH_ENG - English
INCH_ENV - Environmental Sciences
INCH_EPD - Epidemiology
INCH_EXS - Exercise and Sport Science
INCH_FOL - Folklore
INCH_FRN - French
INCH_GBS - Global Studies
INCH_GEG - Geography
INCH_GEO - Geology
INCH_GER - German
INCH_GNT - GENETICS & MOLECULAR BIOLOGY
INCH_GRK - Greek
INCH_HBH - Health Behavior &  Education
INCH_HNU - Hindi-Urdu
INCH_HPM - Health Policy And Management
INCH_HST - History
INCH_ITA - Italian
INCH_JPN - Japanese
INCH_JWS - Jewish Studies
INCH_LAW - Law
INCH_LIN - Linguistics
INCH_LTN - Latin
INCH_MAC - Master of Accounting
INCH_MAS - Marine Science
INCH_MAT - Mathematics
INCH_MBA - Master of Business Admin
INCH_MCB - Microbiology
INCH_MEJ - Media & Journalism
INCH_MHC - Maternal and Child Health
INCH_MUS - Music
INCH_NBI - Neurobiology
INCH_NTR - Nutrition
INCH_NUR - Nursing
INCH_PHL - Philosphy
INCH_PHY - Physics
INCH_PLH - Polish
INCH_PLN - Planning
INCH_PLY - Public Policy
INCH_POL - Political Science
INCH_POR - Portuguese
INCH_PRN - Persian
INCH_PSY - Psychology
INCH_PUA - Public Administration
INCH_PUH - Public Health
INCH_PWD - Peace War & Defense
INCH_REL - Religion
INCH_ROM - Romance Languages
INCH_SOC - Sociology
INCH_SOW - Social Work
INCH_SPA - Spanish
INCH_SPH - Speech & Hearing Sciences
INCH_STR - Stats & Operations Research
INCH_SWA - Swahili
INCH_VIT - Vietnamese
INCS_AEC - Applied Ecology
INCS_AEE - Evaluation in Agricultural Ed
INCS_ANS - Animal Science
INCS_ARC - Architecture
INCS_BAE - BIOLOGICAL & AGRIC ENGINEERING
INCS_BIO - Biological Sciences
INCS_CE - Civil Engineering
INCS_CH - Chemistry
INCS_CS - Crop Science
INCS_CSC - Computer Science
INCS_EAC - Adult & Higher Education
INCS_ECG - Economics (Graduate)
INCS_ED - EDUCATION
INCS_ENT - Entomology
INCS_FB - Forest Biomaterials
INCS_FOR - Forestry
INCS_FTM - Fashion and Textile Management
INCS_FW - Fisheries & Wildlife Sciences
INCS_GD - Graphic Design
INCS_GIS - Geographic Info Systems
INCS_GN - Genetics
INCS_HEA - Health Exercise Aquatics
INCS_HI - History
INCS_HOR - Horticulture
INCS_LAR - Landscape Architecture
INCS_LAT - Latin
INCS_LOG - Logic
INCS_MA - Mathematics
INCS_MAE - Mechanical & Aerospace Egr
INCS_MB - Microbiology
INCS_MEA - Marine,Earth,& Atmospheric Sci
INCS_PA - Public Administration
INCS_PRT - Parks, Rec &Tourism Management
INCS_PS - Political Science
INCS_PSY - Psychology
INCS_PY - Physics
INCS_SOC - Sociology
INCS_SSC - Soil Science
INCS_ST - Statistics
INCS_TT - Textile Technology
INCS_TTM - Textile Technology Management
INCU_APP - Applied Music
INCU_BIO - Biology
INCU_CHM - Chemistry
INCU_CRJ - Criminal Justice
INCU_CTX - Clothing and Textiles
INCU_EAS - Earth Science
INCU_ECO - Economics
INCU_FDN - Foods & Nutrition
INCU_KIN - Kinesiology and Exercise Sci
INCU_LAW - Law
INCU_MAT - Mathematics
INCU_PHY - Physics
INCU_PSY - Psychology
INCU_SPA - SPANISH
INTERDIS - Interdisciplinary
ISS - Information Science + Studies
ITALIAN - Italian
JAM - Journalism & Media
JEWISHST - Jewish Studies
JGER_BCS - Bosnian/ Croatian/ Serbian
JGER_CPL - Comparative Literature
JGER_ENG - English
JGER_FRE - French
JGER_GER - German
JGER_JWS - Jewish Studies
JGER_LAT - Latin
JGER_MUS - MUSIC
JGER_ROM - ROM ST
JGER_SLV - Slavic Languages
JPN - Japanese
KICHE - K'iche' Maya
KOREAN - Korean
K_ARABIC - Arabic
K_ARHU - Arts and Humanities
K_ARTS - Arts
K_BHVSCI - Behavioral Science
K_BIOL - Biology
K_CAPST - Capstone
K_CHEM - Chemistry
K_CHN - Chinese
K_CHSC - Chinese Society and Culture
K_CMPDSG - Computer Design
K_CMPSCI - Computer Science
K_CULANT - Cultural Anthropology
K_CULMVE - Cultures and Movements
K_DATASC - Data Science
K_DKU - DKU
K_EAP - English for Academic Purposes
K_ECE - Electrical and Computer Engine
K_ECON - Economics
K_ENVIR - Environment
K_ETHLDR - Ethics and Leadership
K_FRENCH - French
K_GCHINA - Global China Studies
K_GCULS - Global Cultural Studies
K_GEN - General Electives
K_GERMAN - German
K_GLHLTH - Global Health
K_GLOCHA - Global Challenges in Sci
K_HIST - History
K_I&E - Innovation
K_INDSTU - Independent Study
K_INFOSC - Information Sciences
K_INSGOV - Institutions and Governance
K_INTGSC - Integrated Science
K_ITAL - Italian
K_JAPN - Japanese
K_KOREAN - Korean
K_LATIN - Latin
K_LIT - Literature
K_MATH - Mathematics
K_MATSC - Material Science
K_MEDART - Media and Arts
K_MEDIA - Media
K_MEDPHY - Medical Physics
K_MILSCI - Military Science
K_MMS - Markets and Management
K_MONG - Mongolian
K_MUSIC - Music
K_NEURSC - Neuroscience
K_PHIL - Philosophy
K_PHYEDU - Physical Education
K_PHYS - Physics
K_POLECO - Political Economy
K_POLSCI - Political Science
K_PSYCH - Psychology
K_PUBPOL - Public Policy
K_REG - Dual-Enrollment at DKU
K_RELIG - Religious Studies
K_RINDST - Research Independent Study
K_SOCIOL - Sociology
K_SOSC - Social Science
K_SPAN - Spanish
K_STATS - Statistics
K_TBTN - Tibetan
K_TLANG - Third Language
K_USTUD - US Studies
K_WOC - Written and Oral Communication
LATAMER - Latin American Studies
LATIN - Latin
LAW - Law
LINGUIST - Linguistics
LIT - Literature
LS - Liberal Studies
LSGS - Latino Studies Global South
LTS - Liturgical Studies
MALAGASY - Malagasy
MANAGEMT - Management
MARKETNG - Marketing
MARSCI - Marine Science Conservation
MAT - Master of Arts in Teaching
MATH - Mathematics
ME - Mechanical Engr/Materials Sci
MEDHUM - Medical Humanities Study Progr
MEDICINE - Medicine
MEDPHY - Medical Physics
MEDREN - Medieval and Renaissance
MENG - Master of Engineering
MERP - Medical Education Research Prg
MFAEDA - MFA in Experimental & Doc Arts
MGM - Molec Genetics & Microbiology
MGMTCOM - Management Communications
MGRECON - Economics
MIDIP - MIDIP
MILITSCI - Military Science (Army ROTC)
MMCI - Mstrs in Manage in Cln Info
MMS - Markets and Management Studies
MOLCAN - Molecular Cancer Biology
MOLMED - Molecular Medicine
MSEG - Materials Science & Engineerng
MSIS - M of Sci of Info Sci Study Pro
MSLS - M of Sci of Lib Sci Study Pro
MUSIC - Music
NANOSCI - Nanosciences
NAVALSCI - Naval Science (Navy ROTC)
NCS - Nonlinear and Complex Systems
NEURO - Neurology
NEUROBIO - Neurobiology
NEUROSCI - Neuroscience
NEUROSUR - Neurosurgery
NEWTEST - New Testament
NSS - Neurosciences Study Program
NURSING - Nursing
OBGYN - Obstetrics and Gynecology
OLDTEST - Old Testament
OPERATNS - Operations
OPHTHAL - Ophthalmology
OPTECH - Ophthalmic Medical Technician
OPTRS - Optional Research Studies
ORTHO - Orthopaedics
OT-D - Occupational Therapy-Doctorate
OTOLARYN - Otolaryngology
OVS - Ophthalmology/Visual Sci St Pr
PARISH - Care of Parish
PASTCARE - Pastoral Care
PATHASST - Pathologist's Assistant Progr
PATHOL - Pathology
PCLT - Primary Care Leadership Track
PEDS - Pediatrics
PERSIAN - Persian
PHARM - Pharm and Cancer Biology
PHIL - Philosophy
PHOTO - Photography
PHSR - Pop Hlth Science Research
PHYASST - Physician Assistant Program
PHYSEDU - Physical Education
PHYSICS - Physics
PJMS - Policy Journalism and Media St
POE - Practice-Oriented Education
POLISH - Polish
POLSCI - Political Science
POPHS - Population Health Sciences
PORTUGUE - Portuguese
PREACHNG - Preaching
PSC - Psychiatry
PSP - Pathology Study Program
PSY - Psychology
PSYCHTRY - Psychiatry
PT-D - Physical Therapy - Doctorate
PTH - Pathology
PUBPOL - Public Policy
QM - Quantitative Management
QUECHUA - Quechua
RACESOC - Race & Society
RAD - Radiology
RADIOL - Radiology
RADONC - Radiation Oncology
REG - Registration
RELIGION - Religion
RESEARCH - Research
RIGHTS - Human Rights
ROBT_AAD - Afri, Afri-Amer, Diaspora Stds
ROBT_AMT - American Studies
ROBT_ANT - Anthropology
ROBT_ARB - Arabic
ROBT_ARH - Art History
ROBT_ASA - Asian Studies
ROBT_AST - Astronomy
ROBT_BIO - Biology
ROBT_BST - Biostatistics
ROBT_BUS - Business
ROBT_CHM - Chemistry
ROBT_CHN - Chinese
ROBT_CHR - CHEROKEE
ROBT_CML - Comparative Literature
ROBT_COM - Communications
ROBT_CPS - Computer Science
ROBT_DRA - Drama
ROBT_ECO - Economics
ROBT_EDU - Education
ROBT_ENE - Environment & Ecology
ROBT_ENG - English
ROBT_ENV - Environment Sciences
ROBT_EPD - Epidemiology
ROBT_ESS - Exercise and Sport Science
ROBT_FOL - Folklore
ROBT_FRE - French
ROBT_GBS - Global Studies
ROBT_GEG - Geography
ROBT_GEO - Geology
ROBT_GRM - German
ROBT_HBH - Health Behavior &  Education
ROBT_HEB - Hebrew
ROBT_HNR - Honors
ROBT_HNU - Hindi/Urdu
ROBT_HPM - Health Policy & Management
ROBT_HST - History
ROBT_IDS - Inter-disciplinary Studies
ROBT_ILS - Information & Library Science
ROBT_ITA - Italian
ROBT_JPN - Japanese
ROBT_KOR - Korean
ROBT_MEJ - Media and Journalism
ROBT_MGT - Social Relations in Workplace
ROBT_MTH - Math
ROBT_MUS - Music
ROBT_NSC - NEUROSCIENCE
ROBT_NTR - Health Nutrition
ROBT_PBH - Public Health
ROBT_PHA - Physical Activities
ROBT_PHL - Philosophy
ROBT_PHY - Physics
ROBT_PLN - City and Regional Planning
ROBT_POL - Political Science
ROBT_PRS - Persian
ROBT_PSY - Psychology
ROBT_PUB - Public Policy
ROBT_PWD - Peace, War, & Defense
ROBT_REL - Religion
ROBT_RUS - Russian
ROBT_SOC - Sociology
ROBT_SPA - Spanish
ROBT_SPC - Exp & Spl Studies
ROBT_SPH - Speech & Hearing Sciences
ROBT_STR - Stats & Oprtns Resrch
ROBT_SWA - Swahili
ROBT_WGS - Women's and Gender Studies
ROMST - Romance Studies
RROMP - Radiology, RadOnc & Med Physic
RUSSIAN - Russian
SANSKRIT - Sanskrit
SBB - Structural Bio & Biophysics
SCISOC - Science & Society
SERBCRO - Serbian and Croatian
SES - Slavic and Eurasian Studies
SOCENT - Social Entrepreneurship
SOCIOL - Sociology
SPANISH - Spanish
SPIRIT - Spirituality
STA - Statistical Science
STDYAWAY - Study Away
STRATEGY - Strategy
SURGERY - Surgery
SUSTAIN - Sustainability Engagement
SWAHILI - Swahili
SXL - Study of Sexualities
SYSEGR - Systems Egr for Autonomy
SYSENG - Systems Engineering
THEATRST - Theater Studies
THESIS - Thesis
TIBETAN - Tibetan
TURKISH - Turkish
UKRAIN - Ukrainian
UNIV - University Course
UPE - University Program in Ecology
UPGEN - University Program in Genetics
URDU - Urdu
UROLOGY - Urology
VMS - Visual and Media Studies
WRITING - Writing
WXTIAN - World Christianity
XTIANEDU - Christian Education
XTIANETH - Christian Ethics
XTIANPRC - Christian Practice
XTIANSTU - Christian Studies
XTIANTHE - Christian Theology
ZZZ - Duke Equivalent Transfer Cred

    Parameters:
        subject (string): subject

    Returns:
        A Python dictionary of the following format:

        {
  "ssr_get_courses_resp": {
    "course_search_result": {
      "ssr_crs_gen_msg": null,
      "ssr_crs_srch_count": "18",
      "subjects": {
        "subject": {
          "institution": "DUKEU",
          "institution_lov_descr": "Duke University",
          "subject": "AIPI",
          "subject_lov_descr": "AI for Product Innovation",
          "subject_crs_count": "18",
          "course_summaries": {
            "course_summary": [
              {
                "crse_id": "027568",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 501",
                "course_title_long": "AIPI Seminar",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027569",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 502",
                "course_title_long": "AIPI Workshops",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027560",
                "crse_id_lov_descr": null,
                "effdt": "2021-05-01",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 503",
                "course_title_long": "Python Bootcamp",
                "ssr_crse_typoff_cd": "OCCASIONAL",
                "ssr_crse_typoff_cd_lov_descr": "Occasionally",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027566",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 504",
                "course_title_long": "Introductory Residency",
                "ssr_crse_typoff_cd": "FALL",
                "ssr_crse_typoff_cd_lov_descr": "Fall Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027565",
                "crse_id_lov_descr": null,
                "effdt": "2022-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 505",
                "course_title_long": "Mid-Program Residency",
                "ssr_crse_typoff_cd": null,
                "ssr_crse_typoff_cd_lov_descr": null,
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027564",
                "crse_id_lov_descr": null,
                "effdt": "2023-05-01",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 506",
                "course_title_long": "Concluding Residency",
                "ssr_crse_typoff_cd": "OCCASIONAL",
                "ssr_crse_typoff_cd_lov_descr": "Occasionally",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027038",
                "crse_id_lov_descr": null,
                "effdt": "2020-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 510",
                "course_title_long": "Sourcing Data for Analytics",
                "ssr_crse_typoff_cd": "FALL",
                "ssr_crse_typoff_cd_lov_descr": "Fall Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027039",
                "crse_id_lov_descr": null,
                "effdt": "2023-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 520",
                "course_title_long": "Modeling Process and Algorithms",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027040",
                "crse_id_lov_descr": null,
                "effdt": "2022-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 530",
                "course_title_long": "Optimization in Practice",
                "ssr_crse_typoff_cd": "FALL",
                "ssr_crse_typoff_cd_lov_descr": "Fall Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "028750",
                "crse_id_lov_descr": null,
                "effdt": "2023-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 531",
                "course_title_long": "Deep Reinforcement Learning Applications",
                "ssr_crse_typoff_cd": "FALL",
                "ssr_crse_typoff_cd_lov_descr": "Fall Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027041",
                "crse_id_lov_descr": null,
                "effdt": "2023-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 540",
                "course_title_long": "Deep Learning Applications",
                "ssr_crse_typoff_cd": "SPRING",
                "ssr_crse_typoff_cd_lov_descr": "Spring Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027563",
                "crse_id_lov_descr": null,
                "effdt": "2025-01-01",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 549",
                "course_title_long": "Capstone Practicum 1",
                "ssr_crse_typoff_cd": "SPRING",
                "ssr_crse_typoff_cd_lov_descr": "Spring Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027042",
                "crse_id_lov_descr": null,
                "effdt": "2025-05-01",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 560",
                "course_title_long": "Legal, Societal, and Ethical Implications of AI",
                "ssr_crse_typoff_cd": "SU ONLY",
                "ssr_crse_typoff_cd_lov_descr": "Summer Only",
                "msg_text": "** available as of 2025-05-01",
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027042",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 560",
                "course_title_long": "Legal, Societal, and Ethical Implications of AI",
                "ssr_crse_typoff_cd": "SU ONLY",
                "ssr_crse_typoff_cd_lov_descr": "Summer Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027043",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 561",
                "course_title_long": "Operationalizing AI",
                "ssr_crse_typoff_cd": "SU ONLY",
                "ssr_crse_typoff_cd_lov_descr": "Summer Only",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027570",
                "crse_id_lov_descr": null,
                "effdt": "2024-01-01",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 590",
                "course_title_long": "Advanced Topics in AI for Product Innovation",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027571",
                "crse_id_lov_descr": null,
                "effdt": "2021-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 590L",
                "course_title_long": "Advanced Topics in AI for Products Innovation (with Lab)",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              },
              {
                "crse_id": "027567",
                "crse_id_lov_descr": null,
                "effdt": "2024-08-15",
                "crse_offer_nbr": "1",
                "institution": "DUKEU",
                "institution_lov_descr": "Duke University",
                "subject": "AIPI",
                "subject_lov_descr": "AI for Product Innovation",
                "catalog_nbr": " 591",
                "course_title_long": "Special Readings in AI for Product Innovation",
                "ssr_crse_typoff_cd": "FALL-SPRNG",
                "ssr_crse_typoff_cd_lov_descr": "Fall and/or Spring",
                "msg_text": null,
                "multi_off": "N",
                "crs_topic_id": "0",
                "course_off_summaries": null
              }
            ]
          }
        }
      }
    },
    "@xmlns": "http://xmlns.oracle.com/Enterprise/Tools/services"
  }
}

    '''

     # Construct the URL with the subject parameter
    url = f'https://streamer.oit.duke.edu/curriculum/courses/subject/{urllib.parse.quote(subject)}?access_token={os.getenv("DUKE_API_KEY")}'
    
    print(f'Calling the API with {subject} subject')
    
    # Make the GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON body from the response
    else:
        raise Exception(f"Error fetching data from API: {response.status_code} - {response.text}")




# # Define the schema for the tool's input using Pydantic
# class APICallInput(BaseModel):
#     endpoint: str
#     parameters: dict

# # Wrapper function to execute the API call
# def tool_wrapper(*args, **kwargs):
    
#     # For demonstration, we'll return a placeholder string
#     return f"Call the API at {kwargs['endpoint']} with parameters {kwargs['parameters']}"

# # Create and return the structured tool
# def create_structured_tool():
#     return CrewStructuredTool.from_function(
#         name='Wrapper API',
#         description="A tool to wrap API calls with structured input.",
#         args_schema=APICallInput,
#         func=tool_wrapper,
#     )

# # Example usage
# structured_tool = create_structured_tool()

# # Execute the tool with structured input
# result = structured_tool._run(**{
#     "endpoint": "https://calendar.duke.edu/events/index.json?&gfu[]=Academic%20Resource%20Center%20%28ARC%29&future_days=45&feed_type=simple",
#     "parameters": {"events": []}
# })
# print(result)  # Output: Call the API at https://example.com/api with parameters {'key1': 'value1', 'key2': 'value2'}