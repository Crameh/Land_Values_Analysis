from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import json

dt2021=pd.read_csv("docs/valeursfoncieres-2021.txt", sep="|")

dt2021['Date mutation'] = pd.to_datetime(dt2021['Date mutation'])
dt2021["Valeur fonciere"] = dt2021["Valeur fonciere"].apply(lambda x:str(x).replace(',', '.'))
dt2021["Valeur fonciere"] = dt2021["Valeur fonciere"].astype(float)
dt2021["No voie"]=dt2021["No voie"].apply(lambda x:str(math.ceil(int(x))) if str(x).lower()!= "nan" and str(x).lower()!= "" else "")
dt2021["Type de voie"]=dt2021["Type de voie"].apply(lambda x:str(x) if str(x).lower()!= "nan"and str(x).lower()!= "" else "")
dt2021["Code postal"]=dt2021["Code postal"].apply(lambda x:str(int(x)) if str(x).lower()!= "nan" and str(x).lower() != "" else "")
dt2021["Commune"]=dt2021["Commune"].apply(lambda x:str(x) if str(x).lower()!= "nan" and str(x).lower() != "" else "")

dt2021["Adresse"]=dt2021["No voie"]+" "+dt2021["Type de voie"]+" "+dt2021["Voie"] + " " + dt2021["Code postal"]+" "+dt2021["Commune"]
dt2021["Prix moyen metre carre"]=dt2021["Valeur fonciere"]/dt2021["Surface terrain"]

dt2021.dropna(how='all', inplace=True, axis=1)

dt2021.drop(['No voie', 'Voie', 
             '1er lot', 'Surface Carrez du 1er lot',
             '2eme lot', 'Surface Carrez du 2eme lot',
             '3eme lot', 'Surface Carrez du 3eme lot',
             '4eme lot', 'Surface Carrez du 4eme lot',
             '5eme lot', 'Surface Carrez du 5eme lot'
            ], inplace=True, axis=1)

data2021 = dt2021.drop(dt2021[dt2021['Type local'] == 'Dépendance'].index)

dt2020=pd.read_csv("docs/valeursfoncieres-2020.txt", sep="|")
dt2019=pd.read_csv("docs/valeursfoncieres-2019.txt", sep="|")
dt2018=pd.read_csv("docs/valeursfoncieres-2018.txt", sep="|")
dt2017=pd.read_csv("docs/valeursfoncieres-2017.txt", sep="|")
    
dt2020["Valeur fonciere"] = dt2020["Valeur fonciere"].apply(lambda x:str(x).replace(',', '.'))
dt2019["Valeur fonciere"] = dt2019["Valeur fonciere"].apply(lambda x:str(x).replace(',', '.'))
dt2018["Valeur fonciere"] = dt2018["Valeur fonciere"].apply(lambda x:str(x).replace(',', '.'))
dt2017["Valeur fonciere"] = dt2017["Valeur fonciere"].apply(lambda x:str(x).replace(',', '.'))
dt2020["Valeur fonciere"] = dt2020["Valeur fonciere"].astype(float)
dt2019["Valeur fonciere"] = dt2019["Valeur fonciere"].astype(float)
dt2018["Valeur fonciere"] = dt2018["Valeur fonciere"].astype(float)
dt2017["Valeur fonciere"] = dt2017["Valeur fonciere"].astype(float)

dt2020["Prix moyen metre carre"]=dt2020["Valeur fonciere"]/dt2020["Surface terrain"]
dt2019["Prix moyen metre carre"]=dt2019["Valeur fonciere"]/dt2019["Surface terrain"]
dt2018["Prix moyen metre carre"]=dt2018["Valeur fonciere"]/dt2018["Surface terrain"]
dt2017["Prix moyen metre carre"]=dt2017["Valeur fonciere"]/dt2017["Surface terrain"]

def index(request):
    context={
        }
    return render(request, 'index.html', context)

def index1(request):
    context={
        }
    return render(request, 'visu.html', context)

