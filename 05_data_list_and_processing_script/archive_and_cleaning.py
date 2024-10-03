### Imports ###
import os
import pandas as pd
from waybackpy import WaybackMachineSaveAPI
import re
import time
import requests
import io
from archive_and_cleaning_functions import (my_date, clear, 
  get_dfs_wd, assign_ids, archive, get_pull_urls, master_cols)
# --- something like that. 
# define functions elsewhere and then import them to here
# so that this script can be a lot shorter and easier to read

#########################################
############ !! IMPORTANT !! ############
##### RUN FUNCTIONS SCRIPT FIRST!!! #####
############ !! IMPORTANT !! ############
#########################################

### Set WD ###
get_dfs_wd()

### Get the user agent ###
# (we don't need this just yet, but input() is annoying)
user_agent = input('Who is working on this right now? \n')

### Convert user agent (can run as blocks now) ###
user_agent = user_agent.lower()
    
### Import the list of dfs ###
dfs = pd.read_csv('dfs_list.csv')
dfs.shape

### Import the list of districts ###
base_df = pd.read_csv('county-district_code_key.csv')

### Define start_num ###
if dfs['id'].notna().sum()==0:
  start_num = 1
else:
  start_num = max(dfs['id'])+1
print(start_num)

### Define categories (e.g., group DFs) ###
# this version will overwrite what's there
# dfs['source_var'] = [
#   re.match(r'^([A-Za-z]+)', u.split('/')[-1].split('.')[0])[0] 
#   for u in dfs['original_url']]

#only for the NA ones, hopefully
cond = dfs[dfs['source_var'].isna()].index

dfs.loc[cond, 'source_var'] = [
  re.match(r'^([A-Za-z]+)', u.split('/')[-1].split('.')[0])[0] 
  for u in dfs.loc[cond, 'original_url']]
  
### Define ID numbers ###
source_vars = list(dfs['source_var'].unique())
print(source_vars)

# seed a dictionary
var_dict = {'1': 'chronicabsenteeism'}

# find which ones need an ID
for var in source_vars:
  if var in var_dict.values():
    continue
  else:
    # put it in the dictionary
    var_dict[str(start_num)] = var
    start_num += 1

# get a backwards copy too
var_dict_rev = {v:k for k, v in var_dict.items()}

# assign the numbers
dfs = assign_ids(dfs, source_vars, var_dict_rev)

### Archive them with the Wayback Machine ###
dfs = archive(dfs)

### Specify where to pull from. ###
pull_urls = get_pull_urls(dfs, 'archive') # 'originals' for originals

### Create some containers
orig_col_names = {}
cleaned_dfs = []
all_merge_cols = {}
all_suffixes = {}

### For each df
for url in pull_urls:

###  # Get it in and see what it's about

###  # Get its name
  name = url.split('/')[-1]
  name = name.split('.')[0]
  print('')
  print('='*15)
  print(name)

###  # are you sure you want to do this?
  # getting the ROW that corresponds to the url we're on
  cond = dfs[pull_urls==url].index[0]
  if dfs.at[cond, 'cleaned']==True:
    do_it_again = input(f"""\
    This df, {name} is already marked as cleaned. If you would like to \n \
    rerun the process, including overwriting previously defined dictionary \n \
    entries, enter YES. Otherwise, enter NO to proceed to the next df.\n\n\n \
    """)
    if do_it_again != 'YES':
      continue
    elif do_it_again == 'YES':
      print('Ok, here we go, overwriting stuff!')
      time.sleep(3)

###  # Load it - let's see what we've got for seps
  
  # loading from the achive is kind of annoying. gotta do this
  # thanks to stackoverflow (and my dad!)
  # https://stackoverflow.com/questions/32400867/pandas-read-csv-from-url
  t = requests.get(url).text
  
  # create a counter to monitor sep situation
  failed_attempts = 0
  seps = ['\t', ',', ';']
  
  # try and try to read it in
  for s in seps:
    try: 
      df = pd.read_csv(io.StringIO(t), low_memory = False, 
        encoding_errors='replace', sep = s)
      if not df.isna().all().all():
        print(s)
        break
    except Exception as e:
      print(url)
      print(e)
      failed_attempts+=1
      continue
  
  if failed_attempts==len(seps):
   print('none of the seps worked.')
   continue

