import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail

def save_picture(form_picture):
    """From the input photo, split the name and save it in database"""
    random_hex = secrets.token_hex(8) #might collide with image names
    _, f_ext = os.path.splitext(form_picture.filename) #returns filename & extension
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path) # save the photo to db
    return picture_fn # return filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made
"""  # _external refers to absolute link
    mail.send(msg)