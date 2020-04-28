from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)

def get_results(sort_by, sort_order, source_region):
    conn = sqlite3.connect('Browdway_touring_theater.sqlite')
    cur = conn.cursor()
    
    if sort_by == 'rating':
        sort_column = 'rating'
    elif sort_by =='price':
         sort_column = 'price'
    else:
        sort_column='review_count'

    where_clause = ''
    if (source_region != 'All'):
        where_clause = f'WHERE t.Name = "{source_region}"'
    
    q = f'''
        SELECT r.name,phone, location, {sort_column}
        FROM recommended_restaurants r 
        JOIN touring_theater t 
            ON r.touring_theatre_id=t.Id
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        LIMIT 50
    '''
    print(q)
    results = cur.execute(q).fetchall()
    conn.close()
    print(results)
    return results

def get_theater(name):
    conn = sqlite3.connect('Browdway_touring_theater.sqlite')
    cur = conn.cursor()
    q=f'''
    SELECT t.Name,City,State,Address,Zipcode,Website_link 
    FROM touring_theater t 
    JOIN show_theater st 
        ON t.Id=st.touring_theater_id 
        JOIN touring_show s 
            ON st.touring_show_id=s.id 
    WHERE s.name='{name}'
    '''
    print(q)
    theaters = cur.execute(q).fetchall()
    conn.close()
    print(theaters)
    return theaters

def get_musical(theater):
    conn = sqlite3.connect('Browdway_touring_theater.sqlite')
    cur = conn.cursor()
    q=f'''
    SELECT s.name FROM touring_theater t 
    JOIN show_theater st 
        ON t.Id=st.touring_theater_id 
        JOIN touring_show s 
            ON st.touring_show_id=s.id 
    WHERE t.name='{theater}';
    '''
    print(q)
    musicals = cur.execute(q).fetchall()
    conn.close()
    print(musicals)
    return musicals

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/theater', methods=['POST'])
def theaters():
    name = request.form['name']
    theater=get_theater(name)
    return render_template('theater.html', 
            theater=theater,name=name)

@app.route('/musical', methods=['POST'])
def musicals():
    theater = request.form['musical']
    musicals=get_musical(theater)
    return render_template('musical.html', 
            musicals=musicals,theater=theater)

@app.route('/results', methods=['POST'])
def restaurants():
    sort_by = request.form['sort']
    sort_order = request.form['dir']
    source_region = request.form['region']
    results = get_results(sort_by, sort_order, source_region)
    bar_results = request.form.get('bar', False)
    hist_results = request.form.get('hist', False)
    if (bar_results):
        x_vals = [r[0] for r in results]
        y_vals = [r[3] for r in results]
        bars_data = go.Bar(
            x=x_vals,
            y=y_vals
        )
        layout = go.Layout(title="Bar Chart")
        fig = go.Figure(data=bars_data,layout=layout)
        div = fig.to_html(full_html=False)
        return render_template("plot.html", plot_div=div)
    elif (hist_results):
        x = [r[3] for r in results]
        layout = go.Layout(title="Histogram Frequency Counts")
        fig = go.Figure(data=[go.Histogram(x=x)],layout=layout)
        div = fig.to_html(full_html=False)
        return render_template("plot.html", plot_div=div)
    else:
        return render_template('results.html', 
            sort=sort_by, results=results,
            region=source_region)

if __name__ == '__main__':
    app.run(debug=True)