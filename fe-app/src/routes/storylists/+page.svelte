<svelte:head>
	<title>Stories</title>
	<meta name='description' content='Stories' />
</svelte:head>
<script>

	/** @type {import('./$types').PageData} */
	export let data;

	import Card from '../Card.svelte';
	import Pagination from '../Pagination.svelte';

	let stories = data.stories;
	let per_page = data.per_page;
	let total_items = data.count;
	let total_pages = data.total_pages;
	let next_page = data.next_page;
	let current_page = data.page;
	async function loadStories(page) {
		const res = await fetch(`http://127.0.0.1:4000/stories?page=`+page);
	const item = await res.json();
	stories = item.stories;
	per_page = item.per_page;
	total_items = item.count;
	total_pages = item.total_pages;
	next_page = item.next_page;
	current_page = item.page;
	}
</script>
<style>

</style>
<Pagination total_pages={total_pages} current_page={current_page} page_click={loadStories}
						total_items={total_items} per_page={per_page} next_page={next_page} />
<div class='container_2'>
	{#each stories as story}
		<Card title={story.title} c_body={story.body} c_link='/story/{story.thread_id}' max_chars_body={200} />
	{/each}

</div>
