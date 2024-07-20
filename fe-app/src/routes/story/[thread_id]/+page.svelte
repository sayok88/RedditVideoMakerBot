<script>
	import { page } from '$app/stores';
	import Comment from '../Comment.svelte';

	/** @type {import('./$types').PageData} */
	export let data;
	let comments = data.comments;
	let showComments = false;
	let selected_comments = [];

	async function fetchComments() {
		showComments = true;
		const response = await fetch('http://127.0.0.1:4000/get_story/' + data.thread_id + '/comments');
		comments = await response.json();
	}

	function createScript() {
		for (let i = 0; i < comments.length; i++) {
			let temp = fetchSelects(JSON.parse(JSON.stringify(comments[i])));
			selected_comments.push(...temp);
		}
		console.log(selected_comments);
		selected_comments = selected_comments;
	}

	function fetchSelects(comm_data) {
		let comms = [];
		let more_data = [];
		console.log('original more_data', more_data);

		if (comm_data.selected === true) {
			if (comm_data.extra === true) {
				comms.push(comm_data.extra_before);
			}
			comms.push(comm_data.body);
		}
		if (comm_data.replies.length > 0) {
			for (let i = 0; i < comm_data.replies.length; i++) {
				console.log('comm_data.replies[i]', comm_data.replies[i]);
				let temp = fetchSelects(comm_data.replies[i]);
				console.log('temp');
				console.log(temp);
				console.log('more_data');
				console.log(more_data);
				more_data.push(...temp);
			}
		}
		if (more_data.length > 0) {
			comms.push(...more_data);
		}
		console.log(comm_data, comms);
		return comms;
	}
</script>
<style>
    textarea {
        field-sizing: content;
    }

    .container {
        display: flex;
        flex-direction: row;
        /*justify-content: flex-start;*/
        /*flex-wrap: wrap;*/
        max-width: 100%;
    }

    .item {
        box-sizing: border-box;
        max-width: 50%;
				display: inline-block;
				width: 100%;


    }
</style>
<svelte:head>
	<title>Home</title>
	<meta name='description' content='Home' />
</svelte:head>
<div class='container'>
	<div class='item'>
		<div class='text-column'>

		</div>
		<div class='text-column'>
			<h1>{data.title}</h1>
			<textarea bind:value={data.body}></textarea>
			<div>Comments</div>

			{#each comments as comment}
				<Comment cdata={comment} thread_id={data.thread_id} />
			{/each}
			{#if !showComments}
				<button on:click={fetchComments}>Fetch comments</button>
			{/if}
		</div>
	</div>
	<div class='item'>
					<button class='btn btn-primary btn-lg' type='button' on:click={createScript}>Create Script</button>

		<div class='text-column'>My script</div>
			{#each selected_comments as comment1}
				<div>{comment1}</div>
			{/each}
	</div>
</div>