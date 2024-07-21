<script>
	import MainEditor from '../MainEditor.svelte';

	/** @type {import('./$types').PageData} */
	export let data;

</script>

<MainEditor data={data} />