const mobilenav = document.querySelector('.mobilenav')
const menu = document.querySelector('.menu')


mobilenav.onclick=()=>{
    if(menu.style.display == "block"){
        mobilenav.textContent="//";
        menu.style.display="none"
    } else{
        mobilenav.textContent="X";
        menu.style.display="block"
    }
}