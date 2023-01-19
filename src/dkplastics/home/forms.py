from flask_wtf import FlaskForm
from wtforms import DateField,StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, RadioField


class applicationFormExternal(FlaskForm):
    """Create web form to take user input on organization information/details."""

    lname = StringField("What is the last name?", validators=[DataRequired()])


    fname = StringField("What is the first name.", validators=[DataRequired()])

    mi = StringField("What your middle initial? ", validators=[DataRequired()])

    entryDate = DateField("What is the date * mm/dd/YYYY.",format='%Y-%m-%d', validators=[DataRequired()])

    streetAddress = StringField("What your address? ", validators=[DataRequired()])

    city = StringField("What city do you live in?", validators=[DataRequired()])

    state = StringField("What state are you from? ", validators=[DataRequired()])

    zipcode = StringField("What is your zipcode?", validators=[DataRequired()])

    phonenum = StringField("What is your phone number? ", validators=[DataRequired()])

    email = StringField("What is your email?", validators=[DataRequired()])

    avalible = StringField("What is your avalibility? ", validators=[DataRequired()])
    #
    ssn = StringField("What is your SSN?", validators=[DataRequired()])

    salary = StringField("What your desired salary? ", validators=[DataRequired()])

    position = StringField('What position applying for?', validators=[DataRequired()])

    usCitizen= RadioField("Are you a US Citizen?",choices=[('yes','yes'),('no','no')], validators=[DataRequired()])

    usCitizenNoAuthorized = RadioField("If you are not a US Citizen are you authorized to work in the U.S.?",
                           choices=[('yes', 'yes'), ('no', 'no')],
                           validators=[DataRequired()])

    previousWork = RadioField("Have you worked for DKPlastics before? ",choices=[('yes','yes'),('no','no')], validators=[DataRequired()])

    previousWorkWhen = StringField("When did you last work for DKPlastics?")

    felon = RadioField("Are you a convicted felon? ", choices=[('yes','yes'),('no','no')], validators=[DataRequired()])

    explainFelon = StringField("If so explain.")





    # This next section is the Education section

    highschool = StringField("High School? ", validators=[DataRequired()])

    highschoolAddress = StringField("Highschool address", validators=[DataRequired()])

    highschoolFrom = DateField("Date from * mm/dd/YYYY.", format='%Y-%m-%d',
                          validators=[DataRequired()])

    highschoolTo = DateField("Date to * mm/dd/YYYY.", format='%Y-%m-%d',
                               validators=[DataRequired()])

    highschoolGraduate = RadioField("Did you graduate?",
                           choices=[('yes', 'yes'), ('no', 'no')],
                           validators=[DataRequired()])

    highschoolDegree = StringField("Degree? ", validators=[DataRequired()])

    college = StringField("College? ", validators=[DataRequired()])
    #
    collegeAddress = StringField("College address", validators=[DataRequired()])

    collegeFrom = DateField("Date from * mm/dd/YYYY.", format='%Y-%m-%d',
                               validators=[DataRequired()])

    collegeTo = DateField("Date to * mm/dd/YYYY.", format='%Y-%m-%d',
                             validators=[DataRequired()])

    collegeGraduate = RadioField("Did you graduate?",
                                    choices=[('yes', 'yes'), ('no', 'no')],
                                    validators=[DataRequired()])

    collegeDegree = StringField("Degree? ", validators=[DataRequired()])

    other = StringField("Other education? ", validators=[DataRequired()])

    otherAddress = StringField("Other address", validators=[DataRequired()])

    otherFrom = DateField("Date from * mm/dd/YYYY.", format='%Y-%m-%d',
                               validators=[DataRequired()])

    otherTo = DateField("Date to * mm/dd/YYYY.", format='%Y-%m-%d',
                             validators=[DataRequired()])

    otherGraduate = RadioField("Did you graduate?",
                                    choices=[('yes', 'yes'), ('no', 'no')],
                                    validators=[DataRequired()])

    otherDegree = StringField("Degree? ", validators=[DataRequired()])



    # This next section is the Reference section

    firstRefName = StringField("Full Name? ", validators=[DataRequired()])

    firstRefRelationship = StringField("Relationship", validators=[DataRequired()])

    firstRefPhone = StringField("Phone Number", validators=[DataRequired()])

    firstRefAddress = StringField("Address", validators=[DataRequired()])

    firstRefCompany = StringField("Company", validators=[DataRequired()])



    secondRefName = StringField("Full Name? ", validators=[DataRequired()])

    secondRefRelationship = StringField("Relationship",
                                       validators=[DataRequired()])

    secondRefPhone = StringField("Phone Number", validators=[DataRequired()])

    secondRefAddress = StringField("Address", validators=[DataRequired()])

    secondRefCompany = StringField("Company", validators=[DataRequired()])





    thirdRefName = StringField("Full Name? ", validators=[DataRequired()])

    thirdRefRelationship = StringField("Relationship",
                                        validators=[DataRequired()])

    thirdRefPhone = StringField("Phone Number", validators=[DataRequired()])

    thirdRefAddress = StringField("Address", validators=[DataRequired()])

    thirdRefCompany = StringField("Company", validators=[DataRequired()])



    # This next section is the Employment section

    firstJobName = StringField("Full Name? ", validators=[DataRequired()])

    firstJobPhone = StringField("Phone",
                                       validators=[DataRequired()])

    firstJobAddress = StringField("Address", validators=[DataRequired()])

    firstJobSupervisor = StringField("Supervisor", validators=[DataRequired()])

    firstJobTitle = StringField("Title", validators=[DataRequired()])

    firstJobSSalary = StringField("Starting Salary", validators=[DataRequired()])

    firstJobESalary = StringField("Ending Salary", validators=[DataRequired()])

    firstJobResponsibilities = StringField("Title", validators=[DataRequired()])

    firstJobFrom = DateField("From Date: i.e. mm/dd/YYYY.",format='%Y-%m-%d',
                             validators=[DataRequired()])

    firstJobTo = DateField("To Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                             validators=[DataRequired()])

    firstJobLeave = StringField("Reason for leaving", validators=[DataRequired()])


    firstJobpreviousWork = RadioField("May we contact your previous Employer? ",
                              choices=[('yes','yes'),('no','no')],
                              validators=[DataRequired()])






    secondJobName = StringField("Full Name? ", validators=[DataRequired()])

    secondJobPhone = StringField("Phone",
                                validators=[DataRequired()])

    secondJobAddress = StringField("Address", validators=[DataRequired()])

    secondJobSupervisor = StringField("Supervisor", validators=[DataRequired()])

    secondJobTitle = StringField("Title", validators=[DataRequired()])

    secondJobSSalary = StringField("Starting Salary",
                                  validators=[DataRequired()])

    secondJobESalary = StringField("Ending Salary", validators=[DataRequired()])

    secondJobResponsibilities = StringField("Title", validators=[DataRequired()])

    secondJobFrom = DateField("From Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                             validators=[DataRequired()])

    secondJobTo = DateField("To Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                           validators=[DataRequired()])

    secondJobLeave = StringField("Reason for leaving",
                                validators=[DataRequired()])



    secondJobpreviousWork = RadioField("May we contact your previous Employer? ",
                              choices=[('yes', 'yes'), ('no', 'no')],
                              validators=[DataRequired()])





    thirdJobName = StringField("Full Name? ", validators=[DataRequired()])

    thirdJobPhone = StringField("Phone",
                                 validators=[DataRequired()])

    thirdJobAddress = StringField("Address", validators=[DataRequired()])

    thirdJobSupervisor = StringField("Supervisor", validators=[DataRequired()])

    thirdJobTitle = StringField("Title", validators=[DataRequired()])

    thirdJobSSalary = StringField("Starting Salary",
                                   validators=[DataRequired()])

    thirdJobESalary = StringField("Ending Salary", validators=[DataRequired()])

    thirdJobResponsibilities = StringField("Title",
                                            validators=[DataRequired()])

    thirdJobFrom = DateField("From Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                              validators=[DataRequired()])

    thirdJobTo = DateField("To Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                            validators=[DataRequired()])

    thirdJobLeave = StringField("Reason for leaving",
                                 validators=[DataRequired()])



    thirdJobpreviousWork = RadioField("May we contact your previous Employer? ",
                                    choices=[('yes', 'yes'), ('no', 'no')],
                                    validators=[DataRequired()])


    #Military service

    branchService = StringField("Branch Name? ", validators=[DataRequired()])

    branchFrom = DateField("From Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                             validators=[DataRequired()])

    branchTo = DateField("To Date: i.e. mm/dd/YYYY.", format='%Y-%m-%d',
                           validators=[DataRequired()])

    branchRankDischarge = StringField("Rank at Discharge",
                                validators=[DataRequired()])

    branchtypeDischarge = RadioField("Type of Discharge",choices=[('Honerable','Honerable'),('Other','Other')], validators=[DataRequired()])

    branchwasHonerable = StringField("Supervisor", validators=[DataRequired()])

    branchexplainHonerable = StringField("Explain if other than Honerable", validators=[DataRequired()])

    #Signiture block
    signiture = StringField("Signiture", validators=[DataRequired()])
    signitureDate = DateField("What is the date signed? * mm/dd/YYYY.", format='%Y-%m-%d',
                          validators=[DataRequired()])



    submit = SubmitField("Submit Application", render_kw={"onclick": "loading()"})


class applicationFormContact(FlaskForm):
    """Create web form to take user input on organization information/details."""

    name = StringField("What is your name?", validators=[DataRequired()])


    email = StringField("What is the email?", validators=[DataRequired()])

    subject = StringField("What your subject? ", validators=[DataRequired()])

    message = TextAreaField("What your is your message? ", validators=[DataRequired()])

    submit = SubmitField("Submit Contact Form", render_kw={"onclick": "loading()"})