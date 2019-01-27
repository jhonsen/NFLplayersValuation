# Project Luther Proposal 

*Jhonsen Djajamuliadi*



**Title:**

- **What is the value of an NFL rookie?** i.e., how much should they be paid after the initial 4-yr contract?



**Scope**: 

- Typically, each drafted player gets a four-year deal (first-round picks have a fifth-year option built in)[1]. As it gets closer to the end of the contract, players and owners renegotiate their contract extensions. In this case, how much should players be paid?   
  - **For example**: Is Russel Wilson really worth $87 million for the Seahawks?  





**Methodology**: 

- Collect a list of NFL players from **2010-2018** (last 8 years)  and their salaries 

  - *Training* set: 201**0**-201**3** (or 4 generations)
  - *Test* set: Draft year 201**4** (for salary negotiation happening in 2018)

- Collect **NFL Combine results**, **Players' Profiles**, and **Performance Stats** over the first 4 years of NFL career (web-scraping)

  - Feature engineering to account for players' **opportunity factor**, **pyschological state**, **popularity rating**, etc.

- Build a **linear regression model** to predict the value of rookie year

    

**Data Sources**:  

- [Pro Football](https://www.pro-football-reference.com/draft/2018-combine.htm)
- [Football Database](https://www.footballdb.com/stats/stats.html?lg=NFL&yr=2018&type=reg&mode=R&conf=&limit=all)
- [Sport Trac](https://www.spotrac.com/nfl/draft/2016/running-back/)
- [Footballiqscore](https://footballiqscore.com/wonderlic-score-database)



**Prediction** (**Target**):  

- **SAL** - Salary of players after their initial contract, or on their 5-th year 



**Features**  

|  No  | **Name** |          **Description**           |
| :--: | :------: | :--------------------------------: |
|  1   |   WNDR   |   Wonderlic Scores (or IQ-score)   |
|  2   |   COLL   |         College of origin          |
|  3   |   AGE    |        Age, drafted/signed         |
|  4   |   DASH   |    COMBINE Result: 40-yard dash    |
|  5   |  BJUMP   |     COMBINE Result: Broad jump     |
|  6   |  VJUMP   |   COMBINE Result: Vertical jump    |
|  7   |   CONE   |    COMBINE Result: 3-cone drill    |
|  8   |   SHUF   |  COMBINE Result: 20-yard shuffle   |
|  9   |    HT    |   Physical Profile: Height (cm)    |
|  10  |    WT    |   Physical Profile: Weight (kg)    |
|  11  |   POS    | Player Position (WR, RB, QB, etc.) |
|  12  |   YDS    | Total Yds (Rush, Pass, Reception)  |
|  13  |   ...    |                ...                 |
|  14  |   ...    |                ...                 |
|  15  |    TD    |          Total Touchdowns          |
|  16  |   PSY    |      Mental health of players      |
|  17  |   OPPF   |         Oppoturnity factor         |
|  18  |          |                                    |
|  19  |          |                                    |
|      |          |                                    |

 **References:**

1. *"Everything you need to know about the NFL's rookie wage scale "* from [SBNATION](https://www.sbnation.com/nfl/2018/4/30/17171726/nfl-rookie-wage-scale-draft)

