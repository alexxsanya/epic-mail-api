from flask import abort, jsonify
import re
class UserValidator():
    user_object = None
    def __init__(self):
        pass

    @staticmethod
    def validator(user):
        user = {
            "email":user.get('email'),
            "firstname":user.get('firstname'),
            "lastname":user.get('lastname'),
            "password":user.get('password'),
            "recovery_email":user.get('recovery_email')
        }
        UserValidator.user_object = user

        for field in user: 
            UserValidator().validate_user(field) 

        return True

    def validate_user(self,field):
        method_name = 'validate_' + str(field)

        method = getattr(self, method_name, lambda: "Invalid Field")
        
        return method()

    def validate_email(self):
        email = self.user_object.get('email')
        UserValidator.is_email_valid(email)
        
    def validate_firstname(self):
        fname = self.user_object.get('firstname')
        if not fname.isalpha() or len(fname) < 2:
            abort(self.error_message(
                error = 'Firstname should be atleast 2 letters without numbers',
                code = 400
            ))           

    def validate_lastname(self):
        fname = self.user_object.get('firstname')
        lname = self.user_object.get('lastname')
        if fname.lower() == lname.lower():
            abort(self.error_message(
                error = 'Firstname & Lastname can not be the same',
                code = 400
            ))             
        if not lname.isalpha() or len(fname) < 2:
            abort(self.error_message(
                error = 'Lastname should be atleast 2 letters without numbers',
                code = 400
            )) 

    def validate_password(self):
        UserValidator.is_pass_valid(self.user_object.get('password'))           

    def validate_recovery_email(self):
        r_email = self.user_object.get('recovery_email')
        email = self.user_object.get('email')
        if r_email.lower() == email.lower():
            abort(self.error_message(
                error = 'Recovery email & your choosen email address can not be the same',
                code = 400
            ))               
        UserValidator.is_email_valid(r_email)
        
    def error_message(self,error,code):
        return jsonify({
            'status':code,
            'error':error
        })

    @staticmethod
    def is_email_valid(email):
        email_regex = email_regex = \
            re.compile(r'''([a-zA-Z0-9._%+-]+@ [a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))''',\
                re.VERBOSE)
        valid_email = email_regex.search(email)
        if valid_email:
            return True
        abort(UserValidator().error_message(
            error = "Invalid email format for {}".format(email),
            code = 400,
        )) 

    @staticmethod
    def is_pass_valid(password):
        pass_regx = re.match(\
            r'''^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$''',\
                password)
        if not pass_regx:
             abort(UserValidator().error_message(
                error = '''Password should be atleast 6 char a combination of \
                    lower & upper letters, numbers and @ # $'''.replace("                     ", " "),
                code = 400,
            ))    
        return True      

class MessageValidator():

    message_object = None

    status = ('draft','sent','unread')

    def __init__ (self):
        pass

    @staticmethod
    def validator(message):
        message = {
            'subject':message.get('subject'),
            'msgBody':message.get('msgBody'),
			'parentId':message.get('parentId'),
			'status':message.get('status','draft'),
            'reciever':message.get('reciever')
        }
        MessageValidator.message_object = message

        for field in message: 
            MessageValidator().validate_message(field) 

        return True

    def validate_message(self,field):
        method_name = 'validate_' + str(field)

        method = getattr(self, method_name, lambda: "Invalid Field")
        
        return method()

    def validate_receiver(self):
        pass
    
    def validate_sender(self):
        pass

    def validate_subject(self):
        pass

    def validate_body(self):
        pass

    def validate_status(self):
        pass