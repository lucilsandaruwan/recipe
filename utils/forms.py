from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField\
    , PasswordField\
    , SubmitField\
    , SelectField\
    , TextAreaField\
    , FileField\
    , IntegerField\
    , FieldList\
    , FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user
from services.auth import AuthService
from services.recipe import RecipeService
from PIL import Image
import os
from werkzeug.utils import secure_filename
import datetime

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    
    def validate_email(self, field):
        if AuthService.get_user_by_email(field.data):
            raise ValidationError('Email already registered. Please choose a different email.')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    def init_prfile(self):
        self.username.data = current_user.name
        self.email.data = current_user.email
    
    def validate_email(self, field):
        user = AuthService.get_user_by_email(field.data)
        if user and user.email != field.data :
            raise ValidationError('Email already registered. Please choose a different email.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', [DataRequired(), Length(min=8, max=20)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('new_password')])
    
    
    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Current password is incorrect.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])

class IngredientForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('Name', validators=[DataRequired(), Length(min = 2, max=50)])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    unit = StringField('Units', validators=[Length( max=20)])

class MethodForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min = 2, max=50)])
    discription = TextAreaField("Description", validators=[DataRequired()])
    class Meta:
        csrf = False

class RecipeCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min = 2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired()])
    recipe_image = FileField('Recipe Image', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), validators=[DataRequired()], min_entries=1)
    methods = FieldList(FormField(MethodForm), validators=[DataRequired()], min_entries=1)

    def init_form(self):
        self.category.choices = [(category.id, category.title) for category in RecipeService().get_category_for_select_field()]
    
    
    def validate_recipe_image(self, field):
        file_data = field.data
        temp_path = current_app.config["UPLOAD_PATH"] +  'dishes/'  

        # Save the uploaded file to a temporary location
        # the prefix datetime has added to unique the file name
        f_name = "{}_{}".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'), secure_filename(file_data.filename))
        file_path = os.path.join(temp_path, f_name)
        file_data.save(file_path)
        try:
            # Validate the width/height ratio within the range
            image = Image.open(file_path)
            width, height = image.size
            w_by_h = width / height
            if not 0.667 <= w_by_h <= 1.5:
                raise ValidationError('''The image dimensions are not suitable. 
                    Please provide an image with a width-to-height ratio between approximately 2:3 and 3:2.''')

            # Validate the file size
            size_in_mb = os.path.getsize(file_path) / 1024 / 1024
            if size_in_mb > 1.5:
                raise ValidationError('''The image size should be less than 1.5MB.''')

            # Validate the file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            _, extension = os.path.splitext(file_data.filename)
            if extension.lower() not in allowed_extensions:
                raise ValidationError('Invalid file extension. Only {} file extensions are allowed.'.format(", ".join(allowed_extensions)))
        except:
            # Clean up the temporary file
            os.remove(file_path)
        
        self.recipe_image_name = f_name
            

            
