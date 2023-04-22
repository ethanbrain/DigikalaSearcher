from ExtractData import ProductScraper
from dash import Dash,dcc,Output,Input,dash_table,State
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dash_table
import os
import  plotly.graph_objects as go 

# CREATE DASH ---------------------------------------------
app = Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ])

# ELEMENTS ---------------------------------------------
Title = html.H1('DIGIKALA SEARCHER',style={'color':'black','margin-top':'30px','font-family':'Georgia'})

TextInput = dbc.Input(placeholder='Type Product Name ...',id='input-on-submit'
,style={'margin-right':'100px','margin-top':'30px','width':'500px','text-align':'center'
        ,'margin-left':'60px','height':'50px','font-family':'Georgia'})

Btn = dbc.Button('Search'
, style={'margin-top':'20px','margin-bottom':'50px','width':'200px','margin-top':'30px',
        'font-family':'Georgia'}, id='submit-val', n_clicks=0)

Graph = dcc.Graph(figure={})

TableDiv = html.Div()

# CREATE LAYOUT ---------------------------------------------
app.layout = dbc.Container(
    [dbc.Row([Title],className='text-center')
    ,dbc.Row([TextInput, Btn],className='text-center')
    ,dbc.Row([TableDiv],className='text-center')
    ,dbc.Row([Graph],className='text-center')
    ]
    )

# ELEMENTS CALLBACK ---------------------------------------------
@app.callback(
    Output(TableDiv,component_property='children'),
    Output(Graph,component_property='figure'),
    Output('submit-val', 'n_clicks'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)

# APP CODES ---------------------------------------------
def update_output(n_clicks, value):
    if n_clicks > 0:
        
        # EXTRACT INFORMATIONS ---------------------------------------------
        scraper = ProductScraper(value)
        scraper.scrape()
        
        # DESGIN TABLE---------------------------------------------
        rows = [html.Tr([html.Th('تصویر'),html.Th('قیمت'),html.Th('عنوان'),],style={'border-width':'3px','border-color':'black','font-family':'Georgia'})]
        
        # READ DATA ---------------------------------------------
        with open("products.txt", encoding="utf-8") as f:
            name = f.read().split('\n')
        with open("prices.txt") as f:
            price = f.read().split('\n')
        with open("links.txt") as f:
            link = f.read().split('\n')
        
        image_list = os.listdir('assets/images/')

        # INSERT DATA IN TABLE ---------------------------------------------
        for t,p,l,image_name in zip(name,price,link,image_list):
            img = html.Img(src=app.get_asset_url(f'images/{image_name}'),width='150px',height='150px')
            d = html.Tr([html.Td(img,style={'border-width':'3px','border-color':'black'})
               ,html.Td(html.B(p),style={'border-width':'3px','border-color':'black','font-family':'Georgia','font-size':'20px'})
               ,html.A(html.B(t),href=l,style={'border-width':'3px','border-color':'black','font-family':'Georgia','font-size':'20px','text-decoration':'none'}),]
                        ,style={'border-width':'3px','border-color':'black'})
            rows.append(d)
        
        # INSERT TABLE DATA ---------------------------------------------
        children = [dbc.Table(rows,style={'width':'100%'})]
        
        # SORT RRICES ---------------------------------------------
        def insertion_sort(arr, simulation=False):
            prices_new = []
            for p in arr:
                spilted = p.split(',')
                temp = ''
                for s in spilted:
                    temp += s

                if temp != '':
                    prices_new.append(temp)  
                        
            for i in range(len(prices_new)):
                cursor = prices_new[i]
                pos = i
                
                while pos > 0 and prices_new[pos - 1] > cursor:
                    # Swap the number down the list
                    prices_new[pos] = prices_new[pos - 1]
                    pos = pos - 1
                # Break and do the final swap
                prices_new[pos] = cursor

            return prices_new 
        np = insertion_sort(price)
        
        # INSERT GRAPH DATA ---------------------------------------------
        figure = go.Figure(data=go.Scatter(x=list(range(0,len(np))), y=np))
    
        return children, figure, n_clicks
    
# RUN APP ---------------------------------------------
if __name__ == '__main__':
    app.run_server(port='2020')