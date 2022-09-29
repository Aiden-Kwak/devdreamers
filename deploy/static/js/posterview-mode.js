const poster_mode = () => {
        
    card_container_contest[0].style.gridTemplateColumns = "repeat(auto-fill, minmax(300px, 1fr))"
    contest_card = document.querySelectorAll('.contest-card');

    for(var i = 0; i < contest_card.length; i++) {
        let contest_detail = contest_card[i].querySelector('.contest-detail');
        let contest_thumbnail = contest_card[i].querySelector('.contest-card-thumbnail')

        contest_card[i].style.gridTemplateColumns = "unset"
        contest_card[i].style.height = "unset"
        contest_detail.style.display = "none"
        contest_thumbnail.style.borderRadius = "15px 15px 15px 15px"
    } 
}

const default_mode = () => {
    if(window.innerWidth < 576) card_container_contest[0].style.gridTemplateColumns = "repeat(auto-fill, minmax(375px, 1fr))"
    else card_container_contest[0].style.gridTemplateColumns = "repeat(auto-fill, minmax(450px, 1fr))"
    
    contest_card = document.querySelectorAll('.contest-card');
    
    for(var i = 0; i < contest_card.length; i++) {
        let contest_detail = contest_card[i].querySelector('.contest-detail');
        let contest_thumbnail = contest_card[i].querySelector('.contest-card-thumbnail')

        contest_card[i].style.gridTemplateColumns = "10rem 1fr"
        contest_card[i].style.height = "14rem"
        contest_detail.style.display = "block"
        contest_thumbnail.style.borderRadius = "15px 0px 0px 15px"
    }
}