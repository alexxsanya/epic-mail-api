const APP_URL = '/api/v1/'
const TOKEN = sessionStorage.getItem('token')
const loadLocalHTML = (uri) =>  {
    let htmlCode = '';
    const uri = `./components/${uri}`;
    fetch(uri, {
        method: 'GET',
        })
        .then(response => response.text())
        .then(data => {
            htmlCode = data;
            document.getElementById('main-body').innerHTML = htmlCode;

            if (uri == "./components/groups.html") {
                groups = document.getElementById('group-list')

                fetch(
                    `${APP_URL}groups`,
                    {
                        headers: new Headers({
                            'User-agent': 'Mozilla/4.0 Custom User Agent'
                        })
                    })
                    .then(response => response.text())
                    .then(data => {
                        groupList = data.data

                        groupHTML = `
                    <table style="min-width:400px !important;">
                    <caption>User Groups</caption>
                    `
                        groupList.forEach(group => {
                            groupHTML += `
                        <tr>
                        <td onclick="showMembers(${group.id},'${group.name}')">${group.name}</td>
                        <td>${group.role}</td>
                        <td class='td-action positive' onclick="sendGroupMessage(${group.id},'${group.name}')">
                            <i class="far fa-paper-plane"></i>
                        </td>
                        <td class='td-action' onclick="deleteGroup(${group.id})">
                            <i class="far fa-trash-alt"></i>
                        </td>
                        </tr>
                    `
                        })
                        if (groupList.length < 0) {
                            groupHTML = `
                    <table style="min-width:400px !important;">
                    <caption>You Currently Have No Groups</caption>
                    `
                        }
                        groupHTML += `</table>`

                        groups.innerHTML = groupHTML
                    })
                    .catch(error => console.error(error))
            }
        })
        .catch(error => console.error(error))
}

const loadMessage = (caption) => {

    document.getElementById('main-body').innerHTML = "Loading...";
    let url = `${APP_URL}messages/${caption}`
    sessionStorage.setItem('current_page', caption)
    url = {
        'inbox': 'messages',
        'sent': 'messages/sent',
        'draft': 'messages/draft',
        'unread': 'messages/unread'
    }
    fetch(
        `${APP_URL}${url[caption]}`,
        {
            method: 'GET',
            mode: "cors",
            headers: new Headers({
                'User-agent': 'Mozilla/4.0 Custom User Agent',
                'Authorization': `Bearer ${TOKEN}`
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg == "Token has expired") {
                alert("session expired")
                sessionStorage.removeItem('username')
                sessionStorage.removeItem('token')
                location.reload()
            }
            let ui_data = "<table>";
            if (isEmpty(data.data)) {
                ui_data += `<caption> Currently No ${caption} Messages</caption>`;
            } else {
                ui_data += `<caption>${caption} Messages</caption>`;
                data.data.forEach(msg => {
                    ui_data += `<tr>
                            <td onclick='readMessage(${msg.id})'> ${msg.subject}</td>
                            <td class='msg-body' onclick='readMessage(${msg.id})'> ${msg.msgbody} </td>
                            <td onclick='readMessage(${msg.id})'> ${msg.createdon}</td>
                            <td class='td-action' onclick="deleteMessage(${msg.id})"><i class="far fa-trash-alt"></i></td>
                            <td class='td-action'></td>
                        </tr>`;
                });
            }
            ui_data += "</table>";
            document.getElementById('main-body').innerHTML = ui_data;
        })
        .catch(error => {
            document.getElementById('main-body').innerHTML = `
            <error>Kindly contact epicmail support team</error>
            `;
        });

    const isEmpty = (arg) => {
        for (let item in arg) {
            return false;
        }
        return true;
    }
}

const readMessage = (msg_id) => {
    current_page = sessionStorage.getItem('current_page')
    fetch(
        `${APP_URL}messages/${msg_id}`,
        {
            headers: new Headers({
                'User-agent': 'Mozilla/4.0 Custom User Agent',
                'Authorization': `Bearer ${TOKEN}`
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            message = data.data[0]

            messageCode = `<div class="msg-container">
            <div class="msg-bar">
                <div class="back-btn"> 
                    <button onclick="loadMessage('${current_page}')">
                            Back
                    </div>
                <div class="msg-actions">
                    <div class="item" onclick="deleteMessage(${message.id})">
                        Delete
                    </div>
                </div>
            </div>
            <div class="msg-display">
                <div class="msg-title">
                    <div class="subject"> ${message.subject}</div>
                    <div class="sender"> <from>from</from> ${message.sender}</div>
                    <div class="timedate"> ${message.createdon}</div>
                </div>
                <div class="msg-body">
                    ${message.msgbody}
                </div>

                <!--div class="msg-reply-form">
                    <textarea class="reply-msg-txtarea" placeholder="reply" 
                        id="reply-msg-body" parent_id="${message.id}"></textarea>
                    <button type="button" id="reply-msg-btn" class="reply-msg-btn">reply</button>
                </div-->
            </div>

        </div>`
            document.getElementById('main-body').innerHTML = messageCode;
        })
        .catch(error => console.error(error))

}

const resetPassword = () => {
    let reset_btn = document.getElementById('reset-pass')
    let reset_value = document.getElementById('recover-to')

    reset_btn.disabled = true

    reset_btn.addEventListener('click', () => {
        reset_value.value = ""
        alert("Check Your Email or Phone SMS for Reset Link")

        document.getElementById('reset-pass-modal').style.display = 'none'

    })

    reset_value.addEventListener('keyup', () => {
        if (reset_value.value.length > 12) {
            reset_btn.disabled = false
        }
    })
}

const addGroup = () => {
    let add_group = document.getElementById('create-group-container')
    let add_member = document.getElementById('add-member-container')
    let create_group_btn = document.getElementById('create-group')
    add_group.setAttribute('style', 'display:flex');
    add_member.setAttribute('style', 'display:none')

    create_group_btn.addEventListener('click', () => {

        let name = document.getElementById('group-name').value
        let role = document.getElementById('group-description').value
        let status_label = document.getElementById('resp-status')
        status_label.innerHTML = 'processing...'
        group = {
            "name": name,
            "role": role
        }
        url = `${APP_URL}groups`
        fetch(url, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify(group),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    status_label.innerHTML = '<success>Group successfully created</success>'
                    setTimeout( () => {
                        loadLocalHTML('groups.html')
                        status_label.innerHTML = ""
                    }, 2000)

                } else {
                    console.log(data.error)
                }
            })
            .catch(error => console.error(error))
    });
}

const addMembertoGroup = () => {
    let add_group_div = document.getElementById('create-group-container')
    let add_member_div = document.getElementById('add-member-container')
    let add_member_btn = document.getElementById('add-member')
    add_member_div.setAttribute('style', 'display:flex')
    add_group_div.setAttribute('style', 'display:none')

    generateGroupList()

    generateUserList()

    add_member_btn.onclick = () => {
        let group_id = document.getElementById('member-group-name').value
        let user_name = document.getElementById('member-user-name').value
        let user_role = document.getElementById('member-user-role').value
        let status_label = document.getElementById('mgroup-status')

        user_id = user_name.split("-")[0]

        group_user = {
            "user_id": user_id,
            "user_role": user_role
        }
        url = `${APP_URL}groups/${group_id}/users`
        fetch(url, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify(group_user),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    status_label.innerHTML = '<success>Member successfully added</success>'
                    setTimeout( () => {
                        loadLocalHTML('groups.html')
                        status_label.innerHTML = ""
                    }, 2000)
                } else {
                    status_label.innerHTML = `<error>${data.error}</error>`
                    console.log(data.error)
                }
            })
            .catch(error => console.error(error))
    }
}

