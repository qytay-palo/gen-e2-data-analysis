---
name: build-dashboard
description: Build an interactive Dash web application with charts, filters, and tables. Use when creating an executive overview with KPI cards, turning query results into a dynamic dashboard, building a team monitoring tool, or needing multiple charts with interactive callbacks.
argument-hint: "<description> [data source]"
---

# /build-dashboard - Build Interactive Dashboards

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Build an interactive Dash web application with charts, filters, tables, and professional styling using callbacks for full interactivity.

## Usage

```
/build-dashboard <description of dashboard> [data source]
```

## Workflow

### 1. Understand the Dashboard Requirements

Determine:

- **Purpose**: Executive overview, operational monitoring, deep-dive analysis, team reporting
- **Audience**: Who will use this dashboard?
- **Key metrics**: What numbers matter most?
- **Dimensions**: What should users be able to filter or slice by?
- **Data source**: Database query, CSV file, Parquet, or sample data
- **Deployment**: Local development (`localhost:8050`) or production server

### 2. Gather the Data

**If data warehouse is connected:**
1. Query the necessary data
2. Save to Parquet or CSV files
3. Load into global dataframes at app startup

**If data is pasted or uploaded:**
1. Parse and clean the data
2. Save to appropriate format (Parquet/CSV)
3. Load at startup

**If working from a description without data:**
1. Create a realistic sample dataset matching the described schema
2. Note in the dashboard that it uses sample data
3. Provide instructions for swapping in real data

### 3. Design the Dashboard Layout

Follow a standard Dash dashboard layout pattern using Bootstrap Grid:

```
┌──────────────────────────────────────────────────┐
│  Dashboard Title                    [Filters ▼]  │
├────────────┬────────────┬────────────┬───────────┤
│  KPI Card  │  KPI Card  │  KPI Card  │ KPI Card  │
├────────────┴────────────┼────────────┴───────────┤
│                         │                        │
│    Primary Chart        │   Secondary Chart      │
│    (dcc.Graph)          │   (dcc.Graph)          │
│                         │                        │
├─────────────────────────┴────────────────────────┤
│                                                  │
│    Detail Table (dash_table.DataTable)           │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Adapt the layout to the content:**
- 2-4 KPI cards at the top (using `dbc.Card` components)
- 1-3 charts in the middle section (`dcc.Graph` for trends and breakdowns)
- Optional detail table at bottom (`dash_table.DataTable` for drill-down data)
- Filters in header or sidebar using `dcc.Dropdown`, `dcc.RadioItems`, `dcc.RangeSlider`

### 4. Build the Dash Application

Generate a Dash application using the base structure below. The application includes:
- No external data fetches required
- Dashboard is fully interactive with real-time filtering
- Can be deployed for team access or run locally

### 5. Implement Chart Types

Use Plotly via `dcc.Graph` for all charts. Common dashboard chart patterns:

- **Line chart** (`px.line` or `go.Scatter`): Time series trends
- **Bar chart** (`px.bar` or `go.Bar`): Category comparisons
- **Pie/Doughnut chart** (`px.pie`): Composition (when <6 categories)
- **Stacked bar** (`px.bar` with `barmode='stack'`): Composition over time
- **Mixed charts** (`go.Figure` with multiple traces): Volume with rate overlay

Use the Plotly chart integration patterns below for each chart type.

### 6. Add Interactivity

Use Dash callbacks to connect filters to outputs. Common patterns below include dropdown filters, date range filters, combined multi-filter logic, and data tables with sorting/filtering.

### 7. Run and Test

1. Save the dashboard as a Python file with a descriptive name (e.g., `app_sales_dashboard.py`)
2. Run the Dash server using `python app_sales_dashboard.py`
3. Open browser to `http://localhost:8050` to view the dashboard
4. Confirm it renders correctly and callbacks work
5. Provide instructions for updating data, customizing, and deploying to production

---

## Base Template

Every Dash dashboard follows this structure:

