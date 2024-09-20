# getting a master list of district names

# read it in
cds_key = pd.read_csv(
  './../02_data_a_ignore/key_to_school_and_district_names.txt',
  sep = '\t', encoding_errors = 'replace', 
  low_memory = False, na_values = '*')
cds_key.shape
cds_key.columns

# drop columns we def don't need
keep_cols = ['CDSCode', 'NCESDist', 'County', 'District']
cds_key = cds_key.loc[:, keep_cols]
cds_key.shape

# who is being the problem?
for i in list(cds_key.columns):
  print(i)
  print(cds_key[i].nunique())  # it's the cds_code. it's unique per school
  print('')

# take out the school ID numbers; leave only district and county
cds_key['cds_code'] = [(str(a).zfill(14))[:7] for a in cds_key['CDSCode']]  # annoying leading 0s
cds_key.drop(columns = ['CDSCode'], inplace = True)
cds_key.shape

cds_key.groupby(cds_key['District'])['cds_code'].nunique()[x]

# # look for defunct schools
# closed_schools = cds_key[cds_key['StatusType']=='Closed']
# 
# for i in list(closed_schools.columns):
#   print(i)
#   print(closed_schools[i].nunique())
#   print('')
# 
# # can pandas do the datetime magic?
# closed_schools.info()

# OK, it actually doesn't matter.  
# Leave the defunct ones in.  Who cares!?
# This is the leftmost of the left joins.
# If these guys have disappeared, then no one
# will join on them! And we'll just drop them!

# dedupe
cds_key.drop_duplicates(inplace = True)
cds_key.shape # (1443, 4), AHA!
cds_key.columns

for i in cds_key.columns:
  print(i)
  print(cds_key[i].nunique())
  print('')

cds_key = cds_key.loc[:, ['cds_code', 'County', 'District', 'NCESDist']]
cds_key.columns = ['cds_code', 'county', 'district', 'nces_code']
cds_key.to_csv('county-district_code_key.csv', index = False)

#### DON'T LET IT READ IT IN AS AN INTEGER!!! ####
read_in_cds_key = pd.read_csv('county-district_code_key.csv', 
  dtype = object)

# # why do I have ~100 more unique cds_codes than unique districts?
# cds_key.isna().sum() # all 0s, that's good
# x = lambda a: a>1
# cds_key['District'].value_counts()[x]
# 
# cds_key.groupby(cds_key['District'])['cds_code'].nunique()[x]
# pd.set_option('display.max_rows', None)
# 
# cds_key_whole = cds_key_whole.loc[:, ['cds_code', 'District', 
#   'County', 'NCESDist', 'FederalDFCDistrictID', 'School',
#   'StatusType', 'DOCType', 'EdOpsCode', 'EILCode', 'GSoffered', 
#   'OpenDate', 'ClosedDate', 'Latitude', 'Longitude', 'LastUpDate']]
# 
# cds_key_whole.sort_values(by = ['District', 'cds_code'], inplace = True)
# 
# # test section
# test_cds = cds_key_whole[cds_key_whole['District']=='Walnut Creek Elementary']


test_cds = cds_key[cds_key['District']=='Walnut Creek Elementary']
