"""Flask application will add new stakeholder information to the PE Database.

Automate the process to add stakeholder information to Cyber Sixgill portal.
"""
# Standard Python Libraries

#Send Emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


# Third-Party Libraries
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.units import inch
from werkzeug.utils import secure_filename

# Local file import
from datetime import datetime
import logging
import os.path
import time
# from data.config import config1, config2

from flask import Blueprint, \
    render_template, \
    flash,\
    redirect,\
    url_for,\
    current_app,\
    request
# from dkplastics import recaptcha




logging.basicConfig(filename='dkplasticsLog',filemode='a',format="%(asctime)-15s %(levelname)s %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S",
                    level=logging.INFO)


from dkplastics.data.config import config
from dkplastics.home.forms import applicationFormExternal, applicationFormContact

from dkplastics import recaptcha

home_blueprint = Blueprint(
    "home", __name__, template_folder="templates/home"
)


@home_blueprint.route("/")
# @app.route("/", methods=["GET", "POST"])
def index():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    year = datetime.now().year
    return render_template("home.html",year=year)

@home_blueprint.route("/company")
# @app.route("/", methods=["GET", "POST"])
def company():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("company.html")

@home_blueprint.route("/sheets")
# @app.route("/", methods=["GET", "POST"])
def sheets():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("sheets.html")

@home_blueprint.route("/thermoforming")
# @app.route("/", methods=["GET", "POST"])
def thermoforming():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("thermoforming.html")

@home_blueprint.route("/cnc")
# @app.route("/", methods=["GET", "POST"])
def cnc():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("cnc.html")

@home_blueprint.route("/gallery")
# @app.route("/", methods=["GET", "POST"])
def gallery():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("gallery.html")

@home_blueprint.route("/representatives")
# @app.route("/", methods=["GET", "POST"])
def representatives():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("representatives.html")

@home_blueprint.route("/community")
# @app.route("/", methods=["GET", "POST"])
def community():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("community.html")

def allowed_file(filename):
    '''Definition of allowed file types.'''
    #Allowed  file extensions to upload.
    ALLOWED_EXTENSIONS = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@home_blueprint.route("/upload", methods=["GET", "POST"])
def upload_file():
    """Directroy where bulk picutures will be uploaded."""
    filename = ''
    UPLOAD_FOLDER = current_app.config["UPLOAD_FOLDER"]

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        logging.info("There was a directory created for upload")
    except FileExistsError:
        logging.info("The upload folder already exists")

    if request.method == "POST":
        if "files[]" not in request.files:
            flash("No files where a present", "warning")
            return redirect(request.url)
        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER,filename))
                flash("The file was saved", "success")

        #If the user does not select a file, the browser submits on
        # empty file without a filename.
        # if file.filename == "":
        #     flash("No selected file", "warning")
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(UPLOAD_FOLDER, filename))
        #     flash("The file was saved", "success")
        else:
            flash("The file that was chosen cannot be uploaded", "warning")
            logging.info("The file that was chosen cannot be uploaded")
            return redirect(url_for('home.upload_file', name=filename))
        # return redirect(url_for('home.upload_file'))
    return render_template('upload.html')



@home_blueprint.route("/contact", methods=["GET", "POST"])
# @app.route("/", methods=["GET", "POST"])
def contact():
    """Create add customer html form.

    Gather data from form and insert into database.
    """

    name = False

    email = False

    subject = False

    message = False

    formContact = applicationFormContact()
    if recaptcha.verify():
        if formContact.validate_on_submit():
            flash('Your request has been submitted. We will be in touch shortly. Thank you!',category='success')
            # logging.info("Got to the submit validate")

            name = formContact.name.data
            email = formContact.email.data
            subject = formContact.subject.data
            message = formContact.message.data

            logging.info(f'The name is {name} and email is {email} and subject {subject} and message {message}')

            # Set fields to blank
            formContact.name.data = ''
            formContact.email.data = ''
            formContact.subject.data = ''
            formContact.message.data = ''

            logging.info(message)


            sendContactEmail(name, email, subject,message)
    else:
        flash('Please check the re-captcha to send your requests.', category='warning')

    return render_template(
        "contact.html",
        formContact=formContact,

    )




    return render_template("contact.html")

@home_blueprint.route("/terms")
# @app.route("/", methods=["GET", "POST"])
def terms():
    """Create add customer html form.

    Gather data from form and insert into database.
    """
    return render_template("terms.html")

