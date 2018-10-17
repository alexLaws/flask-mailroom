import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['name']).get()
        except Donor.DoesNotExist:
            new_donor = Donor(name=request.form['name'])
            new_donor.save()
            new_donation = Donation(value=request.form['amount'],
                                    donor=new_donor)
            new_donation.save()
        else:
            new_donation = Donation(value=request.form['amount'], donor=donor)
            new_donation.save()

        return redirect(url_for('all'))

    return render_template('create.jinja2')


@app.route('/view/')
def view():
    name = request.args.get('name', None)

    if name is None:
        return render_template('view.jinja2')
    else:
        try:
            donor = Donor.get(Donor.name == name)
        except Donor.DoesNotExist:
            return render_template('view.jinja2', error="Donor Not Found")

        donations = Donation.select().where(Donation.donor == donor)
        total = 0
        for donation in donations:
            total += donation.value

        return render_template('view.jinja2',
                               donations=donations,
                               name=donor.name,
                               total=total)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
