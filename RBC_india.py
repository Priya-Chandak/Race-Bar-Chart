import numpy as np
import matplotlib.pyplot as plt
import bar_chart_race as bcr
from IPython.display import HTML
import warnings
warnings.filterwarnings("ignore")
from ipywidgets import DOMWidget, Image, Video, Audio, register, widget_serialization
import pandas as pd

covid_data_complete = pd.read_excel('E:/work/Python/Race_bar_chart/Race_bar_chart/BCR_Data.xlsx', index_col=False)
covid_data_complete.head()
covid_data_complete.info()
covid_data_complete.isnull().sum()

# change datatype of date to a pandas datetime format
covid_data_complete['date'] = pd.to_datetime(covid_data_complete['date'], dayfirst=True)
#covid_data_complete["date"] = covid_data_complete["date"].apply(pd.to_datetime)

#drop columns other than total_cases
drop_cols = ['cured', 'death']
covid_data_complete.drop(covid_data_complete[drop_cols],axis=1,inplace=True)



#dropping data before Feb 29 2020 as only Kerala had 3 cases till then in a span of one month
covid_data_complete = covid_data_complete[covid_data_complete['date'] >pd.to_datetime(pd.DataFrame({'year': [2020],'month': [1],'day': [30]}))[0]]


covid_data = covid_data_complete.copy() #make a copy for analysis
covid_data.head(10)
covid_data.columns = ['date', 'States', 'Cases'] #rename columns

total_states = covid_data['States'].nunique()
total_states

# transpose the dataframe to have countries as columns and dates as rows
covid_data_by_date = covid_data.set_index(['States','date']).unstack()['Cases'].T.reset_index()
#covid_data_by_date=covid_data.set_index(['date', 'States', 'Cases'], append=True).T.reset_index()

covid_data_by_date = covid_data_by_date.set_index('date') #make date as index - desired by barchartrace

covid_data_by_date = covid_data_by_date.fillna(0) #fill na with 0

covid_data_by_date



#make the mp4 file with the BarChartRace and save it
df = covid_data_by_date
bcr.bar_chart_race(
    df=df,
    filename='Confirmed_Cases_India.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=10,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B %d, %Y',
    period_summary_func=lambda v, r: {'x': .99, 'y': .05,
                                      's': f'Total cases: {v.nlargest(total_states).sum():,.0f}\n\nDeveloper: Priya Chandak',
                                      #'s': '',
                                      'ha': 'right', 'size': 10, 'family': 'Courier New'},
    perpendicular_bar_func='median',
    period_length=1000,
    figsize=(5, 3),
    dpi=500,
    cmap='dark24',
    title='COVID-19 cases in India',
    title_size=10,
    bar_label_size=10,
    tick_label_size=10,
    shared_fontdict={'color' : '.1'},
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=True)

