function showMenu(){
    document.getElementById('menuP').style.display="block";
}
function hideMenu(){
    if(!document.getElementById('menuP').onmouseover){
        document.getElementById('menuP').style.display="none";}
}
function count(){
    let a = document.getElementsByTagName('input')[1].value - document.getElementsByTagName('input')[0].value;
    let price_ = document.getElementById('price');
    if(a*3>0) {
        price_.innerHTML = 'Цена:' + a * 3 + 'р.';
    }
}

function getprice(){
    let a = document.getElementsByTagName('input')[1].value - document.getElementsByTagName('input')[0].value;
    let price_ = document.getElementById('lastprice');
    price_.value = a*3;
}
