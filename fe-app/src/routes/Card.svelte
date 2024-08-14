<script>

	export let title, c_body, max_chars_body, c_link;

	function truncate(text, totalChars, endChars = 0) {
		endChars = Math.min(endChars, totalChars);
		const start = text.slice(0, totalChars - endChars);
	  const end = endChars > 0 ? text.slice(-endChars) : '';

		if (start.length + end.length < text.length) {
			return start + '…' + end;
		} else {
			return text;
		}
	}
</script>
<style>
    .card {
        /* Add shadows to create the "card" effect */
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        transition: 0.3s;
        max-width: 25%;
        margin: 1em;
    }

    /* On mouse-over, add a deeper shadow */
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }

    /* Add some padding inside the card container */
    .container1 {
        padding: 2px 16px;
    }
</style>

<div class='card bg-gray-800 text-white '>
	<a target="_self" href={c_link}>
		<div class='container1'>
			<h4><b>{title}</b></h4>
			<p>{truncate(c_body, max_chars_body, 6)}</p>
		</div>
	</a>
</div>