###  # Save and show some information
  orig_col_names[name] = list(df.columns)
  print('')
  print(list(df.columns), flush = True)

###  # Define a DF ID# for a suffix
  cond = dfs[pull_urls==url].index
  df_id = int(dfs.loc[cond[0], 'id'])

###  # Reformat column names
  # create a container
  new_col_names = []
  
  # for every column name
  for i in list(df.columns):
    title_case = re.search(r'[a-z][A-Z]', i) # first check for TitleCase
    while title_case != None: # gotta get 'em all!
      letters = title_case[0] # yank the letters out of the object
      i = i.replace(letters, letters[0]+'_'+letters[1].lower()) # insert _
      title_case = re.search(r'[a-z][A-Z]', i) # check again
    # once all the TitleCases are gone, do the reformatting that 
    # used to be in the list comp, and append it to that list
    new_col_names.append(f"{i.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__df{str(df_id).zfill(2)}")
    
  # check my work, reassign that list to be the new column names
  if len(list(df.columns))==len(new_col_names):
    df.columns = new_col_names
  else:
    print(f'wrong number of columns after reformatting for df_id: {df_id}, {url}')
    break

###  # Clear the console for this next bit
  clear()

###  # Filtering #  ###

###  # Any chance this could be easy?
  # identify aggregation columns
  agg = 'cats'
  agg_cols = []
  while agg.lower() != 'done':
    # Print all column names
    print(df.columns, flush = True)
    # ask for levels of aggregation
    agg = input("""
      If any of those columns are a 'level of aggregation' 
      column, enter its name.  One at a time, please.  When 
      you are done, or if there are none, enter 'Done.'
      """)
    if agg in list(df.columns):
      # pick the level
      print(df[agg].value_counts(dropna = False), flush = True)   # may have to wait for this
      level = input('Which of these levels do you want? \n\n')
      # narrow the df
      df = df[df[agg]==level]
      # sanity check
      print('', flush = True)
      print(df[agg].value_counts(dropna = False), flush = True)
      # set these guys up for dropping
      agg_cols.append(agg)
    else:
      continue 
###  # Specify "master" columns
  # create a dictionary container
  merge_cols = {}
  
  # district
  x = master_cols(df, 'district')
  if x is not None:
    merge_cols[x[0]] = 'district'
  
  # year
  x = master_cols(df, 'year')
  if x is not None:
    merge_cols[x[0]] = 'year'
  
  # cds code
  x = master_cols(df, 'cds_code')
  if x is not None:
    merge_cols[x[0]] = 'cds_code'
  
  # county
  x = master_cols(df, 'county')
  if x is not None:
    merge_cols[x[0]] = 'county'
  
  # save the merge cols
  all_merge_cols[name] = merge_cols
  
  # check my work and remove the suffixes
  # are the keys (suffixed) longer than the values (unsuffixed & standardized)?
  # the operator is <= so this should be a sum of FALSES, = 0
  len_check = sum([len(k) <= len(v) for k, v in merge_cols.items()])
  
  # check that the df is the right shape AND that the lengths are right
  if ((df.rename(columns = merge_cols).shape == df.shape) and (len_check==0)):
    df.rename(columns = merge_cols, inplace = True)
  else:
    print(f'something is wrong in the master column section for df_id: {df_id}, {url}')
    break

###  # clean up again
###  # Clear the console for this next bit
  clear()

###  # Print all column names
  print(df.columns, flush = True)

###  # Now let's make sure the year isn't screwed up
  # there should only be one school year per file
  year_check = 'cats'
  if df['year'].nunique()!=1:
    while year_check.lower()!='yes':
      print(df['year'].value_counts(dropna = False))
      print('''There appear to be multiple years. These MUST \
      \nbe flattened before any other descriptive variable.''')
      year_check = input('Please confirm by typing yes')

