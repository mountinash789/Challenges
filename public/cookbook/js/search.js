function get_cards(){
    $.ajax({
        url: AJAX_URL,
        data: {'search':SEARCH_QUERY,'selected_tags': SELECTED_TAGS},
        success: function(data){
            console.log(data);
            display_cards(data);
        }
    });
}

function add_tag(tag_id){
    if (!SELECTED_TAGS.includes(tag_id)){
        SELECTED_TAGS.push(tag_id);
        get_cards();
    };
}

function remove_tag(tag_id){
    let i = SELECTED_TAGS.indexOf(tag_id)
    if (i >= 0){
        SELECTED_TAGS.splice(i, 1);
        get_cards();
    };
}

function create_card(container, card){
    var template = document.querySelectorAll("#recipe-card-template")[0];
    let clone = template.content.cloneNode(true);
    let name = clone.querySelectorAll(".title");
    let description = clone.querySelectorAll(".description");
    let cooking_time = clone.querySelectorAll(".cooking-time");
    let tags = clone.querySelectorAll(".tags");
    name[0].textContent = card.name;
    description[0].textContent = card.description;
    tags[0].innerHTML = card.tags_display;
    cooking_time.forEach(function (el) {
        el.textContent = card.cooking_time_format;
    });
    let card_el = clone.querySelectorAll(".recipe-card")[0];
    clone.querySelectorAll(".recipe-card")[0].style.opacity = 0;
    container[0].appendChild(clone);
    setTimeout(function(){
    card_el.style.opacity = 1;
    }, 100)
}

function display_cards(data){
    let container = $('#card-container');
    container.html('');

    if (data.count === 0){
        var temp = document.querySelectorAll("#none-found")[0];
        var clone = temp.content.cloneNode(true);
        container[0].appendChild(clone);
    } else {
        let cards = data.cards;
        cards.forEach(function (card) {
            create_card(container, card);
        });
    }
}

$(document).ready(function() {
    $('.tag-btn').on('click',function(){
        $(this).toggleClass('active');
        if ($(this).hasClass('active')){
            add_tag($(this).attr('data-id'));
        } else {
            remove_tag($(this).attr('data-id'));
        }
        get_cards();
    });
    $('.search-btn').on('click',function(){
        SEARCH_QUERY = $('#search-input').val();
        get_cards();
    });
    get_cards();
} );