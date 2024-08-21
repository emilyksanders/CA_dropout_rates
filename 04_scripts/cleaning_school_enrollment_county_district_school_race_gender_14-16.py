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

###### THESE DON'T APPLY ######
# enroll = enroll[enroll['aggregate_level__enrolled_14-16']=='D']
# enroll = enroll[enroll['dass__enrolled_14-16']=='All']
# enroll = enroll[enroll['charter_school__enrolled_14-16']=='All']

# Let's see
# enroll.shape
# # enroll['aggregate_level__enrolled_14-16'].value_counts()
# enroll['school_name__enrolled_14-16'].unique()
# enroll['school_name__enrolled_14-16'].value_counts(dropna = False)

# the columns have different names, because of course they do
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
  
# NOT APPLICABLE
# # a bunch of columns have the exact same 5291 NAs
# enroll_nas = enroll[enroll['excused_absences--count__enrolled_14-16'].isna()]
# enroll_nas.shape
# enroll_nas.isna().sum()

# we do have NAs in some of the "weird" columns. I don't know what 
# else to do but to call them 0s.

# a bunch of columns have the exact same 5291 NAs
# I don't know what's up with them, but it doesn't matter.
# NONE of these rows have ANY useful data in them. So drop them.
enroll = enroll[enroll['excused_absences--count__enrolled_14-16'].notna()]
enroll.shape
enroll.isna().sum() 

# the only NAs left are in school name
enroll['school_name__enrolled_14-16'].unique()

# what is going on with them? -- SEE SEPARATE SCRIPT
enroll_wo_school_name = enroll[enroll['school_name__enrolled_14-16'].isna()]
enroll_w_school_name = enroll[enroll['school_name__enrolled_14-16'].notna()]

# it's either "District Office" or NaN.  it doesn't matter.

# why are there more unique district codes than district names?

weird_d_codes = [
  i for i in (list(enroll['district_name__enrolled_14-16'].unique())) if
  (enroll.loc[(enroll[
    'district_name__enrolled_14-16']==i), 
    ('district_code__enrolled_14-16')]).nunique()>1
]

for i in weird_d_codes:
  print(i)
  print((enroll.loc[(enroll[
    'district_name__enrolled_14-16']==i), 
    ('district_code__enrolled_14-16')]).nunique())

# because there are duplicate district names in different counties!
# why are you like this, california!?


# drop columns
enroll.columns

drop_cols = ['dass__enrolled_14-16', 'charter_school__enrolled_14-16',
  'aggregate_level__enrolled_14-16', 'school_code__enrolled_14-16', 
  'county_name__enrolled_14-16', 'school_name__enrolled_14-16',
  'district_name__enrolled_14-16'] # beGONE, agent of confusion!
  
enroll.drop(columns = drop_cols, inplace = True)
enroll.shape

enroll.info()

# # needed to go back and define * as NA
# enroll['district_code__enrolled_14-16'].unique()[510:]
# enroll.dtypes
# enroll.map(int)
# 
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

enroll_CAN = enroll.loc[enroll[a=='CAN'].index, split_cols]
enroll_CAY = enroll.loc[enroll[a=='CAY'].index, split_cols]
enroll_GF = enroll.loc[enroll[a=='GF'].index, split_cols]
enroll_GM = enroll.loc[enroll[a=='GM'].index, split_cols]
enroll_GR13 = enroll.loc[enroll[a=='GR13'].index, split_cols]
enroll_GR46 = enroll.loc[enroll[a=='GR46'].index, split_cols]
enroll_GR78 = enroll.loc[enroll[a=='GR78'].index, split_cols]
enroll_GR912 = enroll.loc[enroll[a=='GR912'].index, split_cols]
enroll_GRK8 = enroll.loc[enroll[a=='GRK8'].index, split_cols]
enroll_GRKN = enroll.loc[enroll[a=='GRKN'].index, split_cols]
enroll_RA = enroll.loc[enroll[a=='RA'].index, split_cols]
enroll_RB = enroll.loc[enroll[a=='RB'].index, split_cols]
enroll_RD = enroll.loc[enroll[a=='RD'].index, split_cols]
enroll_RF = enroll.loc[enroll[a=='RF'].index, split_cols]
enroll_RH = enroll.loc[enroll[a=='RH'].index, split_cols]
enroll_RI = enroll.loc[enroll[a=='RI'].index, split_cols]
enroll_RP = enroll.loc[enroll[a=='RP'].index, split_cols]
enroll_RT = enroll.loc[enroll[a=='RT'].index, split_cols]
enroll_RW = enroll.loc[enroll[a=='RW'].index, split_cols]
enroll_SD = enroll.loc[enroll[a=='SD'].index, split_cols]
enroll_SE = enroll.loc[enroll[a=='SE'].index, split_cols]
enroll_SF = enroll.loc[enroll[a=='SF'].index, split_cols]
enroll_SH = enroll.loc[enroll[a=='SH'].index, split_cols]
enroll_SS = enroll.loc[enroll[a=='SS'].index, split_cols]
enroll_TA = enroll.loc[enroll[a=='TA'].index, :]
enroll_GX = enroll.loc[enroll[a=='GX'].index, split_cols]
enroll_SM = enroll.loc[enroll[a=='SM'].index, split_cols]


