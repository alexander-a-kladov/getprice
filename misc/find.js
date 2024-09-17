var input,search,pr,result,result_arr, locale_HTML, result_store;

function func() {
 	locale_HTML = document.body.innerHTML;   // сохраняем в переменную весь body (Первоначальный)
}
setTimeout(func, 1000);  //ждем подгрузки Jsona и выполняем

function FindOnPage(name, status) {

	input = document.getElementById(name).value; //получаем значение из поля в html
	
	if(input.length<3&&status==true)
	{
		alert('Для поиска вы должны ввести три или более символов');
		function FindOnPageBack() { document.body.innerHTML = locale_HTML; }
	}
	
	if(input.length>=3)
	{
		function FindOnPageGo() {

			search = '/'+input+'/g';  //делаем из строки регуярное выражение
			//search = input;
			pr = document.body.innerHTML;   // сохраняем в переменную весь body
			result = pr.match(/alt="(.*?)"/g);  //отсекаем все теги и получаем только текст
			result_arr = [];   //в этом массиве будем хранить результат работы (подсветку)
			//alert(result)
			//alert(search)
			var warning = true;
                        var search_result;
			var index=0;
			for(var i=0;i<result.length;i++) {
				if((search_result=result[i].match(eval(search)))!=null) {
					warning = false;
					index = i;
					break;
				}
			}

			var scrollHeight = Math.max(
  			document.body.scrollHeight, document.documentElement.scrollHeight,
  			document.body.offsetHeight, document.documentElement.offsetHeight,
  			document.body.clientHeight, document.documentElement.clientHeight
			);
			if(warning == true) {
				alert('Не найдено ни одного совпадения');
			} else {
				//alert(Math.floor(i/6));
				window.scrollTo(0,395*Math.floor((i-1)/6));
				//alert(search_result);
			}

			//for(var i=0; i<result.length;i++) {
				//result_arr[i] = result[i].replace(eval(search), '<span style="background-color:yellow;">'+input+'</span>'); //находим нужные элементы, задаем стиль и сохраняем в новый массив
			//}
			//for(var i=0; i<result.length;i++) {
				//pr=pr.replace(result[i],result_arr[i])  //заменяем в переменной с html текст на новый из новогом ассива
			//}
			//document.body.innerHTML = pr;  //заменяем html код
		}
	}
	function FindOnPageBack() { document.body.innerHTML = locale_HTML; }
	if(status) { FindOnPageBack(); FindOnPageGo(); } //чистим прошлое и Выделяем найденное
	if(!status) { FindOnPageBack(); } //Снимаем выделение
}

