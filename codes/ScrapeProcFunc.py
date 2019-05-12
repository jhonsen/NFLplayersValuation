
# Combining URL's to scrape from
def combineUrl(yearStart, yearEnd):
    '''function returns a list of urls from yearStart to yearEnd, for NFL combine results
    '''
    urls = []
    for ind in range(yearStart, yearEnd+1):
        url = 'https://www.pro-football-reference.com/draft/{}-combine.htm'.format(ind)
        urls.append(url)
    return urls

# making soups
def tabulateSoup(urls, html_tag, attribute={}):
    '''function returns a list of soups (), obtained BeautifoulSoup(page, 'lxml') parser
    inputs:
        urls - list of urls to investigate
        html_tag - tag to search for (e.g., 'table', or 'a')
        attribute - is dictionary of html tags identifiers
    '''
    import requests
    from bs4 import BeautifulSoup

    list_tables = []

    for each in urls:
        response = requests.get(each)
        if response.status_code == 200:
            print('url reached, ', each)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        list_tables.append(soup.find(html_tag, attrs=attribute))
    return list_tables

# Collecting table headings
def makeVariables(soups):
    '''function returns a list of variables from table heading
    The variables are extracted from table headings of the first table (only)
    input:
        soups - is list of soups from tabulateSoup() function
    '''

    rows = [row for row in soups[0].find_all('tr')]
    var_selector = rows[0].find_all('th')
    variables = [var_selector[i].text for i in range(len(var_selector))]
    return variables

# Make dictionaries
def makeDictionaries(soups, variables):
    '''function returns a list of dictionaries
    input:
        soups - is list of soups from tabulateSoup()
        variables - is the table headings
    '''
    dictionaries= []

    for each in soups:

        collectionDict = dict()
        collectionDict[makeVariables(soups)[0]] = []

        # Iterating over each row
        combvariables = each.find_all('tr')
        for ind, var in enumerate(combvariables):

            # Adding players in column
            if var.find_all('th')[0].text == 'Player':
                continue
            else:
                collectionDict['Player'] += [var.find_all('th')[0].text]

            # Iterating over each column
            for key,val in zip(variables[1:], combvariables[ind].find_all('td')):
                if key not in collectionDict.keys():
                    collectionDict[key] = [val.text]
                else:
                    collectionDict[key] += [val.text]
        dictionaries.append(collectionDict)

    return dictionaries

# Print out dataframe info()
def reportResult(dictionaries):
    ''' function prints out tuples of keys-size pairs from a list of dictionaries
    Input:
        dictionaries - list of dictionaries
    '''
    for diction in dictionaries:
        print('\n')
        print(*zip(diction.keys(),
          [len(val) for key,val in diction.items()]), sep='\n')

# Turning Dictionaries into Dataframes
def toPandas(dictionaries, statname, yearStart, yearEnd):
    '''Function creates dataframes in global variable space
    input:
        dictionaries - list of dictionaries
        statname  - stats requestion,(options: 'comb', 'pass', 'rush')
        yearStart - starting year to scrape
        yearEnd   - ending year to scrape
    '''
    import pandas as pd

    listdfs =[]

    for diction, yr in zip(dictionaries, range(yearStart, yearEnd+1)):
        globals()['df%s_%s' %(statname,yr)] = pd.DataFrame(diction)
        listdfs.append(globals()['df%s_%s' %(statname,yr)])

    return listdfs

