from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

class DASH_CPA:
    def __init__(self, attack):
        self.app = Dash(__name__)
        if "CPA" in str(type(attack)):
            self.number_traces = np.shape(attack.traces)[0]
            self.guesses_correlation_evolution = attack.guesses_correlation_evolution
            self.recover_subkey = attack.recover_subkey
            self.number_step = np.shape(attack.guesses_correlation_evolution)[2]
            self.setup_CPA_layout()
            self.setup_CPA_callbacks()

    def setup_CPA_layout(self):
        self.app.layout = html.Div([

            # Header
            html.Div([
                html.H1("Correlation Power Analysis", 
                        style={'textAlign': 'center', 
                               'color': '#2c3e50',
                               'fontFamily': 'Helvetica, Arial, sans-serif',
                               'fontSize': '32px',
                               'fontWeight': '300',
                               'marginBottom': '20px',
                               'marginTop': '20px'}),
                html.Div([
                    "Recover key: ",
                    html.Span(
                        [f"0x{int(val):02X} " for val in self.recover_subkey],
                        style={'fontWeight': 'bold'}
                    ),
                    html.Br(),
                    "ASCII: ",
                    html.Span(
                        ''.join([chr(int(val)) if 32 <= int(val) <= 126 else '.' for val in self.recover_subkey]),
                        style={'fontWeight': 'bold'}
                    )
                ], style={'textAlign': 'center', 'marginBottom': '20px'})
            ]),

            
            # Container
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='correlation-plot',
                        config={'displayModeBar': False}
                    )
                ], style={'marginBottom': '30px'}),
                
                # Slider
                html.Div([
                    html.Label('Select a byte',
                             style={'color': '#2c3e50',
                                    'marginBottom': '10px',
                                    'fontFamily': 'Helvetica, Arial, sans-serif'}),
                    dcc.Slider(
                        id='byte-slider',
                        min=0,
                        max=15,
                        value=0,
                        marks={i: {'label': str(i), 
                                  'style': {'color': '#2c3e50'}} 
                               for i in range(16)},
                        step=1,
                        tooltip={'placement': 'bottom', 'always_visible': True},
                        className='custom-slider'
                    )
                ], style={'width': '80%', 'margin': 'auto'})
            ], style={'width': '90%', 
                     'margin': 'auto',
                     'backgroundColor': 'white',
                     'padding': '20px',
                     'borderRadius': '8px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
        ], style={'backgroundColor': '#f5f6fa', 
                  'minHeight': '100vh',
                  'padding': '20px'})
        
    def create_figure_for_byte(self, byte):
        retained_key = int(self.recover_subkey[byte])
        is_single_step = self.number_step == 1
        
        if is_single_step:
            correlations = self.guesses_correlation_evolution[byte, :, 0]
            fig = go.Figure()
            mask = np.ones(256, dtype=bool)
            mask[retained_key] = False
            
            fig.add_trace(go.Bar(
                x=[f'0x{i:02X}' for i in range(256) if i != retained_key],
                y=correlations[mask],
                orientation='v',
                marker_color='rgba(128, 128, 128, 0.6)',
                showlegend=False
            ))
            
            fig.add_trace(go.Bar(
                x=[f'0x{retained_key:02X}'],
                y=[correlations[retained_key]],
                orientation='v',
                marker_color='#2e7d32',
                name=f'{retained_key} - Retained 0x{retained_key:02X}, ASCII: {chr(retained_key) if 32 <= retained_key <= 126 else "non-imprimable"}'
            ))
            
            fig.update_layout(
                template='plotly_white',
                title=dict(
                    text=f"Correlation coefficients according to hypothesis - Byte {byte}",
                    font=dict(size=18, color='#2c3e50', family='Helvetica, Arial, sans-serif'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title="Correlation coefficient",
                    titlefont=dict(size=14, color='#2c3e50'),
                    showgrid=True,
                    gridcolor='rgba(189, 195, 199, 0.2)',
                    zeroline=False
                ),
                yaxis=dict(
                    title="Hypothesis",
                    titlefont=dict(size=14, color='#2c3e50'),
                    showgrid=False,
                    zeroline=False,
                    tickfont=dict(size=10)
                ),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)'
                ),
                margin=dict(l=60, r=30, t=80, b=60),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=800
            )
            
        else:
            x_values = [(t + 1) * (self.number_traces // self.number_step) for t in range(self.number_step)]
            fig = go.Figure()

            for hypothesis in range(256):
                if hypothesis != retained_key:
                    correlations = self.guesses_correlation_evolution[byte, hypothesis, :]
                    fig.add_trace(go.Scatter(
                        x=x_values,
                        y=correlations,
                        mode='lines',
                        name=f'{hypothesis} Hypothesis 0x{hypothesis:02X}',
                        line=dict(color='rgba(128, 128, 128, 0.6)', width=1),
                        showlegend=False
                    ))
            
            correlations = self.guesses_correlation_evolution[byte, retained_key, :]
            fig.add_trace(go.Scatter(
                x=x_values,
                y=correlations,
                mode='lines',
                name=f'{retained_key} - Retained 0x{retained_key:02X}, ASCII: {chr(retained_key) if 32 <= retained_key <= 126 else "non-printable"}',
                line=dict(color='#2e7d32', width=2.5)
            ))
            
            fig.update_layout(
                template='plotly_white',
                title=dict(
                    text=f"Correlation coefficient as a function of the number of traces - Byte {byte}",
                    font=dict(size=18, color='#2c3e50', family='Helvetica, Arial, sans-serif'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title="Number of traces",
                    titlefont=dict(size=14, color='#2c3e50'),
                    showgrid=True,
                    gridcolor='rgba(189, 195, 199, 0.2)',
                    zeroline=False
                ),
                yaxis=dict(
                    title="Correlation coefficient",
                    titlefont=dict(size=14, color='#2c3e50'),
                    showgrid=True,
                    gridcolor='rgba(189, 195, 199, 0.2)',
                    zeroline=False
                ),
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="right",
                    x=0.99,
                    bgcolor='rgba(255, 255, 255, 0.8)'
                ),
                margin=dict(l=60, r=30, t=80, b=60),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
        
        return fig

    def setup_CPA_callbacks(self):
        @self.app.callback(
            Output('correlation-plot', 'figure'),
            [Input('byte-slider', 'value')]
        )
    
        def update_figure(selected_byte):
            return self.create_figure_for_byte(selected_byte)

    def run(self, debug=True, port=8050):
        self.app.run(debug=debug, port=port)
