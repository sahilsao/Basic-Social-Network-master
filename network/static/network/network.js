document.addEventListener('DOMContentLoaded', function(){

    try {
        document.getElementById("submitPost").disabled = true;
    
        document.getElementById("postContent").onkeyup = () => {
            if (document.getElementById("postContent").value.length > 0) {
                document.getElementById("submitPost").disabled = false;
            }
            else {
                document.getElementById("submitPost").disabled = true;
            }
        }
    }

    catch(TypeError) {
    }

    try {
        var target_user = document.querySelector("#about_user > h3").innerHTML;
        var target_user = target_user.replace("About ", "");
    
        document.getElementById("followUser").addEventListener('click', ()=> follow(target_user, 'Follow'));
        document.getElementById("unfollowUser").addEventListener('click', ()=> follow(target_user, 'Unfollow'));
    }

    catch(TypeError) {
    }

    try {
        var like_buttons = document.querySelectorAll(".likePost");
        var unlike_buttons = document.querySelectorAll(".dislikePost");

        like_buttons.forEach(like_button => {
            var target_like = like_button.parentNode.id
            like_button.addEventListener('click', ()=> like(like_button, target_like, 'Like'));
        });
            
        unlike_buttons.forEach(unlike_button => {
            var target_unlike = unlike_button.parentNode.id
            unlike_button.addEventListener('click', ()=> like(unlike_button, target_unlike, 'Dislike'));
        });
    }

    catch(TypeError) {
    }

    try {
        var editLinks = document.querySelectorAll(".editLink");

        editLinks.forEach(editLink => {
            var target_post = editLink.parentNode.id
            editLink.addEventListener('click', ()=> editPost(target_post))
        });
    }

    catch(TypeError) {
    }


});

function follow(targetUser, whatDo) {

    var current_text = document.querySelector('#about_user > li').innerHTML;
    var total_followers = current_text.replace("Total Followers: ","");
    parseInt(total_followers);

    if (whatDo === 'Follow') {
        total_followers++;
    }
    else {
        total_followers--;
    }

    document.querySelector('#about_user > li').innerHTML = `Total Followers: ${total_followers}`;

    if (whatDo === 'Follow') {
        document.querySelector("#followUser").style.display = 'none';
        document.querySelector("#unfollowUser").style.display = 'block';
    }
    else {
        document.querySelector("#followUser").style.display = 'block';
        document.querySelector("#unfollowUser").style.display = 'none';
    }

    fetch(`/follow`, {
        method: 'PUT',
        body: JSON.stringify({
            target_User: targetUser,
            whatDo: whatDo,
        })
    })
}

function like(current_button ,targetPost, whatDo) {

    var current_like = document.querySelector(`#${targetPost} > .total_likes`).innerHTML;
    parseInt(current_like);

    if (whatDo === 'Like') {
        current_like++;
    }
    else {
        current_like--;
    }

    document.querySelector(`#${targetPost} > text`).innerHTML = `${current_like}`;

    if (whatDo === 'Like') {
        current_button.style.display = 'none';
        current_button.nextElementSibling.style.display = 'block';
    }
    else {
        current_button.style.display = 'none';
        current_button.previousElementSibling.style.display = 'block';
    }

    fetch(`/like`, {
        method: 'PUT',
        body: JSON.stringify({
            target_Post: targetPost,
            whatDo: whatDo,
        })
    })
}

function editPost(targetPost) {
    
    document.querySelector(`#${targetPost} > .editLink`).style.display = 'none';
    document.querySelector(`#${targetPost} > .content`).style.display = 'none';
    document.querySelector(`#${targetPost} > img`).style.display = 'none';
    document.querySelector(`#${targetPost} > .total_likes`).style.display = 'none';
    document.querySelector(`#${targetPost} > .content`).style.display = 'none';
    if (document.querySelector(`#${targetPost} > .likePost`).style.display == 'none'){
        var likeCheck = 'dislike';
        document.querySelector(`#${targetPost} > .dislikePost`).style.display = 'none';
    }
    else {
        var likeCheck = 'like';
        document.querySelector(`#${targetPost} > .likePost`).style.display = 'none';
    }
    
    document.querySelector(`#${targetPost} > .dislikePost`).style.display = 'none';
    document.querySelector(`#${targetPost} > .time`).style.display = 'none';

    var textBox = document.createElement('textarea');
    textBox.id =`textBox_${targetPost}`
    textBox.setAttribute('class', 'updateText');
    textBox.value = document.querySelector(`#${targetPost} > .content`).innerHTML;

    var br = document.createElement('br');

    var updateButton = document.createElement('button');
    updateButton.innerHTML = 'Save';
    updateButton.id = `submit_${targetPost}`
    updateButton.setAttribute('class', 'submit_post');

    document.querySelector(`#${targetPost}`).append(textBox);
    document.querySelector(`#${targetPost}`).append(br);
    document.querySelector(`#${targetPost}`).append(updateButton);

    textBox.focus()

    try {
        document.querySelector(`#textBox_${targetPost}`).onkeyup = () => {
            if (document.querySelector(`#textBox_${targetPost}`).value.length > 0) {
                document.querySelector(`#submit_${targetPost}`).disabled = false;
            }
            else {
                document.querySelector(`#submit_${targetPost}`).disabled = true;
            }
        }
    }

    catch(TypeError) {
    }

    updateButton.addEventListener('click', ()=> {
        fetch(`/editPost`, {
            method: 'PUT',
            body: JSON.stringify({
                target_Post: targetPost,
                newContent: document.querySelector(`#textBox_${targetPost}`).value,
            })
        });

        document.querySelector(`#${targetPost} > .content`).innerHTML = document.querySelector(`#textBox_${targetPost}`).value;
        textBox.remove();
        br.remove;
        document.querySelector(`#${targetPost} > br`).remove()
        updateButton.remove();
        document.querySelector(`#${targetPost} > .editLink`).style.display = 'block';
        document.querySelector(`#${targetPost} > .content`).style.display = 'block';
        document.querySelector(`#${targetPost} > img`).style.display = 'inline';
        document.querySelector(`#${targetPost} > .total_likes`).style.display = 'inline';
        document.querySelector(`#${targetPost} > .content`).style.display = 'block';
        document.querySelector(`#${targetPost} > .content`).style.display = 'block';
        if (likeCheck == 'like') {
            document.querySelector(`#${targetPost} > .likePost`).style.display = 'block';
        }
        else {
            document.querySelector(`#${targetPost} > .dislikePost`).style.display = 'block';
        }
        
        document.querySelector(`#${targetPost} > .time`).style.display = 'block';

    });
}