def btq_pie():
    btq = data2021['B/T/Q'].value_counts()[0:10]
    fig = px.pie(btq, values = btq.values, names = btq.index, title="Représentation de la répartition de l'indice de répartition")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def btq_scatter():
    vector = data2021[['Surface terrain', 'Valeur fonciere', 'Code departement']]
    cond = vector['Code departement']==75 
    fig = px.scatter(x=vector[cond]['Surface terrain'].values, y=vector[cond]['Valeur fonciere'].values, range_x=(0,10000), range_y=(0,150000000))
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def type_voie_pie():
    voie_count = data2021['Type de voie'].value_counts()[0:7]
    fig = px.pie(values = voie_count.values, names = voie_count.index, title="Représentation de la répartition des différents types de voie",
    labels={
    '1': 'Sans type de voie', 
    "RUE" :'rue', 
    'AV' : 'avenue',
    'RTE' : 'route',
    'CHE' : 'chemin',
    'BD' : 'boulevard',
    'ALL' : 'allée',})
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def type_voie_bar():
    fig = px.bar(data2021.groupby(by=['Type de voie']).mean()['Valeur fonciere'].loc[['', 'RUE', 'AV', 'RTE', 'CHE', 'BD', 'ALL']],
    title="Moyenne des valeurs foncieres en fonction du type de voie")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def nature_mutation_count():
    fig = px.bar(dt2021['Nature mutation'].value_counts(), title="Représentation de la répartition des différentes natures de mutation")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def nature_mutation_bar():
    fig = px.bar(dt2021.groupby('Nature mutation').mean()['Valeur fonciere'], orientation='h', title='Valeur fonciere en fonction des différentes natures de mutation')
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def departement_count():
    tmp = data2021['Code departement']
    tmp = tmp.value_counts().reset_index()
    geodoc=json.load(open('docs/geodepartement.geojson'))
    fig = px.choropleth(tmp,
                    geojson=geodoc,
                    locations='index',
                    featureidkey='properties.code',
                    color='Code departement',
                    color_continuous_scale='plasma',
                    range_color=(0,40000),
                    scope='europe',
                    labels={'Code departement':'Nombre de transactions',
                           'index':'Code département'})
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def departement_vf():
    tmp = data2021[['Code departement', 'Valeur fonciere']]
    tmp = tmp.groupby('Code departement').mean().reset_index()
    geodoc=json.load(open('docs/geodepartement.geojson'))
    fig = px.choropleth(tmp,
                    geojson=geodoc,
                    locations='Code departement',
                    featureidkey='properties.code',
                    color='Valeur fonciere',
                    color_continuous_scale='Viridis',
                    range_color=(0,500000),
                    scope='europe',
                    labels={'Valeur fonciere':'Valeur fonciere moyenne'})
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def departement_bar():
    tmp = data2021.groupby('Code departement', sort=False).size().sort_values()
    tmp = tmp.apply(lambda x:int(x))
    tmp2={}
    for i in tmp.index:
        try:
            i=int(i)
            if i<100:
                tmp2[i]=tmp[i]
        except:
                tmp2[i]=tmp[i]

    fig = px.bar(x=tmp2.values(), y=tmp2.keys(), orientation='h')
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html


def surface_terrain():
    vector = data2021[['Surface terrain', 'Valeur fonciere', 'Code departement']]
    cond1 = vector['Code departement']==75 
    cond2 = vector['Code departement']==77
    vector = vector[cond1 | cond2]
    fig = px.scatter(vector, x='Surface terrain', y='Valeur fonciere',facet_col='Code departement' ,range_x=(0,10000), range_y=(0,150000000))
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def surface_bati():
    vector = data2021[['Valeur fonciere', 'Code departement', 'Surface reelle bati']]
    cond1 = vector['Code departement']==75 
    cond2 = vector['Code departement']==77 
    fig = px.scatter(vector[cond1 | cond2],x='Surface reelle bati', y='Valeur fonciere',facet_col='Code departement', range_x=(0,10000), range_y=(0,150000000))
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def nb_lot():
    fig = px.scatter(data2021.groupby('Nombre de lots').mean()['Valeur fonciere'], title="Valeur fonciere moyenne par rapport au nombre de lots")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def local_pie():
    local_count = dt2021['Type local'].value_counts()
    fig = px.pie(values = local_count.values, names = local_count.index, title="Représentation de la répartition des différents types de locaux")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def local_bar():
    fig = px.bar(dt2021.groupby('Type local').mean()['Valeur fonciere'], orientation='h', title='Valeur fonciere en fonction des différents types de locaux')
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def date_graph():
    fig = px.line(data2021[data2021['Valeur fonciere'] < 10000000].groupby('Date mutation').mean()['Valeur fonciere'],
       title='Valeur fonciere moyenne en fonction de la date de mutation')
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def nb_piece_pie():
    nb_piece = dt2021['Nombre pieces principales'].value_counts()[4:7]
    fig = px.pie(values = nb_piece.values, names = nb_piece.index, title="Représentation du nombre de pièces par vente")
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def nb_piece_bar():
    fig = px.bar(dt2021.groupby('Nombre pieces principales').mean()['Valeur fonciere'][0:27], title='Valeur fonciere en fonction du nombre de pièces')
    plot_html=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot_html

