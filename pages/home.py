from dash import html, register_page  #, callback # If you need callbacks, import it here.


register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/',

)

def layout():
    layout = html.Div([
        html.H1(
            [
                "Home Page"
            ]
            ),
        html.Div(html.H4("""Welcome to the Borden
                            test data display dashboard home page.  
                            Below are the available data sets 
                            that can be visualized by following
                            the links above."""
                        )
                ),
        html.Div(className='gap',style={'height':'10px'}),
        html.Img(src='assets/skyline.jpg', alt='View from top of tower'),
        html.Div([
            html.Div(children="""CR3000 temperature data""",className="box1",
                        style={
                        'backgroundColor':'aqua',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }
                    ),
            html.Img(src='assets/CR3000_temperature.jpg', alt='CR3000 Plot Capture'),
                ]),
        html.Div(className='gap',style={'height':'10px'}),
        html.Div([
            html.Div(children="""Borden Picarro trace gas data""",className="box1",
                        style={
                        'backgroundColor':'aqua',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }
                    ),
            html.Img(src='assets/borden_gases.jpg', alt='Picarro Plot Capture' ),
                ]),
            ])
    return layout