# Wrapper FUNCTION to Make Dataframes
# This function calls the 5 functions above
def createDFs(statname, yearStart, yearEnd, annotrep=True, rep=False):
    ''' Function scrapes, tabulates soup objects and makes dataframes, by
    calling other functions: combineUrl() or (rushUrl(), passUrl(), recUrl()),
                        makeVariables(), tabulateSoup(), reportResult(),
                        toPandas()
    Input:
        statname  - stats requestion,(options: 'comb', 'pass', 'rush')
        yearStart - starting year to scrape
        yearEnd   - ending year to scrape
        annotrep  - True (to list out df names) or False
        rep       - True (to return df.info()) or False
    '''
    if statname =='comb':
        urllist = combineUrl(yearStart, yearEnd)
    elif statname == 'rush':
        urllist = rushUrl(yearStart,yearEnd)
    elif statname == 'pass':
        urllist = passUrl(yearStart,yearEnd)
    elif statname == 'rec':
        urllist = recUrl(yearStart,yearEnd)

    listab = tabulateSoup(urllist, 'table', attribute={'class':'sortable stats_table'})
    print("finished collecting soups")

    if statname =='comb':
        allvars = makeVariables(listab)
        print('finished making variables')
        dixies = makeDictionaries(listab, allvars)
    elif statname =='rush' or statname =='pass' or statname =='rec':
        dixies = makeRushDictionaries(statname, listab)

    if rep == True:
        reportResult(dixies)

    print('finished making dictionaries')

    listdfs = toPandas(dixies, statname, yearStart, yearEnd)
    print('finished making dataframes')

    if annotrep == True:
        print("\n {} Pandas df's created, which are:\n".format(len(dixies)))
        print(*['df{}_{}'.format(statname, each) \
                for each in range(yearStart, yearEnd+1)],
              sep ='\n')

    return listdfs

# SEtting up URLS to scrape Rushing Stats
def rushUrl(yearStart, yearEnd):
    '''function returns a list of urls from yearStart to yearEnd
    '''
    urls = []
    for ind in range(yearStart, yearEnd+1):
        url = 'https://www.pro-football-reference.com/years/{}/rushing.htm'.format(ind)
        urls.append(url)
    return urls

def passUrl(yearStart, yearEnd):
    '''function returns a list of urls from yearStart to yearEnd
    '''
    urls = []
    for ind in range(yearStart, yearEnd+1):
        url = 'https://www.pro-football-reference.com/years/{}/passing.htm'.format(ind)
        urls.append(url)
    return urls

def recUrl(yearStart, yearEnd):
    '''function returns a list of urls from yearStart to yearEnd
    '''
    urls = []
    for ind in range(yearStart, yearEnd+1):
        url = 'https://www.pro-football-reference.com/years/{}/receiving.htm'.format(ind)
        urls.append(url)
    return urls

# Making more dictionaries for Rush, Pash, etc.
def makeRushDictionaries(statname, tables):
    '''function returns a list of dictionaries
    input:
        tables - is list of tables from tabulateSoup()

    '''
    if statname=='rush':
        headings = ['Player','team','age','pos','g','gs','rush_att','Yds','TD','rush_long',
           'rush_yds_per_att','rush_yds_per_g','fumbles']
    elif statname =='pass':
        headings = ['Player','Tm','Age','Pos','G','GS','QBrec','Cmp','Att','Cmp%','Yds','TD','TD%','Int',
                   'Int%','Lng','Y/A','AY/A','Y/C','Y/G','Rate','QBR','Sk','Ydslost','NY/A','ANY/A','Sk%',
                   '4QC','GWD']
    elif statname == 'rec':
        headings = ['Player','Tm','Age','Pos','G','GS','Tgt','Rec','Catch%','Yds','Y/R','TD','Lng','R/G','Y/G','Fumb']
#     Tm	Age	Pos	G	GS	Tgt	Rec	Ctch%	Yds	Y/R	TD	Lng	R/G	Y/G	Fmb

    dictionaries = []

    for table in tables:

        collectionDict = dict()

        rows = table.find_all('tbody')[0].find_all('tr')

        for ii in range(len(rows)):
            for key,val in zip(headings, [temp.text for temp in rows[ii].find_all('td')]):
                if key not in collectionDict:
                    collectionDict[key] = [val]
                else:
                    collectionDict[key] += [val]

        dictionaries.append(collectionDict)

    return dictionaries