def mean_price_m2(test):
    mean=0
    count=0
    for i in test:
        try:
            i=int(i)
            mean+=i
        except:
            count+=1
    mean/=len(test)-count
    return mean

def plot1():
    vector2017 = dt2017['Valeur fonciere'].mean()
    vector2018 = dt2018['Valeur fonciere'].mean()
    vector2019 = dt2019['Valeur fonciere'].mean()
    vector2020 = dt2020['Valeur fonciere'].mean()
    vector2021 = dt2021['Valeur fonciere'].mean()
    vect_y = [vector2017, vector2018, vector2019, vector2020, vector2021]
    vect_x = ['2017','2018','2019','2020','2021']
    fig = px.line(x=vect_x, y=vect_y, title='Valeur foncière moyenne au fil des 5 dernières années')
    plot=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot

def plot2():
    vector2017 = dt2017['Valeur fonciere'].shape[0]
    vector2018 = dt2018['Valeur fonciere'].shape[0]
    vector2019 = dt2019['Valeur fonciere'].shape[0]
    vector2020 = dt2020['Valeur fonciere'].shape[0]
    vector2021 = dt2021['Valeur fonciere'].shape[0]
    vect_y = [vector2017, vector2018, vector2019, vector2020, vector2021]
    vect_x = ['2017','2018','2019','2020','2021']
    fig = px.line(x=vect_x, y=vect_y, title='Nombre de transactions au fil des 5 dernières années')
    plot=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot
    
def plot3a():
    tmp = dt2017[['Code departement', 'Valeur fonciere']]
    tmp = tmp.groupby('Code departement').mean().reset_index()
    geodoc=json.load(open('docs/geodepartement.geojson'))

    fig = px.choropleth(tmp,
                    geojson=geodoc,
                    locations='Code departement',
                    featureidkey='properties.code',
                    color='Valeur fonciere',
                    color_continuous_scale='Viridis',
                    range_color=(0,500000),
                    scope='europe',
                    labels={'Valeur fonciere':'Valeur fonciere moyenne'})
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    plot=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot

def plot3b():
    tmp = dt2021[['Code departement', 'Valeur fonciere']]
    tmp = tmp.groupby('Code departement').mean().reset_index()
    geodoc=json.load(open('docs/geodepartement.geojson'))
    
    fig = px.choropleth(tmp,
                    geojson=geodoc,
                    locations='Code departement',
                    featureidkey='properties.code',
                    color='Valeur fonciere',
                    color_continuous_scale='Viridis',
                    range_color=(0,500000),
                    scope='europe',
                    labels={'Valeur fonciere':'Valeur fonciere moyenne'})
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    plot=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot

def plot4():
    mean2021=mean_price_m2(data2021['Prix moyen metre carre'])
    mean2020=mean_price_m2(dt2020['Prix moyen metre carre'])
    mean2019=mean_price_m2(dt2019['Prix moyen metre carre'])
    mean2018=mean_price_m2(dt2018['Prix moyen metre carre'])
    mean2017=mean_price_m2(dt2017['Prix moyen metre carre'])
    vect_y = [mean2017, mean2018, mean2019, mean2020, mean2021]
    vect_x = ['2017','2018','2019','2020','2021']
    fig = px.line(x=vect_x, y=vect_y, title='Prix moyen au m2 au fil des 5 dernières années')
    plot=fig.to_html(full_html=False, default_height=500, default_width=700)
    return plot

def index2(request):   
    if(request.GET['model']=='surface'):
        plot_list = [surface_terrain(), surface_bati()]
    if(request.GET['model']=='btq'):
        plot_list = [btq_pie(), btq_scatter()]
    if(request.GET['model']=='type_voie'):
        plot_list = [type_voie_pie(), type_voie_bar()]
    if(request.GET['model']=='nature_mutation'):
        plot_list = [nature_mutation_count(), nature_mutation_bar()]
    if(request.GET['model']=='departement'):
        plot_list = [departement_bar(), departement_count(), departement_vf()]  
    if(request.GET['model']=='nb_lot'):
        plot_list = [nb_lot()] 
    if(request.GET['model']=='type_local'):
        plot_list = [local_pie(), local_bar()]
    if(request.GET['model']=='date'):
        plot_list = [date_graph()]
    if(request.GET['model']=='nb_pieces'):
        plot_list = [nb_piece_pie(), nb_piece_bar()]   
    if(request.GET['model']=='comparaison'):                              
        plot_list = [plot1(), plot2(), plot3a(), plot3b(), plot4(), plot5()] 
        
    context={
            'plot_list':plot_list
        }
    return render(request, 'visu.html', context)