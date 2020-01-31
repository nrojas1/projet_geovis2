from flask import Flask, render_template, request, redirect, jsonify
import psycopg2 as psql

app = Flask(__name__)
db = psql.connect("dbname=musical_talent user=postgres password=uuuu" )

D = {
    'name': '', 'lastname': '', 'email': '', 'pt': '', 'instrument_id': '',
    'skill_id1': '', 'skill_id2': '', 'skill_id3': '', 'skill_id4': '',
    'genre_id1': '', 'genre_id2': '', 'genre_id3': '', 'genre_id4': '',
    'genre_id5': ''
    }

def strToPoint(d):
    point = d['latitude'], d['longitude']
    pt = 'SRID=3857;POINT'+str(point)
    pt = pt.replace(',','')
    pt = pt.replace('[','')
    pt = pt.replace(']','')
    pt = pt.replace("'",'')
    return pt

def tuplListToList(l):
    ll = list()
    for i in l:
        i = str(i)
        i = i.replace(',','')
        i = i.replace('(','')
        i = i.replace(')','')
        i = int(i)
        ll.append(i)
    return ll


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/form') # Show form on html
def new_talent():
    return render_template('new_musician.html')

@app.route('/db_new_musician', methods=['POST', 'GET']) # adding data to db
def db_update():
    # Fetch data from js
    r = request.form.to_dict(flat=False)
    pt = strToPoint(r)

    # Getting id's from database
    instrument = r['instrument']
    c1 = db.cursor()
    c1.execute("""
        SELECT id FROM instruments WHERE name = %s;
    """, instrument)
    inst_id = c1.fetchone()
    c1.close()
    skills = r['skill']
    if (len(skills)!=1):
        skills = tuple(skills)
        c2 = db.cursor()
        c2.execute("""
            SELECT id FROM skills WHERE name in {};
        """.format(skills))
        skills_ids = c2.fetchall()
        c2.close()
    else:
        c2 = db.cursor()
        c2.execute("""
            SELECT id FROM skills WHERE name = %s;
        """ ,skills)
        skills_ids = c2.fetchall()
        c2.close()
    genres = r['genre']
    if (len(genres) != 1):
        genres = tuple(genres)
        c3 = db.cursor()
        c3.execute("""
            SELECT id FROM genres WHERE name in {};
        """.format(genres))
        genres_ids = c3.fetchall()
        c3.close()
    else:
        c3 = db.cursor()
        c3.execute("""
            SELECT id FROM genres WHERE name = %s;
        """, genres)
        genres_ids = c3.fetchall()
        c3.close()

    # Preparing/formatting
    inst_id = tuplListToList(inst_id)
    skills_ids = tuplListToList(skills_ids)
    genres_ids = tuplListToList(genres_ids)

    # Placeholding
    D['name'] = r['name']
    D['lastname'] = r['lastname']
    D['email'] = r['email']
    D['pt'] = pt
    D['instrument_id'] = inst_id[0]

    # Conditioning: spaguetti
    if len(skills_ids) == 4:
        D['skill_id1'] = skills_ids[0]
        D['skill_id2'] = skills_ids[1]
        D['skill_id3'] = skills_ids[2]
        D['skill_id4'] = skills_ids[3]
    elif len(skills_ids) == 3:
        D['skill_id1'] = skills_ids[0]
        D['skill_id2'] = skills_ids[1]
        D['skill_id3'] = skills_ids[2]
        D['skill_id4'] = 123
    elif len(skills_ids) == 2:
        D['skill_id1'] = skills_ids[0]
        D['skill_id2'] = skills_ids[1]
        D['skill_id3'] = 123
        D['skill_id4'] = 123
    else:
        D['skill_id1'] = skills_ids[0]
        D['skill_id2'] = 123
        D['skill_id3'] = 123
        D['skill_id4'] = 123
    if len(genres_ids) == 5:
        D['genre_id1'] = genres_ids[0]
        D['genre_id2'] = genres_ids[1]
        D['genre_id3'] = genres_ids[2]
        D['genre_id4'] = genres_ids[3]
        D['genre_id5'] = genres_ids[4]
    elif len(genres_ids) == 4:
        D['genre_id1'] = genres_ids[0]
        D['genre_id2'] = genres_ids[1]
        D['genre_id3'] = genres_ids[2]
        D['genre_id4'] = genres_ids[3]
        D['genre_id5'] = 123
    elif len(genres_ids) == 3:
        D['genre_id1'] = genres_ids[0]
        D['genre_id2'] = genres_ids[1]
        D['genre_id3'] = genres_ids[2]
        D['genre_id4'] = 123
        D['genre_id5'] = 123
    elif len(genres_ids) == 2:
        D['genre_id1'] = genres_ids[0]
        D['genre_id2'] = genres_ids[1]
        D['genre_id3'] = 123
        D['genre_id4'] = 123
        D['genre_id5'] = 123
    else:
        D['genre_id1'] = genres_ids[0]
        D['genre_id2'] = 123
        D['genre_id3'] = 123
        D['genre_id4'] = 123
        D['genre_id5'] = 123

    # Insert data to db
    c4 = db.cursor()
    c4.execute("""
         INSERT INTO musicians
         (name, lastname, email, pt, instrument_id, skill_id1, skill_id2,
         skill_id3, skill_id4, genre_id1, genre_id2, genre_id3, genre_id4,
         genre_id5)
         VALUES
         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
     """, (D['name'], D['lastname'], D['email'], D['pt'], D['instrument_id'],
     D['skill_id1'], D['skill_id2'], D['skill_id3'], D['skill_id4'],
     D['genre_id1'], D['genre_id2'], D['genre_id3'], D['genre_id4'],
     D['genre_id5']))
    c4.close()
    db.commit()

    return redirect('/')


