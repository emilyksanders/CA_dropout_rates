# Imports
import pandas as pd
import os

os.getcwd()

# Read in data
absent = pd.read_csv(
  '02_data/eks_new/absenteeism_counts_by_reason_22-23.txt', 
  sep='\t', na_values = '*', encoding_errors='replace')
absent.shape

# Make a copy of the column names
orig_names = list(absent.columns)

# Rename columns
absent.columns = [
  f"{x.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__absentee_22-23" 
  for x in absent.columns]
absent.columns

# Narrow down 

# district-level, charter-nonspecific, DASS-nonspecific
absent = absent[absent['aggregate_level__absentee_22-23']=='D']
absent = absent[absent['dass__absentee_22-23']=='All']
absent = absent[absent['charter_school__absentee_22-23']=='All']

# Let's see
absent.shape
absent['aggregate_level__absentee_22-23'].value_counts()
absent['school_name__absentee_22-23'].unique()
absent['school_name__absentee_22-23'].value_counts(dropna = False)

# Let's see how many things per thing we have
for i in list(absent.columns):
  print(i)
  print(f'unique: {absent[i].nunique()}')
  print(f'NAs: {absent[i].isna().sum()}') 
    # after dropping to D, all 0s except school name
  print('')
  
# # Why are there still NAs in school name?
# test = absent[absent['school_name__absentee_22-23'].isna()]
# 
# absent.isna().sum()
# 
# for i in list(absent.columns):
#   print(i)
#   # print('')
#   # print('UNIQUE')
#   # print(f"TOTAL: {absent[i].nunique()}")
#   # print(absent[i].groupby(absent['excused_absences--count__absentee_22-23'].isna()).nunique())
#   print('')
#   print('NAs')
#   print(f"TOTAL: {absent[i].isna().count()}")
#   print(absent[i].groupby(absent['excused_absences--count__absentee_22-23'].isna()).count())
#     # after dropping to D, all 0s except school name
#   print('')
#   print('='*15)
#   print('')

# a bunch of columns have the exact same 5291 NAs
absent_nas = absent[absent['excused_absences--count__absentee_22-23'].isna()]
absent_nas.shape
absent_nas.isna().sum()

# a bunch of columns have the exact same 5291 NAs
# I don't know what's up with them, but it doesn't matter.
# NONE of these rows have ANY useful data in them. So drop them.
absent = absent[absent['excused_absences--count__absentee_22-23'].notna()]
absent.shape
absent.isna().sum() 

# the only NAs left are in school name
absent['school_name__absentee_22-23'].unique()

# what is going on with them? -- SEE SEPARATE SCRIPT
absent_wo_school_name = absent[absent['school_name__absentee_22-23'].isna()]
absent_w_school_name = absent[absent['school_name__absentee_22-23'].notna()]

# it's either "District Office" or NaN.  it doesn't matter.

# why are there more unique district codes than district names?

weird_d_codes = [
  i for i in (list(absent['district_name__absentee_22-23'].unique())) if
  (absent.loc[(absent[
    'district_name__absentee_22-23']==i), 
    ('district_code__absentee_22-23')]).nunique()>1
]

for i in weird_d_codes:
  print(i)
  print((absent.loc[(absent[
    'district_name__absentee_22-23']==i), 
    ('district_code__absentee_22-23')]).nunique())

# because there are duplicate district names in different counties!
# why are you like this, california!?


# drop columns
absent.columns

drop_cols = ['dass__absentee_22-23', 'charter_school__absentee_22-23',
  'aggregate_level__absentee_22-23', 'school_code__absentee_22-23', 
  'county_name__absentee_22-23', 'school_name__absentee_22-23',
  'district_name__absentee_22-23'] # beGONE, agent of confusion!
  
absent.drop(columns = drop_cols, inplace = True)
absent.shape

absent.info()

# # needed to go back and define * as NA
# absent['district_code__absentee_22-23'].unique()[510:]
# absent.dtypes
# absent.map(int)
# 
# for i in list(absent.columns):
#   try:
#     absent['average_days_absent__absentee_22-23'] = pd.to_numeric(absent['average_days_absent__absentee_22-23'], errors='ignore')
#   except:
#     pass
# absent.dtypes

# reporting categories

