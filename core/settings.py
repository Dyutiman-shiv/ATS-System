
HIREQ_SOCIAL_LINKS = {'fb':'https://www.facebook.com/HireQ-102512068424717',
                         'in':'https://www.linkedin.com/company/71023652/',
                         'tw':'https://twitter.com/hireq',
                      'insta':'https://instagram.com/hireq',}
REG_EXPIRY_DAYS = 3
HQ_ADDRESS1 = '5th Main, HSR Layout'
HQ_ADDRESS2 = 'Bangalore, 560102, IN'
YEAR = '2021'

FIELD_LENGTHS = {'name': 128,
                 'mobile': 16,
                 'designation': 128,
                 'pub_id': 32,
                 'street': 128,
                 'city': 64,
                 'zip': 16,
                 'short_comment': 256,
                 'long_comment': 1024}

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'OTHER'))

COUNTRY_CODES = (('IN', 'India'),
                 ('US', 'United States'))

COUNTRY_CODES_REGISTER = (('IN', '🇮🇳 India(+91)'),
                          ('US', '🇺🇸 US(+1)'))

JOB_TYPES = (('FTE', 'Full Time/ Permanent'),
                ('CONT', 'Fixed Term/ Contract'),
                ('CONS', 'Consultant/ Self-Employed'),
                ('INT', 'Intern'),)
USER_TYPES = (('CAND', 'Candidate'),
              ('MINER', 'Miner'),
              ('COMP', 'Company'))

RES_TEMP_NAMES = ['hq001','hq002','hq003','hq004']


JOB_APPLICATION_STAGE = (('APP', 'Application'),
                         ('SCREEN', 'Screening'),
                         ('OFFER','Offer'),
                         ('JOIN', 'Joining'))

JOB_APPLICATION_STATUS = (('APP','Applied'),
                          ('1ST_SCH', '1st round scheduled'),
                          ('1ST_COM', '1st round completed'),
                          ('CLI_SCH', 'Client interview scheduled'),
                          ('CLI_COM', 'Client interview completed'),
                          ('1ST_REJ', 'First round reject'),
                          ('CLI_REJ', 'Client round reject'),
                          ('TBS', 'To be scheduled'),
                          ('NR', 'Not reachable'),
                          ('REJ', 'Rejected'),
                          ('NO_SHOW', 'No show'),
)

MONTH_NAMES = ((1,"January"),
               (2,"February"),
               (3,"March"),
               (4,"April"),
               (5,"May"),
               (6,"June"),
               (7,"July"),
               (8,"August"),
               (9,"September"),
               (10,"October"),
               (11,"November"),
               (12,"December"),)

DEFAULT_TEMPLATE_ID = 1  # Replace with the actual ID of a template in your core_pdf_template table, this is to have no hiccups in the flow of registration. 

RELOCATE_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ] 