const createUser = (e) => {
    let signup_btn = document.getElementById('create-user-btn')
    let status_label = document.getElementById('signup-status')
    e.preventDefault()
    if (false in signup_is_valid) {

        invalid_fields = []

        signup_is_valid.forEach((value, key) => () => {
            if (value == false) {
                invalid_fields.push(key)
            }
        })
        signup_btn.innerText = "CREATE Account"

    } else {
        signup_btn.disabled = true
        signup_btn.innerText = "Loading..."
        signup_btn.style.background = "#808080"
        let signupForm = document.getElementById('signup-form')
        let formData = new FormData(signupForm)
        let userData = {}

        formData.set("email", `${formData.get('email')}@epicmail.com`);
        formData.set('recovery_email', `${formData.get('firstname')}.r@epicmail.com`)

        formData.forEach((value, key) => { userData[key] = value });

        url = `${APP_URL}auth/signup`
        fetch(url, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify(userData),
            headers: new Headers({
                'Content-Type': 'application/json'
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    status_label.innerHTML = '<success>Account Created</success>'
                    sessionStorage.setItem('token', data['data'][0].token)
                    sessionStorage.setItem('username', data['data'][0].user.firstname)
                    location.replace("./")
                } else {
                    status_label.innerHTML = `<error>${data.error}</error>`
                    signup_btn.disabled = false
                    signup_btn.innerText = "CREATE Account"
                    signup_btn.style.background = "#3379f5"
                }
            })
            .catch(error => console.error(error))
    }
}