subs.append(enroll_CAN)
subs.append(enroll_CAY)
subs.append(enroll_GF)
subs.append(enroll_GM)
subs.append(enroll_GR13)
subs.append(enroll_GR46)
subs.append(enroll_GR78)
subs.append(enroll_GR912)
subs.append(enroll_GRK8)
subs.append(enroll_GRKN)
subs.append(enroll_RA)
subs.append(enroll_RB)
subs.append(enroll_RD)
subs.append(enroll_RF)
subs.append(enroll_RH)
subs.append(enroll_RI)
subs.append(enroll_RP)
subs.append(enroll_RT)
subs.append(enroll_RW)
subs.append(enroll_SD)
subs.append(enroll_SE)
subs.append(enroll_SF)
subs.append(enroll_SH)
subs.append(enroll_SS)
subs.append(enroll_TA)
subs.append(enroll_GX)
subs.append(enroll_SM)

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
    'district_code__enrolled_14-16',
    'academic_year__enrolled_14-16', 'county_code__enrolled_14-16',
    'reporting_category__enrolled_14-16',
    'eligible_cumulative_enrollment__enrolled_14-16',
    'count_of_students_with_one_or_more_absences__enrolled_14-16',
    'average_days_enroll__enrolled_14-16',
    'total_days_enroll__enrolled_14-16',
    'excused_absences--percent__enrolled_14-16',
    'unexcused_absences--percent__enrolled_14-16',
    'out-of-school_suspension_absences--percent__enrolled_14-16',
    'incomplete_independent_study_absences--percent__enrolled_14-16',
    'excused_absences--count__enrolled_14-16',
    'unexcused_absences--count__enrolled_14-16',
    'out-of-school_suspension_absences--count__enrolled_14-16',
    'incomplete_independent_study_absences--count__enrolled_14-16'])

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

blank_col_names = ['academic_year__enrolled_14-16', 'county_code__enrolled_14-16',
    'reporting_category__enrolled_14-16',
    'eligible_cumulative_enrollment__enrolled_14-16',
    'count_of_students_with_one_or_more_absences__enrolled_14-16',
    'average_days_enroll__enrolled_14-16',
    'total_days_enroll__enrolled_14-16',
    'excused_absences--percent__enrolled_14-16',
    'unexcused_absences--percent__enrolled_14-16',
    'out-of-school_suspension_absences--percent__enrolled_14-16',
    'incomplete_independent_study_absences--percent__enrolled_14-16',
    'excused_absences--count__enrolled_14-16',
    'unexcused_absences--count__enrolled_14-16',
    'out-of-school_suspension_absences--count__enrolled_14-16',
    'incomplete_independent_study_absences--count__enrolled_14-16']

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

