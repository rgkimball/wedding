"use strict";


(function (window) {

    let user_url = 'https://www.instagram.com/{username}/?__a=1'
    let hashtag_url = 'https://www.instagram.com/explore/tags/{hashtag}/?__a=1'

    const tags = ['div', 'a', 'button', 'article', 'section', 'strong', 'i', 'input', 'script'];
    const attr = ['class', 'src', 'href'];

    let users = {},
        posts = {};

    const user_callback = function(response) {
        users.response = response;
    };

    const post_callback = function(response) {
        posts.response = response;

        // for each post, get user data, assemble something more useful.

        // if has_next_page, set a callback to load more posts when the user scrolls down the page
        // https://www.instagram.com/explore/tags/{{ hashtag }}/?__a=1&max_id={{ end_cursor }}
    };

    window.load_functions.push(function(){
        getJSON(hashtag_url, post_callback);
    });

})(window);