const sendMessage = (action) => {

    msg_receiver = document.getElementById('msg-receiver').value
    msg_body = document.getElementById('msg-body').value
    msg_subject = document.getElementById('msg-subject').value
    send_message = document.getElementById('send_message')
    save_message = document.getElementById('save_message')
    status_label = document.getElementById('message-status')
    if (action == 'save') {
        save_message.innerText = 'saving...'
    } else if (action == 'send') {
        send_message.innerText = 'sending...'
    }
    save_message.style.background = '#808080'
    send_message.style.background = '#808080'
    send_message.disabled = true
    save_message.disabled = true

    option = {
        'save': `${APP_URL}messages/draft`,
        'send': `${APP_URL}messages`
    }

    if (msg_receiver.length > 6 && msg_body.length > 1) {
        message = {
            "subject": msg_subject,
            "receiver": msg_receiver,
            "msgBody": msg_body
        }
        url = option[action]
        fetch(url, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify(message),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    status_label.innerHTML = `<success>${data.data.message}</sucess>`
                    setTimeout( () => {
                        loadMessage('inbox')
                    }, 5000)
                } else {
                    send_message.disabled = false
                    save_message.disabled = false
                    save_message.style.background = '#3379f5'
                    send_message.style.background = '#3379f5'
                    status_label.innerHTML = `<error>${data.error}</error>`
                    if (action === 'save') {
                        save_message.innerText = 'Save As Draft'
                    } else if (action === 'send') {
                        send_message.innerText = 'Send'
                    }
                }
            })
            .catch(error => console.error(error))

    } else {
        if (msg_body.length < 1) {
            status_label.innerHTML = "<error> Message body not written</error>"
        }
        if (msg_receiver.length < 6) {
            status_label.innerHTML = "<error>Invalid Email Address</error>"
        }
        if (action === 'save') {
            save_message.innerText = 'Save As Draft'
        } else if (action === 'send') {
            send_message.innerText = 'Send'
        }
        send_message.disabled = false
        save_message.disabled = false
        save_message.style.background = '#3379f5'
        send_message.style.background = '#3379f5'
    }
    setTimeout( () => {
        status_label.innerHTML = "";
    }, 5000)
}

const deleteMessage = (id) => {
    if (confirm("Are you sure you want to delete this Message!")) {
        url = `${APP_URL}messages/${id}`;
        current_page = sessionStorage.getItem('current_page')
        fetch(url, {
            method: 'DELETE',
            mode: "cors",
            headers: new Headers({
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    alert(data.data.message)
                    location.replace("./")
                } else {
                    console.log(data.error)
                }
            })
            .catch(error => console.error(error))
    }
}

const deleteGroup = (id) => {
    if (confirm("Are you sure you want to delete this Group!")) {
        url = `${APP_URL}groups/${id}`;
        current_page = sessionStorage.getItem('current_page')
        fetch(url, {
            method: 'DELETE',
            mode: "cors",
            headers: new Headers({
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    alert("Group deleted successfully")
                    setTimeout( () => {
                        loadLocalHTML('groups.html')
                    }, 2000)
                } else {
                    console.log(data.error)
                }
            })
            .catch(error => console.error(error))
    }
}

const sendGroupMessage = (group_id, group_name) => {
    document.getElementById('display-modal').style.display = 'block'

    let container = document.getElementById('main-area')
    let modal_title = document.getElementById('modal-title')

    sendGMessage =  () => {

        let msg_subject = document.getElementById('g-msg-subject').value
        let msg_body = document.getElementById('g-msg-body').value
        let send_btn = document.getElementById('send_group_message')
        status_label = document.getElementById('group-msg-status')
        send_btn.innerHTML = "processing.."
        msg = {
            "subject": msg_subject,
            "msgBody": msg_body,
            "parentId": 0,
        };

        fetch(`${APP_URL}groups/${group_id}/messages`, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify(msg),
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {

                if (data.error == undefined) {
                    status_label.innerHTML = `<success>Message has been sent</success>`

                    setTimeout( () => {
                        document.getElementById('display-modal').style.display = 'none'
                        status_label.innerHTML = ""
                    }, 3000)

                } else {
                    status_label.innerHTML = `
                        <error>Message has not been sent, try again</error>
                    `
                    console.log(data.error)
                }
                send_btn.innerText = 'Send'
            })
            .catch(error => console.error(error))
    }

}

const generateUserList = () => {

    let user_selector = document.getElementById('user-list')

    fetch(`${APP_URL}auth/users`, {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
            'Authorization': `Bearer ${TOKEN}`
        }),
    })
        .then(response => response.json())
        .then(data => {

            USERS_LIST = data.data

            if (data.error == undefined) {
                USERS_LIST.forEach(user => {
                    let option = document.createElement('option');

                    username = `${user.id.toString()} - ${user.firstname}` 
                    option.innerHTML = username;
                    user_selector.appendChild(option);

                })
            } else {
                console.log(data.error)
            }
        })
        .catch(error => console.error(error))
}

