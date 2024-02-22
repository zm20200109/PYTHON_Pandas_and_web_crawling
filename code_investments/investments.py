import csv
from sys import stderr
from pathlib import Path
from collections import defaultdict
from datetime import datetime
def read_from_csv():
    fpath = Path.cwd()/'../data/techcrunch.csv'
    try:
        with open(fpath,'r') as fobj:
            return list(csv.DictReader(fobj))
    except csv.Error as err:
        stderr.write(f"CSV Error.\n{err}\n")


def get_top_investments_through_year(investments):
    res_list = defaultdict(list)
    for investment in investments:
        if investment['round'] != 'a':
            continue
        try:
            date_dt =datetime.strptime(investment['fundedDate'],'%d-%b-%y')
        except ValueError as err:
            stderr.write("Value Error!!!")
        else:
            year = date_dt.year
            if year in range(2005,2009):
                res_list[year].append(investment)
    final_dict = defaultdict(tuple)
    for key, val in res_list.items():
        max_value = max(val,key=lambda dic:float(dic['raisedAmt']))
        final_dict[key] = (max_value['company'], max_value['raisedAmt'])
    return final_dict

"""
Napisati funkciju koja priprema podatake koji bi trebalo da omoguće uvid u to da li se tokom 
godina menjala teritorijalna diversifikovanost investicija. Konkretno, potrebno je uraditi 
sledeće: za svaku godinu za koju su raspoloživi podaci, utvrditi ukupan obim investicija za 
svaku državu (state), kao i broj gradova (city) u okviru date države, koji su dobili investicije. 
Tako pripremljene podatke upisati u csv fajl u formatu: "year", "state", "tot_amount", 
"city_cnt". Pre upisa u fajl, podatke sortirati najpre po godini, a zatim po nazivu države. (25 
poena

"""



def write_to_csv(data):
    fpath = Path.cwd()/'../data/teritorial_diversity.csv'
    try:
        with open(fpath,'w') as fobj:
            csv_writer = csv.writer(fobj)
            csv_writer.writerow(['Year','State','City_Cnt','Raised_Amt'])
            csv_writer.writerows(data)
    except OSError as err:
        stderr.write(f"OS Error.\n{err}\n")


def create_teritorial_diversity_stat(investments):
    res_dict_cities = defaultdict(set) # za svaku drzavu i godinu ubaci sve gradove u set
    res_dict_amount = defaultdict(float)
    for investment in investments:
        try:
            date_dt = datetime.strptime(investment['fundedDate'],'%d-%b-%y')
        except ValueError as err:
            stderr.write(f"VALUE ERROR WHILE PARSING DATE!!!\n{err}\n")
        else:
            year_of_investment =date_dt.year
            state = investment['state']
            key = year_of_investment, state
            res_dict_cities[key].add(investment['city'])
            res_dict_amount[key] += float(investment['raisedAmt'])
    final_list = list()
    for key, val in res_dict_cities.items():
        year, state = key
        city_cnt = len(val)
        tot_amount = res_dict_amount[key]
        final_list.append((year,state,city_cnt,tot_amount))
    write_to_csv(sorted(final_list, key=lambda el: (el[0],el[1])))

"""
Metoda ucitava podatke o teritorijalnoj diverzifikovanosti. Metoda prikazuju odnos grada i godine i ulozene svote novca.
"""
def plot_teritorial_diversity():
    try:
        with open(Path.cwd()/'../data/teritorial_diversity.csv') as fobj:
            list_of_data = list(csv.DictReader(fobj))
    except OSError as err:
        stderr.write("OS error.")
    else:
        import pandas as pd
        list_of_tuples = list()
        for elem in list_of_data:
            list_of_tuples.append((elem['Year'],elem['State'],elem['City_Cnt'],elem['Raised_Amt']))
        df_stat =pd.DataFrame(list_of_data, columns=['Year','State','City_Cnt','Raised_Amt'])
        year_state_list = list()
        for el1, el2 in zip(df_stat['Year'], df_stat['State']):
            year_state = str(el1)+", "+str(el2)
            #print(year_state)
            year_state_list.append(year_state)
            #df_stat['Year_State'].apply(str(el1)+", "+str(el2))
        df_year_state = pd.Series(year_state_list)
        df_year_state.name = 'Year_State'
        #print(df_year_state)
        #df_stat = pd.concat([df_stat,df_year_state])
        #print(df_stat)
        x_axis = df_year_state.values
        y_axis =df_stat['Raised_Amt'].values
        import  matplotlib.pyplot as plt
        fg, ax = plt.subplots(figsize=(17,9))
        ax.plot(x_axis, y_axis,marker='*')
        ax.set_xlabel("Year - State")
        ax.tick_params(axis='x',labelrotation=60,labelsize=9)
        ax.set_ylabel("Total amt")
        plt.show()

if __name__=='__main__':
    investments = read_from_csv()
    # for investment in investments:
    #     print(investment)
    result_dict = get_top_investments_through_year(investments)
    create_teritorial_diversity_stat(investments)
    plot_teritorial_diversity()

#%%
