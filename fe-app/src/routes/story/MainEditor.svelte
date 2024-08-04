<script>
	import { page } from '$app/stores';
	import Comment from './Comment.svelte';

	export let data;
	let comments = data.comments;
	let showComments = false;
	let selected_comments = [];
	let vid_script_id;

	async function fetchComments() {
		showComments = true;
		const response = await fetch('http://127.0.0.1:4000/get_story/' + data.thread_id + '/comments');
		comments = await response.json();
	}

	async function createvidscript() {
		const response = await fetch('http://127.0.0.1:4000/create_vid_script', {
			method: 'POST',
			body: JSON.stringify({ selected_comments, 'thread_id': data.thread_id }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	function createScript() {
		selected_comments = [];
		selected_comments.push({ 'datasource': data.thread_url, 'text': data.title });
		selected_comments.push({ 'datasource': data.thread_url, 'text': data.body });
		selected_comments.push({ 'datasource': 'Filler', 'text': 'Comments' });
		for (let i = 0; i < comments.length; i++) {
			let temp = fetchSelects(JSON.parse(JSON.stringify(comments[i])));
			selected_comments.push(...temp);
		}
		// console.log(selected_comments);
		selected_comments = selected_comments;
	}

	function fetchSelects(comm_data) {
		let comms = [];
		let more_data = [];
		console.log('original more_data', more_data);

		if (comm_data.selected === true) {
			if (comm_data.extra === true) {
				comms.push({ 'datasource': 'extra', 'text': comm_data.extra_before });
			}
			if (comm_data.is_by_op) {
				comms.push({ 'datasource': '', 'text': 'OP Replied' });
			}
			comms.push({ 'datasource': comm_data.permalink, 'text': comm_data.body });
		}
		if (comm_data.replies.length > 0) {
			for (let i = 0; i < comm_data.replies.length; i++) {
				let temp = fetchSelects(comm_data.replies[i]);
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
        max-width: 100%;
    }

    .item {
        box-sizing: border-box;
        max-width: 50%;
        display: inline-block;
        width: 100%;
    }
</style>

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
				<button class='btn-primary' on:click={fetchComments}>Fetch comments</button>
			{/if}
		</div>
	</div>
	<div class='item'>
		<button class='btn btn-primary btn-lg' type='button' on:click={createScript}>Create Script</button>
		<div class='text-column'>My script</div>
		{#each selected_comments as comment1}
			<div href='#'
					 class='block p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700'>
				<p class='font-normal text-gray-700 dark:text-gray-400'>{comment1.text}</p>
			</div>
		{/each}
		<button class='btn btn-primary btn-lg' type='button' on:click={createvidscript}>Post Script</button>
	</div>
</div>