# Scraping Base Salaries
def salaryUrl(yearStart, yearEnd):
    '''function returns a list of urls from yearStart to yearEnd
    '''
    urls = []
    for ind in range(yearStart, yearEnd+1):
        url = 'https://www.spotrac.com/nfl/rankings/{}/base/offense'.format(ind)
        urls.append(url)
    return urls

# Making soups usin SELENIUM (used for salary)
def tabulateSoup2(urls):
    '''function returns a list of html tag
    function uses Selenium and web driver, so a chrome browswer will open interactively
    inputs:
        urls - list of urls to investigate
        html_tag - tag to search for (e.g., 'table', or 'a')
    '''
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    import os
    from bs4 import BeautifulSoup

    chromedriver = '/Applications/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver

    list_tables =[]

    driver = webdriver.Chrome(chromedriver)
    for each in urls:
        driver.get(each)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        list_tables.append(soup)

    driver.close()

    return list_tables

# Extracting Names from table
def getNames(soupObj):
    '''Function returns the name or Salary of player from SpoTrac pages
    Input:
        soupObj - is the soup Object
    '''

    Values = [each.text for each in soupObj.findAll('a', attrs={'class':'team-name'})]
    return Values

# Get salaries from pages
def getSalaries(soupObj):
    ''' Function returns the name or Salary of player from SpoTrac pages
    Input:
        soupObj - soup object
    '''
    listSal = []
    for each in soupObj.findAll('span', attrs={'class':'info'}):
        strSal = each.text.strip().split('$')[1]
        numSal = float(strSal.replace(',', ''))
        listSal.append(numSal)

    return listSal

# combining Name column with salaries over multiple years into lists of dataframes
def bindNameSaltoPd(soupObjects, yearStart, yearEnd):
    '''function returns list of dataframes
    input:
        soupbObjects- objects created by tabulateSoup2(), which is a list of Soups
        yearStart   - first year of
        yearEnd     - last year of
    '''

    import pandas as pd
    import numpy as np
    years = range(yearStart, yearEnd+1)

    listdfs = []
    for ind, obj in enumerate(soupObjects):
        listNames = getNames(obj)
        listSal = getSalaries(obj)
        globals()['dfSal_%s' %(years[ind])] = pd.DataFrame(np.c_[listNames, listSal],
                                                   columns = ['Player', 'base'])
        listdfs.append(globals()['dfSal_%s' %(years[ind])])

        print('dfSal_%s created' %(years[ind]))
        if ind == len(soupObjects)-1:
            print("Total {} df's created".format(ind+1))

    return listdfs

# Make a list of dataframes from a specific graduating class
def createDFsalaries(yearStart, yearEnd):
    '''Function returns a list of dataframes as objects,
    function calls testURL(), soupObjs(), bindNameSaltoPd()
    Input:
        yearStart - the first year to scrape
        yearEnd -   the last year to scrape
    '''
    from bs4 import BeautifulSoup

    print('opening Chrome for scraping')
    testURL = salaryUrl(yearStart,yearEnd)
    soupObjs = tabulateSoup2(testURL)
    listdfs = bindNameSaltoPd(soupObjs, yearStart, yearEnd)
    print('closing Chrome')

    return listdfs

# Stripping non alpha characters from name of players
def stripChar(name):
    '''function returns name without trailing characters in listChars
    Input:
        name      - name to strip
        listChars - list of characters (e.g., ['*','+','-'])

    '''
    listChars = ['*','-','+']
    # Use RECURSION to strip trailing characters in listChars (*, -, +)
    if name[-1] in listChars:
        newname = name[:-1]
        newname = stripChar(newname)
    else:
        newname = name

    return newname

# Cleaning up Column
def cleaningupColumn(listdataframes, columnNames):
    '''Function strips nonalphanumeric characters from Players' names, and
    it returns a list of dataframes back, with the correction applied
    Input:
        dataframes - a list of dataframes
        columnNames - a list of column names
    '''
    print('cleaning %s' %columnNames)

    listDfs = []
    for ind, data in enumerate(listdataframes):
        for column in columnNames:
            dfstripped = data.copy()
            dfstripped[column] = dfstripped[column].apply(stripChar)
        listDfs.append(dfstripped)
    return listDfs

