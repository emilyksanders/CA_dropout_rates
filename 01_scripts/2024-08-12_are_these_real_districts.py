# are these all real districts?

# imports
import re

# CREATE THE LIST IN THE OTHER SCRIPT

# clean up the list
district_list = [a.strip() for a in districts.splitlines()]
district_list.sort()
district_list = [a for a in district_list if a!='']
district_list = [re.sub(r'\[[0-9]+\]$', '', a).strip() for a in district_list]
district_list = [re.sub(r'\(California\)$', '', a).strip() for a in district_list]
district_list = [re.sub(r'School District$', '', a).strip() for a in district_list]
district_list = [a for a in district_list if not (
  (re.search(r'County$', a)) and 
  (not re.search(r'District', a))
  )]

len(district_list)
  
# len([a for a in district_list if re.search(r'School District$', a)])
# [a for a in district_list if not re.search(r'School District$', a)]
    
# end up with 939 districts
# which is more or less correct.

data_districts = absent['district_name__absentee_22-23'].unique()
data_districts.sort()
type(data_districts)
len(data_districts)

misfits = [i for i in data_districts if i not in district_list]
misfits.sort()
len(misfits)

# oh dear. (len(misfits)==999 the first time)
misfits[:5]
# data_districts[:5]
district_list[:5]

# all that ^^^ catches most of them.  now...
district_list_2 = [re.sub(r'Elementary$', '', a).strip() for a in district_list]
misfits_2 = [re.sub(r'Elementary$', '', a).strip() for a in misfits]
misfits_2 = [i for i in misfits_2 if i not in district_list_2]
len(misfits_2)

# why are "office of education"s being listed as districts
district_is_office = absent[absent['district_name__absentee_22-23']=='Santa Cruz County Office of Education']

# you absolute jerks
county_level = pd.read_csv(
  '02_data/eks_new/absenteeism_counts_by_reason_22-23.txt', 
  sep='\t', na_values = '*', encoding_errors='replace')
county_level.columns = [
  f"{x.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__absentee_22-23" 
  for x in county_level.columns]
county_level.columns

# Narrow down 

# district-level, charter-nonspecific, DASS-nonspecific
county_level = county_level[county_level['aggregate_level__absentee_22-23']=='C']
county_level = county_level[county_level['dass__absentee_22-23']=='All']
county_level = county_level[county_level['charter_school__absentee_22-23']=='All']

# drop_cols = ['dass__absentee_22-23', 'charter_school__absentee_22-23',
#   'aggregate_level__absentee_22-23', 'school_code__absentee_22-23', 
#   'county_name__absentee_22-23', 'district_name__absentee_22-23', 
#   'school_name__absentee_22-23']
# county_level.drop(columns = drop_cols, inplace = True)
# district_is_office.drop(columns = drop_cols, inplace = True)

# match district_is_office (just this one test county)
county_level = county_level[county_level['county_code__absentee_22-23']==44]

district_is_office.shape
county_level.shape

[a for a in list(county_level.columns) if a not in list(district_is_office.columns)]
# same columns, county_level has 4 extra rows

# Let's see how many things per thing we have
for i in list(county_level.columns):
  print(i)
  print(f'unique: {county_level[i].nunique()}')
  print(f'NAs: {county_level[i].isna().sum()}') 
    # after dropping to D, all 0s except school name
  print('')
  
for i in list(district_is_office.columns):
  print(i)
  print(f'unique: {district_is_office[i].nunique()}')
  print(f'NAs: {district_is_office[i].isna().sum()}')
  print('')
  
a_2_rcs = list(county_level['reporting_category__absentee_22-23'].unique())
t_rcs = list(district_is_office['reporting_category__absentee_22-23'].unique())

[i for i in a_2_rcs if i not in t_rcs]
  
county_level = county_level[
  county_level['reporting_category__absentee_22-23']!='GX']
county_level = county_level[
  county_level['reporting_category__absentee_22-23']!='RF']
county_level = county_level[
  county_level['reporting_category__absentee_22-23']!='RP']
county_level = county_level[
  county_level['reporting_category__absentee_22-23']!='SM']

col_names = list(county_level.columns)

district_is_office.shape
county_level.shape

[i for i in list(district_is_office.columns) if i not in list(county_level.columns)]
[i for i in list(county_level.columns) if i not in list(district_is_office.columns)]

for i in col_names:
  # print(i, county_level[i].dtype)
  if (county_level[i].dtype==float) or (county_level[i].dtype=='int64'):
    continue
  else:
    print(i, county_level[i].dtype)
  print('')
  
for i in col_names:
  # print(i, county_level[i].dtype)
  if (district_is_office[i].dtype==float) or (district_is_office[i].dtype=='int64'):
    continue
  else:
    print(i, district_is_office[i].dtype)
  print('')
  
district_is_office.info()
county_level.info()

district_is_office.isna().sum()
county_level.isna().sum()

district_is_office.reset_index(inplace=True)
county_level.reset_index(inplace=True)

# Make sure they're in the same order
for i in list(range(23)):
  district_is_office.loc[i, z]==county_level.loc[i, z]

a = district_is_office[[z]]

for i in col_names:
  # print(i, county_level[i].dtype)
  if (district_is_office[i].dtype==float) or (district_is_office[i].dtype=='int64'):
    a[i] = (district_is_office[i] - county_level[i])
  else:
    print(i, district_is_office[i].dtype)
  print('')

a.sum()

# Welp.  The numbers are very different.
# That clarified nothing.  But, it means I'm not going to fuss about those.
# remove them
misfits_3 = [a for a in misfits_2 if not re.search(
  r'County Office of Education$', a)]
# check  
print(('\n').join([i for i in misfits_2 if i not in misfits_3]))
# now what?
len(misfits_3)

# I'm just going to check these last few by hand
print(('\n').join(misfits_3))
# all but two are either real districts, or admin offices
no_results = ['SBE - Grossmont Secondary', 'SBE - Sweetwater Secondary']


# for i in col_names:
#   if (county_level[i].dtype is not float) or (county_level[i].dtype is not int):
#     continue
#   else:
#     print(i, county_level[i].dtype)
    
# [
#   a for a in b if not ((
#     re.search(r'County$', a)) and (not re.search(r'District', a)))]
#     
#     
# district_list
# 
# re.match(r'^[A-Za-z ]+ County$', 'San Bernadino County')
# m = re.match(r'[0-9]', '1xb2')
# 
# re.sub()
# 
# import numpy as np
# np.where(district_list=='District')
# 
# 
# 
