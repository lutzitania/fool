function redrawStocks(data){

	var articles = getRandomStocks(data.length);

	//Declare variables once above the loop to avoid memory leaks.
	var stockheadline;
	var stockticker;
	var stockprice;
	var stockimage;
	var imageurl;

	for(var i = 0; i < 3; i++){
		/* A note on how we're grabbing the images:
		 *	There are a lot of ways to do this. I debated building a JS or PY dictionary
		 *	tying company name to icon file url or even building a simple C#.NET json
		 *  service that would return URLs to externally hosted resources. In the end,
		 *  though, I decided to host the img files in the Django static folder and link
		 *	them here, as this is the most consistent with how we're grabbing the rest
		 *  of the data. Theoretically, if we're actually building or consuming a true API
		 *	that we're hitting at runtime, all we should have to change here is the imageurl
		 *	variable to see the same behavior.
		 */

		//Set the string of the jquery element we're going to be looking for.
		stockheadline = "#stock-headline-" + i;
		stockticker = "#stock-ticker-" + i;
		stockprice = "#stock-price-" + i;
		stockimage = "#stock-image-" + i;
		imageurl = ("../../static/img/" + (data[articles[i]].CompanyName.replace(/\s/g, '').toLowerCase() + ".png"));
		
		//Use that dynamically built element name to write the data.
		$(stockheadline).html(data[articles[i]].CompanyName);
		$(stockticker).html(data[articles[i]].Exchange + ": " + data[articles[i]].Symbol);
		$(stockprice).html(data[articles[i]].CurrentPrice.Amount + " (" + data[articles[i]].Change.Amount + (")"));
		$(stockimage).html("<img class='stock-image' src=" + imageurl + " />");

		if(data[articles[i]].Change.Amount > 0.0){
			$(stockprice).addClass('stock-gain');
		} 
		else if (data[articles[i]].Change.Amount < 0.0) {
			$(stockprice).addClass('stock-loss');
		}
		else{
			$(stockprice).removeClass('stock-gain');
			$(stockprice).removeClass('stock-loss');
		}
	}
}

function getRandomStocks(totalStocks){
	/* Get random values for stocks and return an array of three integers representing their indices
	 *	in the JSON file. Make sure we don't get duplicates. 
	 *  Pretty much the same logic as the python script that gets articles for the homepage.
	*/
	var stocks = [-1,-1,-1];
	for(var i = 0; i < 3; i++){
		rand = getRandomInt(0, totalStocks);
		while(stocks.includes(rand)){
			rand = getRandomInt(0, totalStocks);
		}
		stocks[i] = rand;
	}
	return stocks;
}

function getRandomInt(min, max){
	return Math.floor(Math.random() * (max - min)) + min;
}