const generateGroupList = () => {
    let group_select = document.getElementById('member-group-name')
    fetch(`${APP_URL}groups`, {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
            'Authorization': `Bearer ${TOKEN}`
        }),
    })
        .then(response => response.json())
        .then(data => {

            GROUPS_LIST = data.data

            if (data.error == undefined) {
                GROUPS_LIST.forEach(group => {
                    group_select.options[group_select.options.length] = new Option(
                        group.name.toLowerCase(),
                        group.id
                    );
                })
            } else {
                console.log(data.error)
            }
        })
        .catch(error => console.error(error))
}

const showMembers = (group_id, group_name) => {
    document.getElementById('group-member-modal').style.display = 'block'

    members_list = document.getElementById('members-list')

    fetch(`${APP_URL}groups/${group_id}/users`, {
        method: 'GET',
        mode: "cors",
        headers: new Headers({
            'Authorization': `Bearer ${TOKEN}`
        }),
    })
        .then(response => response.json())
        .then(data => {

            USERS_LIST = data.data
            if (data.error == undefined) {

                memberHTML = `
                <table style="min-width:480px !important;">
                <caption style="font-size:17px;"><b>${group_name}</b> Group Members</caption>
                <tr>
                    <th>Member Name</th>
                    <th>Role</th> 
                    <th></th> 
                </tr>
                `
                USERS_LIST.forEach(user => {
                    memberHTML += `
                    <tr>
                        <td>
                            ${user.firstname} ${user.lastname}
                        </td>
                        <td>
                            ${user.role}
                        </td>
                        <td class='td-action positive' onclick="removeGroupUser(${user.id})">
                            <i class="far fa-trash-alt"></i> remove
                        </td>
                    </tr>
                `
                })
                if (USERS_LIST.length < 1) {
                    memberHTML = `
                <table style="min-width:480px !important;">
                <caption>Group currently has no member</caption>
                `
                }
                memberHTML += `</table>`
                members_list.innerHTML = memberHTML
            } else {
                console.log(data.error)
            }
        })
        .catch(error => console.error(error))

    const removeGroupUser = (user_id) => {
        status_label = document.getElementById('memba-msg-status')
        fetch(`${APP_URL}groups/${group_id}/users/${user_id}`, {
            method: 'DELETE',
            mode: "cors",
            headers: new Headers({
                'Authorization': `Bearer ${TOKEN}`
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error == undefined) {
                    status_label.innerHTML = '<success>Member successfully removed</success>'
                    setTimeout( () => {
                        document.getElementById('group_member_modal').style.display = 'none'
                        status_label.innerHTML = ""
                    }, 3000)
                } else {
                    console.log(data.error)
                }
            })
            .catch(error => console.error(error))
    }
}

const logout = () => {
    sessionStorage.removeItem('token')
    location.replace('./login.html')
}

const App = () => {
    
    token = sessionStorage.getItem('token')
    if (token === null || token.length < 150) {
        location.replace('./login.html')
    }

    let modal = document.getElementById('display-modal');
    let group_member_modal = document.getElementById('group-member-modal');
    window.onclick =  (event) => {
        if (event.target == modal) {
            modal.style.display = "none";
        } else if (event.target == group_member_modal) {
            group_member_modal.style.display = "none"
        }

    }
}

const LoginApp = () => {
    resetPassword()
    login_btn = document.getElementById('login-btn')
    login_btn.preventDefault

    login_btn.onclick = () => {
        username = document.getElementById('user-name').value
        pass = document.getElementById('user-pass').value

        status_label = document.getElementById('login-status')

        if (pass.length > 6 && username.length > 3) {
            login_btn.disabled = true
            login_btn.innerText = "Loading..."
            login_btn.style.background = "#808080"
            user = {
                'email': `${username}@epicmail.com`,
                'password': pass
            };
            url = `${APP_URL}auth/login`
            fetch(url, {
                method: 'POST',
                mode: "cors",
                body: JSON.stringify(user),
                headers: new Headers({
                    'Content-Type': 'application/json'
                }),
            })
                .then(response => response.json())
                .then(data => {

                    if (data.error == undefined) {
                        
                        sessionStorage.setItem('token', data['data'][0].token)
                        sessionStorage.setItem('username', data['data'][0].user.firstname)
                        location.replace("./")
                    } else {
                        
                        status_label.innerHTML = `<error>${data.error}</error>`
                        login_btn.disabled = false
                        login_btn.innerText = "Login"
                        login_btn.style.background = "#3379f5"
                    }
                    login_btn.innerText = "Login"
                })
                .catch(error => {
                    console.log(error)
                    login_btn.innerText = "Login"
                })


        } else {
            if (pass.length < 6) {
                status_label.innerHTML = "<error>Invalid Password</error>"
            }
            if (username.length < 3) {
                status_label.innerHTML = "<error>Invalid Username</error>"
            }
            setTimeout( () => {
                status_label.innerHTML = ""
            }, 3000)
        }


    }
}