# # rename columns
# for i in cats_list:
#   print(f"enroll_{i}.rename(columns = &'{cats_col}': '{i}__enrolled_14-16'&&, inplace = True)")
# 
# print('''
# enroll_CAN.rename(columns = &'reporting_category__enrolled_14-16': 'CAN__enrolled_14-16'&&, inplace = True)
# enroll_CAY.rename(columns = &'reporting_category__enrolled_14-16': 'CAY__enrolled_14-16'&&, inplace = True)
# enroll_GF.rename(columns = &'reporting_category__enrolled_14-16': 'GF__enrolled_14-16'&&, inplace = True)
# enroll_GM.rename(columns = &'reporting_category__enrolled_14-16': 'GM__enrolled_14-16'&&, inplace = True)
# enroll_GR13.rename(columns = &'reporting_category__enrolled_14-16': 'GR13__enrolled_14-16'&&, inplace = True)
# enroll_GR46.rename(columns = &'reporting_category__enrolled_14-16': 'GR46__enrolled_14-16'&&, inplace = True)
# enroll_GR78.rename(columns = &'reporting_category__enrolled_14-16': 'GR78__enrolled_14-16'&&, inplace = True)
# enroll_GR912.rename(columns = &'reporting_category__enrolled_14-16': 'GR912__enrolled_14-16'&&, inplace = True)
# enroll_GRK8.rename(columns = &'reporting_category__enrolled_14-16': 'GRK8__enrolled_14-16'&&, inplace = True)
# enroll_GRKN.rename(columns = &'reporting_category__enrolled_14-16': 'GRKN__enrolled_14-16'&&, inplace = True)
# enroll_RA.rename(columns = &'reporting_category__enrolled_14-16': 'RA__enrolled_14-16'&&, inplace = True)
# enroll_RB.rename(columns = &'reporting_category__enrolled_14-16': 'RB__enrolled_14-16'&&, inplace = True)
# enroll_RD.rename(columns = &'reporting_category__enrolled_14-16': 'RD__enrolled_14-16'&&, inplace = True)
# enroll_RF.rename(columns = &'reporting_category__enrolled_14-16': 'RF__enrolled_14-16'&&, inplace = True)
# enroll_RH.rename(columns = &'reporting_category__enrolled_14-16': 'RH__enrolled_14-16'&&, inplace = True)
# enroll_RI.rename(columns = &'reporting_category__enrolled_14-16': 'RI__enrolled_14-16'&&, inplace = True)
# enroll_RP.rename(columns = &'reporting_category__enrolled_14-16': 'RP__enrolled_14-16'&&, inplace = True)
# enroll_RT.rename(columns = &'reporting_category__enrolled_14-16': 'RT__enrolled_14-16'&&, inplace = True)
# enroll_RW.rename(columns = &'reporting_category__enrolled_14-16': 'RW__enrolled_14-16'&&, inplace = True)
# enroll_SD.rename(columns = &'reporting_category__enrolled_14-16': 'SD__enrolled_14-16'&&, inplace = True)
# enroll_SE.rename(columns = &'reporting_category__enrolled_14-16': 'SE__enrolled_14-16'&&, inplace = True)
# enroll_SF.rename(columns = &'reporting_category__enrolled_14-16': 'SF__enrolled_14-16'&&, inplace = True)
# enroll_SH.rename(columns = &'reporting_category__enrolled_14-16': 'SH__enrolled_14-16'&&, inplace = True)
# enroll_SS.rename(columns = &'reporting_category__enrolled_14-16': 'SS__enrolled_14-16'&&, inplace = True)
# enroll_TA.rename(columns = &'reporting_category__enrolled_14-16': 'TA__enrolled_14-16'&&, inplace = True)
# enroll_GX.rename(columns = &'reporting_category__enrolled_14-16': 'GX__enrolled_14-16'&&, inplace = True)
# enroll_SM.rename(columns = &'reporting_category__enrolled_14-16': 'SM__enrolled_14-16'&&, inplace = True)
# '''.replace('&&', '}').replace('&', '{'))
# 
# enroll_CAN.rename(columns = {'reporting_category__enrolled_14-16': 'CAN__enrolled_14-16'}, inplace = True)
# enroll_CAY.rename(columns = {'reporting_category__enrolled_14-16': 'CAY__enrolled_14-16'}, inplace = True)
# enroll_GF.rename(columns = {'reporting_category__enrolled_14-16': 'GF__enrolled_14-16'}, inplace = True)
# enroll_GM.rename(columns = {'reporting_category__enrolled_14-16': 'GM__enrolled_14-16'}, inplace = True)
# enroll_GR13.rename(columns = {'reporting_category__enrolled_14-16': 'GR13__enrolled_14-16'}, inplace = True)
# enroll_GR46.rename(columns = {'reporting_category__enrolled_14-16': 'GR46__enrolled_14-16'}, inplace = True)
# enroll_GR78.rename(columns = {'reporting_category__enrolled_14-16': 'GR78__enrolled_14-16'}, inplace = True)
# enroll_GR912.rename(columns = {'reporting_category__enrolled_14-16': 'GR912__enrolled_14-16'}, inplace = True)
# enroll_GRK8.rename(columns = {'reporting_category__enrolled_14-16': 'GRK8__enrolled_14-16'}, inplace = True)
# enroll_GRKN.rename(columns = {'reporting_category__enrolled_14-16': 'GRKN__enrolled_14-16'}, inplace = True)
# enroll_RA.rename(columns = {'reporting_category__enrolled_14-16': 'RA__enrolled_14-16'}, inplace = True)
# enroll_RB.rename(columns = {'reporting_category__enrolled_14-16': 'RB__enrolled_14-16'}, inplace = True)
# enroll_RD.rename(columns = {'reporting_category__enrolled_14-16': 'RD__enrolled_14-16'}, inplace = True)
# enroll_RF.rename(columns = {'reporting_category__enrolled_14-16': 'RF__enrolled_14-16'}, inplace = True)
# enroll_RH.rename(columns = {'reporting_category__enrolled_14-16': 'RH__enrolled_14-16'}, inplace = True)
# enroll_RI.rename(columns = {'reporting_category__enrolled_14-16': 'RI__enrolled_14-16'}, inplace = True)
# enroll_RP.rename(columns = {'reporting_category__enrolled_14-16': 'RP__enrolled_14-16'}, inplace = True)
# enroll_RT.rename(columns = {'reporting_category__enrolled_14-16': 'RT__enrolled_14-16'}, inplace = True)
# enroll_RW.rename(columns = {'reporting_category__enrolled_14-16': 'RW__enrolled_14-16'}, inplace = True)
# enroll_SD.rename(columns = {'reporting_category__enrolled_14-16': 'SD__enrolled_14-16'}, inplace = True)
# enroll_SE.rename(columns = {'reporting_category__enrolled_14-16': 'SE__enrolled_14-16'}, inplace = True)
# enroll_SF.rename(columns = {'reporting_category__enrolled_14-16': 'SF__enrolled_14-16'}, inplace = True)
# enroll_SH.rename(columns = {'reporting_category__enrolled_14-16': 'SH__enrolled_14-16'}, inplace = True)
# enroll_SS.rename(columns = {'reporting_category__enrolled_14-16': 'SS__enrolled_14-16'}, inplace = True)
# enroll_TA.rename(columns = {'reporting_category__enrolled_14-16': 'TA__enrolled_14-16'}, inplace = True)
# enroll_GX.rename(columns = {'reporting_category__enrolled_14-16': 'GX__enrolled_14-16'}, inplace = True)
# enroll_SM.rename(columns = {'reporting_category__enrolled_14-16': 'SM__enrolled_14-16'}, inplace = True)



