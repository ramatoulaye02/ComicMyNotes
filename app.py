from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired, ValidationError
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Use secrets.token_hex(16) for better security
app.config['UPLOAD_FOLDER'] = 'static/files'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Form for file upload
class UploadFileForm(FlaskForm):
    file = FileField("Upload a PDF", validators=[InputRequired()])
    submit = SubmitField("Upload")

    # Custom validator to allow only PDF files
    def validate_file(self, field):
        if not field.data.filename.lower().endswith('.pdf'):
            raise ValidationError("Only PDF files are allowed!")

@app.route('/', methods=['GET'])
def main_page():
    # Serve the main page (landing page)
    return render_template('main.html')


@app.route('/upload', methods=['GET', 'POST'])
def pdf_upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # Get uploaded file

        # Secure filename and add timestamp to prevent overwrites
        filename = f"{secure_filename("uploadedPDF.pdf")}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return "File has been uploaded successfully."

    return render_template('pdf.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

    
