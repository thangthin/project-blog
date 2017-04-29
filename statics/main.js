$(document).ready(function() {
    // set configuration for the material library
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal({
        dismissible: false
    });

    $('#vote-button').on('click', voteHandler);

    function voteHandler() {
        console.log("voteHandler called");
        let postId = $('#post-id-holder').val();
        // make api call to update vote for by user
        updateVote(postId);
    }
});

// set the constants for url to switch between localhost and hosted url
const WEB_APP_URL = window.location.origin;
const SAVE_COMMENT_URL = `${WEB_APP_URL}/blog/comment/`;
const DELETE_COMMENT_URL = `${WEB_APP_URL}/blog/comment/`;

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
    fetch(SAVE_COMMENT_URL, {
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
    fetch(`${DELETE_COMMENT_URL}${commentId}`, {
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

function updateVote(postId) {
    function updateVoteDisplay(resObj) {
        // update the view with updated vote
        console.log("updateVoteDisplay");
        let currentVoteCount = parseInt($('#votes-display').text());
        currentVoteCount += 1;
        $('#votes-display').text(currentVoteCount);
    }
    // API call to update the vote of post
    // if api call successful, update frontend
    console.log('updateVote called');
    // fetch call
    let form = new FormData();
    form.append('post-id', postId);

    fetch('http://localhost:8080/blog/postvote/', {
        credentials: 'same-origin',
        method: 'put',
        body: form
    }).then((response) => {
        console.log("update vote call", response.status);
        return response.json();
    }).then((resObj) => {
        updateVoteDisplay(resObj);
    });
}