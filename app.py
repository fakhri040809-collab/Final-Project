from flask import Flask, render_template, request

app = Flask(__name__)

students = [
    {"nama":"Devon", "nilai":90},
    {"nama":"Farrel", "nilai":84},
]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/student-tracker', methods=['GET','POST'])
def student_tracker():
    error = None
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        nilai = request.form.get('nilai', '').strip()
        if not nama:
            error = "Nama harus diisi!"
        if not nilai:
            error = "Nilai harus diisi!"
        else:
            nilai = int(nilai)
            if nilai < 0 or nilai > 100:
                error = "Nilai harus antara 0-100"
            else:
                students.append({
                    "nama":nama,
                    "nilai":nilai
                })
    avg = (
        sum(s['nilai'] for s in students)/len(students)
        if students else 0
    )
    return render_template(
        'student_tracker.html',
        students=students,
        avg=avg,
        error=error
    )

transactions = [
    {"type":"masuk", "desc":"Gaji", "amount": 5000000},
    {"type":"keluar", "desc":"Jajan", "amount": 100000},
]

@app.route('/finance', methods=['GET', 'POST'])
def finance():
    error = None
    if request.method == 'POST':
        tipe = request.form.get('type')
        desc = request.form.get('desc', '').strip()
        amount_text = request.form.get('amount', '').strip()
        if not desc:
            error = "Deskripsi harus diisi!"
        elif not amount_text:
            error = "Jumlah harus diisi"
        else:
            amount = int(amount_text)
            if amount <= 0:
                error = "Jumlah harus lebih dari 0"
            else:
                transactions.append({
                    "type": tipe,
                    "desc": desc,
                    "amount": amount
                })
    saldo = sum(
        t['amount'] if t['type'] == 'masuk' else -t['amount']
        for t in transactions
    )
    total_in = sum(
        t['amount']
        for t in transactions
        if t['type'] == 'masuk'
    )
    total_out = sum(
        t['amount']
        for t in transactions
        if t['type'] == 'keluar'
    )
    return render_template(
        'finance.html',
        transactions = transactions,
        saldo = saldo,
        total_in = total_in,
        total_out = total_out,
        error = error
    )    
    
from flask import redirect
@app.route('/hapus/<int:index>')
def hapus(index):
    if 0 <= index < len(transactions):
        del transactions[index]
    return redirect('/finance')

todo_list = [] #berguna menyimpan data todo list

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        item = request.form['item']
        if item != '':
            todo_list.append(item)
        return redirect('/todo')
    return render_template('todo.html', todos=todo_list)

@app.route('/todo/edit/<int:index>', methods=['GET', 'POST'])
def todo_edit(index):
    if request.method == 'POST':
        todo_list[index] = request.form['item']
        return redirect('/todo')
    return render_template('todo.html', 
                           todos=todo_list,
                           edit_index=index, 
                           edit_value=todo_list[index])

@app.route('/todo/hapus/<int:index>')
def todo_hapus(index):
    todo_list.pop(index)
    return redirect('/todo')

if __name__ == '__main__':
    app.run(debug=True)
    