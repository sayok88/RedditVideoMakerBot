<svelte:head>
	<title>Stories</title>
	<meta name='description' content='Stories' />
</svelte:head>
<script>

	/** @type {import('./$types').PageData} */
	export let data;
	let stories = data.response;
</script>
<div class='columns-4'>
	{#each stories as story}
		<a href='/vidscripts/{story.video_id}'
			 class='block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700'>
			<h5 class='mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white'>{story.script}</h5>
		</a>
	{/each}
</div>
