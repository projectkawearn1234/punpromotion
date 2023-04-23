import random
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder='templates')
admins = pd.read_csv('admin.csv')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username:
            error = 'Please enter your username'
            return render_template('admin_login.html', error=error)
        elif not password:
            error = 'Please enter your password'
            return render_template('admin_login.html', error=error)
        elif any((admins['username'] == username) & (admins['password'] == int(password))):
            return redirect(url_for('admin_panel'))
        else:
            error = 'Incorrect username or password'
            return render_template('admin_login.html', error=error)
    else:
        return render_template('admin_login.html')

@app.route('/admin/panel', methods=['GET'])
def admin_panel():
    image_dir = 'static/image_dataset'
    images = os.listdir(image_dir)[:104]
    images_data = []
    for image_name in images:
        image_path = os.path.join(image_dir, image_name)
        image_data = {'image_name': image_name, 'image_path': image_path}
        images_data.append(image_data)
    random.shuffle(images_data)
    return render_template('admin_panel.html', images=images_data)

@app.route('/admin/edit/<string:image_name>', methods=['GET', 'POST'])
def admin_edit(image_name):
    if request.method == 'POST':
        price = request.form['price']
        promotion_time = request.form['promotion_time']
        discount = request.form['discount']
        
        # convert discount to percentage
        discount = str(discount) + '%'
        
        # update the csv file with the new data
        df = pd.read_csv('database.csv')
        df.loc[df['filename'] == image_name, ['Price', 'Promotion Time', 'Discount']] = [price, promotion_time, discount]
        df.to_csv('database.csv', index=False)
        
        return redirect(url_for('admin_panel'))
    else:
        image_path = os.path.join('static/image_dataset', image_name)
        return render_template('admin_edit.html', image_name=image_name, image_path=image_path)

if __name__ == '__main__':
    app.run(debug=True)