# Make dataframes with first year of
def getdfNameYardsTd(listofdfs, listofStats=['Player','Yds','TD']):
    '''function returns a list of new dataframes
    containing only selected Stats: ['Player','Yds','TD']
    Input:
        listofdfs - list of dataframes
        listofStats - list of variables, such as ['Player', 'TD','Yds']
    '''
    listnewdfs =[]
    for df in listofdfs:
        dftemp = df[listofStats]
        listnewdfs.append(dftemp)

    return listnewdfs

# merging Pass, Rush, and Rec STATS
def mergeYdsTD(listofdfs1, listofdfs2, listofdfs3):
    '''function returns list of dataframes with combined pass, rush and receiving STATS
    input:
        listofds1 - list of dataframes containing Passing Yds and TD
        listofds2 - list of dataframes containing Rushing Yds and TD
        listofds3 - list of dataframes containing Receiving Yds and TD
    '''
    from functools import reduce, partial

    list_PassRushRec = []
    for i in range(len(listofdfs1)):
        listofdfs1[i].columns = ['Player','PassYds','PassTD']
        listofdfs2[i].columns = ['Player','RushYds','RushTD']
        listofdfs3[i].columns = ['Player','RecYds','RecTD']

        outer_merge = partial(pd.merge, how='outer')
        combined  = reduce(outer_merge, [listofdfs1[i], listofdfs2[i],  listofdfs3[i]])
        print(combined.shape)
        list_PassRushRec.append(combined)
    return list_PassRushRec

# Make nwe list of dataframes by positions
def makeSubsetPos(listdataframes, position=['QB']):
    '''Function filters out observations that are not in the specified position
    Input:
        listdataframes - list of dataframes containing NFL-combine, obtained by createDFs()
        positions      - list of positions, eg.. ['QB','RB','WR']

    '''
    list_newdf= []
    for df in listdataframes:
        newdf = df[df['Pos'].isin(position)]
        print('dimension of new {} dataframes:\n'.format(position[0]),newdf.shape)
        list_newdf.append(newdf)

    return list_newdf

# Splitting up info in Draft column
def addDraftInfo(listdfs):
    '''Function returns a list of dataframes, where each has 4 new columns:
    i.e., 'draftTeam', 'draftRnd','draftPick', and 'draftYr'
    Input:
        listdfs - a list of dataframes
    '''

    newlistdfs =[]

    for df in listdfs:

        draftTeam,draftRnd, draftPick, draftYr, draftStat = [], [],[],[],[]
        series_draftinfo = df['Drafted (tm/rnd/yr)']

        for each in series_draftinfo:
            test = each.split('/')

            if len(test) >1:
                draftTeam.append(test[0])
                draftRnd.append(test[1])
                draftPick.append(test[2])
                draftYr.append(test[3])
                draftStat.append('Yes')
            else:
                draftTeam.append('')
                draftRnd.append('')
                draftPick.append('')
                draftYr.append('')
                draftStat.append('No')

        df['draftTeam'], df['draftRnd'], df['draftPick'] = draftTeam, draftRnd, draftPick
        df['draftYr'], df['draftStat'] = draftYr, draftStat

        newlistdfs.append(df)

    return newlistdfs

