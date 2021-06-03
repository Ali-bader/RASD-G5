# -*- coding: utf-8 -*-
"""
Created on Sun May 30 15:37:54 2021

@author: Ali
"""


from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
        connect
)


# Create the application instance
app = Flask(__name__, template_folder="GeoApp")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'k12$%dp08453gbbh//?'

# Create a URL route in our application for "/"
@app.route('/')
@app.route('/Home')
def Home():
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
    cur = conn.cursor()
    cur.execute(
             """SELECT system_table.user_id, comments_table.comment_id, comments_table.created,
            comments_table.title, comments_table.body 
               FROM system_table, comments_table WHERE  
                    system_table.user_id = comments_table.user_id"""
                    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    load_logged_in_user()

    return render_template('Home.html', posts=posts)

@app.route('/Index')
@app.route('/Index')
def index():
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
    cur = conn.cursor()
    cur.execute(
             """SELECT system_table.user_id, userdata_table.data_id, userdata_table.longintude, userdata_table.latitude,  userdata_table.Technician_Name, userdata_table.Habitat_Type, userdata_table.Water_Source, userdata_table.Vegetation_Type, userdata_table.Height_Grass_cm, userdata_table.Temperature, userdata_table.Humidity, userdata_table.Density_Grass_cm, userdata_table.Moisture_content FROM system_table, userdata_table WHERE  
                    system_table.user_id = userdata_table.user_id"""
            
                    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    load_logged_in_user()

    return render_template('index.html', posts=posts)

@app.route('/Register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else :
            myFile = open('dbConfig.txt')
            connStr = myFile.readline()
            conn = connect(connStr)
            cur = conn.cursor()
            cur.execute(
           'SELECT user_id FROM system_table WHERE username = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()
                conn.close()

        if error is None:
            cur.execute(
                'INSERT INTO system_table (username,email, password) VALUES (%s, %s, %s)',
                (username, email, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

        flash(error)

    return render_template('login.html')


@app.route('/Home/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        conn = connect(connStr)
        cur = conn.cursor()
        error = None
        cur.execute(
       'SELECT * FROM system_table WHERE username = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('Home'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Home'))

#@app.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        conn = connect(connStr)
        cur = conn.cursor()
        cur.execute(
                    'SELECT * FROM system_table WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
    if g.user is None:
        return False
    else: 
        return True




@app.route('/Index/Analysis/AddComment', methods=('GET', 'POST'))
def addcomment():
    if load_logged_in_user():
        if request.method == 'POST' :
            title = request.form['title']
            body = request.form['body']
            error = None
            
            if not title :
                error = 'Title is required!'
            if not body :
                error = 'body is required!'
            if error is not None :
                flash(error)
                return redirect(url_for('index'))
            else : 
                    myFile = open('dbConfig.txt')
                    connStr = myFile.readline()
                    conn = connect(connStr)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO comments_table (title, body, user_id) VALUES (%s, %s, %s)', 
                               (title, body, g.user[0])
                               )
                    cur.close()
                    conn.commit()
                    conn.close()
                    return redirect(url_for('index'))
        else :
            return render_template('addcomment.html')
    else :
        error = 'Only loggedin users can insert comment!'
        flash(error)
        return redirect(url_for('login'))
   
def get_post(id):
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
    cur = conn.cursor()
    cur.execute(
        """SELECT *
           FROM comments_table
           WHERE comments_table.comment_id = %s""",
        (id,)
    )
    post = cur.fetchone()

    if post is None:
        abort(404, "Post id {} doesn't exist.".format(id))

    if post[1] != g.user[0]:
        abort(403)

    return post

@app.route('/Index/Analysis/EditComment', methods=('GET', 'POST'))
def editcomment(id):
    if load_logged_in_user():
        post = get_post(id)
        if request.method == 'POST' :
            title = request.form['title']
            body = request.form['body']
            error = None
            
            if not title :
                error = 'Title is required!'
            if error is not None :
                flash(error)
                return redirect(url_for('index'))
            else : 
                myFile = open('dbConfig.txt')
                connStr = myFile.readline()
                conn = connect(connStr)
                cur = conn.cursor()
                cur.execute('UPDATE comments_table SET title = %s, body = %s'
                               'WHERE comment_id = %s', 
                               (title, body, id)
                               )
                cur.close()
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        else :
            return render_template('blog/update.html', post=post)
    else :
        error = 'Only loggedin users can insert comments!'
        flash(error)
        return redirect(url_for('login'))

@app.route('/Index/Analysis/deletecomment', methods=('POST',))
def deletecomment(id):
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
                
    cur = conn.cursor()
    cur.execute('DELETE FROM comments_table WHERE comment_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('Comments')) 

@app.route('/Index/Analysis/AddData', methods=('GET', 'POST'))
def Adddata():
    if load_logged_in_user():
        if request.method == 'POST' :
            longintude = request.form['longintude'] 
            latitude = request.form['latitude'] 
            Technician_Name = request.form['Technician_Name'] 
            Habitat_Type = request.form['Habitat_Type']
            Water_Source = request.form['Water_Source']
            Vegetation_Type = request.form['Vegetation_Type']
            Height_Grass_cm = request.form['Height_Grass_cm']
            Temperature = request.form['Temperature']
            Humidity = request.form['Humidity']
            Density_Grass_cm = request.form['Density_Grass_cm']
            Moisture_content = request.form['Moisture_content']
            error = None
            
           
            
            

            if not longintude :
                error = 'longintude is required!'
            if not latitude :
                error = 'latitude is required!'
            
            if not Technician_Name :
                error = 'Technician_Name is required!'
            if not Habitat_Type :
                error = 'Habitat_Type is required!' 
            if not Water_Source :
                error = 'Water_Source is required!'
            if not Vegetation_Type :
                error = 'Vegetation_Type is required!'
            if not Height_Grass_cm :
                error = 'Height_Grass_cm is required!'
            if not Temperature :
                error = 'Temperature is required!'
            if not Humidity :
                error = 'Humidity is required!'
            if not Density_Grass_cm :
                error = 'Density_Grass_cm is required!'
            if not Moisture_content :
                error = 'Moisture_content is required!'
              
            if error is not None :
                flash(error)
                return redirect(url_for('Home'))
            else : 
                    myFile = open('dbConfig.txt')
                    connStr = myFile.readline()
                    conn = connect(connStr)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO userdata_table (user_id, longintude, latitude, Technician_Name, Habitat_Type, Water_Source,Vegetation_Type, Height_Grass_cm, Temperature, Humidity, Density_Grass_cm, Moisture_content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                               ( g.user[0],longintude, latitude,  Technician_Name, Habitat_Type, Water_Source, Vegetation_Type, Height_Grass_cm, Temperature, Humidity, Density_Grass_cm, Moisture_content)
                               )
                    cur.close()
                    conn.commit()
                    conn.close()
                    return redirect(url_for('Analysis'))
        else :
            return render_template('Index.html')
    else :
        error = 'Only loggedin users can insert AddData !'
        flash(error)
        return redirect(url_for('login'))  
def get_Adddata(id):
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
    cur = conn.cursor()
    cur.execute(
        """SELECT *
           FROM data_table
           WHERE data_table.index = %s""",
        (id,)
    )
    Adddata = cur.fetchone()

    if Adddata is None:
        abort(404, "index {} doesn't exist.".format(id))

    if Adddata[1] != g.user[0]:
        abort(403)

    return Adddata
                            
@app.route('/<int:id>/editdata', methods=('GET', 'POST'))
def editdata(id):
    if load_logged_in_user():
        post = get_post(id)
        if request.method == 'POST' :
             longintude = request.form['longintude'] 
             latitude = request.form['latitude'] 
             Technician_Name = request.form['Technician_Name'] 
             Habitat_Type = request.form['Habitat_Type']
             Water_Source = request.form['Water_Source']
             Vegetation_Type = request.form['Vegetation_Type']
             Height_Grass_cm = request.form['Height_Grass_cm']
             Temperature = request.form['Temperature']
             Humidity = request.form['Humidity']
             Density_Grass_cm = request.form['Density_Grass_cm']
             Moisture_content = request.form['Moisture_content']
             error = None
            
             if not longintude :
                error = 'longintude is required!'
             if not latitude :
                error = 'latitude is required!'
            
             if not Technician_Name :
                error = 'Technician_Name is required!'
             if not Habitat_Type :
                error = 'Habitat_Type is required!' 
             if not Water_Source :
                error = 'Water_Source is required!'
             if not Vegetation_Type :
                error = 'Vegetation_Type is required!'
             if not Height_Grass_cm :
                error = 'Height_Grass_cm is required!'
             if not Temperature :
                error = 'Temperature is required!'
             if not Humidity :
                error = 'Humidity is required!'
             if not Density_Grass_cm :
                error = 'Density_Grass_cm is required!'
             if not Moisture_content :
                error = 'Moisture_content is required!'
             else : 
                myFile = open('dbConfig.txt')
                connStr = myFile.readline()
                conn = connect(connStr)
                cur = conn.cursor()
                cur.execute('UPDATE userdata_table SET longintude = %s, latitude = %s, Technician_Name = %s, Habitat_Type = %s, Water_Source = %s, Vegetation_Type = %s, Height_Grass_cm = %s, Temperature = %s, Humidity = %s, Density_Grass_cm = %s, Moisture_content = %s'
                               'WHERE data_id = %s', 
                               (longintude, latitude,  Technician_Name, Habitat_Type, Water_Source, Vegetation_Type, Height_Grass_cm, Temperature, Humidity, Density_Grass_cm, Moisture_content, id)
                               )
                cur.close()
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
        else :
            return render_template('blog/update.html', post=post)
    else :
        error = 'Only loggedin users can insert comments!'
        flash(error)
        return redirect(url_for('login'))

@app.route('/Index/Analysis/deletedata', methods=('POST',))
def deletedata(id):
    myFile = open('dbConfig.txt')
    connStr = myFile.readline()
    conn = connect(connStr)
                
    cur = conn.cursor()
    cur.execute('DELETE FROM userdata_table WHERE data_id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index')) 

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    
    
    
    
    
    