# Imports
import pandas as pd
import os

os.getcwd()

# Read in data
enroll = pd.read_csv(
  '02_data/eks_new/school_enrollment_county_district_school_race_gender_14-16.txt', 
  sep='\t', na_values = '*', encoding_errors='replace')
enroll.shape

# Make a copy of the column names
orig_names = list(enroll.columns)

# Rename columns
enroll.columns = [
  f"{x.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__enrolled_14-16" 
  for x in enroll.columns]
enroll.columns

# Narrow down 

# district-level, charter-nonspecific, DASS-nonspecific

enroll.loc[:, 'eks_districts__enrolled_14-16'] = enroll.loc[:, 'cds_code__enrolled_14-16'].astype(str).str[:7]
# test
enroll.loc[100000, 'cds_code__enrolled_14-16']
enroll.loc[100000, 'eks_districts__enrolled_14-16']

# drop annoying columns
drop_cols = ['cds_code__enrolled_14-16',
  'county__enrolled_14-16', 'district__enrolled_14-16']

enroll.shape
enroll.drop(columns = drop_cols).shape
enroll.drop(columns = drop_cols, inplace = True)
enroll.shape

# aggregate
dist_enroll = enroll.groupby(['eks_districts__enrolled_14-16', 
  'enr_type__enrolled_14-16', 'race_ethnicity__enrolled_14-16', 
  'gender__enrolled_14-16', 'academic_year__enrolled_14-16'], 
  as_index = False).aggregate('sum')

# Let's see
enroll.shape
enroll['school__enrolled_14-16'].nunique()
enroll['school__enrolled_14-16'].value_counts(dropna = False)

enroll['academic_year__enrolled_14-16'].value_counts(dropna = False)

# I think what we're going to want to do here is like

for i in columns:
  # if data[i]== the name of the school:
  #   delete the column, who cares
#   if (data[i].nunique() > 1) and 
#   (data[i].nunique() < (0.5*data.shape[1])) and
#   (data[i].dtype != 'numeric'):
#     #split it up into columns



# Let's see how many things per thing we have
for i in list(enroll.columns):
  print(i)
  print(f'unique: {enroll[i].nunique()}')
  print(f'NAs: {enroll[i].isna().sum()}') 
    # after dropping to D, all 0s except school name
  print('')


enroll.info()

# for i in list(enroll.columns):
#   try:
#     enroll['average_days_enroll__enrolled_14-16'] = pd.to_numeric(enroll['average_days_enroll__enrolled_14-16'], errors='ignore')
#   except:
#     pass
# enroll.dtypes

# reporting categories

# define some time-savers
cats_col = 'reporting_category__enrolled_14-16'
cats_list = list(enroll[cats_col].unique())
a = enroll[cats_col]
district = 'district_code__enrolled_14-16'
subs = []

for i in cats_list:
  if i=='TA':
    print(f"enroll_{i} = enroll.loc[enroll[a=='{i}'].index, :]")
  else:
    print(f"enroll_{i} = enroll.loc[enroll[a=='{i}'].index, split_cols]")
  
for i in cats_list:
  print(f"subs.append(enroll_{i})")



# make sure we got all the rows

for i, j in list(zip(cats_list, subs)):
  print(f"""
  {'='*20}
  {i}
  {'-'*20}
  """)
  if (enroll[a==i].shape[0])==(j.shape[0]):
    print(f'Caught all rows.')
  else:
    print(f"""
Did not catch all rows. 
Original is {enroll[a==i].shape[0]}); reduced is {j.shape[0]}.
""")
  if ((j[district].nunique())/(j.shape[0]))==1:
    print('One row per district.')
  elif ((j[district].nunique())/(j.shape[0]))<1:
    print('Multiple rows per district.')
  else:
    print("Help!  The math ain't mathin'!")

# I don't think I need to rename them or drop the reporting category column.
# I think I can just merge with a suffix and then use a list comp to drop.

# create a df with "placeholder" columns to force pd.merge to put
# a suffix on every single merged-in column 
# (it was previously skipping the first ones, because they were unique)
enroll_remade = pd.DataFrame(
  columns = [
    
    ])

# put in the district codes, to match on
enroll_remade['district_code__enrolled_14-16'] = list(enroll['district_code__enrolled_14-16'].unique())

# do some checks
enroll_remade.shape # (1010, 1)
enroll_remade.isna().sum()

# these names are too long
d = 'district_code__enrolled_14-16'

# for every sub-df, generate suffixes and merge it in
for i, j in list(zip(subs, cats_list)):
  # print(f'{j}: {i[cats_col].unique()}')
  k = f'_{j}'
  enroll_remade = enroll_remade.merge(
    i, on = d, how = 'left', suffixes=(None, k))
enroll_remade.shape # (1010, a lot)

blank_col_names = []

enroll_remade.drop(columns = blank_col_names).shape
enroll_remade.drop(columns = blank_col_names, inplace = True)
enroll_remade.shape

# get rid of the reporting category columns
rc_cols = [a for a in enroll_remade.columns if a.split('__')[0]=='reporting_category']
enroll_remade.drop(columns = rc_cols).shape
enroll_remade.drop(columns = rc_cols, inplace = True)
enroll_remade.shape

# not bad!!
# I'd say that should do it!
os.getcwd()
# os.mkdir('02_data/eks_new/cleaned')
enroll_remade.to_csv('02_data/eks_new/cleaned/enrolleeism-by-reason_22-23')