def writetoJobFile(msg):
    #Personal info
    lname = msg['lname']
    fname = msg['fname']
    mi = msg['mi']
    entryDate = msg['entryDate']
    streetAddress = msg['streetAddress']
    city = msg['city']
    state = msg['state']
    zipcode = msg['zipcode']
    phonenum = msg['phonenum']
    email = msg['email']
    avalible = msg['avalible']
    ssn = msg['ssn']
    salary = msg['salary']
    position = msg['position']
    usCitizen = msg['usCitizen']
    usCitizenNoAuthorized = msg['usCitizenNoAuthorized']
    previousWork = msg['previousWork']
    previousWorkWhen = msg['previousWorkWhen']
    felon = msg['felon']
    explainFelon = msg['explainFelon']

    #Education
    highschool = msg['highschool']
    highschoolAdderess = msg['highschoolAddress']
    highschoolFrom = msg['highschoolFrom']
    highschoolTo = msg['highschoolTo']
    highschoolGraduate = msg['highschoolGraduate']
    highschoolDegree = msg['highschoolDegree']
    college = msg['college']
    collegeAddress = msg['collegeAddress']
    collegeFrom = msg['collegeFrom']
    collegeTo = msg['collegeTo']
    collegeGraduate = msg['collegeGraduate']
    collegeDegree = msg['collegeDegree']
    other = msg['other']
    otherAddress = msg['otherAddress']
    otherFrom = msg['otherFrom']
    otherTo = msg['otherTo']
    otherGraduate = msg['otherGraduate']
    otherDegree = msg['otherDegree']

    #First Ref
    firstRefName = msg['firstRefName']
    firstRefRelationship = msg['firstRefRelationship']
    firstRefPhone = msg['firstRefPhone']
    firstRefAddress = msg['firstRefAddress']
    firstRefCompany = msg['firstRefCompany']

    #Second Ref
    secondRefName = msg['secondRefName']
    secondRefRelationship = msg['secondRefRelationship']
    secondRefPhone = msg['secondRefPhone']
    secondRefAddress = msg['secondRefAddress']
    secondRefCompany = msg['secondRefCompany']


    #Third Ref
    thirdRefName = msg['thirdRefName']
    thirdRefRelationship = msg['thirdRefRelationship']
    thirdRefPhone = msg['thirdRefPhone']
    thirdRefAddress = msg['thirdRefAddress']
    thirdRefCompany = msg['thirdRefCompany']


    #First Job
    firstJobName = msg['firstJobName']
    firstJobPhone = msg['firstJobPhone']
    firstJobAddress = msg['firstJobAddress']
    firstJobSupervisor = msg['firstJobSupervisor']
    firstJobTitle = msg['firstJobTitle']
    firstJobSSalary = msg['firstJobSSalary']
    firstJobESalary = msg['firstJobESalary']
    firstJobResponsibilities = msg['firstJobResponsibilities']
    firstJobFrom = msg['firstJobFrom']
    firstJobTo = msg['firstJobTo']
    firstJobLeave = msg['firstJobLeave']
    firstJobpreviousWork = msg['firstJobpreviousWork']

    # Second Job
    secondJobName = msg['secondJobName']
    secondJobPhone = msg['secondJobPhone']
    secondJobAddress = msg['secondJobAddress']
    secondJobSupervisor = msg['secondJobSupervisor']
    secondJobTitle = msg['secondJobTitle']
    secondJobSSalary = msg['secondJobSSalary']
    secondJobESalary = msg['secondJobESalary']
    secondJobResponsibilities = msg['secondJobResponsibilities']
    secondJobFrom = msg['secondJobFrom']
    secondJobTo = msg['secondJobTo']
    secondJobLeave = msg['secondJobLeave']
    secondJobpreviousWork = msg['secondJobpreviousWork']


    # Third Job
    thirdJobName = msg['thirdJobName']
    thirdJobPhone = msg['thirdJobPhone']
    thirdJobAddress = msg['thirdJobAddress']
    thirdJobSupervisor = msg['thirdJobSupervisor']
    thirdJobTitle = msg['thirdJobTitle']
    thirdJobSSalary = msg['thirdJobSSalary']
    thirdJobESalary = msg['thirdJobESalary']
    thirdJobResponsibilities = msg['thirdJobResponsibilities']
    thirdJobFrom = msg['thirdJobFrom']
    thirdJobTo = msg['thirdJobTo']
    thirdJobLeave = msg['thirdJobLeave']
    thirdJobpreviousWork = msg['thirdJobpreviousWork']


    #Military Service
    branchService = msg['branchService']
    branchFrom = msg['branchFrom']
    branchTo = msg['branchTo']
    branchRankDischarge = msg['branchRankDischarge']
    branchtypeDischarge = msg['branchtypeDischarge']
    branchwasHonerable = msg['branchwasHonerable']
    branchexplainHonerable = msg['branchexplainHonerable']

    #Signiture
    signiture = msg['signiture']
    signitureDate = msg['signitureDate']




    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dkimage.png')
    doc = SimpleDocTemplate(f"{fname}_jobapplication.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=35, bottomMargin=18)
    Story = []
    logo = fn
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    # formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
    im = Image(logo, 2 * inch, .75 * inch)
    im.hAlign = 'LEFT'
    Story.append(im)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT))
    # ptext = '%s' % formatted_time
    # Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 3))


    ptext = f'Employment Application'
    Story.append(Paragraph(ptext, styles["Heading1"]))

    Story.append(Spacer(1, 6))
    ptext = f'Applicant Information'
    Story.append(Paragraph(ptext, styles["Heading2"]))

    Story.append(Spacer(1, 6))
    ptext = f'Last Name: {lname}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'First Name: {fname}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f' M.I. {mi}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Date: {entryDate}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Street Address and Apartment/Unit#: {streetAddress}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'City: {city}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'State: {state}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f' ZIP: {zipcode}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '

    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Phone: {phonenum}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'E-mail Address: {email}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Date Avalible: {avalible}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'SSN: {ssn}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f' Desired Salary: {salary}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Position Applied For: {position}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Are you a U.S. Citizen?: {usCitizen}&nbsp&nbsp&nbsp ' \
            f'If your answer was no, are you authorized to work in the U.S.?: {usCitizenNoAuthorized}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Have you ever worked for this company?: {previousWork}&nbsp&nbsp&nbsp ' \
            f'If so when?: {previousWorkWhen}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Have you ever been convicted of a felony?: {felon}&nbsp&nbsp&nbsp ' \
            f'If yes, explain?: {explainFelon}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    #Section for education
    Story.append(Spacer(1, 6))
    ptext = f'Education'
    Story.append(Paragraph(ptext, styles["Heading2"]))

    Story.append(Spacer(1, 6))
    ptext = f'High School: {highschool}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'High School Address: {highschoolAdderess}'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {highschoolFrom}&nbsp&nbsp&nbsp ' \
            f'To: {highschoolTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Did you graduate?: {highschoolGraduate}&nbsp&nbsp&nbsp ' \
            f'Degree: {highschoolDegree}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'College: {college}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'College Address: {collegeAddress}'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {collegeFrom}&nbsp&nbsp&nbsp ' \
            f'To: {collegeTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Did you graduate?: {collegeGraduate}&nbsp&nbsp&nbsp ' \
            f'Degree: {collegeDegree}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Other: {other}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Other Address: {otherAddress}'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {otherFrom}&nbsp&nbsp&nbsp ' \
            f'To: {otherTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Did you graduate?: {otherGraduate}&nbsp&nbsp&nbsp ' \
            f'Degree: {otherDegree}'
    Story.append(Paragraph(ptext, styles["Normal"]))

    # Section for references
    Story.append(Spacer(1, 6))
    ptext = f'References'
    Story.append(Paragraph(ptext, styles["Heading2"]))

    #First Reference
    Story.append(Spacer(1, 6))
    ptext = f'Full Name: {firstRefName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Relationship: {firstRefRelationship} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Company: {firstRefCompany}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone Number: {firstRefPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {firstRefAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '

    Story.append(Paragraph(ptext, styles["Normal"]))

    # Second Reference
    Story.append(Spacer(1, 6))
    ptext = f'Full Name: {secondRefName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Relationship: {secondRefRelationship} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Company: {secondRefCompany}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone Number: {secondRefPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {secondRefAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '

    Story.append(Paragraph(ptext, styles["Normal"]))

    # Third Reference
    Story.append(Spacer(1, 6))
    ptext = f'Full Name: {thirdRefName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Relationship: {thirdRefRelationship} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Company: {thirdRefCompany}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone Number: {thirdRefPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {firstRefAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '

    Story.append(Paragraph(ptext, styles["Normal"]))

    #Page Break to page 2
    Story.append(PageBreak())

    # Section for Previous Employment
    Story.append(Spacer(1, 6))
    ptext = f'Previous Employment'
    Story.append(Paragraph(ptext, styles["Heading2"]))


    # First Job
    Story.append(Spacer(1, 6))
    ptext = f'Job 1'
    Story.append(Paragraph(ptext, styles["Heading3"]))

    Story.append(Spacer(1, 6))
    ptext = f'Company: {firstJobName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone: {firstJobPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {firstJobAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Supervisor: {firstJobSupervisor} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Title: {firstJobTitle}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Starting Salary: {firstJobSSalary}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp '\
            f'Ending Salary: {firstJobESalary} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Responsibilities: {firstJobResponsibilities} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {firstJobFrom}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'To: {firstJobTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Reason for leaving: {firstJobLeave} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'May we contact your previous supervisor for a reference?: {firstJobpreviousWork} '

    Story.append(Paragraph(ptext, styles["Normal"]))

    # Second Job
    Story.append(Spacer(1, 6))
    ptext = f'Job 2'
    Story.append(Paragraph(ptext, styles["Heading3"]))
    Story.append(Spacer(1, 6))
    ptext = f'Company: {secondJobName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone: {secondJobPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {secondJobAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Supervisor: {secondJobSupervisor} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Title: {secondJobTitle}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Starting Salary: {secondJobSSalary}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Ending Salary: {secondJobESalary} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Responsibilities: {secondJobResponsibilities} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {secondJobFrom}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'To: {secondJobTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Reason for leaving: {secondJobLeave} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'May we contact your previous supervisor for a reference?: {secondJobpreviousWork} '

    Story.append(Paragraph(ptext, styles["Normal"]))

    # Third Job
    Story.append(Spacer(1, 6))
    ptext = f'Job 3'
    Story.append(Paragraph(ptext, styles["Heading3"]))
    Story.append(Spacer(1, 6))
    ptext = f'Company: {thirdJobName}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Phone: {thirdJobPhone} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Address: {thirdJobAddress}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Supervisor: {thirdJobSupervisor} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Title: {thirdJobTitle}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Starting Salary: {thirdJobSSalary}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Ending Salary: {thirdJobESalary} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Responsibilities: {thirdJobResponsibilities} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'From: {thirdJobFrom}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'To: {thirdJobTo}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Reason for leaving: {thirdJobLeave} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'May we contact your previous supervisor for a reference?: {thirdJobpreviousWork} '

    Story.append(Paragraph(ptext, styles["Normal"]))


    #Military Service

    # Section for Previous Employment
    Story.append(Spacer(1, 6))
    ptext = f'Military Service'
    Story.append(Paragraph(ptext, styles["Heading2"]))

    Story.append(Spacer(1, 6))
    ptext = f'Branch: {branchService}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'From: {branchFrom}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'To: {branchTo} '
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'Rank: {branchRankDischarge}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Type of Discharge: {branchtypeDischarge} '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = f'If other than honorable, explain: {branchexplainHonerable} '

    Story.append(Paragraph(ptext, styles["Normal"]))

    # Military Service

    # Section for Disclaimer
    Story.append(Spacer(1, 6))
    ptext = 'Disclaimer and Signiture'
    Story.append(Paragraph(ptext, styles["Heading2"]))

    Story.append(Spacer(1, 6))
    ptext = 'I certify that my answers are ture and complete to the best of my knowledge. '

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    ptext = 'If this application lead to employment, I understand that false or misleading' \
            ' information in my application or interview may result in my release. '

    Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 6))
    ptext = f'Signiture: {signiture}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp' \
            f'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
            f'Date: {signitureDate} '

    Story.append(Paragraph(ptext, styles["Normal"]))


    if doc.build(Story):
        sendEmailJobapp(lname, fname)




def sendEmailJobapp(lname, fname):
    # Set test to 1 when testing
    body = 'There have been some differences in applications found.<br><br> '

    subject = f'Job application from {fname} {lname}'
    test = 1
    if test == 0:
        mypeople = ['cduhn@hotmail.com', 'brianhenry75@yahoo.com', 'cduhn75@gmail.com']

    else:
         mypeople = ['scott@dkplastics.com', 'cduhn75@gmail.com']

    for person in mypeople:
        print(person)
        sender = 'no-reply@dkplastics.com'
        receivers = [f'{person}']
        mail = smtplib.SMTP()
        mail.connect('localhost')
        message = MIMEMultipart("alternative")
        message['From'] = 'DKPlastics Admin no-reply <no-reply@dkplastics.com>'
        message['To'] = f'{person}'
        message['Subject'] = f'{subject}'

        body1 = f'{body}'

        pdf = MIMEApplication(open(f"{fname}_jobapplication.pdf", 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment',
                       filename=f"{fname}_jobapplication.pdf")
        message.attach(pdf)


        part1 = MIMEText(body1, "html")

        message.attach(part1)

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.ehlo()
            smtpObj.sendmail(sender, receivers, message.as_string())
            logging.info(f"The job application for {fname}{lname} was sent successfully {subject}")
            print("Successfully sent email")
        except smtplib.SMTPException:

            logging.error(f'Exception occured ', exc_info=True)
            # print(f"Error: unable to send email{e}")

        except OSError as errorno:
            logging.error(f'The email did not send check to see if mail relay IP address is correct. {errorno}')

def sendContactEmail(name, email, subject,contact_message):
    # Set test to 1 when testing
    body = f'There is an email from {name} .<br><br> ' \
           f'Reply to {email} <br>' \
           f'The subject of the message: {subject}<br>' \
           f'The contact message: {contact_message}'




    subject = f'Job application from {subject}'
    test = 0
    if test == 0:
        mypeople = ['cduhn@hotmail.com', 'cduhn75@gmail.com']

    else:
         mypeople = ['scott@dkplastics.com', 'cduhn75@gmail.com']

    for person in mypeople:
        print(person)
        sender = 'no-reply@dkplastics.com'
        receivers = [f'{person}']
        mail = smtplib.SMTP()
        mail.connect('localhost')
        message = MIMEMultipart("alternative")
        message['From'] = 'DKPlastics Admin no-reply <no-reply@dkplastics.com>'
        message['To'] = f'{person}'
        message['Subject'] = f'{subject}'

        body1 = f'{body}'

        # pdf = MIMEApplication(open(f"{fname}_jobapplication.pdf", 'rb').read())
        # pdf.add_header('Content-Disposition', 'attachment',
        #                filename=f"{fname}_jobapplication.pdf")
        # message.attach(pdf)


        part1 = MIMEText(body1, "html")

        message.attach(part1)

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.ehlo()
            smtpObj.sendmail(sender, receivers, message.as_string())
            logging.info(f"The contact form was from {name} sent successfully {subject}")
            print("Successfully sent email")
        except smtplib.SMTPException:

            logging.error(f'Exception occured ', exc_info=True)
            # print(f"Error: unable to send email{e}")

        except OSError as errorno:
            logging.error(f'The email did not send check to see if mail relay IP address is correct. {errorno}')




@home_blueprint.route("/jobapp", methods=["GET","POST"])
# @app.route("/", methods=["GET", "POST"])
def jobapp():
    """Create add customer html form.
    Gather data from form and insert into database.
    """

    logging.info('Got to job app')
    # TODO keep the following two lines will need to get the attributes to feed into for loop to populate at the html file
    # formNames = [name for name in dir(formJobapp) if callable(getattr(formJobapp, name)) and not name.startswith("__") and not name.startswith("_")]
    # logging.info(formNames)

    applicationInfo = {}

    lname = False
    fname = False
    mi = False
    entryDate = False
    streetAddress = False
    city = False
    state = False
    zipcode = False
    phonenum = False
    email = False
    avalible = False
    ssn = False
    salary = False
    position = False
    usCitizen = False
    usCitizenNoAuthorized = False
    previousWork = False
    previousWorkWhen = False
    felon = False
    explainFelon = False

    #This section is the education section

    highschool = False
    highschoolAddress = False
    highschoolFrom = False
    highschoolTo = False
    highschoolGraduate = False
    highschoolDegree = False
    college = False
    collegeAddress = False
    collegeFrom = False
    collegeTo = False
    collegeGraduate = False
    collegeDegree = False
    other  = False
    otherAddress = False
    otherFrom = False
    otherTo = False
    otherGraduate = False
    otherDegree = False

    # This section is the Reference section
    firstRefName = False
    firstRefRelationship = False
    firstRefPhone = False
    firstRefAddress = False
    firstRefCompany = False

    secondRefName = False
    secondRefRelationship = False
    secondRefPhone = False
    secondRefAddress = False
    secondRefCompany = False

    thirdRefName = False
    thirdRefRelationship = False
    thirdRefPhone = False
    thirdRefAddress = False
    thirdRefCompany = False

    # This section os the employment

    firstJobName = False
    firstJobPhone = False
    firstJobAddress = False
    firstJobSupervisor = False
    firstJobTitle = False
    firstJobSSalary = False
    firstJobESalary = False
    firstJobResponsibilities = False
    firstJobFrom = False
    firstJobTo = False
    firstJobLeave = False
    firstJobpreviousWork = False

    # Second reference
    secondjobName = False
    secondJobPhone = False
    secondJobAddress = False
    secondJobSupervisor = False
    secondJobTitle = False
    secondJobSSalary = False
    secondJobESalary = False
    secondJobResponsibilities = False
    secondJobFrom = False
    secondJobTo = False
    secondJobLeave = False
    secondpreviousWork = False

    # Third reference
    thirdJobName = False
    thirdJobPhone = False
    thirdJobAddress = False
    thirdJobSupervisor = False
    thirdJobTitle = False
    thirdJobSSalary = False
    thirdJobESalary = False
    thirdJobResponsibilities = False
    thirdJobFrom = False
    thirdJobTo = False
    thirdJobLeave = False
    thirdpreviousWork = False

    #Branch of Service
    branchService = False
    branchFrom = False
    branchTo = False
    branchRankDischarge = False
    branchtypeDischarge = False
    branchwasHonerable = False
    branchexplainHonerable = False

    #Signiture
    signiture = False
    signitureDate = False

    formJobapp = applicationFormExternal()
    if recaptcha.verify():
        if formJobapp.validate_on_submit():
            flash('Your application has been submitted.')
            # logging.info("Got to the submit validate")

            lname = formJobapp.lname.data
            fname = formJobapp.fname.data
            mi = formJobapp.mi.data
            entryDate = formJobapp.entryDate.data.strftime('%m/%d/%Y')
            streetAddress = formJobapp.streetAddress.data
            city = formJobapp.city.data
            state = formJobapp.state.data
            zipcode = formJobapp.zipcode.data
            phonenum = formJobapp.phonenum.data
            email = formJobapp.email.data
            avalible = formJobapp.avalible.data
            ssn = formJobapp.ssn.data
            salary = formJobapp.salary.data
            position = formJobapp.position.data
            usCitizen = formJobapp.usCitizen.data
            usCitizenNoAuthorized = formJobapp.usCitizenNoAuthorized.data
            previousWork = formJobapp.previousWork.data
            previousWorkWhen = formJobapp.previousWorkWhen.data
            felon = formJobapp.felon.data
            explainFelon = formJobapp.explainFelon.data

            #This section is the school section
            highschool = formJobapp.highschool.data
            highschoolAddress = formJobapp.highschoolAddress.data
            highschoolFrom = formJobapp.highschoolFrom.data
            highschoolTo = formJobapp.highschoolTo.data
            highschoolGraduate = formJobapp.highschoolGraduate.data
            highschoolDegree = formJobapp.highschoolDegree.data
            college = formJobapp.college.data
            collegeAddress = formJobapp.collegeAddress.data
            collegeFrom = formJobapp.collegeFrom.data
            collegeTo = formJobapp.collegeTo.data
            collegeGraduate = formJobapp.collegeGraduate.data
            collegeDegree = formJobapp.collegeDegree.data
            other = formJobapp.other.data
            otherAddress = formJobapp.otherAddress.data
            otherFrom = formJobapp.otherFrom.data
            otherTo = formJobapp.otherTo.data
            otherGraduate = formJobapp.otherGraduate.data
            otherDegree = formJobapp.otherDegree.data



            #This section is the Reference section
            firstRefName = formJobapp.firstRefName.data
            firstRefRelationship = formJobapp.firstRefRelationship.data
            firstRefPhone = formJobapp.firstRefPhone.data
            firstRefAddress = formJobapp.firstRefAddress.data
            firstRefCompany = formJobapp.firstRefCompany.data

            secondRefName = formJobapp.secondRefName.data
            secondRefRelationship = formJobapp.secondRefRelationship.data
            secondRefPhone = formJobapp.secondRefPhone.data
            secondRefAddress = formJobapp.secondRefAddress.data
            secondRefCompany = formJobapp.secondRefCompany.data

            thirdRefName = formJobapp.thirdRefName.data
            thirdRefRelationship = formJobapp.thirdRefRelationship.data
            thirdRefPhone = formJobapp.thirdRefPhone.data
            thirdRefAddress = formJobapp.thirdRefAddress.data
            thirdRefCompany = formJobapp.thirdRefCompany.data

            #This section os the employment

            firstJobName = formJobapp.firstJobName.data
            firstJobPhone = formJobapp.firstJobPhone
            firstJobAddress = formJobapp.firstJobPhone.data
            firstJobSupervisor = formJobapp.firstJobSupervisor.data
            firstJobTitle = formJobapp.firstJobTitle.data
            firstJobSSalary = formJobapp.firstJobSSalary.data
            firstJobESalary = formJobapp.firstJobESalary.data
            firstJobResponsibilities = formJobapp.firstJobResponsibilities.data
            firstJobFrom = formJobapp.firstJobFrom.data.strftime('%m/%d/%Y')
            firstJobTo = formJobapp.firstJobTo.data.strftime('%m/%d/%Y')
            firstJobLeave= formJobapp.firstJobLeave.data
            firstJobpreviousWork = formJobapp.firstJobpreviousWork.data

            #Second JOB
            secondJobName = formJobapp.secondJobName.data
            secondJobPhone = formJobapp.secondJobPhone
            secondJobAddress = formJobapp.secondJobPhone.data
            secondJobSupervisor = formJobapp.secondJobSupervisor.data
            secondJobTitle = formJobapp.secondJobTitle.data
            secondJobSSalary = formJobapp.secondJobSSalary.data
            secondJobESalary = formJobapp.secondJobESalary.data
            secondJobResponsibilities = formJobapp.secondJobResponsibilities.data
            secondJobFrom = formJobapp.secondJobFrom.data.strftime('%m/%d/%Y')
            secondJobTo = formJobapp.secondJobTo.data.strftime('%m/%d/%Y')
            secondJobLeave = formJobapp.secondJobLeave.data
            secondJobpreviousWork = formJobapp.secondJobpreviousWork.data

            # Third JOB
            thirdJobName = formJobapp.thirdJobName.data
            thirdJobPhone = formJobapp.thirdJobPhone
            thirdJobAddress = formJobapp.thirdJobPhone.data
            thirdJobSupervisor = formJobapp.thirdJobSupervisor.data
            thirdJobTitle = formJobapp.thirdJobTitle.data
            thirdJobSSalary = formJobapp.thirdJobSSalary.data
            thirdJobESalary = formJobapp.thirdJobESalary.data
            thirdJobResponsibilities = formJobapp.thirdJobResponsibilities.data
            thirdJobFrom = formJobapp.thirdJobFrom.data.strftime('%m/%d/%Y')
            thirdJobTo = formJobapp.thirdJobTo.data.strftime('%m/%d/%Y')
            thirdJobLeave = formJobapp.thirdJobLeave.data
            thirdJobpreviousWork = formJobapp.thirdJobpreviousWork.data

            #Service Branch
            branchService = formJobapp.branchService.data
            branchFrom = formJobapp.branchFrom.data.strftime('%m/%d/%Y')
            branchTo = formJobapp.branchTo.data.strftime('%m/%d/%Y')
            branchRankDischarge = formJobapp.branchRankDischarge.data
            branchtypeDischarge = formJobapp.branchtypeDischarge.data
            branchwasHonerable = formJobapp.branchwasHonerable.data
            branchexplainHonerable = formJobapp.branchexplainHonerable.data

            #Sigiture
            signiture = formJobapp.signiture.data
            signitureDate = formJobapp.signitureDate.data.strftime('%m/%d/%Y')









            applicationInfo['lname'] = lname
            applicationInfo['fname'] = fname
            applicationInfo['mi'] = mi
            applicationInfo['entryDate'] = entryDate
            applicationInfo['streetAddress'] = streetAddress
            applicationInfo['city'] = city
            applicationInfo['state'] = state
            applicationInfo['zipcode'] = zipcode
            applicationInfo['phonenum'] = phonenum
            applicationInfo['email'] = email
            applicationInfo['avalible'] = avalible
            applicationInfo['ssn'] = ssn
            applicationInfo['salary'] = salary
            applicationInfo['position'] = position
            applicationInfo['usCitizen'] = usCitizen
            applicationInfo['usCitizenNoAuthorized'] = usCitizenNoAuthorized
            applicationInfo['previousWork'] = previousWork
            applicationInfo['previousWorkWhen'] = previousWorkWhen
            applicationInfo['felon'] = felon
            applicationInfo['explainFelon'] = explainFelon


            applicationInfo['highschool'] = highschool
            applicationInfo['highschoolAddress'] = highschoolAddress
            applicationInfo['highschoolFrom'] = highschoolFrom
            applicationInfo['highschoolTo'] = highschoolTo
            applicationInfo['highschoolGraduate'] = highschoolGraduate
            applicationInfo['highschoolDegree'] = highschoolDegree
            applicationInfo['college'] = college
            applicationInfo['collegeAddress'] = collegeAddress
            applicationInfo['collegeFrom'] = collegeFrom
            applicationInfo['collegeTo'] = collegeTo
            applicationInfo['collegeGraduate'] = collegeGraduate
            applicationInfo['collegeDegree'] = collegeDegree
            applicationInfo['other'] = other
            applicationInfo['otherAddress'] = otherAddress
            applicationInfo['otherFrom'] = otherFrom
            applicationInfo['otherTo'] = otherTo
            applicationInfo['otherGraduate'] = otherGraduate
            applicationInfo['otherDegree'] = otherDegree


            applicationInfo['firstRefName'] = firstRefName
            applicationInfo['firstRefRelationship'] = firstRefRelationship
            applicationInfo['firstRefPhone'] = firstRefPhone
            applicationInfo['firstRefAddress'] = firstRefAddress
            applicationInfo['firstRefCompany'] = firstRefCompany

            applicationInfo['secondRefName'] = secondRefName
            applicationInfo['secondRefRelationship'] = secondRefRelationship
            applicationInfo['secondRefPhone'] = secondRefPhone
            applicationInfo['secondRefAddress'] = secondRefAddress
            applicationInfo['secondRefCompany'] = secondRefCompany

            applicationInfo['thirdRefName'] = thirdRefName
            applicationInfo['thirdRefRelationship'] = thirdRefRelationship
            applicationInfo['thirdRefPhone'] = thirdRefPhone
            applicationInfo['thirdRefAddress'] = thirdRefAddress
            applicationInfo['thirdRefCompany'] = thirdRefCompany

            applicationInfo['firstJobName'] = firstJobName
            applicationInfo['firstJobPhone'] = firstJobPhone
            applicationInfo['firstJobAddress'] = firstJobAddress
            applicationInfo['firstJobSupervisor'] = firstJobSupervisor
            applicationInfo['firstJobTitle'] = firstJobTitle
            applicationInfo['firstJobSSalary'] = firstJobSSalary
            applicationInfo['firstJobESalary'] = firstJobESalary
            applicationInfo['firstJobResponsibilities'] = firstJobResponsibilities
            applicationInfo['firstJobFrom'] = firstJobFrom
            applicationInfo['firstJobTo'] = firstJobTo
            applicationInfo['firstJobLeave'] = firstJobLeave
            applicationInfo['firstJobpreviousWork'] = firstJobpreviousWork

            applicationInfo['secondJobName'] = secondJobName
            applicationInfo['secondJobPhone'] = secondJobPhone
            applicationInfo['secondJobAddress'] = secondJobAddress
            applicationInfo['secondJobSupervisor'] = secondJobSupervisor
            applicationInfo['secondJobTitle'] = secondJobTitle
            applicationInfo['secondJobSSalary'] = secondJobSSalary
            applicationInfo['secondJobESalary'] = secondJobESalary
            applicationInfo['secondJobResponsibilities'] = secondJobResponsibilities
            applicationInfo['secondJobFrom'] = secondJobFrom
            applicationInfo['secondJobTo'] = secondJobTo
            applicationInfo['secondJobLeave'] = secondJobLeave
            applicationInfo['secondJobpreviousWork'] = secondJobpreviousWork

            applicationInfo['thirdJobName'] = thirdJobName
            applicationInfo['thirdJobPhone'] = thirdJobPhone
            applicationInfo['thirdJobAddress'] = thirdJobAddress
            applicationInfo['thirdJobSupervisor'] = thirdJobSupervisor
            applicationInfo['thirdJobTitle'] = thirdJobTitle
            applicationInfo['thirdJobSSalary'] = thirdJobSSalary
            applicationInfo['thirdJobESalary'] = thirdJobESalary
            applicationInfo['thirdJobResponsibilities'] = thirdJobResponsibilities
            applicationInfo['thirdJobFrom'] = thirdJobFrom
            applicationInfo['thirdJobTo'] = thirdJobTo
            applicationInfo['thirdJobLeave'] = thirdJobLeave
            applicationInfo['thirdJobpreviousWork'] = thirdJobpreviousWork

            applicationInfo['branchService'] = branchService
            applicationInfo['branchFrom'] = branchFrom
            applicationInfo['branchTo'] = branchTo
            applicationInfo['branchRankDischarge'] = branchRankDischarge
            applicationInfo['branchtypeDischarge'] = branchtypeDischarge
            applicationInfo['branchwasHonerable'] = branchwasHonerable
            applicationInfo['branchexplainHonerable'] = branchexplainHonerable

            applicationInfo['signiture'] = signiture
            applicationInfo['signitureDate'] = signitureDate


            #Set fields to blank
            formJobapp.lname.data = ''
            formJobapp.fname.data = ''
            formJobapp.mi.data = ''
            formJobapp.entryDate.data = ''
            formJobapp.streetAddress.data = ''
            formJobapp.city.data = ''
            formJobapp.state.data = ''
            formJobapp.zipcode.data = ''
            formJobapp.phonenum.data = ''
            formJobapp.email.data = ''
            formJobapp.avalible.data = ''
            formJobapp.ssn.data = ''
            formJobapp.salary.data = ''
            formJobapp.position.data = ''
            formJobapp.usCitizen.data = ''
            formJobapp.usCitizenNoAuthorized.data = ''
            formJobapp.previousWork.data = ''
            formJobapp.previousWorkWhen.data = ''
            formJobapp.felon.data = ''
            formJobapp.explainFelon.data = ''

            # This section is the school section
            formJobapp.highschool.data = ''
            formJobapp.highschoolAddress.data = ''
            formJobapp.highschoolFrom.data = ''
            formJobapp.highschoolTo.data = ''
            formJobapp.highschoolGraduate.data = ''
            formJobapp.highschoolDegree.data = ''
            formJobapp.college.data = ''
            formJobapp.collegeAddress.data = ''
            formJobapp.collegeFrom.data = ''
            formJobapp.collegeTo.data = ''
            formJobapp.collegeGraduate.data = ''
            formJobapp.collegeDegree.data = ''
            formJobapp.other.data = ''
            formJobapp.otherAddress.data = ''
            formJobapp.otherFrom.data = ''
            formJobapp.otherTo.data = ''
            formJobapp.otherGraduate.data = ''
            formJobapp.otherDegree.data = ''

            #This section is the Reference section
            formJobapp.firstRefName.data = ''
            formJobapp.firstRefRelationship.data = ''
            formJobapp.firstRefPhone.data = ''
            formJobapp.firstRefAddress.data = ''
            formJobapp.firstRefCompany.data = ''
            #
            formJobapp.secondRefName.data = ''
            formJobapp.secondRefRelationship.data = ''
            formJobapp.secondRefPhone.data = ''
            formJobapp.secondRefAddress.data = ''
            formJobapp.secondRefCompany.data = ''

            formJobapp.thirdRefName.data = ''
            formJobapp.thirdRefRelationship.data = ''
            formJobapp.thirdRefPhone.data = ''
            formJobapp.thirdRefAddress.data = ''
            formJobapp.thirdRefCompany.data = ''

            #This section os the employment

            formJobapp.firstJobName.data = ''
            formJobapp.firstJobPhone.data = ''
            formJobapp.firstJobPhone.data = ''
            formJobapp.firstJobSupervisor.data = ''
            formJobapp.firstJobTitle.data = ''
            formJobapp.firstJobSSalary.data = ''
            formJobapp.firstJobESalary.data = ''
            formJobapp.firstJobResponsibilities.data = ''
            formJobapp.firstJobFrom.data = ''
            formJobapp.firstJobTo.data = ''
            formJobapp.firstJobLeave.data = ''
            formJobapp.firstJobpreviousWork.data = ''

            #Second reference
            formJobapp.secondJobName.data = ''
            formJobapp.secondJobPhone.data = ''
            formJobapp.secondJobPhone.data = ''
            formJobapp.secondJobSupervisor.data = ''
            formJobapp.secondJobTitle.data = ''
            formJobapp.secondJobSSalary.data = ''
            formJobapp.secondJobESalary.data = ''
            formJobapp.secondJobResponsibilities.data = ''
            formJobapp.secondJobFrom.data = ''
            formJobapp.secondJobTo.data = ''
            formJobapp.secondJobLeave.data = ''
            formJobapp.secondJobpreviousWork.data = ''

            # Third reference
            formJobapp.thirdJobName.data = ''
            formJobapp.thirdJobPhone.data = ''
            formJobapp.thirdJobPhone.data = ''
            formJobapp.thirdJobSupervisor.data = ''
            formJobapp.thirdJobTitle.data = ''
            formJobapp.thirdJobSSalary.data = ''
            formJobapp.thirdJobESalary.data = ''
            formJobapp.thirdJobResponsibilities.data = ''
            formJobapp.thirdJobFrom.data = ''
            formJobapp.thirdJobTo.data = ''
            formJobapp.thirdJobLeave.data = ''
            formJobapp.thirdJobpreviousWork.data = ''

            # Service Branch
            formJobapp.branchService.data = ''
            formJobapp.branchFrom.data = ''
            formJobapp.branchTo.data = ''
            formJobapp.branchRankDischarge.data = ''
            formJobapp.branchtypeDischarge.data = ''
            formJobapp.branchwasHonerable.data = ''
            formJobapp.branchexplainHonerable.data = ''

            #Signiture
            formJobapp.signiture.data = ''
            formJobapp.signitureDate.data = ''



            # logging.info(f'The application data lname is {lname}')
            writetoJobFile(applicationInfo)

            try:
                logging.info(f'The info is {applicationInfo}')
                # for x in applicationInfo:
                #     logging.info(f'The application data is {x}')
            #
            #     if cust not in allDomain.values():
            #         flash(f"You successfully submitted a new customer {cust} ",
            #               "success")
            #
            #         if setStakeholder(cust):
            #             logging.info(f"The customer {cust} was entered.")
            #
            #             allDomain1 = list(getAgency(cust).keys())[0]
            #             logging.info(f"The allDomain var is {allDomain1}")
            #
            #             if setCustRootDomain(allDomain1, cust, custRootDomainValue):
            #                 rootUUID = getRootID(allDomain1)
            #
            #                 # print(f'The rootUUID is {list(rootUUID.values())[0]}')
            #                 logging.info(
            #                     f"The Root Domain {custRootDomainValue} "
            #                     f"was entered at root_domains."
            #                 )
            #
            #                 if allSubDomain:
            #                     for subdomain in allSubDomain:
            #                         rootUUID1 = list(rootUUID.values())[0]
            #                         # print(f"The stake holder is {cust}")
            #                         # print(f"This is the subdomain {subdomain}")
            #                         # print(f"The subdomain {subdomain} the rootUUID {rootUUID1} and custRootDomainValue {custRootDomain[0]}")
            #
            #                         if setCustSubDomain(
            #                                 subdomain, rootUUID1, custRootDomain[0]
            #                         ):
            #                             logging.info(
            #                                 "The subdomains have been entered.")
            #                             #
            #                             # print(f"The cust {cust}")
            #                             # print(f"The custDomainAliases {custDomainAliases}")
            #                             # print(f"The custRootDomain {custRootDomain}")
            #                             # print(f'The allValidIP {allValidIP}')
            #                             # print(f'The executives {custExecutives}')
            #
            #                             setNewCSGOrg(
            #                                 cust,
            #                                 custDomainAliases,
            #                                 custRootDomain,
            #                                 allValidIP,
            #                                 custExecutives,
            #                             )
            #
            #     else:
            #         flash(f"The customer {cust} already exists.", "warning")
            #
            except ValueError as e:
                flash(f"The customer IP {e} is not a valid  please try again.",
                      "danger")
                return redirect(url_for("home.jobapp"))
            return redirect(url_for("home.jobapp"))
    else:
        flash('Please check the re-captcha to send your requests.', category='warning')
    return render_template(
        "jobapp.html",
        formJobapp=formJobapp,

    )


