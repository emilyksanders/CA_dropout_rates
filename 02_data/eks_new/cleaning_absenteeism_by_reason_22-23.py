# Imports
import pandas as pd
import os

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
absent['school_name__absentee_22-23'].unique()[:100]
absent['school_name__absentee_22-23'].value_counts(dropna = False)

# Let's see how many things per thing we have
for i in list(absent.columns):
  print(i)
  print(f'unique: {absent[i].nunique()}')
  print(f'NAs: {absent[i].isna().sum()}') 
    # after dropping to D, all 0s except school name
  print('')
  
# Why are there still NAs in school name?
test = absent[absent['school_name__absentee_22-23'].isna()]

absent.isna().sum()

for i in list(absent.columns):
  print(i)
  # print('')
  # print('UNIQUE')
  # print(f"TOTAL: {absent[i].nunique()}")
  # print(absent[i].groupby(absent['excused_absences--count__absentee_22-23'].isna()).nunique())
  print('')
  print('NAs')
  print(f"TOTAL: {absent[i].isna().count()}")
  print(absent[i].groupby(absent['excused_absences--count__absentee_22-23'].isna()).count())
    # after dropping to D, all 0s except school name
  print('')
  print('='*15)
  print('')

# a bunch of columns have the exact same 34500 NAs
absent = absent[absent['excused_absences--count__absentee_22-23'].notna()]
absent.shape
absent.isna().sum() # the only ones left are in school name

# drop columns
absent.columns

drop_cols = ['dass__absentee_22-23', 'charter_school__absentee_22-23',
  'aggregate_level__absentee_22-23', 'school_code__absentee_22-23', 
  'county_name__absentee_22-23', 'district_name__absentee_22-23', 
  'school_name__absentee_22-23']
  
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
  print(f"absent_{i} = absent.loc[absent[a=='{i}'].index, [district, cats_col]]")
  subs.append(absent_{i})

absent_CAN = absent.loc[absent[a=='CAN'].index, [district, cats_col]]
absent_CAY = absent.loc[absent[a=='CAY'].index, [district, cats_col]]
absent_GF = absent.loc[absent[a=='GF'].index, [district, cats_col]]
absent_GM = absent.loc[absent[a=='GM'].index, [district, cats_col]]
absent_GR13 = absent.loc[absent[a=='GR13'].index, [district, cats_col]]
absent_GR46 = absent.loc[absent[a=='GR46'].index, [district, cats_col]]
absent_GR78 = absent.loc[absent[a=='GR78'].index, [district, cats_col]]
absent_GR912 = absent.loc[absent[a=='GR912'].index, [district, cats_col]]
absent_GRK8 = absent.loc[absent[a=='GRK8'].index, [district, cats_col]]
absent_GRKN = absent.loc[absent[a=='GRKN'].index, [district, cats_col]]
absent_RA = absent.loc[absent[a=='RA'].index, [district, cats_col]]
absent_RB = absent.loc[absent[a=='RB'].index, [district, cats_col]]
absent_RD = absent.loc[absent[a=='RD'].index, [district, cats_col]]
absent_RF = absent.loc[absent[a=='RF'].index, [district, cats_col]]
absent_RH = absent.loc[absent[a=='RH'].index, [district, cats_col]]
absent_RI = absent.loc[absent[a=='RI'].index, [district, cats_col]]
absent_RP = absent.loc[absent[a=='RP'].index, [district, cats_col]]
absent_RT = absent.loc[absent[a=='RT'].index, [district, cats_col]]
absent_RW = absent.loc[absent[a=='RW'].index, [district, cats_col]]
absent_SD = absent.loc[absent[a=='SD'].index, [district, cats_col]]
absent_SE = absent.loc[absent[a=='SE'].index, [district, cats_col]]
absent_SF = absent.loc[absent[a=='SF'].index, [district, cats_col]]
absent_SH = absent.loc[absent[a=='SH'].index, [district, cats_col]]
absent_SS = absent.loc[absent[a=='SS'].index, [district, cats_col]]
absent_TA = absent.loc[absent[a=='TA'].index, [district, cats_col]]
absent_GX = absent.loc[absent[a=='GX'].index, [district, cats_col]]
absent_SM = absent.loc[absent[a=='SM'].index, [district, cats_col]]

# make sure we got all the rows

