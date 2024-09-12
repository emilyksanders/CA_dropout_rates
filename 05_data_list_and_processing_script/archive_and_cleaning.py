### Imports ###
import os
import pandas as pd
from waybackpy import WaybackMachineSaveAPI
import re
import time

### Set WD ###
def get_dfs_wd():
  wd_check = None
  while wd_check != "Yes":
    
    wd_list = ('\n').join(os.listdir())
  
    wd_prompt = f'''
    The current working directory is
    {os.getcwd()}.
    
    It contains
    {wd_list}
    
    If this is the correct directory (i.e., the list of dataframes is
    in it), please enter "Yes," with no punctuation.
    
    If it is not the correct directory, please enter the correct path,
    including any "backup dots" ("..") but WITHOUT QUOTATION MARKS.
    
    '''
    
    wd_check = input(wd_prompt)
    
    if wd_check.lower() != "yes":
      os.chdir(wd_check)
    elif wd_check.lower() == "yes":
      return 'Working directory set.'
    

get_dfs_wd()

### Get the user agent ###
# (we don't need this just yet, but input() is annoying)
user_agent = input('Who is working on this right now? \n')

### Convert user agent (can run as blocks now) ###
user_agent = user_agent.lower()
    
### Import the list ###
dfs = pd.read_csv('dfs_list.csv')
dfs.shape

### Define start_num ###
if dfs['id'].notna().sum()==0:
  start_num = 1
else:
  start_num = max(dfs['id'])+1

### Define categories (e.g., group DFs) ###
dfs['source_var'] = [
  re.match(r'^([A-Za-z]+)', u.split('/')[-1].split('.')[0])[0] 
  for u in dfs['original_url']]
  
### Define ID numbers ###
source_vars = list(dfs['source_var'].unique())

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
def assign_ids(dfs, source_vars, var_dict_rev):
  ''' Assign ID numbers to the source variables in dfs.
  dfs = the dataframe of data info
  source_vars = the list of variables that need/have IDs
  var_dict_rev = the reversed dictionarty where the variables  
                 are the keys and the numbers are the values
  '''
  for var in source_vars:
    sub_df = dfs[dfs['source_var']==var]
    # if NONE of them are NA (isna = False = 0 -> sum(0)=0), AND all the same
    if ((sub_df['id'].isna().sum()==0) and (len(list(sub_df['id'].unique()))==1)):
      continue
    elif ((sub_df['id'].isna().sum()==0) and (len(list(sub_df['id'].unique()))>1)):
      print(f'Multiple IDs for source_var {var}.')
      break
    elif sub_df['id'].notna().sum()==0: # if NOBODY is populated; ALL are NA
      rows = dfs[dfs['source_var']==var].index
      dfs.loc[rows, 'id'] = int(var_dict_rev[var])
    elif ((sub_df['id'].isna().sum()>0) and (len(list(sub_df['id'].unique()))>2)): # not all NA, some are populated but we have a value, an NA, and a mystery entry
      print(f'Multiple non-NA IDs for source_var {var}.')
      break
    elif ((sub_df['id'].isna().sum()>0) and (len(list(sub_df['id'].unique()))==2)): # not all NA, some are populated; we have a value, an NA, and nothing else
        rows = dfs[dfs['source_var']==var].index
        dfs.loc[rows, 'id'] = int(var_dict_rev[var])
    else:
      print(f'We got to else on {var}; something is broken.')
      break
  return dfs

dfs = assign_ids(dfs, source_vars, var_dict_rev)


### Archive them with the Wayback Machine ###

def archive(dfs):

  # define the condition (no archival url)
  cond = dfs['archive_url'].isna()
  
  for i in dfs[cond].index: #[1:]:
    # extra security
    s = str(dfs.loc[i, 'archive_url'])
    if ((s==s.replace(' ', '')) and (re.match(r'https://web.archive.org/web', s) is not None)):
      continue
    # now here we go
    else:
      # define the URL to save
      url = dfs.loc[i, 'original_url']
      # signs of life
      print(url)
  
      # create the save object
      save_api = WaybackMachineSaveAPI(url, user_agent)
      
      # hedge our bets
      try:
        print('trying to save')
        # save it, and gather the output url
        saved_url = save_api.save()
        # put that url in the df
        dfs.loc[i, 'archive_url'] = saved_url
        # collect the timestamp data
        t = save_api.timestamp()
        # put the archive date in the df
        dfs.loc[i, 'archive_date'] = t.strftime('%Y-%m-%d')
        # put the archive time in the df
        dfs.loc[i, 'archive_time_GMT'] = t.strftime('%H:%M')
        # record who did it
        dfs.loc[i, 'user_agent'] = user_agent
      except Exception as e:
        print(e)
        continue
      
      print('')
      
      # be polite to the server
      time.sleep(2)
  
  return dfs

test_dfs = archive(dfs)

### That ^ does not quite work. ###
### I'll come back to it later. ###

### For now, specify where to pull from. ###

def get_pull_urls():
  done = False
  
  while done == False:
    pull_urls = input('Pull original URLs (0) or archived URLs (1)? \n')
    
    if pull_urls == '0':
      pull_urls = dfs['original_url']
      done = True
    elif pull_urls == '1':
      pull_urls = dfs['archive_url']
      done = True
    else:
      print('Try again, ding dong!')
  
  return pull_urls

