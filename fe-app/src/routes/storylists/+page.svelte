<svelte:head>
	<title>Stories</title>
	<meta name='description' content='Stories' />
</svelte:head>
<script>

	/** @type {import('./$types').PageData} */
	export let data;
	let stories = data.stories;
</script>
<div class='columns-4'>
	{#each stories as story}
		<a href='/story/{story.thread_id}'
			 class='block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700'>

			<h5 class='mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white'>{story.title}</h5>
			<p class='font-normal text-gray-700 dark:text-gray-400'>{story.body}.</p>
		</a>
	{/each}

</div>