for i, j in list(zip(cat_list, subs)):
  print("""
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



# rename columns
for i in cats_list:
  print(f"absent_{i}.rename(columns = &cats_col: '{i}'&&, inplace = True)")

print('''
absent_CAN.rename(columns = &cats_col: 'CAN'&&, inplace = True)
absent_CAY.rename(columns = &cats_col: 'CAY'&&, inplace = True)
absent_GF.rename(columns = &cats_col: 'GF'&&, inplace = True)
absent_GM.rename(columns = &'{cats_col}': 'GM'&&, inplace = True)
absent_GR13.rename(columns = &'{cats_col}': 'GR13'&&, inplace = True)
absent_GR46.rename(columns = &'{cats_col}': 'GR46'&&, inplace = True)
absent_GR78.rename(columns = &'{cats_col}': 'GR78'&&, inplace = True)
absent_GR912.rename(columns = &'{cats_col}': 'GR912'&&, inplace = True)
absent_GRK8.rename(columns = &'{cats_col}': 'GRK8'&&, inplace = True)
absent_GRKN.rename(columns = &'{cats_col}': 'GRKN'&&, inplace = True)
absent_RA.rename(columns = &'{cats_col}': 'RA'&&, inplace = True)
absent_RB.rename(columns = &'{cats_col}': 'RB'&&, inplace = True)
absent_RD.rename(columns = &'{cats_col}': 'RD'&&, inplace = True)
absent_RF.rename(columns = &'{cats_col}': 'RF'&&, inplace = True)
absent_RH.rename(columns = &'{cats_col}': 'RH'&&, inplace = True)
absent_RI.rename(columns = &'{cats_col}': 'RI'&&, inplace = True)
absent_RP.rename(columns = &'{cats_col}': 'RP'&&, inplace = True)
absent_RT.rename(columns = &'{cats_col}': 'RT'&&, inplace = True)
absent_RW.rename(columns = &'{cats_col}': 'RW'&&, inplace = True)
absent_SD.rename(columns = &'{cats_col}': 'SD'&&, inplace = True)
absent_SE.rename(columns = &'{cats_col}': 'SE'&&, inplace = True)
absent_SF.rename(columns = &'{cats_col}': 'SF'&&, inplace = True)
absent_SH.rename(columns = &'{cats_col}': 'SH'&&, inplace = True)
absent_SS.rename(columns = &'{cats_col}': 'SS'&&, inplace = True)
absent_TA.rename(columns = &'{cats_col}': 'TA'&&, inplace = True)
absent_GX.rename(columns = &'{cats_col}': 'GX'&&, inplace = True)
absent_SM.rename(columns = &'{cats_col}': 'SM'&&, inplace = True)
'''.replace('&&', '}').replace('&', '{'))

absent_CAN.rename(columns = {'reporting_category__absentee_22-23': 'CAN'}, inplace = True)
absent_CAY.rename(columns = {'reporting_category__absentee_22-23': 'CAY'}, inplace = True)
absent_GF.rename(columns = {'reporting_category__absentee_22-23': 'GF'}, inplace = True)
absent_GM.rename(columns = {'reporting_category__absentee_22-23': 'GM'}, inplace = True)
absent_GR13.rename(columns = {'reporting_category__absentee_22-23': 'GR13'}, inplace = True)
absent_GR46.rename(columns = {'reporting_category__absentee_22-23': 'GR46'}, inplace = True)
absent_GR78.rename(columns = {'reporting_category__absentee_22-23': 'GR78'}, inplace = True)
absent_GR912.rename(columns = {'reporting_category__absentee_22-23': 'GR912'}, inplace = True)
absent_GRK8.rename(columns = {'reporting_category__absentee_22-23': 'GRK8'}, inplace = True)
absent_GRKN.rename(columns = {'reporting_category__absentee_22-23': 'GRKN'}, inplace = True)
absent_RA.rename(columns = {'reporting_category__absentee_22-23': 'RA'}, inplace = True)
absent_RB.rename(columns = {'reporting_category__absentee_22-23': 'RB'}, inplace = True)
absent_RD.rename(columns = {'reporting_category__absentee_22-23': 'RD'}, inplace = True)
absent_RF.rename(columns = {'reporting_category__absentee_22-23': 'RF'}, inplace = True)
absent_RH.rename(columns = {'reporting_category__absentee_22-23': 'RH'}, inplace = True)
absent_RI.rename(columns = {'reporting_category__absentee_22-23': 'RI'}, inplace = True)
absent_RP.rename(columns = {'reporting_category__absentee_22-23': 'RP'}, inplace = True)
absent_RT.rename(columns = {'reporting_category__absentee_22-23': 'RT'}, inplace = True)
absent_RW.rename(columns = {'reporting_category__absentee_22-23': 'RW'}, inplace = True)
absent_SD.rename(columns = {'reporting_category__absentee_22-23': 'SD'}, inplace = True)
absent_SE.rename(columns = {'reporting_category__absentee_22-23': 'SE'}, inplace = True)
absent_SF.rename(columns = {'reporting_category__absentee_22-23': 'SF'}, inplace = True)
absent_SH.rename(columns = {'reporting_category__absentee_22-23': 'SH'}, inplace = True)
absent_SS.rename(columns = {'reporting_category__absentee_22-23': 'SS'}, inplace = True)
absent_TA.rename(columns = {'reporting_category__absentee_22-23': 'TA'}, inplace = True)
absent_GX.rename(columns = {'reporting_category__absentee_22-23': 'GX'}, inplace = True)
absent_SM.rename(columns = {'reporting_category__absentee_22-23': 'SM'}, inplace = True)




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
