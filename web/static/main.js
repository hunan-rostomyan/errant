$(document).ready(function() {

	var PORT = 8005;

	// Instantiate a scheduler that runs things every second.
	var scheduler = new Scheduler(1000);

	var api = 'http://localhost:' + PORT;

	var $annotate = $('#annotate');
	var $annotations = $('.annotations');

	// load the data
	var scheduled = undefined;
	$.get(api + '/load', function(data) {
		data.forEach(function(datum) {
			var $sentence = $('<input>').attr('value', datum);
			$sentence.on('keyup', function() {
				if (!scheduled) {
					scheduled = scheduler.assign(saveData, 2000);
				} else {
					scheduler.delay(1000);
				}
			});
			var $item = $('<li>').append($sentence);
			$('#sentences').append($item);
		});
	});

	function prepSentences() {
		return $('#sentences input').map(function(_, sent) {
  			return sent.value;
		}).get();
	}

	// save the data
	function saveData() {
		$annotate.attr('disabled', 'true');
		$annotations.text('Inferring annotations...');
		$.ajax({
			url: api + '/save',
			type: 'post',
			data: JSON.stringify(prepSentences()),
			contentType : 'application/json'}
		).done(function(data) {
			$annotate.removeAttr('disabled');
			$annotations.empty();
			data.raw.forEach(function(datum) {
				var value = datum;
				var $item = $('<li>').append($('<span>').text(value));
				$item.attr('data-type', value[0])
				$annotations.append($item);
			});
			$('#annotations-json').jsonViewer(data.json);
		});
	}

	$annotate.click(saveData);
})