###  # Specify the columns to "flatten" (i.e., the descriptive columns)
  print('')
  desc_cols = input('Which are the descriptive columns (to flatten)? \n\n')
  desc_cols = desc_cols.split(',')
  ###  add syntax to deal with quotation marks and spaces ###

###  # Specify the columns to preserve (i.e., the informative columns)
  print('')
  info_cols = input('Which are the informative columns (the data)? \n\n')
  info_cols = info_cols.split(',')

###  # Drop all other columns
  # everyone else goes on this list
  drop_cols = [col for col in list(df.columns) if (
    (col not in merge_cols.values()) and
    (col not in desc_cols) and
    (col not in info_cols) )]
  # create a toggle
  drop_inplace = False
  # edit the list as needed
  while drop_inplace == False:
    print(drop_cols)
    print("""
    Would you like to drop these columns? Enter Yes to proceed, 
    Add to add to the list, or Remove to remove from the list.
    """)
    drop_confirm = input()
    
    if drop_confirm.lower()=='yes':
      drop_inplace = True
    elif drop_confirm.lower()=='add':
      add_cols = input('Enter any additional columns to drop. \n\n')
      add_cols = add_cols.split(',')
      drop_cols.extend(add_cols)
    elif drop_confirm.lower()=='remove':    
      remove_cols = input('Enter any columns to NOT drop. \n\n')
      remove_cols = remove_cols.split(',')
      drop_cols = [col for col in drop_cols if col not in remove_cols]
    else:
      print('You have entered an invalid string. Please try again.')
    
  # check my work
  now_rows = df.shape[0]
  now_cols = df.shape[1]
  new_rows = df.drop(columns = drop_cols).shape[0]
  new_cols = df.drop(columns = drop_cols).shape[1]
  
  if ((now_rows!=new_rows) or (now_cols != new_cols+len(drop_cols))):
    print('''something wrong with drop cols on df_id: {df_id}, url: {url}. \
    \n drop_cols: {drop_cols}''')
    break
  else:
    # when that's done (the list of columns to drop is complete)
    df.drop(columns = drop_cols, inplace = drop_inplace)

# create a dictionary to hold ALL the suffixes that come out of this df
  suffix_list = {}

###  # For each descriptive column
  for col in desc_cols:

###  #   # Create a container list that will hold all the sub_dfs
    sub_list = []

###  #   # Specify a descriptive suffix for the overall column
    print(f""" \
    \n The current column is {col}. \
    \n What is its overall suffix? \
    """)
    suf1 = input('Enter suffix: \n\n')
    
    # write that down
    

###  #   # Specify descriptive suffixes for each level
    col_vals = list(df[col].unique())
    
    suffixes = input(f""" \
    \n {col} has the following levels: \
    \n {col_vals} \
    \n \
    \n Please enter a list of suffixes corresponding to each \
    \n of those values. Separate each suffix with a comma. Do \
    \n NOT wrap the suffixes in quotation marks, and do NOT use \
    \n any characters that do not belong in column names. \
    \n \
    \n Enter suffixes: \
    \n """)
    
    # clean up that input
    suffixes = suffixes.split(',')
    suffixes = [s.strip() for s in suffixes]
    # and JIC
    suffixes = [f"{i.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}" 
      for i in suffixes]
      
    ### create a dictionary of suffixes
    
    # create a container
    suffix_dict = {}
    # fill it
    for i, j in list(zip(col_vals, suffixes)):
      print(i, j)
      suffix_dict[i] = j
    
    # save that
    suffix_list[col] = [suf1, suffix_dict]
        

###  #  Do the stuff to it

# for each level of the descriptive column...
    for i in col_vals:    

###  #   # Pull out the right level-suffix
      suf2 = suffix_dict[i]

###  #   # Split the df apart by these levels
      sub_df = df[df[col]==i]
      
###  #   # Get a list of the non-info columns for later
      shared_cols = [c for c in sub_df.columns if ((c not in info_cols) and (c!=col))]
      