# Combining NFL-combine result with Stats
def mergeCombYdsTD(listCombine_dfs, listYdsTD_dfs, n=4, method='left'):
    '''function returns a list of n-aggregated dfs containing NFL-Combine and YdsTD
    Input:
        listCombine_dfs - list of Combine dfs
        listYdsTD_dfs   - list of aggregated YardsTD dfs, or _agg1234
        n               - default: 4 years aggregate
        method          - merge/join method 'outer' or 'inner'
    '''
    from functools import reduce, partial
    import pandas as pd

    m = len(listYdsTD_dfs)

    list_all = []
    for i in range(m):
        combined = pd.merge(listCombine_dfs[i], listYdsTD_dfs[i], on='Player', how=method)
        #outer_merge = partial(pd.merge, how=method)
        #combined  = reduce(outer_merge, [listCombine_dfs[i],listYdsTD_dfs[i]])
        print(combined.shape)
        list_all.append(combined)

    totalobs = sum([df.shape[0] for df in list_all])
    position = list_all[0]['Pos'][0]
    print("we should expect a total of {} {}s from these df's".format(totalobs, position))

    return list_all

# Count and print the number of duplicates in list of dataframes
def countDuplicates(listofdfs):
    '''Function prints out how many duplicate entries in each df (in tuples)
    Input:
        listofdfs - a list of dataframes
    '''

    list_duplicated_dfs = []
    n = len(listofdfs)
    for i in range(n):
        ids = listofdfs[i]["Player"]
        list_duplicated_dfs.append(listofdfs[i][ids.isin(ids[ids.duplicated()])])

    print(*[each.shape for each in list_duplicated_dfs], sep='\n')
    return

# Return the dataframe with duplicate observations
def findDuplicates(dataframe, colName='Player'):
    ids = dataframe[colName]
    dupes_df = dataframe[ids.isin(ids[ids.duplicated()])].sort_values(by=colName)

    return dupes_df

# aggregating 5 years worth of stats with combine results too
def addYearsTD(list_YdsTDdfs, yrStart,yrEnd, n=4):
    '''Function returns aggregate Stats(Yds&TD)-dataframes in series of n years
    Input:
        list_YdsTDdfs - list of dataframes with Stats
        yrStart       - Start year, must be same as the list_df_Combine
        yrStart       - End year, must be same as the list_df_Combine
        n .           - how many years to aggregate by
    '''
    from functools import reduce
    import pandas as pd
    list_df_agg1234 =[]

    m = len(list_YdsTDdfs)
    # making a list of 1234series
    for ind in range(m-n+1):
        series1234 = [list_YdsTDdfs[k] for k in range(ind, ind+n)]
        df_agg1234 = reduce(lambda x,y: pd.merge(x,y, on='Player',how='outer'), series1234)
        list_df_agg1234.append(df_agg1234)
        print('4yr-period {}-{} has {}'.format(int(yrStart)+ind, int(yrStart)+(n-1)+ind, df_agg1234.shape[0]))
    return list_df_agg1234


# Renaming columns after merging 4 years Stats together
def renamingYrsColumns(listdfs):
    ''' function returns the same list of dataframes, with their column Names renamed
    This makes Yds_yr1
    Input:
        listdfs - the list of dataframes containing concatenated df's
    '''
    #newcolName = ['Player', 'Pos', 'School', 'College', 'Ht', 'Wt', '40yd', 'Vertical',
    #   'Bench', 'Broad Jump', '3Cone', 'Shuttle', 'Drafted (tm/rnd/yr)',
    #   'draftTeam', 'draftRnd', 'draftPick', 'draftYr', 'draftStat', 'Yds_1',
    #   'TD_1', 'Yds_2', 'TD_2', 'Yds_3', 'TD_3', 'Yds_4', 'TD_4']
    newcolName = ['Player','Yds_1','TD_1', 'Yds_2', 'TD_2', 'Yds_3', 'TD_3', 'Yds_4', 'TD_4']

    listnewdfs=[]
    for df in listdfs:
        df.columns = newcolName
        listnewdfs.append(df)

    return listnewdfs

# Concatenating all 4-Yr sets dataframes
def concatAll4YrSets(list_4yrsets):
    '''function returns a concatenated dataframe containing all sets of 4year-STATS
    Input:
        list_4yrsets - a list of dataframes containing 4Yr sets
    '''
    from functools import reduce
    import pandas as pd

    n = len(list_4yrsets)
    for each in range(n):
        print(list_4yrsets[each].shape[0])
        newdf = reduce(lambda top,bottom: pd.concat([top,bottom], axis=0), list_4yrsets)
    print('Total of {}'.format(newdf.shape[0]))
    return newdf

