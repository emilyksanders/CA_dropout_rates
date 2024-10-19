### Define the most common "reporting category" prefixes

s = '''RB = African American
RI = American Indian or Alaska Native
RA = Asian
RF = Filipino
RH = Hispanic or Latino
RD = Did not Report
RP = Pacific Islander
RT = Two or More Races
RW = White
GM = Male
GF = Female
GX = Non-Binary Gender (Beginning 2019–20)
GZ = Missing Gender
SE = English Learners
SD = Students with Disabilities
SS = Socioeconomically Disadvantaged
SM = Migrant
SF = Foster
SH = Homeless
GRKN = Kindergarten (GRK prior to 2020–21)
GR13 = Grades 1–3
GR46 = Grades 4–6
GR78 = Grades 7–8
GRK8 = Grades K–8
GR912 = Grades 9–12
CAY = Chronically Absent
CAN = Not Chronically Absent
TA = Total'''

print(s.replace("\n", "\',\n\'").replace(" = ", "\': \'"))

default_suffixes = {'RB': 'black',
'RI': 'native',
'RA': 'asian',
'RF': 'filipino',
'RH': 'latine',
'RD': 'no_race',
'RP': 'pacific',
'RT': 'mutli_race',
'RW': 'white',
'GM': 'male',
'GF': 'female',
'GX': 'nonbin',
'GZ': 'no_gender',
'SE': 'esl_ell',
'SD': 'disabled',
'SS': 'poor',
'SM': 'migrant',
'SF': 'foster',
'SH': 'homeless',
'GRKN': 'gr_k',
'GR13': 'gr_1–3',
'GR46': 'gr_4–6',
'GR78': 'gr_7–8',
'GRK8': 'gr_K–8',
'GR912': 'gr_9–12',
'CAY': 'chron_absent',
'CAN': 'not_chron_absent',
'TA': 'total'}