###  #   # Apply suffixes to the informative columns
      new_sub_col_names = [f'{c}-{suf1}-{suf2}' if (c in info_cols) else c for c in sub_df.columns]
      
      # check my work
      if len(new_sub_col_names)==sub_df.shape[1]:
        sub_df.columns = new_sub_col_names
      else:
        print(f'''something is broken assigning col names to a sub_df.\
        \n df_id: {df_id} \
        \n col: {col} \
        \n col_val level: {i} \
        \n suf1: {suf1} \
        \n suf2: {suf2} \
        \n current names: {list(sub_df.columns)}, shape: {sub_df.shape} \
        \n new names: {new_sub_col_names}, length: {len(new_sub_col_names)} \
        \n Ending operation now.''')
        break
        
###  #   # Delete the original descriptive column
      # safety first
      old_shape = sub_df.shape
      new_shape = sub_df.drop(columns = [col]).shape
      if ((old_shape[0]==new_shape[0]) and (old_shape[1]==(new_shape[1]-1))):
        sub_df.drop(columns = [col], inplace = True)
      else:
        print(f'''something is broken dropping a desc column.\
        \n df_id: {df_id} \
        \n col: {col} \
        \n col_val level: {i} \
        \n suf1: {suf1} \
        \n suf2: {suf2} \
        \n current names: {list(sub_df.columns)}, shape: {sub_df.shape} \
        \n new names: {sub_df.drop(columns = [col]).columns}, shape: {sub_df.drop(columns = [col]).shape} \
        \n Ending operation now.''')
        break

###  #   # storage the sub_df to be remerged later
      sub_list.append(sub_df)      

###  #   # Merge the separate DFs back together on 
    # define columns to merge on
    merge_keys = ['year', 'district', 'cds_code']
    merge_keys = [k for k in merge_keys if k in list(sub_df.columns)]
    merge_keys = merge_keys + shared_cols
    
    new_df = base_df.merge(sub_list[0], 
      how = 'outer', on = merge_keys, suffixes = (None, '+dupe'))
    
    for i in sub_list[1:]:
      new_df = new_df.merge(i,
        how = 'outer', on = merge_keys, suffixes = (None, '+dupe'))

###  #   # Save the merged, flattened df to a list 
#             #(there'll be one df here PER desc column PER df)
    cleaned_dfs.append(new_df)

# save some of the interactive stuff to a JSON; as a dictionary
  all_suffixes[name] = [url, suffix_list]
  # THAT'S THE LAST THING FOR EACH URL
  # BACK TO THE TOP!!
################################################################
#################### !!!!! END OF LOOP !!!! ####################
################################################################

# once that huge loop is totally done, do the BIG merge of all dfs

# one by hand
big_df = base_df.merge(cleaned_dfs[0], 
  how = 'outer', on = list(base_df.columns), suffixes = (None, '+dupe'))

# and the rest
for i in cleaned_dfs[1:]:
  big_df = big_df.merge(i, how = 'outer', 
    on = list(base_df.columns), suffixes = (None, '+dupe'))

# save that df
# I'm terrified of how big this will be, but here we go!
big_df.to_csv(f'../02_data_cleaned/big_df_{my_date()}_{user_agent}.csv', index = False)

# save the dictionaries
os.chdir('../04_dictionaries')

f = "var_dict.json"
with open(f, 'w', encoding = "utf-8") as file:
  json.dump(var_dict, file, indent=2)

f = "var_dict_rev.json"
with open(f, 'w', encoding = "utf-8") as file:
  json.dump(var_dict_rev, file, indent=2)

f = "orig_col_names.json"
with open(f, 'w', encoding = "utf-8") as file:
  json.dump(orig_col_names, file, indent=2)

f = "all_merge_cols.json"
with open(f, 'w', encoding = "utf-8") as file:
  json.dump(all_merge_cols, file, indent=2)

f = 'all_suffixes.json'
with open(f, 'w', encoding = "utf-8") as file:
  json.dump(all_suffixes, file, indent=2)



