$(document).ready(function(){
    let quote = [
        {phrase: "시작할 때 위대할 필요는 없다. 그러나 시작하면 위대해진다.", author:"지그 지글러"},
        {phrase: "기회는 일어나는 것이 아니라 만들어내는 것이다.", author:"크리스 그로서"},
        {phrase: "꿈☆은 이루어 진다.", author:"2002 월드컵 응원글"},
        {phrase: "큰 목표를 이루고 싶다면 허락을 구하지 마라.", author:"미상"},
        {phrase: "오랫동안 꿈을 그리는 사람은 마침내 그 꿈을 닮아간다.", author:"앙드레 말로"},
        {phrase: "이 세상에 재능이 있는데 성공하지 못한 사람보다 더 흔한 것은 없다.", author:"미상"},
        {phrase: "골을 넣으려면 일단 공을 차야한다.", author:"드라마 '미생'中"},
        {phrase: "못할 것 같은 일도 시작해 놓으면 이루어진다.", author:"채근담"},
        {phrase: ":wq!", author:"vi/vim"},
        {phrase: "한 곳에 모이는 것은 시작이고, 같이 머무는 것은 진전이며 , 같이 일하는 것은 성공이다", author:"헨리 포드"},
    ]
    const refresh = () => {
        var num = Math.floor(Math.random()*(quote.length));
        $(".phrase").text("\'  " + quote[num].phrase + "  \'");
        $(".author").text("- " + quote[num].author + " -");
    }
    refresh()

    $(".refreshBtn").on("click", () => {refresh()});
});

const changeposter = () => {
    let i;
    for(i = 0; i < 3; i++) {
        document.querySelectorAll(".carousel-item")[i].querySelector("img").src = window.innerWidth < 992 ? `/static/img/landingpagem${i + 1}.png` : `/static/img/landingpage${i + 1}.png`
    }
}

window.addEventListener('resize', () => {
    changeposter()
});