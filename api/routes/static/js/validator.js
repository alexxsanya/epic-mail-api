/*firstname */
signup_is_valid = {}

fname = document.getElementById('user-firstname')
fname.onkeyup =function(){ 

    if(fname.value.match('([A-Za-z]).{2,25}')){   
        fname.setAttribute('style',"border:2px solid green")
        signup_is_valid['fname'] = true
    }else{
        fname.setAttribute('style',"border:2px solid red")
        signup_is_valid['fname'] = false
    }
}

lname = document.getElementById('user-lastname')
lname.onkeyup =function(){ 

    if(lname.value.match('([A-Za-z]).{2,25}')){   
        lname.setAttribute('style',"border:2px solid green")
        signup_is_valid['lname'] = true
    }else{
        lname.setAttribute('style',"border:2px solid red")
        signup_is_valid['lname'] = false
    }
}
lname.onblur = function(){
    if(lname.value == fname.value){
        alert("firstname & lastname can't be the same")
        lname.setAttribute('style',"border:2px solid red")
        signup_is_valid['lname'] = false
    }
}


email = document.getElementById('user-email')
email.onkeyup =function(){ 

    if(email.value.match('([A-Za-z0-9]).{2,25}')){   
        email.setAttribute('style',"border:2px solid green")
        signup_is_valid['email'] = true
    }else{
        email.setAttribute('style',"border:2px solid red")
        signup_is_valid['email'] = false
    }
}

pass = document.getElementById('user-pass')
pass.onkeyup =function(){ 

    if(pass.value.match('([A-Za-z0-9]).{7,25}')){   
        pass.setAttribute('style',"border:2px solid green")
        signup_is_valid['pass'] = true
    }else{
        pass.setAttribute('style',"border:2px solid red")
        signup_is_valid['pass'] = false
    }
}

pass.onfocus = function(){
    pass_status = document.getElementById('pass-status')
    pass_status.setAttribute('style','display:block')
}
pass.onblur = function(){
    pass_status = document.getElementById('pass-status')
    pass_status.setAttribute('style','display:none')
}

pass2 = document.getElementById('user-pass2')
pass2.onkeyup =function(){ 

    if(pass.value == pass2.value){   
        pass2.setAttribute('style',"border:2px solid green")
        signup_is_valid['pass'] = true
        show_signup_btn.removeAttribute('style')
        createUserbtn = document.getElementById('create-user-btn')
        createUserbtn.removeAttribute('disabled')
    }else{
        pass2.setAttribute('style',"border:2px solid red")
        show_signup_btn.setAttribute('style','display:none')
        signup_is_valid['pass'] = true
    }
}