```python
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from datetime import datetime

# Initialize app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data (use global dataframes for efficiency)
df = pl.read_csv('data/sales_data.csv')
# Or for larger files: df = pl.scan_csv('data/large_file.csv').collect()

#############################################
# Layout
#############################################

app.layout = dbc.Container([
    # Header with title and filters
    dbc.Row([
        dbc.Col(html.H1("Dashboard Title", className="text-primary mb-3"), width=6),
        dbc.Col([
            dcc.Dropdown(
                id='filter-region',
                options=[{'label': 'All Regions', 'value': 'all'}] + 
                        [{'label': r, 'value': r} for r in df['region'].unique().to_list()],
                value='all',
                className="mb-2"
            ),
        ], width=6)
    ], className="mb-4"),
    
    # KPI Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Revenue", className="text-muted"),
                    html.H3(id="kpi-revenue", children="$0"),
                    html.P(id="kpi-revenue-change", className="text-success")
                ])
            ])
        ], width=3),
        # Add more KPI cards as needed
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='revenue-trend-chart')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='category-breakdown-chart')
        ], width=6),
    ], className="mb-4"),
    
    # Data Table
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='detail-table',
                page_size=20,
                sort_action='native',
                filter_action='native',
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'}
            )
        ])
    ]),
    
    # Footer
    html.Footer([
        html.P(f"Data as of: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
               className="text-muted mt-4")
    ])
], fluid=True, className="p-4")

#############################################
# Callbacks
#############################################

@app.callback(
    [
        Output('kpi-revenue', 'children'),
        Output('revenue-trend-chart', 'figure'),
        Output('category-breakdown-chart', 'figure'),
        Output('detail-table', 'data'),
        Output('detail-table', 'columns')
    ],
    [Input('filter-region', 'value')]
)
def update_dashboard(selected_region):
    # Filter data
    filtered_df = df if selected_region == 'all' else df.filter(pl.col('region') == selected_region)
    
    # Calculate KPIs
    total_revenue = filtered_df['revenue'].sum()
    
    # Create charts
    revenue_fig = px.line(
        filtered_df.to_pandas(),
        x='date',
        y='revenue',
        title='Revenue Trend'
    )
    
    category_fig = px.bar(
        filtered_df.group_by('category').agg(pl.col('revenue').sum()).to_pandas(),
        x='category',
        y='revenue',
        title='Revenue by Category'
    )
    
    # Table data
    table_data = filtered_df.head(100).to_pandas().to_dict('records')
    table_columns = [{'name': col, 'id': col} for col in filtered_df.columns]
    
    return (
        f"${total_revenue:,.0f}",
        revenue_fig,
        category_fig,
        table_data,
        table_columns
    )

#############################################
# Run Server
#############################################

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8050)
```

## KPI Card Pattern

Use Bootstrap Card components for KPI displays:

```python
# In app.layout
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H6("Total Revenue", className="text-muted text-uppercase"),
                html.H2(id="kpi-revenue", className="mb-0"),
                html.P(id="kpi-revenue-change", className="mb-0")
            ])
        ], className="shadow-sm")
    ], width=3),
    # Repeat for more KPIs
], className="mb-4")

# In callback
@app.callback(
    [
        Output('kpi-revenue', 'children'),
        Output('kpi-revenue-change', 'children'),
        Output('kpi-revenue-change', 'className')
    ],
    [Input('filter-date', 'value')]
)
def update_kpi(date_range):
    current_revenue = calculate_revenue(date_range)
    previous_revenue = calculate_revenue(previous_period(date_range))
    
    # Format the value
    formatted_value = format_currency(current_revenue)
    
    # Calculate change
    if previous_revenue > 0:
        pct_change = ((current_revenue - previous_revenue) / previous_revenue) * 100
        change_text = f"{'+' if pct_change >= 0 else ''}{pct_change:.1f}% vs prior period"
        change_class = "text-success" if pct_change >= 0 else "text-danger"
    else:
        change_text = "N/A"
        change_class = "text-muted"
    
    return formatted_value, change_text, change_class

def format_currency(value):
    """Format large numbers with K/M suffixes"""
    if value >= 1e6:
        return f"${value/1e6:.1f}M"
    elif value >= 1e3:
        return f"${value/1e3:.1f}K"
    else:
        return f"${value:,.0f}"
```

## Plotly Chart Integration

### Chart Container Pattern

Use `dcc.Graph` components for all charts:

```python
# In app.layout
dbc.Row([
    dbc.Col([
        html.H5("Monthly Revenue Trend"),
        dcc.Graph(id='revenue-chart')
    ], width=6)
])
```

### Line Chart

```python
import plotly.express as px
import plotly.graph_objects as go

@app.callback(
    Output('revenue-chart', 'figure'),
    [Input('filter-region', 'value')]
)
def update_line_chart(selected_region):
    filtered_df = apply_filters(df, selected_region)
    
    # Using Plotly Express (easier)
    fig = px.line(
        filtered_df.to_pandas(),
        x='month',
        y='revenue',
        color='category',  # For multiple series
        title='Monthly Revenue Trend',
        labels={'revenue': 'Revenue ($)', 'month': 'Month'},
        template='plotly_white'
    )
    
    # Or using Graph Objects (more control)
    fig = go.Figure()
    for category in filtered_df['category'].unique():
        category_data = filtered_df.filter(pl.col('category') == category)
        fig.add_trace(go.Scatter(
            x=category_data['month'].to_list(),
            y=category_data['revenue'].to_list(),
            mode='lines+markers',
            name=category,
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig
```

