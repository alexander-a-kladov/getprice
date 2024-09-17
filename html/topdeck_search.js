function comparePrice(name,en_name) {
    if (event.ctrlKey) {
    var re=/\+/gi
    window.open("https://www.mtggoldfish.com/q?utf8=%E2%9C%93&query_string="+en_name.replace('+',' '),"_blank")
    } 
    else {
    window.open("https://topdeck.ru/apps/toptrade/singles/search?q="+name,"_blank")
    }
}
