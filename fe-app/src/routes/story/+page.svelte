<script>
	import MainEditor from './MainEditor.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

</script>
<svelte:head>
	<title>Home</title>
	<meta name='description' content='Home' />
</svelte:head>
<MainEditor data={data} />