# scraps

# # make sure each district code is only shown once per sub_df
# for i in cats_list:
#   print(f"(enroll_{i}['district_code__enrolled_14-16'].nunique())/(enroll_{i}.shape[0])")
# 
# (enroll_CAN['district_code__enrolled_14-16'].nunique())/(enroll_CAN.shape[0])
# (enroll_CAY['district_code__enrolled_14-16'].nunique())/(enroll_CAY.shape[0])
# (enroll_GF['district_code__enrolled_14-16'].nunique())/(enroll_GF.shape[0])
# (enroll_GM['district_code__enrolled_14-16'].nunique())/(enroll_GM.shape[0])
# (enroll_GR13['district_code__enrolled_14-16'].nunique())/(enroll_GR13.shape[0])
# (enroll_GR46['district_code__enrolled_14-16'].nunique())/(enroll_GR46.shape[0])
# (enroll_GR78['district_code__enrolled_14-16'].nunique())/(enroll_GR78.shape[0])
# (enroll_GR912['district_code__enrolled_14-16'].nunique())/(enroll_GR912.shape[0])
# (enroll_GRK8['district_code__enrolled_14-16'].nunique())/(enroll_GRK8.shape[0])
# (enroll_GRKN['district_code__enrolled_14-16'].nunique())/(enroll_GRKN.shape[0])
# (enroll_RA['district_code__enrolled_14-16'].nunique())/(enroll_RA.shape[0])
# (enroll_RB['district_code__enrolled_14-16'].nunique())/(enroll_RB.shape[0])
# (enroll_RD['district_code__enrolled_14-16'].nunique())/(enroll_RD.shape[0])
# (enroll_RF['district_code__enrolled_14-16'].nunique())/(enroll_RF.shape[0])
# (enroll_RH['district_code__enrolled_14-16'].nunique())/(enroll_RH.shape[0])
# (enroll_RI['district_code__enrolled_14-16'].nunique())/(enroll_RI.shape[0])
# (enroll_RP['district_code__enrolled_14-16'].nunique())/(enroll_RP.shape[0])
# (enroll_RT['district_code__enrolled_14-16'].nunique())/(enroll_RT.shape[0])
# (enroll_RW['district_code__enrolled_14-16'].nunique())/(enroll_RW.shape[0])
# (enroll_SD['district_code__enrolled_14-16'].nunique())/(enroll_SD.shape[0])
# (enroll_SE['district_code__enrolled_14-16'].nunique())/(enroll_SE.shape[0])
# (enroll_SF['district_code__enrolled_14-16'].nunique())/(enroll_SF.shape[0])
# (enroll_SH['district_code__enrolled_14-16'].nunique())/(enroll_SH.shape[0])
# (enroll_SS['district_code__enrolled_14-16'].nunique())/(enroll_SS.shape[0])
# (enroll_TA['district_code__enrolled_14-16'].nunique())/(enroll_TA.shape[0])
# (enroll_GX['district_code__enrolled_14-16'].nunique())/(enroll_GX.shape[0])
# (enroll_SM['district_code__enrolled_14-16'].nunique())/(enroll_SM.shape[0])
