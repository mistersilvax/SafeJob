from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import models, config, os

app = Flask(__name__)

# Login (simple). In production, protect this properly.
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        pw = request.form.get('password')
        # default admin: user=admin password=changeme (change it)
        if user == 'admin' and pw == 'changeme':
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    rows = models.session.query(models.Candidate).order_by(models.Candidate.id.desc()).all()
    return render_template('dashboard.html', rows=rows, config=config)

@app.route('/candidate/<int:cid>')
def candidate(cid):
    row = models.session.query(models.Candidate).filter_by(id=cid).first()
    if not row:
        return 'Not found', 404
    return render_template('candidate.html', row=row)

@app.route('/uploads/resumes/<path:filename>')
def uploaded_resume(filename):
    return send_from_directory(config.RESUME_DIR, filename, as_attachment=True)

@app.route('/uploads/videos/<path:filename>')
def uploaded_video(filename):
    return send_from_directory(config.VIDEO_DIR, filename, as_attachment=True)

@app.route('/set_public_group', methods=['POST'])
def set_public_group():
    val = request.form.get('public_group')
    config.PUBLIC_JOBS_GROUP_LINK = val
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # run locally
    app.run(host='0.0.0.0', port=5000, debug=True)
