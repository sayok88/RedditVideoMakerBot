<script>
	export let thread_id;
	export let cdata = {};
	export let margin = 10;
	let showComments = false;
	let selected = false;
	let extra = false;
	async function fetchReplies() {
		showComments = true;
		const response = await fetch('http://127.0.0.1:4000/comment/' + cdata.id + '/replies');
		cdata.replies = await response.json();
	}
	$: cdata.selected = selected;
</script>
<style>
    textarea {
        field-sizing: content;
    }
</style>
<div class='text-margin' style="margin-left: {margin}px; border-left:1px dotted black">
	{#if cdata.is_by_op}
		<div style='color: green'>OP</div>
	{/if}
	Selected <input type='checkbox' class='checkbox' bind:checked={selected}>
	Add Extra<input type='checkbox' class='checkbox' bind:checked={extra}>
	{#if extra}
	<textarea style="min-width: 100px;" bind:value={cdata.extra_before}></textarea>
	{/if}
	<br>
	<textarea bind:value={cdata.body}  style=" border: {selected?'2px solid red':'1px solid black'}"></textarea>
	{#if cdata.replies !== undefined && cdata.replies.length > 0}
		{#each cdata.replies as reply, i}
			<svelte:self cdata={reply} thread_id={thread_id} margin={margin+10} />
		{/each}
	{/if}
	{#if !showComments}
		<button class='btn-primary' on:click={fetchReplies}>Fetch replies</button>
	{/if}
</div>