# define some time-savers
cats_col = 'reporting_category__absentee_22-23'
cats_list = list(absent[cats_col].unique())
a = absent[cats_col]
district = 'district_code__absentee_22-23'
subs = []

for i in cats_list:
  if i=='TA':
    print(f"absent_{i} = absent.loc[absent[a=='{i}'].index, :]")
  else:
    print(f"absent_{i} = absent.loc[absent[a=='{i}'].index, split_cols]")
  
for i in cats_list:
  print(f"subs.append(absent_{i})")

absent_CAN = absent.loc[absent[a=='CAN'].index, split_cols]
absent_CAY = absent.loc[absent[a=='CAY'].index, split_cols]
absent_GF = absent.loc[absent[a=='GF'].index, split_cols]
absent_GM = absent.loc[absent[a=='GM'].index, split_cols]
absent_GR13 = absent.loc[absent[a=='GR13'].index, split_cols]
absent_GR46 = absent.loc[absent[a=='GR46'].index, split_cols]
absent_GR78 = absent.loc[absent[a=='GR78'].index, split_cols]
absent_GR912 = absent.loc[absent[a=='GR912'].index, split_cols]
absent_GRK8 = absent.loc[absent[a=='GRK8'].index, split_cols]
absent_GRKN = absent.loc[absent[a=='GRKN'].index, split_cols]
absent_RA = absent.loc[absent[a=='RA'].index, split_cols]
absent_RB = absent.loc[absent[a=='RB'].index, split_cols]
absent_RD = absent.loc[absent[a=='RD'].index, split_cols]
absent_RF = absent.loc[absent[a=='RF'].index, split_cols]
absent_RH = absent.loc[absent[a=='RH'].index, split_cols]
absent_RI = absent.loc[absent[a=='RI'].index, split_cols]
absent_RP = absent.loc[absent[a=='RP'].index, split_cols]
absent_RT = absent.loc[absent[a=='RT'].index, split_cols]
absent_RW = absent.loc[absent[a=='RW'].index, split_cols]
absent_SD = absent.loc[absent[a=='SD'].index, split_cols]
absent_SE = absent.loc[absent[a=='SE'].index, split_cols]
absent_SF = absent.loc[absent[a=='SF'].index, split_cols]
absent_SH = absent.loc[absent[a=='SH'].index, split_cols]
absent_SS = absent.loc[absent[a=='SS'].index, split_cols]
absent_TA = absent.loc[absent[a=='TA'].index, :]
absent_GX = absent.loc[absent[a=='GX'].index, split_cols]
absent_SM = absent.loc[absent[a=='SM'].index, split_cols]


subs.append(absent_CAN)
subs.append(absent_CAY)
subs.append(absent_GF)
subs.append(absent_GM)
subs.append(absent_GR13)
subs.append(absent_GR46)
subs.append(absent_GR78)
subs.append(absent_GR912)
subs.append(absent_GRK8)
subs.append(absent_GRKN)
subs.append(absent_RA)
subs.append(absent_RB)
subs.append(absent_RD)
subs.append(absent_RF)
subs.append(absent_RH)
subs.append(absent_RI)
subs.append(absent_RP)
subs.append(absent_RT)
subs.append(absent_RW)
subs.append(absent_SD)
subs.append(absent_SE)
subs.append(absent_SF)
subs.append(absent_SH)
subs.append(absent_SS)
subs.append(absent_TA)
subs.append(absent_GX)
subs.append(absent_SM)

# make sure we got all the rows

