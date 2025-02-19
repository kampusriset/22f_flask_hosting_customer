from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi koneksi MySQL
db = MySQLdb.connect(host="localhost", user="root", passwd="", db="hosting_db")
cursor = db.cursor()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            error_message = "Username atau password salah. Silakan coba lagi."
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (username, hashed_password))
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Mengambil parameter search dan page dari URL
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Jumlah item per halaman
    
    # Query dasar
    base_query = "FROM hosting WHERE user_id = %s"
    count_query = "SELECT COUNT(*) " + base_query
    params = [session['user_id']]
    
    # Menambahkan kondisi search jika ada
    if search:
        base_query += " AND domain LIKE %s"
        count_query += " AND domain LIKE %s"
        params.append(f"%{search}%")
    
    # Mengambil total jumlah data
    cursor.execute(count_query, tuple(params))
    total_items = cursor.fetchone()[0]
    
    # Menghitung total halaman
    total_pages = (total_items + per_page - 1) // per_page
    
    # Memastikan page dalam range yang valid
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1
    
    # Query untuk mengambil data dengan pagination
    offset = (page - 1) * per_page
    query = f"SELECT * {base_query} ORDER BY domain LIMIT %s OFFSET %s"
    params.extend([per_page, offset])
    
    cursor.execute(query, tuple(params))
    hostings = cursor.fetchall()
    
    return render_template('dashboard.html', 
                         hostings=hostings,
                         page=page,
                         total_pages=total_pages,
                         search=search)

@app.route('/add_hosting', methods=['POST'])
def add_hosting():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    domain = request.form['domain']
    expiry_date = request.form['expiry_date']

    cursor.execute("INSERT INTO hosting (user_id, domain, expiry_date) VALUES (%s, %s, %s)", 
                   (session['user_id'], domain, expiry_date))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_hosting/<int:id>')
def delete_hosting(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cursor.execute("DELETE FROM hosting WHERE id = %s AND user_id = %s", (id, session['user_id']))
    db.commit()
    return redirect(url_for('dashboard'))

# Fitur Edit
@app.route('/edit_hosting/<int:id>', methods=['GET', 'POST'])
def edit_hosting(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Menampilkan data hosting untuk diedit jika metode adalah GET
    if request.method == 'GET':
        cursor.execute("SELECT * FROM hosting WHERE id = %s AND user_id = %s", (id, session['user_id']))
        hosting = cursor.fetchone()
        if hosting:
            return render_template('edit_hosting.html', hosting=hosting)
        else:
            return redirect(url_for('dashboard'))  # Jika hosting tidak ditemukan
    
    # Jika metode adalah POST, perbarui data hosting
    if request.method == 'POST':
        domain = request.form['domain']
        expiry_date = request.form['expiry_date']

        cursor.execute("UPDATE hosting SET domain = %s, expiry_date = %s WHERE id = %s AND user_id = %s", 
                       (domain, expiry_date, id, session['user_id']))
        db.commit()
        return redirect(url_for('dashboard'))

@app.route('/view_hosting/<int:id>')
def view_hosting(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Ambil data hosting berdasarkan id dan user_id
    cursor.execute("SELECT * FROM hosting WHERE id = %s AND user_id = %s", (id, session['user_id']))
    hosting = cursor.fetchone()
    if hosting:
        return render_template('view_hosting.html', hosting=hosting)
    else:
        return redirect(url_for('dashboard'))  # Jika hosting tidak ditemukan
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Cek password saat ini
        cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        if not bcrypt.checkpw(current_password.encode('utf-8'), user[0].encode('utf-8')):
            return render_template('change_password.html', error="Password saat ini salah")
        
        # Cek konfirmasi password baru
        if new_password != confirm_password:
            return render_template('change_password.html', error="Password baru dan konfirmasi tidak cocok")
        
        # Update password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
                      (hashed_password, session['user_id']))
        db.commit()
        
        return render_template('change_password.html', success="Password berhasil diubah")
    
    return render_template('change_password.html')

if __name__ == '__main__':
    app.run(debug=True)