### Bar Chart

```python
import plotly.express as px

@app.callback(
    Output('category-chart', 'figure'),
    [Input('filter-date', 'value')]
)
def update_bar_chart(date_range):
    filtered_df = filter_by_date(df, date_range)
    
    # Aggregate data
    agg_df = (
        filtered_df
        .group_by('category')
        .agg(pl.col('revenue').sum())
        .sort('revenue', descending=True)
        .head(10)
    )
    
    # Determine orientation based on number of categories
    is_horizontal = len(agg_df) > 8
    
    if is_horizontal:
        fig = px.bar(
            agg_df.to_pandas(),
            y='category',
            x='revenue',
            orientation='h',
            title='Revenue by Category',
            labels={'revenue': 'Revenue ($)', 'category': 'Category'}
        )
    else:
        fig = px.bar(
            agg_df.to_pandas(),
            x='category',
            y='revenue',
            title='Revenue by Category',
            labels={'revenue': 'Revenue ($)', 'category': 'Category'}
        )
    
    fig.update_traces(marker_color='#4C72B0')
    fig.update_layout(
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig
```

### Pie/Doughnut Chart

```python
import plotly.express as px

@app.callback(
    Output('distribution-chart', 'figure'),
    [Input('filter-metric', 'value')]
)
def update_pie_chart(metric):
    # Aggregate data
    dist_df = (
        df
        .group_by('segment')
        .agg(pl.col(metric).sum())
        .sort(metric, descending=True)
        .head(10)
    )
    
    fig = px.pie(
        dist_df.to_pandas(),
        values=metric,
        names='segment',
        title=f'{metric.title()} Distribution',
        hole=0.4  # Creates doughnut effect; omit for regular pie
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=400
    )
    
    return fig
```
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: COLORS.map(c => c + 'CC'),
                borderColor: '#ffffff',
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: { usePointStyle: true, padding: 15 }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${formatValue(context.parsed, 'number')} (${pct}%)`;
                        }
                    }
                }
            }
```

## Filter and Interactivity Implementation

### Dropdown Filter

```python
# In app.layout
dbc.Row([
    dbc.Col([
        html.Label("Region:"),
        dcc.Dropdown(
            id='filter-region',
            options=[{'label': 'All Regions', 'value': 'all'}],  # Populated dynamically
            value='all',
            clearable=False
        )
    ], width=4)
])

# Populate dropdown options from data
def get_dropdown_options(df, column):
    unique_values = df[column].unique().sort().to_list()
    return [{'label': 'All', 'value': 'all'}] + [{'label': v, 'value': v} for v in unique_values]

# In callback
@app.callback(
    Output('some-output', 'figure'),
    [Input('filter-region', 'value')]
)
def update_on_filter(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df.filter(pl.col('region') == selected_region)
    # ... rest of logic
```

### Date Range Filter

```python
from datetime import datetime, timedelta

# In app.layout
dbc.Row([
    dbc.Col([
        html.Label("Date Range:"),
        dcc.DatePickerRange(
            id='filter-date-range',
            start_date=datetime.now() - timedelta(days=90),
            end_date=datetime.now(),
            display_format='YYYY-MM-DD'
        )
    ], width=6)
])

# In callback
@app.callback(
    Output('chart', 'figure'),
    [
        Input('filter-date-range', 'start_date'),
        Input('filter-date-range', 'end_date')
    ]
)
def update_on_date_range(start_date, end_date):
    filtered_df = df.filter(
        (pl.col('date') >= start_date) & (pl.col('date') <= end_date)
    )
    # ... rest of logic
```

### Radio Buttons Filter

```python
# In app.layout
dbc.Row([
    dbc.Col([
        html.Label("View:"),
        dcc.RadioItems(
            id='filter-view',
            options=[
                {'label': 'Daily', 'value': 'day'},
                {'label': 'Weekly', 'value': 'week'},
                {'label': 'Monthly', 'value': 'month'}
            ],
            value='day',
            inline=True
        )
    ])
])
```

### Combined Multi-Filter Callback

