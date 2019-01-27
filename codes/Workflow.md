# Workflow of Data-Preprocessing

## Collect and clean stats data
1. Make a list of dataframes containing *NFL-Combines Data*

    - list_df_Combines = **createDFs(**'comb', 2008, 2014**)**

2. Make a list of dataframes containing *Rushing stats*

    - list_df_Rush = **createDFs(**'rush', 2008, 2014**)**

3. Make a list of dataframes containing *Passing stats*

    - list_df_Pass = **createDFs(**'pass', 2008, 2014**)**

4. Make a list of dataframes containing *Receiving stats*

    - list_df_Rec = **createDFs(**'rec',2008, 2014**)**

5. Clean up Player names, by removing non alpha-numeric characters 
    - list_df_Pass_tmp = **cleaningupColumn(**list_df_Pass, ['Player']**)**
    - list_df_Rec_tmp = **cleaningupColumn(**list_df_Rec, ['Player']**)**
    - list_df_Rush_tmp = **cleaningupColumn(**list_df_Rush, ['Player']**)**

6. Merge *Rush, Pass,* and *Rec Stats* together
    - list_df_Pass_clean = **getdfNameYardsTd(**list_df_Pass_tmp**)**
    - list_df_Rush_clean = **getdfNameYardsTd(**list_df_Rush_tmp**)**
    - list_df_Rec_clean = **getdfNameYardsTd(**list_df_Rec_tmp**)**

7. Make subsets of NFL-Combine dataframes for each of the 3 positions
    - list_df_Combines_QB = **makeSubsetPos(**list_df_Combines, ['QB']**)**
    - list_df_Combines_RB = **makeSubsetPos(**list_df_Combines, ['RB']**)**
    - list_df_Combines_WR = **makeSubsetPos(**list_df_Combines, ['WR']**)**

8. Clean up draft_info column in list of df_Combines
    - list_df_Combines_QB = **addDraftInfo(**list_df_Combines_QB**)**
    - list_df_Combines_RB = **addDraftInfo(**list_df_Combines_RB**)**
    - list_df_Combines_WR = **addDraftInfo(**list_df_Combines_WR**)**

9. Aggregate Stats(Yds+TD)-dataframes into 4-year sets
    - list_df_Pass_agg1234 = **addYearsTD(**list_df_Pass_clean, '2008', '2012'**)**
    - list_df_Rush_agg1234 = **addYearsTD(**list_df_Rush_clean, '2008', '2012'**)**
    - list_df_Rec_agg1234 = **addYearsTD(**list_df_Rec_clean,'2008', '2012'**)**

10. Rename columns Years columns
  - list_df_Pass_agg1234 = **renamingYrsColumns(**list_df_Pass_agg1234**)**
  - list_df_Rush_agg1234 = **renamingYrsColumns(**list_df_Rush_agg1234**)**
  - list_df_Rec_agg1234 = **renamingYrsColumns(**list_df_Rec_agg1234**)**

11. Merge aggregated (4yr) Stats data with the NFL_Combine data. Use methods='left' to keep only players that are invited to the NFL_Combine
    - list_4yrSet_QB = **mergeCombYdsTD(**list_df_Combines_QB, list_df_Pass_agg1234, method='left'**)**
    - list_4yrSet_RB = **mergeCombYdsTD(**list_df_Combines_RB, list_df_Rush_agg1234, method='left'**)**
    - list_4yrSet_WR = **mergeCombYdsTD(**list_df_Combines_WR, list_df_Rec_agg1234, method='left'**)**

12. Count how many duplicates (if any) in the df's
    - **countDuplicates(**list_4yrSet_QB**)**
    - **countDuplicates(**list_4yrSet_RB**)**
    - **countDuplicates(**list_4yrSet_WR**)**

13. (b) First try to drop all duplicates

    - list_4yrSet_QB = [df.drop_duplicates() for df in list_4yrSet_QB]
    - list_4yrSet_RB = [df.drop_duplicates() for df in list_4yrSet_RB]
    - list_4yrSet_WR = [df.drop_duplicates() for df in list_4yrSet_WR]

14. Then,  find those duplicates in the specific df's 

    - **findDuplicates(**list_4yrSet_WR[2]**)**

15. (c) Check the original websites for accuracy and drop the inaccurate rows (duplicates)

    - list_4yrSet_RB[2] = list_4yrSet_RB[2].drop([36,37,38]) 

    - list_4yrSet_RB[7] = list_4yrSet_RB[7].drop([18,19,20,21,22,23,24]) # Adrian Peterson

    - list_4yrSet_RB[5] = list_4yrSet_RB[5].drop([12])                   # Chris Henry

    - list_4yrSet_WR[7] = list_4yrSet_WR[7].drop([9])                    # Chris Davis

    - list_4yrSet_WR[7] = list_4yrSet_WR[7].drop([55,54,40,41,42,43,44,45,46,47,48,49,50,51,53]) # Steve Smith

      

## Collect and clean Salary data
1. Make a list of base *Salaries*
    - list_df_Salaries = **createDFsalaries(**2008, 2018**)**
2. Concatenate Salaries into a dataframe
    - df_Salary_agg = **bindSal(**list_df_Salaries, 2008**)**
3. Adjust the value of past years' salaries, based on US inflation rate
    - df_Salary_agg = **includeInflation(**df_Salary_agg, 2003**)**