for i, j in list(zip(cats_list, subs)):
  print(f"""
  {'='*20}
  {i}
  {'-'*20}
  """)
  if (absent[a==i].shape[0])==(j.shape[0]):
    print(f'Caught all rows.')
  else:
    print(f"""
Did not catch all rows. 
Original is {absent[a==i].shape[0]}); reduced is {j.shape[0]}.
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
absent_remade = pd.DataFrame(
  columns = [
    'district_code__absentee_22-23',
    'academic_year__absentee_22-23', 'county_code__absentee_22-23',
    'reporting_category__absentee_22-23',
    'eligible_cumulative_enrollment__absentee_22-23',
    'count_of_students_with_one_or_more_absences__absentee_22-23',
    'average_days_absent__absentee_22-23',
    'total_days_absent__absentee_22-23',
    'excused_absences--percent__absentee_22-23',
    'unexcused_absences--percent__absentee_22-23',
    'out-of-school_suspension_absences--percent__absentee_22-23',
    'incomplete_independent_study_absences--percent__absentee_22-23',
    'excused_absences--count__absentee_22-23',
    'unexcused_absences--count__absentee_22-23',
    'out-of-school_suspension_absences--count__absentee_22-23',
    'incomplete_independent_study_absences--count__absentee_22-23'])

# put in the district codes, to match on
absent_remade['district_code__absentee_22-23'] = list(absent['district_code__absentee_22-23'].unique())

# do some checks
absent_remade.shape # (1010, 1)
absent_remade.isna().sum()

# these names are too long
d = 'district_code__absentee_22-23'

# for every sub-df, generate suffixes and merge it in
for i, j in list(zip(subs, cats_list)):
  # print(f'{j}: {i[cats_col].unique()}')
  k = f'_{j}'
  absent_remade = absent_remade.merge(
    i, on = d, how = 'left', suffixes=(None, k))
absent_remade.shape # (1010, a lot)

blank_col_names = ['academic_year__absentee_22-23', 'county_code__absentee_22-23',
    'reporting_category__absentee_22-23',
    'eligible_cumulative_enrollment__absentee_22-23',
    'count_of_students_with_one_or_more_absences__absentee_22-23',
    'average_days_absent__absentee_22-23',
    'total_days_absent__absentee_22-23',
    'excused_absences--percent__absentee_22-23',
    'unexcused_absences--percent__absentee_22-23',
    'out-of-school_suspension_absences--percent__absentee_22-23',
    'incomplete_independent_study_absences--percent__absentee_22-23',
    'excused_absences--count__absentee_22-23',
    'unexcused_absences--count__absentee_22-23',
    'out-of-school_suspension_absences--count__absentee_22-23',
    'incomplete_independent_study_absences--count__absentee_22-23']

absent_remade.drop(columns = blank_col_names).shape
absent_remade.drop(columns = blank_col_names, inplace = True)
absent_remade.shape

# get rid of the reporting category columns
rc_cols = [a for a in absent_remade.columns if a.split('__')[0]=='reporting_category']
absent_remade.drop(columns = rc_cols).shape
absent_remade.drop(columns = rc_cols, inplace = True)
absent_remade.shape

# not bad!!
# I'd say that should do it!
os.getcwd()
# os.mkdir('02_data/eks_new/cleaned')
absent_remade.to_csv('02_data/eks_new/cleaned/absenteeism-by-reason_22-23')

# # rename columns
# for i in cats_list:
#   print(f"absent_{i}.rename(columns = &'{cats_col}': '{i}__absentee_22-23'&&, inplace = True)")
# 
# print('''
# absent_CAN.rename(columns = &'reporting_category__absentee_22-23': 'CAN__absentee_22-23'&&, inplace = True)
# absent_CAY.rename(columns = &'reporting_category__absentee_22-23': 'CAY__absentee_22-23'&&, inplace = True)
# absent_GF.rename(columns = &'reporting_category__absentee_22-23': 'GF__absentee_22-23'&&, inplace = True)
# absent_GM.rename(columns = &'reporting_category__absentee_22-23': 'GM__absentee_22-23'&&, inplace = True)
# absent_GR13.rename(columns = &'reporting_category__absentee_22-23': 'GR13__absentee_22-23'&&, inplace = True)
# absent_GR46.rename(columns = &'reporting_category__absentee_22-23': 'GR46__absentee_22-23'&&, inplace = True)
# absent_GR78.rename(columns = &'reporting_category__absentee_22-23': 'GR78__absentee_22-23'&&, inplace = True)
# absent_GR912.rename(columns = &'reporting_category__absentee_22-23': 'GR912__absentee_22-23'&&, inplace = True)
# absent_GRK8.rename(columns = &'reporting_category__absentee_22-23': 'GRK8__absentee_22-23'&&, inplace = True)
# absent_GRKN.rename(columns = &'reporting_category__absentee_22-23': 'GRKN__absentee_22-23'&&, inplace = True)
# absent_RA.rename(columns = &'reporting_category__absentee_22-23': 'RA__absentee_22-23'&&, inplace = True)
# absent_RB.rename(columns = &'reporting_category__absentee_22-23': 'RB__absentee_22-23'&&, inplace = True)
# absent_RD.rename(columns = &'reporting_category__absentee_22-23': 'RD__absentee_22-23'&&, inplace = True)
# absent_RF.rename(columns = &'reporting_category__absentee_22-23': 'RF__absentee_22-23'&&, inplace = True)
# absent_RH.rename(columns = &'reporting_category__absentee_22-23': 'RH__absentee_22-23'&&, inplace = True)
# absent_RI.rename(columns = &'reporting_category__absentee_22-23': 'RI__absentee_22-23'&&, inplace = True)
# absent_RP.rename(columns = &'reporting_category__absentee_22-23': 'RP__absentee_22-23'&&, inplace = True)
# absent_RT.rename(columns = &'reporting_category__absentee_22-23': 'RT__absentee_22-23'&&, inplace = True)
# absent_RW.rename(columns = &'reporting_category__absentee_22-23': 'RW__absentee_22-23'&&, inplace = True)
# absent_SD.rename(columns = &'reporting_category__absentee_22-23': 'SD__absentee_22-23'&&, inplace = True)
# absent_SE.rename(columns = &'reporting_category__absentee_22-23': 'SE__absentee_22-23'&&, inplace = True)
# absent_SF.rename(columns = &'reporting_category__absentee_22-23': 'SF__absentee_22-23'&&, inplace = True)
# absent_SH.rename(columns = &'reporting_category__absentee_22-23': 'SH__absentee_22-23'&&, inplace = True)
# absent_SS.rename(columns = &'reporting_category__absentee_22-23': 'SS__absentee_22-23'&&, inplace = True)
# absent_TA.rename(columns = &'reporting_category__absentee_22-23': 'TA__absentee_22-23'&&, inplace = True)
# absent_GX.rename(columns = &'reporting_category__absentee_22-23': 'GX__absentee_22-23'&&, inplace = True)
# absent_SM.rename(columns = &'reporting_category__absentee_22-23': 'SM__absentee_22-23'&&, inplace = True)
# '''.replace('&&', '}').replace('&', '{'))
# 
# absent_CAN.rename(columns = {'reporting_category__absentee_22-23': 'CAN__absentee_22-23'}, inplace = True)
# absent_CAY.rename(columns = {'reporting_category__absentee_22-23': 'CAY__absentee_22-23'}, inplace = True)
# absent_GF.rename(columns = {'reporting_category__absentee_22-23': 'GF__absentee_22-23'}, inplace = True)
# absent_GM.rename(columns = {'reporting_category__absentee_22-23': 'GM__absentee_22-23'}, inplace = True)
# absent_GR13.rename(columns = {'reporting_category__absentee_22-23': 'GR13__absentee_22-23'}, inplace = True)
# absent_GR46.rename(columns = {'reporting_category__absentee_22-23': 'GR46__absentee_22-23'}, inplace = True)
# absent_GR78.rename(columns = {'reporting_category__absentee_22-23': 'GR78__absentee_22-23'}, inplace = True)
# absent_GR912.rename(columns = {'reporting_category__absentee_22-23': 'GR912__absentee_22-23'}, inplace = True)
# absent_GRK8.rename(columns = {'reporting_category__absentee_22-23': 'GRK8__absentee_22-23'}, inplace = True)
# absent_GRKN.rename(columns = {'reporting_category__absentee_22-23': 'GRKN__absentee_22-23'}, inplace = True)
# absent_RA.rename(columns = {'reporting_category__absentee_22-23': 'RA__absentee_22-23'}, inplace = True)
# absent_RB.rename(columns = {'reporting_category__absentee_22-23': 'RB__absentee_22-23'}, inplace = True)
# absent_RD.rename(columns = {'reporting_category__absentee_22-23': 'RD__absentee_22-23'}, inplace = True)
# absent_RF.rename(columns = {'reporting_category__absentee_22-23': 'RF__absentee_22-23'}, inplace = True)
# absent_RH.rename(columns = {'reporting_category__absentee_22-23': 'RH__absentee_22-23'}, inplace = True)
# absent_RI.rename(columns = {'reporting_category__absentee_22-23': 'RI__absentee_22-23'}, inplace = True)
# absent_RP.rename(columns = {'reporting_category__absentee_22-23': 'RP__absentee_22-23'}, inplace = True)
# absent_RT.rename(columns = {'reporting_category__absentee_22-23': 'RT__absentee_22-23'}, inplace = True)
# absent_RW.rename(columns = {'reporting_category__absentee_22-23': 'RW__absentee_22-23'}, inplace = True)
# absent_SD.rename(columns = {'reporting_category__absentee_22-23': 'SD__absentee_22-23'}, inplace = True)
# absent_SE.rename(columns = {'reporting_category__absentee_22-23': 'SE__absentee_22-23'}, inplace = True)
# absent_SF.rename(columns = {'reporting_category__absentee_22-23': 'SF__absentee_22-23'}, inplace = True)
# absent_SH.rename(columns = {'reporting_category__absentee_22-23': 'SH__absentee_22-23'}, inplace = True)
# absent_SS.rename(columns = {'reporting_category__absentee_22-23': 'SS__absentee_22-23'}, inplace = True)
# absent_TA.rename(columns = {'reporting_category__absentee_22-23': 'TA__absentee_22-23'}, inplace = True)
# absent_GX.rename(columns = {'reporting_category__absentee_22-23': 'GX__absentee_22-23'}, inplace = True)
# absent_SM.rename(columns = {'reporting_category__absentee_22-23': 'SM__absentee_22-23'}, inplace = True)



# scraps

# # make sure each district code is only shown once per sub_df
# for i in cats_list:
#   print(f"(absent_{i}['district_code__absentee_22-23'].nunique())/(absent_{i}.shape[0])")
# 
# (absent_CAN['district_code__absentee_22-23'].nunique())/(absent_CAN.shape[0])
# (absent_CAY['district_code__absentee_22-23'].nunique())/(absent_CAY.shape[0])
# (absent_GF['district_code__absentee_22-23'].nunique())/(absent_GF.shape[0])
# (absent_GM['district_code__absentee_22-23'].nunique())/(absent_GM.shape[0])
# (absent_GR13['district_code__absentee_22-23'].nunique())/(absent_GR13.shape[0])
# (absent_GR46['district_code__absentee_22-23'].nunique())/(absent_GR46.shape[0])
# (absent_GR78['district_code__absentee_22-23'].nunique())/(absent_GR78.shape[0])
# (absent_GR912['district_code__absentee_22-23'].nunique())/(absent_GR912.shape[0])
# (absent_GRK8['district_code__absentee_22-23'].nunique())/(absent_GRK8.shape[0])
# (absent_GRKN['district_code__absentee_22-23'].nunique())/(absent_GRKN.shape[0])
# (absent_RA['district_code__absentee_22-23'].nunique())/(absent_RA.shape[0])
# (absent_RB['district_code__absentee_22-23'].nunique())/(absent_RB.shape[0])
# (absent_RD['district_code__absentee_22-23'].nunique())/(absent_RD.shape[0])
# (absent_RF['district_code__absentee_22-23'].nunique())/(absent_RF.shape[0])
# (absent_RH['district_code__absentee_22-23'].nunique())/(absent_RH.shape[0])
# (absent_RI['district_code__absentee_22-23'].nunique())/(absent_RI.shape[0])
# (absent_RP['district_code__absentee_22-23'].nunique())/(absent_RP.shape[0])
# (absent_RT['district_code__absentee_22-23'].nunique())/(absent_RT.shape[0])
# (absent_RW['district_code__absentee_22-23'].nunique())/(absent_RW.shape[0])
# (absent_SD['district_code__absentee_22-23'].nunique())/(absent_SD.shape[0])
# (absent_SE['district_code__absentee_22-23'].nunique())/(absent_SE.shape[0])
# (absent_SF['district_code__absentee_22-23'].nunique())/(absent_SF.shape[0])
# (absent_SH['district_code__absentee_22-23'].nunique())/(absent_SH.shape[0])
# (absent_SS['district_code__absentee_22-23'].nunique())/(absent_SS.shape[0])
# (absent_TA['district_code__absentee_22-23'].nunique())/(absent_TA.shape[0])
# (absent_GX['district_code__absentee_22-23'].nunique())/(absent_GX.shape[0])
# (absent_SM['district_code__absentee_22-23'].nunique())/(absent_SM.shape[0])