# JSON
@app.route('/musicians.json')
def m_json():
    c = db.cursor()
    c.execute("""
        SELECT
        id, name, lastname, email, ST_X(pt), ST_Y(pt), instrument_id,
        skill_id1, skill_id2, skill_id3, skill_id4, genre_id1, genre_id2,
        genre_id3, genre_id4, genre_id5
        FROM musicians
        ORDER BY id;
    """)
    rows = [{
    'id': l[0], 'name': l[1], 'lastname': l[2], 'email': l[3], 'x': l[4],
    'y': l[5], 'instrument_id': l[6], 'skill_id1': l[7], 'skill_id2': l[8],
    'skill_id3': l[9], 'skill_id4': l[10], 'genre_id1': l[11],
    'genre_id2': l[12], 'genre_id3': l[13], 'genre_id4': l[14],
    'genre_id5': l[15]} for l in c]
    c.close()
    return jsonify(rows)

@app.route('/stats.json')
def get_stats():
    c1 = db.cursor()
    c1.execute("""
        -- number of entries in db
        Select COUNT(*)
        FROM musicians;
    """)
    n_entries = c1.fetchone()
    c1.close()
    c2 = db.cursor()
    c2.execute("""
        -- number of distinct musicians
        SELECT COUNT(*) FROM (SELECT
        DISTINCT name, lastname, email
        FROM musicians) AS foo;
    """)
    n_musician = c2.fetchone()
    c2.close()
    c3 = db.cursor()
    c3.execute("""
        -- number each instrument in db
        SELECT COUNT(instruments.name), instruments.name
        FROM musicians
        JOIN instruments on musicians.instrument_id = instruments.id
        GROUP BY instruments.name
        ORDER BY instruments.name;
    """)
    n_per_instruments = c3.fetchall()
    c3.close()
    di = dict()
    for i in n_per_instruments:
        di[i[1]]=i[0]
    d = {'number of entries': n_entries[0], 'number of musicians': n_musician[0],
    'count of each instrument': di}
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