## Joining Salary and Stat Dataframes
1. Concatenate dataframes at each position
    - df_Concat_QB = **concatAll4YrSets(**list_4yrSet_QB**)**
    - df_Concat_RB = **concatAll4YrSets(**list_4yrSet_RB**)**
    - df_Concat_WR = **concatAll4YrSets(**list_4yrSet_WR**)**

2. Renaming last column (e.g.,"Sal_2013") into "salary", so we can merge df's on it later
    - list_data_QB = **renameSalCol(**list_data_QB**)**
    - list_data_RB = **renameSalCol(**list_data_RB**)**
    - list_data_WR = **renameSalCol(**list_data_WR**)**

3. (a) Looking for and handling duplicates at QB position
    - print(**countDuplicates(**list_data_QB**)**)
    - list_data_QB = [df.drop_duplicates() for df in list_data_QB]
    - list_data_QB[5] = list_data_QB[5].drop([149]) # Alex smith QB not TE

4. (b) Looking for and handling duplicates at RB
    - print(**countDuplicates(**list_data_RB**)**)
    - **findDuplicates(**list_data_RB[7]**)**
    - list_data_RB[7] = list_data_RB[7].drop([1])

5. (c) Looking for and handling duplicates at WR
    - print(**countDuplicates(**list_data_WR,4**)**)
    - list_data_WR = [df.drop_duplicates() for df in list_data_WR]
    - findDuplicates(list_data_WR[10])  
    - list_data_WR[5] = list_data_WR[5].drop([12,15,16])    # Chris Henry
    - list_data_WR[6] = list_data_WR[6].drop([13])          # Derek Hagan
    - list_data_WR[7] = list_data_WR[7].drop([39])          # Steve Smith 
    - list_data_WR[10] = list_data_WR[10].drop([43, 47,55]) # Mike Williams
6. Concatenate dataframes for each position
    - df_Concat_QB = **concatAll4YrSets(**list_data_QB**)**.reset_index()

    - df_Concat_RB = **concatAll4YrSets(**list_data_RB**)**.reset_index()

    - df_Concat_WR = **concatAll4YrSets(**list_data_WR**)**.reset_index()

      


## Cleaning Concatenated DataFrame for EDA and Modeling

1. Fill in NAN with zeros

   - df_Concat_QB= df_Concat_QB.fillna(0)
   - df_Concat_RB= df_Concat_RB.fillna(0)
   - df_Concat_WR= df_Concat_WR.fillna(0)

2. Look at attrition rate, what % survive 5years in NFL

   - calcDropOuts(df_Concat_QB, 2000, 2014)
   - calcDropOuts(df_Concat_RB, 2000, 2014)
   - calcDropOuts(df_Concat_WR, 2000, 2014)

3. Convert height from Foot-Inches to (only) Inches

   - df_Concat_QB = engineerHt(df_Concat_QB)
   - df_Concat_RB = engineerHt(df_Concat_RB)
   - df_Concat_WR = engineerHt(df_Concat_WR)

4. Renaming column name: '40yd' into dash'

   - df_Concat_QB.rename(columns = {'40yd':'dash'}, inplace=True)
   - df_Concat_RB.rename(columns = {'40yd':'dash'}, inplace=True)
   - df_Concat_WR.rename(columns = {'40yd':'dash'}, inplace=True)

5. Select columns to use 

   - select_columns = ['Player','ht_inch','draftTeam','draftStat','draftRnd',
                           'Wt','dash',
                          'Yds_1','TD_1','Yds_2','TD_2','Yds_3','TD_3',
                          'Yds_4','TD_4','Salary']
   - df_QB = df_Concat_QB[select_columns]
   - df_RB = df_Concat_RB[select_columns]
   - df_WR = df_Concat_WR[select_columns]

6. Find Players that survive 4 years,i.e., those receiving payment on 4th year

   - df_QB_active = df_QB[df_QB['Salary'] != 0]
   - df_RB_active = df_RB[df_RB['Salary'] != 0]
   - df_WR_active = df_WR[df_WR['Salary'] != 0]

7. Converting STATS and Salaries to numeric values

   - intcols = ['Yds_1', 'TD_1','Yds_2','TD_2','Yds_3','TD_3','Yds_4','TD_4']
     for col in intcols:
         df_QB_active[col] = df_QB_active[col].astype(int)
         df_RB_active[col] = df_RB_active[col].astype(int)
         df_WR_active[col] = df_WR_active[col].astype(int)

   - df_QB_active['Salary'] = df_QB_active['Salary'].astype(float)
     df_QB_active['dash'] = df_QB_active['dash'].astype(float)
     df_QB_active['draftRnd'] = df_QB_active['draftRnd'].apply(removeTh)

   - df_RB_active['Salary'] = df_RB_active['Salary'].astype(float)
     df_RB_active['dash'] = df_RB_active['dash'].astype(float)
     df_RB_active['draftRnd'] = df_RB_active['draftRnd'].apply(removeTh)

   - df_WR_active['Salary'] = df_WR_active['Salary'].astype(float)
     df_WR_active['dash'] = df_WR_active['dash'].astype(float)
     df_WR_active['draftRnd'] = df_WR_active['draftRnd'].apply(removeTh)

8. Saving dataframes
	- df_QB_active.to_csv('QBactive_4th.csv')
	  df_RB_active.to_csv('RBactive_4th.csv')
	  df_WR_active.to_csv('WRactive_4th.csv')