```python
@app.callback(
    [
        Output('kpi-revenue', 'children'),
        Output('revenue-chart', 'figure'),
        Output('detail-table', 'data')
    ],
    [
        Input('filter-region', 'value'),
        Input('filter-category', 'value'),
        Input('filter-date-range', 'start_date'),
        Input('filter-date-range', 'end_date')
    ]
)
def update_all_components(region, category, start_date, end_date):
    # Apply all filters
    filtered_df = df
    
    if region != 'all':
        filtered_df = filtered_df.filter(pl.col('region') == region)
    
    if category != 'all':
        filtered_df = filtered_df.filter(pl.col('category') == category)
    
    if start_date and end_date:
        filtered_df = filtered_df.filter(
            (pl.col('date') >= start_date) & (pl.col('date') <= end_date)
        )
    
    # Update KPI
    total_revenue = filtered_df['revenue'].sum()
    
    # Update chart
    fig = create_revenue_chart(filtered_df)
    
    # Update table
    table_data = filtered_df.head(100).to_pandas().to_dict('records')
    
    return f"${total_revenue:,.0f}", fig, table_data
```

### Data Table with Dash

```python
from dash import dash_table

# In app.layout
dbc.Row([
    dbc.Col([
        html.H5("Detailed Data"),
        dash_table.DataTable(
            id='detail-table',
            columns=[],  # Populated in callback
            data=[],     # Populated in callback
            page_size=50,
            page_action='native',
            sort_action='native',
            sort_mode='multi',
            filter_action='native',
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '10px',
                'fontSize': '13px',
                'fontFamily': 'sans-serif'
            },
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': '#f8f9fa',
                'borderBottom': '2px solid #dee2e6',
                'textTransform': 'uppercase',
                'fontSize': '12px'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa'
                },
                {
                    'if': {'state': 'selected'},
                    'backgroundColor': '#e3f2fd',
                    'border': '1px solid #2196f3'
                }
            ],
            # Formatting specific columns
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'revenue',
                        'filter_query': '{revenue} > 100000'
                    },
                    'backgroundColor': '#d4edda',
                    'color': '#155724'
                }
            ]
        )
    ])
])

# In callback
@app.callback(
    [
        Output('detail-table', 'data'),
        Output('detail-table', 'columns')
    ],
    [Input('filter-region', 'value')]
)
def update_table(selected_region):
    filtered_df = apply_filters(df, selected_region)
    
    # Limit rows for performance (use pagination)
    display_df = filtered_df.head(1000)
    
    # Format data
    table_data = display_df.to_pandas().to_dict('records')
    
    # Define columns with formatting
    table_columns = [
        {'name': 'Date', 'id': 'date', 'type': 'datetime'},
        {'name': 'Region', 'id': 'region', 'type': 'text'},
        {
            'name': 'Revenue',
            'id': 'revenue',
            'type': 'numeric',
            'format': {'specifier': '$,.2f'}  # Currency formatting
        },
        {
            'name': 'Growth %',
            'id': 'growth_pct',
            'type': 'numeric',
            'format': {'specifier': '.1%'}  # Percentage formatting
        }
    ]
    
    return table_data, table_columns
```

## Styling Dash Applications

### Using Bootstrap Themes

Dash Bootstrap Components provides ready-to-use themes:

```python
import dash_bootstrap_components as dbc

# Available themes:
# BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA,
# LUMEN, LUX, MATERIA, MINTY, MORPH, PULSE, QUARTZ, SANDSTONE, SIMPLEX,
# SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, VAPOR, YETI, ZEPHYR

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
```

### Custom CSS Styling

For custom styles, create `assets/custom.css`:

```css
/* assets/custom.css */

/* Custom color variables */
:root {
    --primary-color: #4C72B0;
    --secondary-color: #DD8452;
    --success-color: #55A868;
    --danger-color: #C44E52;
    --bg-light: #f8f9fa;
}

/* Card customization */
.card {
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    border: none;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}

/* Dashboard header */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 8px;
    color: white;
    margin-bottom: 2rem;
}

/* KPI value highlighting */
.kpi-value-large {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
}
```

Dash automatically loads CSS files from the `assets/` directory.

### Inline Styling

```python
# Using style dictionaries
html.Div(
    "Dashboard Title",
    style={
        'fontSize': '24px',
        'fontWeight': 'bold',
        'color': '#2c3e50',
        'marginBottom': '20px'
    }
)

# Bootstrap utility classes (with dbc)
dbc.Card(
    dbc.CardBody([
        html.H4("Revenue", className="card-title text-muted"),
        html.H2("$1.2M", className="text-primary mb-0")
    ]),
    className="shadow-sm border-0"
)
```

## Performance Considerations for Large Datasets

### Data Size Guidelines

| Data Size | Approach |
|---|---|
| <10,000 rows | Load full dataset. Use Polars for efficient processing. |
| 10,000 - 100,000 rows | Load full dataset with lazy evaluation. Pre-aggregate for charts. |
| 100,000 - 1M rows | Pre-aggregate before loading. Use sampling for detail tables. |
| >1M rows | Use database queries with filters. Implement server-side pagination. |

