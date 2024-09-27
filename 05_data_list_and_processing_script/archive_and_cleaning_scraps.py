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

  #### TAKE THE SUFFIX OFF OF THE ONES WE'RE MERGING ON ####
  
  ## take 1 VVV  ##
  # # define the types of columns that we're probably after
  # merge_col_names = ['academic_year', 'year', 'school_year', 
  #   'district', 'district_code', 'school_district']
  # # look for them
  # merge_cols = {'seed': 'dictionary'}
  # for i in merge_col_names:
  #   # merge_cols.extend([c.split('__')[0] for c in new_col_names if re.search(i, c)])
  #   merge_cols[c] = c.split('__')[0] for c in new_col_names if re.search(i, c)
