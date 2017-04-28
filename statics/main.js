$(document).ready(function() {
    // set configuration for the material library
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal({
        dismissible: false
    });
});

function setModalContentFor(commentId) {
    // Prefill the modal form content with comment value, and add click listener to modal button
    function saveCommentWrapper() {
        // helper function to update commentID, and commentContent
        commentContent = document.getElementById('modal-form-content').value;
        saveComment(commentId, commentContent);
    }
    commentContent = $(`#comment-${commentId}`).text();
    $("#modal-form-content").text(commentContent);
    // reset the save listener so only one handler gets called on click
    $('#modal-form-save-button').off('click');
    $('#modal-form-save-button').on('click', saveCommentWrapper);
}

function setModalContentForDelete(commentId) {
    console.log('setmodal to delete called');
    // Prefill the delete confirmation modal with comment value, add click listener to delete button
    function deleteCommentWrapper() {
        // helper function to delete commentID
        deleteComment(commentId);
    }
    let comment_content_elem = $('#delete-comment-content');
    let original_comment_content = $(`#comment-${commentId}`).text();
    comment_content_elem.text(original_comment_content);
    // reset the delete listener on modal delete button
    $('#modal-delete-form-yes-button').off('click');
    $('#modal-delete-form-yes-button').on('click', deleteCommentWrapper);
}

function saveComment(commentId, commentContent) {
    console.log('saveComment called with arguments:', commentId, commentContent);
    let form = new FormData();
    form.append('comment-content', commentContent);
    form.append('comment-id', commentId);
    // fetch post the form to comment handler
    fetch('http://localhost:8080/blog/comment/', {
        credentials: 'same-origin',
        method: 'post',
        body: form
    }).then((request) => {
        console.log(request, request.status);
        return request.json();
    }).then((data) => {
        console.log(data);
        updateComment(commentId, data);
    });
}

function deleteComment(commentId) {
    console.log('deleteComment called with arguments:', commentId);
    let form = new FormData();
    form.append('comment-id', commentId);
    // fetch delete the form to comment Handler
    fetch(`http://localhost:8080/blog/comment/${commentId}`, {
        credentials: 'same-origin',
        method: 'delete'
    }).then((request) => {
        console.log("delete request status:", request.status);
        return request.json();
    }).then((data) => {
        console.log(data);
        if (data.success) {
            removeCommentElem(commentId);
        }
    });
}

function removeCommentElem(commentId) {
    $(`#comment-container-${commentId}`).remove();
}

function updateComment(commentId, data) {
    let comment_content_el = document.getElementById(`comment-${commentId}`);
    let comment_created_date_el = document.getElementById(`comment-created-id-${commentId}`);
    comment_content_el.innerText = data.comment_content;
    comment_created_date_el = data.updated_date;
}

function addComment(post_id, comment_content) {
    let form = new FormData();
    form.append('comment', comment_content)
    fetch(`http://localhost:8080/blog/post/${post_id}`, {
        credentials: 'same-origin',
        method: 'post',
        body: form
    })
}