### Pre-Aggregation Pattern

For large datasets, pre-aggregate before creating visualizations:

```python
# DON'T: Load 500,000 raw rows into memory
df = pl.read_csv('large_file.csv')  # Slow and memory-intensive

# DO: Use lazy evaluation and pre-aggregate
df_agg = (
    pl.scan_csv('large_file.csv')
    .group_by('month', 'category')
    .agg([
        pl.col('revenue').sum().alias('total_revenue'),
        pl.col('order_id').count().alias('order_count')
    ])
    .collect()  # Only collect aggregated data
)

# Or for time series: downsample high-frequency data
df_daily = (
    pl.scan_csv('minute_level_data.csv')
    .group_by_dynamic('timestamp', every='1d')
    .agg([
        pl.col('value').mean().alias('avg_value'),
        pl.col('value').max().alias('max_value')
    ])
    .collect()
)
```

### Chart Performance

- **Line charts**: Limit to <500 data points per series (use downsampling for larger datasets)
- **Bar charts**: Limit to <50 categories (show top N, aggregate rest as "Other")
- **Scatter plots**: Cap at 1,000 points (use sampling: `df.sample(n=1000)`)
- **Tables**: Use pagination (`page_size=50`) for datasets >100 rows
- **Callbacks**: Avoid expensive computations in callbacks; pre-compute where possible

```python
# Efficient downsampling for charts
def downsample_timeseries(df, max_points=500):
    \"\"\"Reduce data points while preserving visual fidelity\"\"\"
    if len(df) <= max_points:
        return df
    
    # Calculate interval to achieve target points
    interval = len(df) // max_points
    return df.take_every(interval)
```

### Callback Performance

```python
# DON'T: Expensive computation in callback
@app.callback(Output('chart', 'figure'), [Input('filter', 'value')])
def update_chart(filter_val):
    # Reads entire file on every filter change - SLOW
    df = pl.read_csv('large_file.csv')
    filtered = df.filter(pl.col('category') == filter_val)
    return create_chart(filtered)

# DO: Load data globally, filter in callback
# At top of file (outside callbacks)
df = pl.read_csv('data.csv')  # Load once

@app.callback(Output('chart', 'figure'), [Input('filter', 'value')])
def update_chart(filter_val):
    # Fast filtering on in-memory data
    filtered = df.filter(pl.col('category') == filter_val)
    return create_chart(filtered)
```

### Deployment Considerations

For production deployment:

```python
# Development server (DO NOT use in production)
if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8050)

# Production server (use Gunicorn)
# Install: uv pip install gunicorn
# Run: gunicorn app:server --bind 0.0.0.0:8080 --workers 4
server = app.server  # Expose the Flask server for WSGI

# Or use waitress (Windows-compatible)
# Install: uv pip install waitress
# Run: waitress-serve --port=8080 app:server
```

## Examples

```
/build-dashboard Monthly sales dashboard with revenue trend, top products, and regional breakdown. Data is in the orders table.
```

```
/build-dashboard Here's our support ticket data [pastes CSV]. Build a dashboard showing volume by priority, response time trends, and resolution rates.
```

```
/build-dashboard Create a template executive dashboard for a SaaS company showing MRR, churn, new customers, and NPS. Use sample data.
```

## Tips

- **Development**: Dash apps run on `localhost:8050` during development with `debug=True` for hot-reloading
- **Production**: Deploy with Gunicorn (Linux/Mac) or Waitress (Windows) for production workloads
- **Static Export**: Add a "Download Report" button using `dcc.Download` to export static HTML snapshots
- **Real-time Updates**: Use `dcc.Interval` component for auto-refreshing dashboards (e.g., monitoring)
- **Theming**: Request specific Bootstrap themes (FLATLY, DARKLY, SOLAR, etc.) for different styling
- **Authentication**: Add user authentication with `dash-auth` for restricted access dashboards
- **Sharing**: Deploy to cloud platforms (Heroku, AWS, Azure) or share via URL for team access
- **Custom Components**: Extend with custom React components when needed for specialized visualizations

## Package Installation

Install required packages using `uv`:

```bash
uv pip install dash>=2.14.0
uv pip install dash-bootstrap-components>=1.5.0
uv pip install polars>=0.20.0
uv pip install plotly>=5.18.0

# For production deployment
uv pip install gunicorn  # Linux/Mac
# OR
uv pip install waitress  # Windows

# Optional: authentication
uv pip install dash-auth
```