# create a dataframe that binds list of salaries dataframe
def bindSal(list_dfSal, startYear):
    ''' function returns a dataframe with multiple number of years salaries
    Input :
         list_dfSal - list of dfSalary
         startYear  - specify 1st year for proper labeling of the columns
    '''
    from functools import reduce
    import pandas as pd

    n = len(list_dfSal)
    dfsalbyYear = [list_dfSal[i] for i in range(n)]

    dfsal = reduce(lambda left,right: pd.merge(left, right, on='Player', how='outer'), dfsalbyYear)
    listYears = ['Sal_'+str(yr) for yr in range(startYear, startYear+n)]
    dfsal.columns = ['Player'] + listYears
    dfsal = dfsal.fillna(0).drop_duplicates()
    return dfsal

# Adding 5th year salaries to df stats
def bindingSaltoStat(list_df_stat, df_sal,method='left'):
    '''function returns a list of dfs, containing Stats data & the 5th-year salary

    Input:
        df_stat - dataframe containing all stats for QB/ RB/ WR
        df_sal  - dataframe containing salaries
        n .     - the number of dataframe aggregates
    '''
    import pandas as pd

    max_n = len(list_df_stat)

    list_dfs =[]

    for i in range(max_n):
        newdf = pd.merge(list_df_stat[i], df_sal.iloc[:,[0, i+1]],
                         on='Player',how=method)
        list_dfs.append(newdf)
    return list_dfs

# Renaming the last column in list of dataframes to "Salary"
def renameSalCol(list_df):
    '''function returns a list of dataframes with the last column renamed to 'Salary'
    Input:
        list_df - list of dataframes
    '''
    for df in list_df:
        df.rename(columns={list(df)[-1]:'Salary'}, inplace=True)

    return list_df

# Calculate dropout rates for a 4-year periodn class
def calcDropOuts(dataframe, yearbegin,yearend):
    '''Function calculates how many players do not survive 5-years of NFL carreer
    Input:
        dataframe  - the dataframe
         yearbegin - the start year in this df
         yearEnd   - the end year in this df
    '''
    # Players who have zero salaries
    df_out = dataframe[dataframe['Salary']==0]
    perc = df_out.shape[0]/dataframe.shape[0]
    print('{}% players in {}-{} start years didnt make it 5 years'.format(round(perc*100),yearbegin, yearend))
    return

# Feature Engineering
# Converting Height in ft-inches to inches (only)
def engineerHt(dataframe):
    '''Function returns dataframe back with tranformed Height (Ht)
    Input:
        dataframe - the concatenated df
    '''
    test= dataframe['Ht'].str.split('-')
    foot_inch = [int(x[0])*12 for x in test]
    inches = [int(x[1]) for x in test]
    totht = [x+y for x,y in zip(foot_inch, inches)]
    dataframe['ht_inch'] = totht

    return dataframe

def plot_learning_curves(model, X_train, X_val, y_train, y_val):
    '''function returns
    Input:
        model   - the model you are building, after training it (e.g., after lr.fit(X,y))
        X_train - the training set
        X_val   - the validation set
        y_train - training target
        y_val   - validation target

    '''
    from sklearn.metrics import mean_squared_error, r2_score
    import matplotlib.pyplot as plt
    import numpy as np

    train_errors, val_errors = [], []

    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        train_errors.append(mean_squared_error(y_train_predict, y_train[:m]))
        val_errors.append(mean_squared_error(y_val_predict, y_val))

    plt.figure(figsize=(10,6))
    plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label='train')
    plt.plot(np.sqrt(val_errors), "b-", linewidth=3, label='val')
    plt.legend()
    plt.ylabel('RMSE')
    plt.xlabel('Training set size')
    plt.title('LEARNING CURVES')
