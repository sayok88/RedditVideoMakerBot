<svelte:head>
	<title>Stories</title>
	<meta name='description' content='Stories' />
</svelte:head>
<style>


</style>
<script>

	/** @type {import('./$types').PageData} */
	import Card from '../Card.svelte';
	export let data;
	let stories = data.response;
</script>
<div class='container_2'>
	{#each stories as story}
	<Card title={story.title} c_body={story.body} max_chars_body={100} c_link='/vidscripts/{story.video_id}'></Card>
	{/each}
</div>