pull_urls = get_pull_urls()

### Create some containers
orig_col_names = {}


### For each df
for url in [pull_urls[1]]:
###  # Get its name
  name = url.split('/')[-1]
  name = name.split('.')[0]
  print('')
  print('='*15)
  print(name)
###  # Load it - let's see what we've got for seps
  failed_attempts = 0
  seps = ['\t', ',', ';']
  for s in seps:
    try: 
      df = pd.read_csv(url, low_memory = False, 
        encoding_errors='replace', sep = s)
      if not df.isna().all().all():
        print(s)
        break
    except:
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
  cond = dfs[dfs['original_url']==url].index
  df_id = int(dfs.loc[cond[0], 'id'])
###  # Reformat column names
  df.columns = [
    f"{x.lower().replace(' (', '--').replace(' ', '_').replace(')', '')}__df{df_id}" 
    for x in df.columns]
    
    #### TAKE THE SUFFIX OFF OF THE ONES WE'RE MERGING ON ####
    # colname.split('__')[0]
    
    
###  # Print all column names
  print(df.columns, flush = True)
###  # Any chance this could be easy?
  # identify aggregation columns
  agg = 'cats'
  agg_cols = []
  while agg.lower() != 'done':
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
###  # Specify the "master" district column
  print('')
  master_col = []
  while len(master_col)!=1:
    master_col = input('Which column is the "master" district column? \n\n')
    master_col = master_col.split(',')
  master_col = master_col[0]
###  # Specify the columns to "flatten" (i.e., the descriptive columns)
  print('')
  desc_cols = input('Which are the descriptive columns (to flatten)? \n\n')
  desc_cols = desc_cols.split(',')
###  # Specify the columns to preserve (i.e., the informative columns)
  print('')
  info_cols = input('Which are the informative columns (the data)? \n\n')
  info_cols = info_cols.split(',')
###  # Drop all other columns
  # everyone else goes on this list
  drop_cols = [col for col in list(df.columns) if (
    (col != master_col) and
    (col not in desc_cols) and
    (col not in info_cols) )]
  # create a toggle
  drop_inplace = False
  # edit the list as needed
  while drop_inplace == False:
    print("""
    Would you like to drop these columns? Enter Yes to proceed, 
    Add to add to the list, or Remove to remove
    """)
    print(drop_cols)
    drop_confirm = input()
    
    if drop_confirm.lower()=='yes':
      drop_inplace = True
    elif drop_confirm.lower()=='add':
      add_cols = input('Enter any additional columns to drop. \n\n')
      add_cols = add_cols.split(',')
      drop_cols.extend(add_cols)
    elif drop_confirm.lower()=='remove':    
      keep_cols = input('Enter any columns to NOT drop. \n\n')
      keep_cols = keep_cols.split(',')
      drop_cols = [col for col in drop_cols if col not in keep_cols]    
    
###  # For each descriptive column
  for col in desc_cols:
###  #   # Specify a descriptive suffix for the overall column
    print(f"The current column is {col}. What is its suffix?")
    suf = input('Enter suffix: \n\n')
###  #   # Specify descriptive suffixes for each level
###  #   # Split the df apart by these levels
###  #   # Apply suffixes to the informative columns
###  #   # Delete the original descriptive column
###  #   # Merge the separate DFs back together on 
###  #   # ###  all remaining descriptive columns
  
# save some of the interactive stuff to a JSON
# save it as a dictionary - i.e., 
# 'reporting_category__dfX' -> 'type' every time

# ###  # Any chance this could be easy?  -- TAKE 1
#   agg_cols = [col for col in list(df.columns) if 
#     ((re.search('aggregat', col)) or (re.search('level', col)))]
#   if len(agg_cols)>0:
#     # show what we've got
#     print(agg_cols)
#     print('')
#     # check them out
#     agg = input("""
#     If any of those columns are a 'level of aggregation' 
#     column, enter its name.  Otherwise, just hit enter.
#     """)
#     # proceed with that info
#     if (agg in list(df.columns)):

  # try: 
  #   df = pd.read_csv(url, low_memory = False, 
  #     encoding_errors='replace', sep = '\t')
  #   print('tab')
  # except:
  #   try: 
  #     df = pd.read_csv(url, low_memory = False, 
  #       encoding_errors='replace', sep = ',')
  #     print('comma')
  #   except:
  #     try: 
  #       df = pd.read_csv(url, low_memory = False, 
  #         encoding_errors='replace', sep = ';')
  #       print('semi-colon')
  #     except: 
  #       print('failed to load')
  #       continue
  
  
# assigning ID scraps
# for i in dfs.loc[cond, 'id'].index:
#   dfs.loc[i, 'id'] = start_num
#   start_num += 1
# 
#     
#     # define the conditions
#     # define condition 1 (no id number)
#     cond1 = dfs[dfs['id'].isna()].index
#     # define condition 2 (correct source_var)
#     cond2 = dfs[dfs['source_var']==var].index
#     # define the intersection (both conds = True)
#     cond = list(set(cond1).intersection(cond2))
#     # put it in order, JIC
#     cond.sort()
